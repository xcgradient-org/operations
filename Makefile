PYTHON ?= python3
GRAPH_BUILDER_DIR := graph-builder
GRAPH_SCRIPT := $(GRAPH_BUILDER_DIR)/build_knowledge_graph.py
OPEN_OBSIDIAN_SCRIPT := $(GRAPH_BUILDER_DIR)/open_obsidian.py
SOURCE_ROOT := internal
GRAPH_JSON := graphify-out/graph.json
GRAPH_HTML := graphify-out/graph.html
GRAPH_REPORT := graphify-out/GRAPH_REPORT.md
GRAPH_WIKI_INDEX := graphify-out/wiki/index.md
OBSIDIAN_VAULT := $(HOME)/vault/graphify/xcgradient-org

.PHONY: internal internal-build internal-no-obsidian validate-internal clean-graph show-graph-paths

internal: internal-build
	$(PYTHON) $(OPEN_OBSIDIAN_SCRIPT) "$(OBSIDIAN_VAULT)"

internal-build:
	$(PYTHON) $(GRAPH_SCRIPT) --source-root "$(SOURCE_ROOT)"

internal-no-obsidian:
	$(PYTHON) $(GRAPH_SCRIPT) --source-root "$(SOURCE_ROOT)" --skip-obsidian

validate-internal:
	$(PYTHON) $(GRAPH_SCRIPT) --source-root "$(SOURCE_ROOT)" --validate-only

clean-graph:
	rm -rf graphify-out

show-graph-paths:
	@printf '%s\n' "$(GRAPH_JSON)" "$(GRAPH_HTML)" "$(GRAPH_REPORT)" "$(GRAPH_WIKI_INDEX)"
