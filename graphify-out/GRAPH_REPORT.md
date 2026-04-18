# Graph Report - operations  (2026-04-18)

## Corpus Check
- 13 files · ~10,197 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 85 nodes · 122 edges · 9 communities detected
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 5 edges (avg confidence: 0.65)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Vision Mission - RAG Pipeline|Vision Mission - RAG Pipeline]]
- [[_COMMUNITY_Vision Mission - XC Gradient|Vision Mission - XC Gradient]]
- [[_COMMUNITY_Notion System - Notion OS|Notion System - Notion OS]]
- [[_COMMUNITY_Planning System - Q2 2026 OKRs|Planning System - Q2 2026 OKRs]]
- [[_COMMUNITY_Infrastructure - XCGradient Infrastructure OS|Infrastructure - XCGradient Infrastructure OS]]
- [[_COMMUNITY_Legal Clo - Legal (CLO)|Legal Clo - Legal (CLO)]]
- [[_COMMUNITY_Marketing Cmo - Marketing (CMO)|Marketing Cmo - Marketing (CMO)]]
- [[_COMMUNITY_Sales Cro - Sales (CRO)|Sales Cro - Sales (CRO)]]
- [[_COMMUNITY_Hr People - HR & People|Hr People - HR & People]]

## God Nodes (most connected - your core abstractions)
1. `XC Gradient` - 19 edges
2. `Notion OS` - 12 edges
3. `RAG Pipeline` - 12 edges
4. `Private AI Knowledge Layer` - 10 edges
5. `Product Vision` - 7 edges
6. `Sales (CRO)` - 6 edges
7. `Real-Time OEE Dashboard` - 6 edges
8. `Financial (CFO)` - 5 edges
9. `Q2 2026 OKRs` - 5 edges
10. `Phase 1: PoC Execution` - 5 edges

## Surprising Connections (you probably didn't know these)
- `XC Gradient` --uses--> `Drive`  [EXTRACTED]
  internal/01_executive_ceo/vision_mission.md → internal/03_operations_coo/platform/notion-system.md
- `Sales (CRO)` --uses--> `PoC Pipeline`  [INFERRED]
  internal/07_sales_cro/README.md → internal/03_operations_coo/platform/notion-system.md
- `Sales (CRO)` --tracks--> `Pipeline Conversations per Week`  [INFERRED]
  internal/07_sales_cro/README.md → internal/03_operations_coo/platform/planning-system.md
- `PoC Pipeline` --tracks--> `Pipeline Conversations per Week`  [INFERRED]
  internal/03_operations_coo/platform/notion-system.md → internal/03_operations_coo/platform/planning-system.md
- `XC Gradient` --operates-in--> `Proof-of-Concept Phase`  [EXTRACTED]
  internal/01_executive_ceo/vision_mission.md → internal/01_executive_ceo/pitch.md

## Communities

### Community 0 - "Vision Mission - RAG Pipeline"
Cohesion: 0.15
Nodes (21): A Score, Automated Machine State Reporting, Decfa PoC, Domain Ontology, LLM-Assisted Error Documentation, Local LLM Inference, Markov + Choquet Reranking, Mean Time to Repair (MTTR) (+13 more)

### Community 1 - "Vision Mission - XC Gradient"
Cohesion: 0.16
Nodes (17): Adam Sarrate, Bootstrap-First Funding Strategy, Client Data Sovereignty, Data Room, Depth-First SME Entry, European Manufacturing SMEs, Executive Office, Financial (CFO) (+9 more)

### Community 2 - "Notion System - Notion OS"
Cohesion: 0.25
Nodes (11): Company Calendar, CORE, Decision Log, Discord, Discord /update Bot, Drive, Execution Log, LOI Count (+3 more)

### Community 3 - "Planning System - Q2 2026 OKRs"
Cohesion: 0.2
Nodes (10): 2026 Annual Goal, ARR, Company Constitution, Dr. Lluís Padró, NEON, Phase 2: Pipeline Building, Phase 3: Constitution + Launch, Pipeline Conversations per Week (+2 more)

### Community 4 - "Infrastructure - XCGradient Infrastructure OS"
Cohesion: 0.24
Nodes (10): Arnau Noguer, Brand Assets Repository, CI/CD Pipeline, Docker Standard, GitHub Container Registry, Hardware Management, On-Prem Deployment Runbook, Technical (CTO) (+2 more)

### Community 5 - "Legal Clo - Legal (CLO)"
Cohesion: 0.5
Nodes (4): Contracts, Corporate Compliance, Intellectual Property, Legal (CLO)

### Community 6 - "Marketing Cmo - Marketing (CMO)"
Cohesion: 0.5
Nodes (4): Brand Identity, Collateral, Market Research, Marketing (CMO)

### Community 7 - "Sales Cro - Sales (CRO)"
Cohesion: 0.5
Nodes (4): Leads, Partnerships, Revenue Models, Sales (CRO)

### Community 8 - "Hr People - HR & People"
Cohesion: 0.5
Nodes (4): Culture, HR & People, Onboarding, Talent

## Knowledge Gaps
- **33 isolated node(s):** `Dr. Lluís Padró`, `Xavier Vera`, `Bootstrap-First Funding Strategy`, `Proof-of-Concept Phase`, `2026 Annual Goal` (+28 more)
  These have ≤1 connection - possible missing edges or undocumented components.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `XC Gradient` connect `Vision Mission - XC Gradient` to `Vision Mission - RAG Pipeline`, `Notion System - Notion OS`, `Infrastructure - XCGradient Infrastructure OS`, `Legal Clo - Legal (CLO)`, `Marketing Cmo - Marketing (CMO)`, `Sales Cro - Sales (CRO)`, `Hr People - HR & People`?**
  _High betweenness centrality (0.625) - this node is a cross-community bridge._
- **Why does `Private AI Knowledge Layer` connect `Vision Mission - RAG Pipeline` to `Vision Mission - XC Gradient`, `Infrastructure - XCGradient Infrastructure OS`?**
  _High betweenness centrality (0.201) - this node is a cross-community bridge._
- **Why does `Notion OS` connect `Notion System - Notion OS` to `Vision Mission - RAG Pipeline`, `Vision Mission - XC Gradient`?**
  _High betweenness centrality (0.192) - this node is a cross-community bridge._
- **What connects `Dr. Lluís Padró`, `Xavier Vera`, `Bootstrap-First Funding Strategy` to the rest of the system?**
  _33 weakly-connected nodes found - possible documentation gaps or missing edges._