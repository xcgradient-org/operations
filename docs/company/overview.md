# XC Gradient

> **Making the invisible visible in manufacturing SMEs** — we convert fragmented operational data into real-time OEE insight, eliminate equipment diagnosis time with a private AI, and go where enterprise vendors won't.

---

## Table of Contents

1. [Mission & Vision](#mission--vision)
2. [Company Overview](#company-overview)
3. [The Problem](#the-problem)
4. [The Solution — What We Build](#the-solution--what-we-build)
5. [Data Privacy Model](#data-privacy-model)
6. [Competitive Moat](#competitive-moat)
7. [Core Architecture](#core-architecture)
8. [Technical IP — Core System](#technical-ip)
   - [Arnau — RAG Engine & Ontologies](#arnau--rag-engine--ontologies)
   - [Oriol — Reranking & Model Serving](#oriol--reranking--model-serving)
   - [Adam — Topology & Data Security](#adam--topology--data-security)
9. [Evaluation Framework](#evaluation-framework)
10. [Deployment](#deployment)
11. [Go-to-Market](#go-to-market)
12. [Active PoC Relationships](#active-poc-relationships)
13. [Team](#team)
14. [Infrastructure & Stack](#infrastructure--stack)
15. [Company Operating System](#company-operating-system)
16. [Roadmap](#roadmap)
17. [Thesis ↔ Product IP Pipeline](#thesis--product-ip-pipeline)

---

## Mission & Vision

Manufacturing SMEs are sitting on enormous amounts of operational data — machine logs, maintenance records, machining parameters, quality procedures, institutional knowledge in the heads of senior technicians. None of it is tangible. None of it is searchable. None of it shows up in a dashboard.

**XC Gradient's mission**: make that data tangible, measurable, and actionable. We give shop floor operators a real-time view of every machine's OEE, reduce equipment diagnosis time to zero, and do it with a private AI system that never exposes their data to external services.

We go where enterprise vendors don't — deep inside the departments of 20-to-200-employee manufacturing companies — because that is exactly where the problem lives and where no one else is willing to go.

---

## Company Overview

| Field | Details |
|---|---|
| **Name** | XC Gradient |
| **Stage** | Early-stage B2B industrial SaaS (pre-public, no web presence) |
| **Segment** | European manufacturing SMEs (20–200 employees) |
| **Differentiator** | Depth-first SME entry + OEE visibility + MTTR elimination via private RAG AI |
| **Founding** | Oriol Farrés i Vilar (CEO/CFO), Arnau Noguer (CTO/AI), Adam Sarrate (COO/CISO) |
| **Equity** | Equal split (1/3 each) |
| **Funding strategy** | Bootstrap-first; no external funding until Seed round post 100+ clients |
| **Origin** | All three founders are CS engineers from UPC-FIB (Facultat d'Informàtica de Barcelona) |

---

## The Problem

Manufacturing SMEs generate enormous amounts of operational data — and almost none of it is usable. The problem is not that the data doesn't exist. The problem is that it's invisible.

**Hidden data:**
- Maintenance logs live in paper binders or Excel files nobody reads
- Machining parameters and quality tolerances are scattered across PDFs and the memory of senior staff
- Machine state is tracked in the head of one experienced technician — when they leave, the knowledge walks out with them
- There is no unified view: no one knows the actual OEE of any machine at any given moment

**Downtime costs:**
- When equipment fails, the bottleneck is almost never fixing it — it's *diagnosing* it
- Diagnosis means: find the right person, pull the right document, cross-reference with past incidents
- This process can take hours or days, and it depends entirely on who happens to be available

Formally:

```
MTTR = time to diagnose + time to fix

In most SMEs, time to diagnose >> time to fix.
The bottleneck is always diagnosis.
```

**Why existing tools don't work:**
- Cloud AI tools (ChatGPT, Microsoft Copilot, Notion AI) require sending proprietary manufacturing data to external servers — a non-starter for most industrial clients
- Generic document search tools have no manufacturing domain depth and produce unreliable answers on technical queries
- Enterprise MES platforms (SAP, IBM Maximo) are priced and scoped for corporations with dedicated IT teams — not for 30-employee CNC shops

---

## The Solution — What We Build

XC Gradient provides a **private AI knowledge layer** embedded directly into the client's operational workflow. The system has five interconnected capabilities:

### 1. Real-Time OEE Dashboard

A 2D interactive plant map where each machine is a clickable node. For every machine:

```
OEE = Availability × Efficiency × Quality

Availability = Total theoretical time − MTTR
             = Total theoretical time − (time to diagnose + time to fix)
```

Operators see the exact OEE value for each machine, broken down into its three components, in real time. This converts the invisible into the measurable.

### 2. Zero-Latency Diagnosis (MTTR Elimination)

The RAG system has ingested every document, manual, maintenance record, and procedure relevant to each machine. When something breaks:

- The operator describes the symptom in natural language
- The system retrieves the exact relevant context (schematics, past incident reports, parameter specs, supplier notes)
- The LLM synthesizes a precise diagnostic answer in seconds

**Result: time to diagnose → 0.** MTTR collapses to time to fix only.

### 3. Unstructured → Structured Data Pipeline

All legacy documents — PDFs, Word files, handwritten logs, maintenance tickets — are ingested, indexed, and made queryable. Data that was invisible and locked in filing cabinets becomes a live, searchable knowledge base.

### 4. Automated Machine State Reports

The system can generate structured reports on machine condition, maintenance history, and OEE trends automatically. Reports that previously required a skilled engineer to produce manually are generated on demand or on schedule.

### 5. LLM-Assisted Error Documentation

When a technician resolves an incident, documenting it is a 2-minute conversation: the system asks a few targeted questions, and the LLM generates the correctly formatted maintenance record. Documentation that nobody does because it takes too long now happens automatically.

---

## Data Privacy Model

This is not "plug your data into ChatGPT." The architecture is fundamentally different.

**How it works:**
- Client data (documents, machine logs, maintenance records) is collected into a **private, isolated container** — one container per client, never shared
- The LLM inference runs locally against that container only
- No client data is ever sent to OpenAI, Microsoft Azure, Google, or any external AI provider
- XC Gradient does not access or read the raw client data for any purpose other than building and improving that client's private knowledge base
- The container is refined over time as the ontology improves — but only to serve that specific client better

**Why this matters:**
- Manufacturing processes are trade secrets. CNC parameters, quality tolerances, and supplier relationships are competitive assets that cannot be exposed to third-party AI training pipelines.
- The private container model gives clients the power of a large language model with zero exposure risk.
- This is architecturally impossible to replicate by pointing a cloud AI tool at a folder of documents — the inference itself must stay private.

---

## Competitive Moat

We are not competing with Microsoft Copilot, Azure OpenAI, or SAP. Those products target a different buyer, require cloud connectivity, and are built for general knowledge work. We go to a place they will not go.

### The Depth-First Strategy

```
Enterprise vendors (SAP, IBM, Microsoft)
└── serve large manufacturers (500+ employees)
    └── ROI justifies the complexity and price
    └── avoid SMEs — diminishing returns per account

XC Gradient
└── enters deep inside SME departments (20–200 employees)
    └── learns the specific machines, processes, and documents
    └── becomes structurally embedded before any competitor notices the segment
```

Enterprise players have no incentive to compete at this depth for this account size. By the time XC Gradient has 100 clients with embedded ontologies, the switching cost for any one of those clients is enormous — the system knows *their* machines, *their* terminology, *their* procedures.

### Why Generic SaaS Tools Also Fail Here

Generic document Q&A tools (Notion AI, Confluence, etc.) fail in manufacturing SMEs for two reasons:
1. They have no manufacturing domain depth — answers on CNC maintenance or injection moulding parameters are unreliable
2. They require cloud connectivity — raw machine data and internal procedures cannot be sent to external services

### Three-Part USP Test

```
Unique?      → Yes. No competitor combines OEE visualization + private RAG
               + MTTR elimination at SME price points.

Valuable?    → Yes. Diagnosis time is the primary driver of maintenance cost
               in SMEs. Eliminating it is a direct, measurable P&L impact.

Defensible?  → Yes. Per-client ontology depth + domain expertise +
               relationship-driven entry creates compounding switching costs.
```

---

## Core Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENT FACILITY                               │
│                                                                       │
│  ┌─────────────────────┐    ┌───────────────────────────────────┐   │
│  │  Data Collection    │    │      XC Gradient Private Layer     │   │
│  │                     │    │                                     │   │
│  │  • Machine sensors  │    │  ┌─────────────────────────────┐  │   │
│  │  • Maintenance logs │───▶│  │   Private Client Container   │  │   │
│  │  • Documents / PDFs │    │  │   (isolated per client)      │  │   │
│  │  • Incident records │    │  └──────────────┬──────────────┘  │   │
│  └─────────────────────┘    │                 │                  │   │
│                               │  ┌──────────────▼──────────────┐  │   │
│  ┌─────────────────────┐    │  │   RAG Retrieval Engine       │  │   │
│  │  OEE Dashboard      │    │  │   + Post-Retrieval Optimizer │  │   │
│  │                     │    │  │   (Markov + Choquet)         │  │   │
│  │  2D Plant Map       │◀───│  └──────────────┬──────────────┘  │   │
│  │  Per-machine OEE    │    │                 │                  │   │
│  │  A × E × Q detail  │    │  ┌──────────────▼──────────────┐  │   │
│  │  MTTR breakdown     │    │  │   Local LLM Inference       │  │   │
│  └─────────────────────┘    │  │   (S-QDoRA fine-tuned,      │  │   │
│                               │  │    no external API calls)   │  │   │
│  ┌─────────────────────┐    │  └──────────────┬──────────────┘  │   │
│  │  Operator Interface │◀───┤                 │                  │   │
│  │                     │    │  ┌──────────────▼──────────────┐  │   │
│  │  • Natural language │    │  │   Output Layer               │  │   │
│  │    diagnosis query  │    │  │   • Diagnostic answers       │  │   │
│  │  • Automated reports│    │  │   • Automated reports        │  │   │
│  │  • Error doc assist │    │  │   • Documentation generation │  │   │
│  └─────────────────────┘    │  └─────────────────────────────┘  │   │
│                               └───────────────────────────────────┘   │
│  ← No data sent to external AI providers. Inference is local. ──── │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Technical IP

The core technical IP is developed across the three founders, each owning a distinct layer of the system. The academic formalization is in Oriol's master's thesis (UPC-FIB, supervised by Dr. Lluís Padró, target defense: July 1, 2026).

### Arnau — RAG Engine & Ontologies

Arnau owns the retrieval foundation: the full RAG pipeline from document ingestion through retrieval, and the ontology layer that makes the system manufacturing-domain-aware.

- **Document ingestion pipeline**: processes PDFs, maintenance logs, manuals, and structured machine data into a queryable index
- **Retrieval engine**: dense + sparse hybrid retrieval over the per-client vector store
- **Ontology construction**: builds and refines the domain ontology that maps manufacturing concepts (machine types, failure modes, parameter families) across the client's knowledge base — this is the core of what gets better over time and creates switching cost
- **Per-client vector store**: isolated index per client, never shared across accounts

### Oriol — Reranking & Model Serving

Oriol owns the post-retrieval optimization layer (the thesis IP) and the model serving stack.

**Reranking:** The retrieval step returns candidate chunks; the reranker selects the optimal context window to pass to the LLM. The approach is formalized as a Markov chain over candidate document sets, with reranking transitions evaluated via a game-theoretic framework (Choquet integral) that captures synergies and redundancies between chunks — something additive scoring methods cannot do.

**Model serving:**
- **S-QDoRA** (Sparse Quantized DoRA): multi-tenant fine-tuning method that gives each client a lightweight sparse adapter on top of a shared quantized base model, enabling per-client specialization without per-client full model storage
- **Speculative decoding**: small draft model generates token candidates verified in parallel by the target model, achieving 2–4× latency reduction — critical for deployments without GPU cluster access

### Adam — Topology & Data Security

Adam owns the system's deployment topology and the security architecture that defines how data moves through the stack.

- **Network topology**: maps how the XC Gradient layer sits within the client's existing infrastructure — what connects to what, where the private container lives, how the LLM inference node is accessed by operators
- **Data security architecture**: defines the isolation guarantees between clients, access control on the private container, and the data flow model that ensures no client data reaches external AI providers
- **Deployment security documentation**: the security-facing assets used in client conversations (what we collect, how it's stored, who can access it)

---

## Deployment

> **Status: Planned.** The client deployment runbook is Arnau's Q2 KR3 (target: May 2026). This section will be populated as the runbook is written.

The deployment model for client sites will cover:

- Minimum hardware requirements for the local LLM inference stack
- Private container setup and initial data ingestion
- OEE dashboard integration with existing machine data sources (sensors, SCADA, manual feeds)
- Ongoing model improvement and ontology refinement process

Until the runbook exists, deployment is handled directly by the XC Gradient team for each PoC site.

---

## Go-to-Market

Pricing model is not yet defined. Leading candidates include per-machine pricing and flat-tier SaaS — to be validated during PoC conversations.

### Strategy

- **Depth-first entry**: go inside a single department, demonstrate measurable OEE improvement, expand from there
- **Land-and-expand**: start with one department or use case, grow to the full plant as trust builds
- **Bootstrap-first**: no external funding until post-100-client milestone; preserves equity and strategic independence
- **No public web presence** at current stage (PoC-first, relationship-driven)
- **Seed round** planned after reaching 100+ paying clients

---

## Active PoC Relationships

### Decfa
- **Sector**: Precision turning / CNC machining
- **Size**: ~30 employees
- **Relationship**: Oriol's family business (father's company) — direct access, low friction
- **Use case**: Eliminate diagnosis time on CNC machine failures; query machining parameter documentation, maintenance records, and quality procedures via natural language; OEE visibility per machine

### Paver
- **Contact**: Xavier Vera (CEO)
- **Location**: Granollers
- **Status**: PoC demo stage
- **Use case**: OEE dashboard across the production plant; RAG-assisted access to operational knowledge base for floor staff; automated maintenance documentation

---

## Team

| Person | Role | Background |
|---|---|---|
| **Oriol Farrés i Vilar** | CEO / CFO | CS Engineering, UPC-FIB; Master's thesis constitutes core IP |
| **Arnau Noguer** | CTO / AI | CS Engineering, UPC-FIB; responsible for RAG engine and LLM infrastructure |
| **Adam Sarrate** | COO / CISO | CS Engineering, UPC-FIB; responsible for operations, security architecture, and client deployment |

All three founders hold equal equity (1/3 each). Responsibilities at PoC stage:
- **Arnau**: RAG pipeline on Decfa corpus, LLM inference setup, A-score target (>0.80 by May 15)
- **Adam**: Network topology graph, on-prem deployment runbook
- **Oriol**: Pain point mapping, client relationship management, thesis → product IP pipeline

---

## Infrastructure & Stack

### Development Workstation (Oriol)

Oriol's personal workstation doubles as the primary development and inference machine during the pre-revenue phase. Electricity cost is €0 (industrial facility flat rate).

| Component | Spec |
|---|---|
| OS | Kubuntu 24.04 |
| CPU | AMD Ryzen 9 9900X |
| GPU | 2× NVIDIA RTX 3090 (24GB VRAM each) |
| RAM | 48GB DDR5 |
| Remote access | Tailscale |
| Vast.ai listing | Machine ID 58948, $0.13/hr per GPU (interruptible) |

Primary use: LLM inference (local), thesis development, SaaS backend development.

### Inference Stack

- Local LLM inference on dual RTX 3090 (48GB total VRAM — sufficient for 70B quantized models)
- Speculative decoding pipeline
- Per-client private vector store

---

## Company Operating System

XC Gradient runs on a Notion-based OS with cascading OKRs, gamified daily logging, and a structured weekly sync cadence.

- Strategic planning, phases, and OKRs: [planning-system.md](../operations/planning-system.md)
- Notion workspace architecture and automation system: [notion-system.md](../operations/notion-system.md)

---

## Roadmap

### Near-Term (Q2 2026)
- [ ] Close Decfa PoC → convert to paying client
- [ ] Close Paver PoC → convert to paying client
- [ ] Thesis defense (target: July 1, 2026) → formalizes IP
- [ ] Ship evaluation framework (Week 1 of coding sprint: April 6–12)
- [ ] Ship Markov + Choquet reranking system (Weeks 2–6)
- [ ] Ship S-QDoRA fine-tuning pipeline (Weeks 7–8)
- [ ] Build OEE dashboard MVP (2D plant map, per-machine A × E × Q breakdown)
- [ ] Write client deployment runbook (Arnau, target: May 2026)

### Medium-Term
- [ ] Reach 10 paying clients
- [ ] Launch public web presence
- [ ] Productize deployment tooling (reduce time-to-deploy for new clients)
- [ ] Expand OEE integration to additional machine data sources

### Long-Term
- [ ] Reach 100+ paying clients → trigger Seed round
- [ ] Expand beyond Catalonia/Spain into broader European manufacturing corridor (Germany, Netherlands, Northern Italy)

---

## Thesis ↔ Product IP Pipeline

The master's thesis (UPC-FIB, supervised by Dr. Lluís Padró) is not academic work isolated from the product — it **is** the product's core technical IP. The mapping is direct:

| Thesis Component | Product Component | Owner |
|---|---|---|
| Markov chain RAG formalization | Reranking pipeline state model | Oriol |
| Choquet integral reranking | Production reranker (post-retrieval optimizer) | Oriol |
| S-QDoRA multi-tenant fine-tuning | Client-specific model adaptation | Oriol |
| Speculative decoding | Inference latency optimization | Oriol |
| Evaluation framework (7-feature ensemble) | Internal quality benchmarking | Oriol |

Defense target: **June 25 / July 1, 2026** | Supervisor: **Dr. Lluís Padró**

---

*XC Gradient — Confidential. No public web presence. Contact via founders.*
