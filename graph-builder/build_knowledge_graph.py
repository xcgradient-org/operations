#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

import networkx as nx
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.cluster import cluster, score_all
from graphify.export import to_html, to_json, to_obsidian
from graphify.report import generate as generate_report
from graphify.wiki import to_wiki

DEFAULT_OBSIDIAN_DIR = Path.home() / "vault" / "graphify" / "xcgradient-org"
ALLOWED_NODE_TYPES = {
    "concept",
    "person",
    "system",
    "metric",
    "phase",
    "legal",
    "org-unit",
}
CONFIDENCE_SCORES = {
    "EXTRACTED": 1.0,
    "INFERRED": 0.65,
    "AMBIGUOUS": 0.3,
}


def parse_args() -> argparse.Namespace:
    script_dir = Path(__file__).resolve().parent
    operations_dir = script_dir.parent

    parser = argparse.ArgumentParser(
        description="Build the operations knowledge graph for operations/internal from a checked-in semantic seed."
    )
    parser.add_argument("--operations-dir", type=Path, default=operations_dir)
    parser.add_argument("--source-root", type=Path, default=operations_dir / "internal")
    parser.add_argument("--seed", type=Path, default=script_dir / "knowledge_graph_seed.json")
    parser.add_argument("--output-dir", type=Path, default=operations_dir / "graphify-out")
    parser.add_argument("--obsidian-dir", type=Path, default=DEFAULT_OBSIDIAN_DIR)
    parser.add_argument("--skip-obsidian", action="store_true")
    parser.add_argument("--skip-html", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    return parser.parse_args()


def slugify(value: str, *, fallback: str = "node") -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or fallback


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_source_path(value: str) -> str:
    cleaned = normalize_text(value).replace("\\", "/").lstrip("./")
    if cleaned.startswith("operations/"):
        cleaned = cleaned[len("operations/") :]
    return cleaned


def normalize_source_files(primary: str, extra: list[str] | None) -> list[str]:
    files = []
    for value in [primary, *(extra or [])]:
        cleaned = normalize_source_path(value)
        if cleaned and cleaned not in files:
            files.append(cleaned)
    return files


def collect_markdown_files(source_root: Path) -> list[Path]:
    files: list[Path] = []
    for path in source_root.rglob("*.md"):
        files.append(path)
    return sorted(files)


def cleanup_markdown_dir(path: Path) -> None:
    if not path.exists():
        return
    for child in path.iterdir():
        if child.is_file() and child.suffix.lower() == ".md":
            child.unlink()


def cleanup_obsidian_dir(path: Path) -> None:
    if not path.exists():
        return
    for child in path.iterdir():
        if child.is_file() and child.suffix.lower() == ".md":
            child.unlink()


def load_seed(seed_path: Path) -> dict[str, Any]:
    try:
        data = json.loads(seed_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"Seed file not found: {seed_path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Seed file is not valid JSON: {seed_path}\n{exc}") from exc

    if not isinstance(data, dict):
        raise SystemExit("Seed file root must be an object.")
    if not isinstance(data.get("nodes"), list) or not isinstance(data.get("edges"), list):
        raise SystemExit("Seed file must contain 'nodes' and 'edges' arrays.")
    return data


def validate_seed(
    seed: dict[str, Any],
    operations_dir: Path,
    source_root: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    normalized_nodes: list[dict[str, Any]] = []
    normalized_edges: list[dict[str, Any]] = []
    node_ids: set[str] = set()
    source_root_rel = source_root.relative_to(operations_dir).as_posix().rstrip("/")

    def ensure_in_source_root(source_file: str, *, kind: str, ref: str) -> None:
        if source_file != source_root_rel and not source_file.startswith(source_root_rel + "/"):
            raise SystemExit(
                f"{kind} {ref} must reference files under {source_root_rel}/, got: {source_file}"
            )

    for raw in seed["nodes"]:
        if not isinstance(raw, dict):
            raise SystemExit("Every node entry must be an object.")
        node_id = slugify(str(raw.get("id", "")), fallback="")
        if not node_id:
            raise SystemExit(f"Invalid node id: {raw}")
        if node_id in node_ids:
            raise SystemExit(f"Duplicate node id: {node_id}")
        node_ids.add(node_id)

        node_type = normalize_text(str(raw.get("type", "")))
        if node_type not in ALLOWED_NODE_TYPES:
            raise SystemExit(f"Invalid node type for {node_id}: {node_type}")

        source_file = normalize_source_path(str(raw.get("source_file", "")))
        if not source_file:
            raise SystemExit(f"Node {node_id} is missing source_file")
        ensure_in_source_root(source_file, kind="Node", ref=node_id)
        if not (operations_dir / source_file).exists():
            raise SystemExit(f"Node {node_id} references missing source file: {source_file}")

        source_files = normalize_source_files(
            source_file,
            raw.get("source_files") if isinstance(raw.get("source_files"), list) else None,
        )
        for item in source_files:
            ensure_in_source_root(item, kind="Node", ref=node_id)
            if not (operations_dir / item).exists():
                raise SystemExit(f"Node {node_id} references missing source file: {item}")

        normalized_nodes.append(
            {
                "id": node_id,
                "label": normalize_text(str(raw.get("label", ""))) or node_id.replace("-", " ").title(),
                "type": node_type,
                "description": normalize_text(str(raw.get("description", ""))),
                "source_file": source_file,
                "source_files": source_files,
            }
        )

    edge_signatures: set[tuple[str, str, str]] = set()
    for raw in seed["edges"]:
        if not isinstance(raw, dict):
            raise SystemExit("Every edge entry must be an object.")
        source = slugify(str(raw.get("source", "")), fallback="")
        target = slugify(str(raw.get("target", "")), fallback="")
        relation = slugify(str(raw.get("relation", "")), fallback="")
        if not source or not target or not relation:
            raise SystemExit(f"Invalid edge entry: {raw}")
        if source == target:
            raise SystemExit(f"Self-edge is not allowed: {source}")
        if source not in node_ids or target not in node_ids:
            raise SystemExit(f"Edge references unknown nodes: {source} -> {target}")

        confidence = normalize_text(str(raw.get("confidence", "EXTRACTED"))).upper()
        if confidence not in CONFIDENCE_SCORES:
            raise SystemExit(f"Invalid edge confidence for {source}->{target}: {confidence}")

        source_file = normalize_source_path(str(raw.get("source_file", "")))
        if not source_file:
            raise SystemExit(f"Edge {source}->{target} is missing source_file")
        ensure_in_source_root(source_file, kind="Edge", ref=f"{source}->{target}")
        if not (operations_dir / source_file).exists():
            raise SystemExit(f"Edge {source}->{target} references missing source file: {source_file}")

        source_files = normalize_source_files(
            source_file,
            raw.get("source_files") if isinstance(raw.get("source_files"), list) else None,
        )
        for item in source_files:
            ensure_in_source_root(item, kind="Edge", ref=f"{source}->{target}")
            if not (operations_dir / item).exists():
                raise SystemExit(f"Edge {source}->{target} references missing source file: {item}")

        signature = tuple(sorted((source, target)) + [relation])
        if signature in edge_signatures:
            raise SystemExit(f"Duplicate edge: {source} - {relation} - {target}")
        edge_signatures.add(signature)

        confidence_score = raw.get("confidence_score")
        if confidence_score is None:
            confidence_score = CONFIDENCE_SCORES[confidence]
        else:
            confidence_score = float(confidence_score)

        normalized_edges.append(
            {
                "source": source,
                "target": target,
                "relation": relation,
                "confidence": confidence,
                "confidence_score": confidence_score,
                "source_file": source_file,
                "source_files": source_files,
            }
        )

    return normalized_nodes, normalized_edges


def build_graph(nodes: list[dict[str, Any]], edges: list[dict[str, Any]]) -> nx.Graph:
    graph = nx.Graph()

    for node in nodes:
        graph.add_node(
            node["id"],
            label=node["label"],
            file_type="document",
            source_file=node["source_file"],
            source_files=node["source_files"],
            source_count=len(node["source_files"]),
            description=node["description"],
            type=node["type"],
            mentions=len(node["source_files"]),
        )

    for edge in edges:
        graph.add_edge(
            edge["source"],
            edge["target"],
            relation=edge["relation"],
            confidence=edge["confidence"],
            confidence_score=edge["confidence_score"],
            weight=edge["confidence_score"],
            source_file=edge["source_file"],
            source_files=edge["source_files"],
            source_count=len(edge["source_files"]),
            mentions=len(edge["source_files"]),
            _src=edge["source"],
            _tgt=edge["target"],
        )

    graph.graph["hyperedges"] = []
    return graph


def assign_communities(graph: nx.Graph, communities: dict[int, list[str]]) -> None:
    for community_id, node_ids in communities.items():
        for node_id in node_ids:
            graph.nodes[node_id]["community"] = community_id


def source_title(source_file: str) -> str:
    path = Path(source_file)
    stem = path.parent.name if path.stem.lower() == "readme" else path.stem
    stem = re.sub(r"^\d+[_ -]*", "", stem)
    stem = stem.replace("_", " ").replace("-", " ").strip()
    return stem.title() or "Community"


def build_community_labels(graph: nx.Graph, communities: dict[int, list[str]]) -> dict[int, str]:
    labels: dict[int, str] = {}
    for community_id, node_ids in communities.items():
        if not node_ids:
            labels[community_id] = f"Community {community_id}"
            continue

        dominant_source = max(
            (
                graph.nodes[node_id].get("source_file", "")
                for node_id in node_ids
                if graph.nodes[node_id].get("source_file")
            ),
            key=lambda value: sum(
                1 for node_id in node_ids if graph.nodes[node_id].get("source_file") == value
            ),
            default="",
        )

        anchor_nodes = sorted(
            node_ids,
            key=lambda node_id: (
                graph.degree(node_id),
                len(graph.nodes[node_id].get("description", "")),
            ),
            reverse=True,
        )
        anchors = [graph.nodes[node_id].get("label", node_id) for node_id in anchor_nodes[:2]]
        base = source_title(dominant_source) if dominant_source else ""

        if base and anchors:
            label = anchors[0] if anchors[0].lower() in base.lower() else f"{base} - {anchors[0]}"
        elif base:
            label = base
        else:
            label = anchors[0] if anchors else f"Community {community_id}"
        labels[community_id] = label[:80]
    return labels


def write_report(
    graph: nx.Graph,
    communities: dict[int, list[str]],
    cohesion: dict[int, float],
    community_labels: dict[int, str],
    output_path: Path,
    *,
    total_files: int,
    total_words: int,
    root_name: str,
) -> None:
    report = generate_report(
        graph,
        communities,
        cohesion,
        community_labels,
        god_nodes(graph),
        surprising_connections(graph, communities),
        {
            "total_files": total_files,
            "total_words": total_words,
        },
        {
            "input": 0,
            "output": 0,
        },
        root_name,
        suggested_questions=suggest_questions(graph, communities, community_labels),
    )
    output_path.write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    operations_dir = args.operations_dir.expanduser().resolve()
    source_root = args.source_root.expanduser().resolve()
    seed_path = args.seed.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()
    obsidian_dir = args.obsidian_dir.expanduser()
    wiki_dir = output_dir / "wiki"

    if not source_root.exists():
        raise SystemExit(f"Source root does not exist: {source_root}")
    if not source_root.is_dir():
        raise SystemExit(f"Source root is not a directory: {source_root}")
    if operations_dir not in source_root.parents and source_root != operations_dir:
        raise SystemExit(f"Source root must live inside operations dir: {source_root}")

    markdown_files = collect_markdown_files(source_root)
    total_words = sum(len(path.read_text(encoding="utf-8").split()) for path in markdown_files)

    seed = load_seed(seed_path)
    nodes, edges = validate_seed(seed, operations_dir, source_root)

    if args.validate_only:
        print(
            f"Seed is valid for {source_root}: "
            f"{len(nodes)} nodes, {len(edges)} edges."
        )
        return 0

    graph = build_graph(nodes, edges)

    communities = cluster(graph)
    assign_communities(graph, communities)
    cohesion = score_all(graph, communities)
    community_labels = build_community_labels(graph, communities)

    output_dir.mkdir(parents=True, exist_ok=True)
    cleanup_markdown_dir(wiki_dir)
    to_json(graph, communities, str(output_dir / "graph.json"))

    if not args.skip_html:
        to_html(graph, communities, str(output_dir / "graph.html"), community_labels=community_labels)

    to_wiki(
        graph,
        communities,
        wiki_dir,
        community_labels=community_labels,
        cohesion=cohesion,
        god_nodes_data=god_nodes(graph),
    )

    if not args.skip_obsidian:
        cleanup_obsidian_dir(obsidian_dir)
        to_obsidian(
            graph,
            communities,
            str(obsidian_dir),
            community_labels=community_labels,
            cohesion=cohesion,
        )

    write_report(
        graph,
        communities,
        cohesion,
        community_labels,
        output_dir / "GRAPH_REPORT.md",
        total_files=len(markdown_files),
        total_words=total_words,
        root_name=operations_dir.name,
    )

    print(
        f"Graph build complete: {graph.number_of_nodes()} nodes, "
        f"{graph.number_of_edges()} edges, {len(communities)} communities."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
