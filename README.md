# Operations Knowledge Graph

This repository is the company documentation repo for XC Gradient.

## Structure

- `internal/`
  Company-internal documentation used as the source corpus for the internal knowledge graph.
- `external/`
  External-facing material. This is not included in the internal graph build.
- `graph-builder/`
  Local graph builder code and the checked-in semantic graph seed.
- `graphify-out/`
  Generated outputs: `graph.json`, wiki pages, HTML graph, and report.

## Build The Internal Graph

From inside `operations/`:

```bash
make internal
```

What this does:

- builds the graph from `internal/`
- regenerates `graphify-out/`
- exports Obsidian notes to `~/vault/graphify/xcgradient-org`
- opens that Obsidian vault

If you want the rebuild without opening Obsidian:

```bash
make internal-no-obsidian
```

If you want to validate the semantic seed before rebuilding:

```bash
make validate-internal
```

## When Documentation Changes

There are two cases:

### 1. Documentation text changed, but the graph meaning did not

Example:
- wording cleanup
- better explanations
- formatting changes

In this case, just rebuild:

```bash
make internal
```

### 2. The actual business knowledge changed

Example:
- new system
- new OKR
- new phase
- new team responsibility
- new relationship between concepts

In this case:

1. Update the documentation in `internal/`
2. Update `graph-builder/knowledge_graph_seed.json`
3. Validate:
   ```bash
   make validate-internal
   ```
4. Rebuild:

```bash
make internal
```

## Why The Seed File Exists

The graph is intentionally built from a checked-in semantic seed instead of raw markdown parsing at build time.

Reason:
- deterministic output
- no external API dependency
- no hidden extraction step
- fully reviewable graph structure in git

The file to edit is:

- [graph-builder/knowledge_graph_seed.json](/home/sterry/Desktop/xcgradient-org/operations/graph-builder/knowledge_graph_seed.json)

## Main Files

- [Makefile](/home/sterry/Desktop/xcgradient-org/operations/Makefile)
- [graph-builder/build_knowledge_graph.py](/home/sterry/Desktop/xcgradient-org/operations/graph-builder/build_knowledge_graph.py)
- [graphify-out/graph.json](/home/sterry/Desktop/xcgradient-org/operations/graphify-out/graph.json)
- [graphify-out/wiki/index.md](/home/sterry/Desktop/xcgradient-org/operations/graphify-out/wiki/index.md)
- [graphify-out/GRAPH_REPORT.md](/home/sterry/Desktop/xcgradient-org/operations/graphify-out/GRAPH_REPORT.md)
