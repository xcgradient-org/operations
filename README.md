# XC Gradient: The Private AI Knowledge Layer for Manufacturing

> **Making the Invisible Visible.** XC Gradient is an industrial AI startup dedicated to centralizing "tribal knowledge" within manufacturing SMEs. We eliminate equipment downtime by converting fragmented, invisible data into a private, on-premise intelligence layer that stays within the factory walls.

---

## 📑 Table of Contents
1.  [Mission & Vision](#-mission--vision)
2.  [The Problem: The Invisible Manufacturing Iceberg](#-the-problem-the-invisible-manufacturing-iceberg)
3.  [The Product: Private AI Knowledge Layer](#-the-product-private-ai-knowledge-layer)
4.  [Technical IP: The Core Moat](#-technical-ip-the-core-moat)
5.  [Operational Model: The Company OS](#-operational-model-the-company-os)
6.  [Planning System: Phases & OKRs](#-planning-system-phases--okrs)
7.  [Technical Standards & Infrastructure](#-technical-standards--infrastructure)
8.  [GTM & Market Strategy](#-gtm--market-strategy)
9.  [Organizational Structure & Departments](#-organizational-structure--departments)
10. [Traction & Validation](#-traction--validation)
11. [The Automation Layer](#-the-automation-layer)
12. [Data Privacy, Sovereignty & Security](#-data-privacy-sovereignty--security)
13. [Founder Bios](#-founder-bios)
14. [Exhaustive Repository Guide](#-exhaustive-repository-guide)
15. [Master Roadmap & Constitution](#-master-roadmap--constitution)

---

## 🎯 Mission & Vision

XC Gradient is built on the belief that the next industrial revolution won't be powered by generic "Cloud AI," but by deep, localized intelligence that respects the sovereignty of manufacturing data.

- **The Vision:** To become the default intelligence layer for the European industrial corridor, making every SME as efficient as a global conglomerate.
- **The Mission:** To capture, centralize, and activate the "invisible" knowledge of the shop floor—manuals, logs, and technician experience—to eliminate equipment diagnosis time.
- **The Philosophy:**
    - **AI is a Tool, Not a Miracle:** We treat LLMs as token predictors. Their utility is 100% dependent on the deterministic data foundation we provide.
    - **Depth-First Entry:** We don't sell broad tools; we solve specific departmental pains, building a moat of per-client ontologies that makes us irreplaceable.
    - **Bootstrap-First:** We maintain strategic independence, funding our growth through value delivery rather than speculative capital until we reach a 100-client milestone.

---

## 🏭 The Problem: The Invisible Manufacturing Iceberg

Manufacturing SMEs generate gigabytes of operational data daily, yet 80% of it is "invisible."

### The MTTR Bottleneck
In the industrial context, **Mean Time To Repair (MTTR)** is the primary driver of maintenance costs.
```
MTTR = Time to Diagnose + Time to Fix
```
In most SMEs, **Time to Diagnose >> Time to Fix**. 
- Operators spend hours searching for the right manual or waiting for a specific senior technician.
- Legacy knowledge is trapped in paper binders, fragmented Excel files, or "tribal knowledge" in the heads of aging staff.

### The Demographic Crisis
The average age of a senior industrial technician in Europe is 55+. As this workforce retires, their decades of intuitive diagnostic experience walk out the door. XC Gradient captures this knowledge before it's gone.

### The Privacy Barrier
Cloud-based AI solutions (ChatGPT, Azure OpenAI) are non-starters for manufacturers. Their machining parameters, quality tolerances, and supplier relations are competitive trade secrets that cannot leave their premises.

---

## 🛠️ The Product: Private AI Knowledge Layer

XC Gradient deploys a self-contained, on-premise intelligence system with four core capabilities:

### 1. Zero-Latency Diagnosis
Operators query the system in natural language (e.g., *"The CNC spindle is vibrating at 4000 RPM, what's the likely cause?"*). The system retrieves the exact machine schematics, past incident logs, and maintenance records to provide a precise diagnostic answer in seconds.

### 2. Real-Time OEE Dashboard
A clickable 2D map of the plant floor where every machine node shows its live **Overall Equipment Effectiveness (OEE)**.
- **Availability:** Total time - MTTR.
- **Efficiency:** Actual output vs. Theoretical max.
- **Quality:** Good units vs. Total units.

### 3. Unstructured → Structured Pipeline
Legacy data (scanned PDFs, handwritten logs, technician notes) is ingested and indexed into a per-client vector store, turning a filing cabinet into a searchable brain.

### 4. LLM-Assisted Documentation
We eliminate the friction of reporting. Technicians "talk" to the system to log a repair, and the AI generates correctly formatted maintenance records and updates the knowledge base automatically.

---

## 🧠 Technical IP: The Core Moat

Our competitive advantage is not "using AI," but *how* we optimize retrieval for the industrial domain.

### Markov + Choquet Reranking
Standard RAG systems use additive scoring (cosine similarity) to rank documents. This fails when multiple documents are needed to understand a single problem. 
- **Markov Chain State Model:** We model the retrieval process as a transition between document sets.
- **Choquet Integral:** We use a game-theoretic "fuzzy measure" to rank context windows. This allows the system to detect **synergies** (where two documents together are worth more than the sum of their parts) and **redundancies** (where a second document adds no new information).

### S-QDoRA (Sparse Quantized DoRA)
Industrial SMEs rarely have multi-million dollar GPU clusters. S-QDoRA is a multi-tenant fine-tuning method that allows us to serve specialized, factory-specific models on a shared quantized base model, significantly reducing the VRAM footprint and deployment cost.

### Speculative Decoding
We use a small "draft model" to predict token sequences, which are then verified in parallel by our target model. This achieves a **2-4x reduction in latency**, ensuring operators get answers in real-time even on mid-range hardware.

---

## 🛠️ Operational Model: The Company OS

XC Gradient is run as a "Documentation-First" organization. If a decision isn't in Notion, it didn't happen.

### The Notion-Discord-Drive Trinity
- **Notion:** Long-term memory. Structured databases for OKRs, Tasks, and Knowledge.
- **Discord:** Working memory. Ephemeral communication and the interface for our automation bot.
- **Drive:** Binary storage. The "attic" for PPTs, contracts, and raw data exports.

### Task ID & Scoping Scheme
Tasks are project-scoped and role-scoped to ensure perfect traceability.
- **Format:** `[PROJECT]-[ROLE]-[SEQ]`
- **Example:** `NEON-CTO-14` (Project Neon, Arnau, Task 14).
- **Rule:** Every task must trace up to a Key Result (KR) and a quarterly Objective.

---

## 📈 Planning System: Phases & OKRs

We operate on a strict 13-week quarterly sprint cycle, following a 4-phase model for 2026.

### The 2026 Phase Model
- **Phase 0: Ignition (Apr 3–7):** Team readiness, OS installation, demo scope definition.
- **Phase 1: PoC Execution (Apr 7 → Jul 1):** Proving value on real industrial data (Decfa/Paver). **Gate:** Thesis defense.
- **Phase 2: Pipeline Building (Jul 1 → Sep/Oct):** Builder-to-Seller pivot. Securing 10 LOIs.
- **Phase 3: Constitution + Launch (Oct → Dec):** Legal incorporation and ARR growth.

### Q2 2026 OKRs (Current)
- **Objective:** Prove the product works on real industrial data.
- **KR1:** 2 PoCs with documented **A-Score > 0.80**.
- **KR2:** 5 qualified pipeline conversations active by Jun 30.
- **KR3:** Thesis defended Jul 1 with RAG results as core IP claim.

---

## 💻 Technical Standards & Infrastructure

### "Infrastructure OS" Principles
1.  **Single Source of Brand:** Assets live in `brand-assets` and are linked via submodules.
2.  **Docker-Only Execution:** Every tool must be containerized. If it can't run in a container, it isn't production-ready.
3.  **CI/CD Reliability:** No code merges to `main` without passing automated tests and linting.

### Hardware Spec (The Inference Node)
Primary development and inference are conducted on a specialized workstation:
- **CPU:** AMD Ryzen 9 9900X
- **GPU:** 2× NVIDIA RTX 3090 (48GB VRAM total)
- **VRAM Capacity:** Sufficient for 70B parameter quantized models.
- **Inference Stack:** Local LLM serving with speculative decoding and isolated vector stores.

---

## 🌍 GTM & Market Strategy

### The ICP (Ideal Customer Profile)
- **Size:** 20–200 employees.
- **Sector:** High-precision manufacturing (CNC, Injection Moulding, Assembly).
- **Pain Point:** High technical downtime and aging workforce.

### TAM / SAM / SOM
- **TAM:** €1 Trillion (Total European Manufacturing).
- **SAM:** €100 Billion (European Manufacturing SMEs).
- **SOM:** €31 Billion (Industrial SMEs in the Spain/Catalonia Corridor).

### Competitive Moat
Generic tools like **Glean** or **Microsoft Copilot** target administrative tasks in large corporations. XC Gradient targets the **Shop Floor** in SMEs. Our moat is not just the algorithm; it's the **per-client ontology** accumulated over months that makes us structurally embedded in their operations.

---

## 👥 Organizational Structure & Departments

XC Gradient is structured into 8 functional units, each with a defined "Source of Truth" (SoT):

| Dept | Role | SoT | Responsibility |
|---|---|---|---|
| **01 CEO** | Oriol | `pitch.md` | Strategic vision, Board updates, Fundraising. |
| **02 CTO** | Arnau | `infrastructure.md` | RAG Engine, Engineering Standards, Deployment Runbook. |
| **03 COO** | Adam | `notion-system.md` | Workspace Ops, Topology, Security Architecture. |
| **04 CFO** | Oriol | `README.md` | Fiscal health, Runway models, Data Room. |
| **05 CLO** | Adam | `README.md` | IP Protection, Contracts, NIS2 Compliance. |
| **06 CMO** | Oriol | `README.md` | Brand DNA, Marketing Collateral, Market Research. |
| **07 CRO** | Adam | `README.md` | Lead pipeline, Partnerships, Revenue Models. |
| **08 HR** | Oriol | `README.md` | Talent, Culture, Founder Onboarding. |

---

## 🚀 Traction & Validation

### Active Proof-of-Concepts (PoCs)
1.  **Decfa:** Precision CNC turning shop (~30 employees). Direct access to documentation and technician workflows. Focus: Spindle diagnosis and parameter lookup.
2.  **Paver (Granollers):** Large production plant. Focus: Real-time OEE visibility and maintenance documentation for floor staff.

### Learning from Explorer UPC
Originally, we envisioned a "ChatGPT for documentation." Customer discovery with industrial CEOs revealed they didn't want a chatbot—they wanted to **know where they are losing money.** This led to our pivot toward **Diagnosis Elimination and OEE Visibility.**

---

## 🤖 The Automation Layer

To ensure zero manual overhead, we maintain two background services:

### 1. Discord /update Bot
A daily founder interface that handles task logging.
- **Step 1:** Select completed tasks from the current week.
- **Step 2:** Select tomorrow's focus tasks.
- **Step 3:** Optional qualitative note and milestone adjustment.
- **Action:** Writes to the Notion Execution Log and Daily Log databases.

### 2. Notion Polling Daemon
A background service that monitors Notion for changes (Decision Log entries, Pipeline stage changes, etc.) and triggers Discord notifications or secondary updates to keep systems in sync.

---

## 🔒 Data Privacy, Sovereignty & Security

### NIS2 by Design
We comply with European digital sovereignty requirements by ensuring:
- **No Shared Data:** Every client has an isolated "Private Container."
- **On-Prem Inference:** Raw data never touches the cloud; inference is 100% local.
- **Architecture Sovereignty:** Built using proprietary IP and open-source models, removing dependency on US-based API providers (OpenAI, Google).

---

## 👥 Founder Bios

- **Oriol Farrés i Vilar (CEO/CFO):** Computer Science Engineer from UPC-FIB. Architect of the core AI IP (Markov-Choquet Reranking). Owns strategy and Notion architecture.
- **Arnau Noguer (CTO/AI):** Computer Science Engineer from UPC-FIB. Specialist in RAG pipelines and LLM infrastructure. Owns the retrieval engine and ontologies.
- **Adam Sarrate (COO/CISO):** Computer Science Engineer from UPC-FIB. Specialist in networking and security. Owns deployment topology and compliance.

---

## 📁 Exhaustive Repository Guide

```bash
operations/
├── Makefile                # Master entry point for docs/graph build
├── README.md               # This document (Source of Truth)
├── external/               # Third-party strategy & reference docs
│   └── pol/                # Marketing/Business Plan assets
├── graph-builder/          # Python tools for KG generation
│   ├── build_knowledge_graph.py  # Graph generation script
│   └── knowledge_graph_seed.json # Semantic map of the company
├── graphify-out/           # Output of the Graphify build
│   ├── GRAPH_REPORT.md     # Narrative report of company health
│   └── wiki/               # Auto-generated knowledge wiki
├── internal/               # Core departmental strategies
│   ├── 01_executive_ceo/   # Strategic vision & Pitches
│   ├── 02_technical_cto/   # Infrastructure & Code standards
│   ├── 03_operations_coo/  # Notion OS & Planning systems
│   ├── 04_financial_cfo/   # Fiscal health & Fundraising
│   ├── 05_legal_clo/       # IP & Compliance
│   ├── 06_marketing_cmo/   # Brand & Research
│   ├── 07_sales_cro/       # Pipeline & Leads
│   └── 08_hr_people/       # Talent & Culture
└── scripts/                # Utility scripts for operations
```

---

## 📅 Master Roadmap & Constitution

- **Q2 2026:** Finalize PoCs (Decfa/Paver) and reach A-Score > 0.80.
- **July 1, 2026:** Master's Thesis Defense (Formalizing Core IP).
- **Q3 2026:** Secure 10 Pioneer Client commitments (LOIs).
- **Q4 2026:** Legal Incorporation (Constitution) and first revenue conversion.
- **2027:** Scale to 50 clients; expansion in Spain/Catalonia.
- **2028:** Scale to 100 clients; trigger Seed Round.
- **2029:** Expansion into the European Industrial Corridor (Germany/Italy).

---

*XC Gradient — Proprietary & Confidential. No public web presence. Contact founders for authorized access.*
