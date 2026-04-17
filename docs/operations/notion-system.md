# XC Gradient — Notion System

> **Self-contained context for new conversations.** This document contains everything needed to work on the XC Gradient Notion workspace and its automation layer without prior context.

---

## Company Context

**XC Gradient** is an early-stage B2B industrial SaaS (founded 2026) targeting European manufacturing SMEs. Three co-founders, equal equity:

| Person | Role | Notion responsibility |
|---|---|---|
| **Oriol Farrés i Vilar** | CEO / CFO | Owns all Notion structure and documentation |
| **Arnau Noguer** | CTO / AI | Fills daily logs and sprint cards; owns Product pages |
| **Adam Sarrate** | COO / CISO | Fills daily logs and sprint cards; owns security/topology docs |

**Operating rule:** Oriol owns Notion structure. Arnau and Adam never touch the architecture — they only fill in their own logs and sprint cards. Oriol extracts decisions from them in the weekly sync and writes everything up.

**Tool stack:**
- **Notion** — single source of truth for all structured knowledge
- **Discord** — working memory, ephemeral; decisions get logged to Notion
- **Drive** — binary storage (PPTs, contracts, invoices, large files)
- **WhatsApp** — personal/emergency only

**The Discord → Notion rule:** when a Discord thread resolves into a decision, someone posts it in `#announcements` and logs it in Notion. Discord is working memory. Notion is long-term memory.

---

## Table of Contents

1. [Planning Hierarchy](#1-planning-hierarchy)
2. [Project Model](#2-project-model)
3. [Task ID Scheme](#3-task-id-scheme)
4. [Database Schemas](#4-database-schemas)
   - [DB1 · OKRs](#db1--okrs)
   - [DB2 · Projects](#db2--projects)
   - [DB3 · Tasks (master)](#db3--tasks-master)
   - [DB4 · Execution Log](#db4--execution-log)
   - [Daily EOD Log](#daily-eod-log)
   - [Weekly Sprint Cards](#weekly-sprint-cards)
   - [Company Calendar](#company-calendar)
   - [Decision Log](#decision-log)
   - [PoC Pipeline](#poc-pipeline)
   - [Personal Finance — Daily Snapshots](#personal-finance--daily-snapshots)
   - [Personal Finance — Monthly Closes](#personal-finance--monthly-closes)
   - [Company Finance — Monthly Closes](#company-finance--monthly-closes)
5. [Auto-Computed Progress Chain](#5-auto-computed-progress-chain)
6. [Workspace Architecture](#6-workspace-architecture)
7. [Operating Procedures](#7-operating-procedures)
   - [Daily EOD Routine](#daily-eod-routine)
   - [Weekly Sync Format](#weekly-sync-format)
   - [Meeting Archive Pipeline](#meeting-archive-pipeline)
   - [Gamification & Streaks](#gamification--streaks)
8. [Notion Build Order](#8-notion-build-order)
9. [Automation System](#9-automation-system)
   - [Vision](#vision)
   - [Discord Bot — /update Flow](#discord-bot---update-flow)
   - [Polling Daemon](#polling-daemon)
   - [Script Architecture](#script-architecture)
   - [Implementation Plan](#implementation-plan)

---

## 1. Planning Hierarchy

The smallest OKR unit is the quarter. Everything below that is execution.

```
Annual Goal      directional, qualitative, frozen for the year
    └── Quarterly OKR    Objective + 3 KRs, hard numbers, expires at quarter end
            └── Monthly Milestone    binary gate per KR — "on track by Apr 30?"
                    └── Weekly Tasks    concrete actions, owned per founder, ID'd
```

**Monthly milestones are not OKRs.** They are progress checkpoints on existing KRs. No new Objective is needed — just a binary answer to "are we on track?" by the end of the month.

Example:
```
KR:               A score > 0.80 on Decfa corpus by Jun 30
April milestone:  Ingestion pipeline complete, baseline A score logged
May milestone:    A score > 0.70 (intermediate gate)
June milestone:   A score > 0.80 ✓/✗
```

**Weekly tasks** are the atomic unit. Milestone progress is computed automatically from task completion — no human updates required above task level.

---

## 2. Project Model

A **project** is a calendar-decoupled container of work. It has a start week and end week, not calendar months. Every task belongs to a project.

**Project types:**

| Type | Description | Example |
|---|---|---|
| Named project | Codename-based scope, multi-founder | **NEON** — Q2 PoC delivery |
| Client work | External deliverable, may span quarters | ServiGalvez CRM |
| Cross-quarter | Transcends OKR cycles, owns its own milestones | Thesis |
| CORE | Permanent ops/admin/BAU bucket | Infrastructure, admin tasks |

**Rules:**
- Every task belongs to exactly one project or CORE
- A project links to one or more KRs in DB1 (optional for CORE)
- Projects close when their deliverable is measured — not at calendar boundaries

### Active Q2 Project: NEON

```
Name:        NEON
Scope:       PoC delivery for Decfa + Paver
Owners:      CEO, CTO, COO (all three)
Week start:  W15 (Apr 7)
Week end:    ~W26 (Jul 1 — thesis defense / phase gate)
KRs served:  Q2-KR1 (2 PoCs with A > 0.80), Q2-KR2 (5 qualified pipeline conversations)
Task IDs:    NEON-CEO-N, NEON-CTO-N, NEON-COO-N
```

CORE runs in parallel for everything outside NEON scope (bot infrastructure, admin, Notion OS setup, finance).

---

## 3. Task ID Scheme

Task IDs are **project-scoped** and **role-scoped**. The sequence resets to 1 each quarter per project per role.

```
Format:    [PROJECT]-[ROLE]-[SEQ]

Examples:
  NEON-CEO-14     →  project NEON, Oriol, task 14
  NEON-CTO-3      →  project NEON, Arnau, task 3
  NEON-COO-7      →  project NEON, Adam, task 7
  CORE-COO-2      →  ops/admin, Adam, task 2
```

**What the founder sees:** `NEON-COO-7` (clean, short).
**What Notion stores:** display ID + year + quarter + role + project — fully unambiguous across the company's entire history.

**The bot handles all ID generation.** When a new task is created, the bot queries DB3: *"how many tasks exist where project = NEON AND role = COO AND quarter = Q2 AND year = 2026?"* It increments by 1 and writes `NEON-COO-N` as the display title. Founders never assign IDs manually.

---

## 4. Database Schemas

Four master databases. Everything lives here — no per-project or per-quarter databases.

### DB1 · OKRs

One row per Key Result (not per Objective). KRs as rows enables clean rollups.

| Property | Type | Notes |
|---|---|---|
| Title | Text | e.g. "KR1 · 2 PoCs with A > 0.80" |
| Objective | Select | Parent objective text |
| Quarter | Select | Q2 2026, Q3 2026, Q4 2026 |
| Year | Select | 2026, 2027, ... |
| Owner | Select | CEO / CTO / COO / All |
| Project | Relation | → DB2 (which project serves this KR) |
| Target | Text | The hard number + deadline |
| Milestone Apr | Formula | % of Apr-tagged tasks done in linked project |
| Milestone May | Formula | % of May-tagged tasks done in linked project |
| Milestone Jun | Formula | % of Jun-tagged tasks done in linked project |
| Overall % | Rollup | tasks_done / tasks_total from DB3 |
| Status | Formula | 🔴 / 🟡 / 🟢 based on pace (see §5) |
| Last EOD note | Text | Bot writes qualitative delta from last /update |

### DB2 · Projects

| Property | Type | Notes |
|---|---|---|
| Name | Title | e.g. "NEON", "CORE", "Thesis" |
| Type | Select | Named / Client / Cross-quarter / CORE |
| Owners | Multi-select | CEO / CTO / COO |
| Week start | Number | e.g. W15 |
| Week end | Number | e.g. W26 |
| KRs | Relation | → DB1 (which KRs this project serves) |
| Tasks | Relation | Backlink from DB3 |
| Tasks done | Rollup | count of DB3 tasks where Status = done |
| Tasks total | Rollup | count of all DB3 tasks |
| Progress | Formula | tasks_done / tasks_total |
| Status | Select | Active / Closed |

### DB3 · Tasks (master)

One master table for every task across all projects, all quarters, all founders. Never reset.

| Property | Type | Notes |
|---|---|---|
| Display ID | Title | e.g. "NEON-COO-7" |
| Role | Select | CEO / CTO / COO |
| Project | Relation | → DB2 |
| KR | Relation | → DB1 (optional, for precise KR attribution) |
| Month | Select | Apr / May / Jun / Jul / ... |
| Year | Number | 2026, 2027, ... |
| Quarter | Select | Q2 2026, Q3 2026, ... |
| Status | Checkbox | Done / Not done |
| Done date | Date | Auto-filled by bot on completion |
| Description | Text | What the task actually is |
| Sprint week | Number | W15, W16, ... |

### DB4 · Execution Log

Append-only. Written exclusively by the bot. Never edited manually.

| Property | Type | Notes |
|---|---|---|
| Date | Date | Log date |
| Person | Select | Oriol / Arnau / Adam |
| Tasks completed | Relation | → DB3 (tasks marked done today) |
| Tomorrow plan | Relation | → DB3 (tasks selected for tomorrow) |
| Milestone % raw | Number | tasks_done / tasks_total at time of log |
| Milestone % adjusted | Number | founder-adjusted value (may differ from raw) |
| Qualitative note | Text | Optional delta text typed by founder |
| Sprint | Relation | → weekly sprint card |

---

### Daily EOD Log

One Notion page per person per day — the human-readable surface of DB4. Generated and written by the bot after `/update` completes. Founders never write this manually.

**Page title format:** `2026-04-09 — Adam`

**Bot-generated page body:**
```
── NEON-COO · Wed Apr 9 ──────────────────────────────
Completed today    NEON-COO-15 · NEON-COO-16
Tomorrow           [tasks selected in step 2]
April milestone    ████████░░░░  38%  (9/24 tasks)
Note               [qualitative delta if provided, else omitted]
──────────────────────────────────────────────────────
```

---

### Weekly Sprint Cards

Created every Sunday night or Monday morning. One per founder per week.

**Page title format:** `W15 — Apr 7–13 — Arnau`

**Properties:**

| Property | Type | Notes |
|---|---|---|
| Week number | Number | W15, W16, ... |
| Owner | Select | Oriol / Arnau / Adam |
| Date range | Date range | Mon–Fri |
| Linked OKR | Relation | → DB1 |
| Status | Select | 🔴 Not started / 🟡 In progress / ✅ Done |

**Page body template:**
```
GOALS THIS WEEK
┌─────────────────────────────────┬────────┬──────────────┐
│ Goal                            │ %      │ Status       │
├─────────────────────────────────┼────────┼──────────────┤
│ [goal 1]                        │  0%    │ 🔴 Not started│
│ [goal 2]                        │  0%    │ 🔴 Not started│
└─────────────────────────────────┴────────┴──────────────┘

WEEK OUTCOME  (filled Friday EOD)
What shipped, what didn't, and why.
```

---

### Company Calendar

Shared calendar on the Home page. Rule: **only events all 3 co-founders need to know about.**

| Property | Type | Notes |
|---|---|---|
| Name | Title | Event name |
| Date | Date | Supports ranges |
| Type | Select | 📅 Meeting / 🏁 Milestone / ⏰ Deadline / 🤝 External |
| Prep required | Checkbox | Does this need preparation? |
| Prep deadline | Date | 2 days before main event |
| Owner | Person | Who drives it |
| Notes | Text | Link to Notion page or Drive folder |

**Pre-seeded events:**
```
Every Tuesday     📅 Weekly Sync
Every Sunday      ⚠️ PREP DUE for Tuesday sync
Apr 11            🤝 Paver intro meeting (Adam)
Apr 30            📅 April Monthly Close + milestone gate review
May 15            🏁 A score > 0.70 gate (Arnau)
May 21            ⏰ Seguiment Report Deadline (Oriol)
May 31            📅 May Monthly Close
Jun 18            ⏰ Thesis Submission (Oriol)
Jun 30            📅 Q2 OKR Review + Q3 Planning
Jul 1             🏁 Phase 1 Gate — Thesis Defense
Sep 15            🏁 Constitution Paperwork Target
Oct 1             🏁 Phase 3 — Launch Gate
```

---

### Decision Log

Permanent record of every significant company decision. Never archived.

| Property | Type | Notes |
|---|---|---|
| Date | Date | When the decision was made |
| Decision | Title | One sentence, declarative |
| Context | Text | Why this decision was needed |
| Alternatives considered | Text | What else was on the table |
| Owner | Select | Who is accountable for executing |

---

### PoC Pipeline

Kanban + table view. One row per prospective client.

**Stages:**
```
Identified → Contacted → Qualifying done → Demo scheduled
          → Demo done → LOI signed → Paying client
```

| Property | Type | Notes |
|---|---|---|
| Company | Title | Client name |
| Stage | Select | Kanban stage |
| Contact | Text | Name + role |
| Location | Text | City / region |
| Sector | Text | Type of manufacturing |
| Size | Number | Approximate employee count |
| A score | Number | RAG accuracy on their corpus (0–1) |
| Next action | Text | What needs to happen next |
| Owner | Select | Oriol / Arnau / Adam |
| Notes | Text | Free field |

---

### Personal Finance — Daily Snapshots

Pushed automatically by personal finance app at month end (31 rows per month).

| Property | Type | Notes |
|---|---|---|
| Date | Date | Day |
| T212 | Number | Trading 212 balance (€) |
| Kraken | Number | Kraken balance (€) |
| Santander | Number | Santander balance (€) |
| Revolut | Number | Revolut balance (€) |
| Cash | Number | Cash (€) |
| Total | Number | Sum of all above |
| Delta | Number | Change from previous day (€) |
| Note | Text | Annotation for anomalies |

---

### Personal Finance — Monthly Closes

| Property | Type | Notes |
|---|---|---|
| Month | Title | e.g. "April 2026" |
| Income | Number | Total income (€) |
| Fixed expenses | Number | Rent, subscriptions, etc. (€) |
| Variable expenses | Number | Everything else (€) |
| Savings | Number | Net savings (€) |
| Net worth | Number | Total across all accounts (€) |
| Savings rate | Number | Savings / Income (%) |
| Report | Text | Full Claude-generated monthly summary |
| Drive link | URL | Link to raw data export |

---

### Company Finance — Monthly Closes

| Property | Type | Notes |
|---|---|---|
| Month | Title | e.g. "April 2026" |
| MRR | Number | Monthly recurring revenue (€) |
| ARR | Number | MRR × 12 (€) |
| Burn | Number | Monthly spend (€) |
| Runway | Number | Cash / Burn (months) |
| Cash | Number | Company cash on hand (€) |
| New clients | Number | Clients added this month |
| CFO Report | Text | Full Claude-generated CFO summary |
| Drive link | URL | Link to raw data export |

---

## 5. Auto-Computed Progress Chain

The full chain from task checkbox to annual goal is automatic. Nobody updates anything above task level manually.

```
DB3 Task checkbox ticked
        ↓
DB2 Project rollup: tasks_done / tasks_total = Progress %
        ↓
DB1 KR formula: monthly milestone % (filtered by month tag)
DB1 KR rollup: overall % across all months
        ↓
DB1 KR status formula:
  expected_pace = (current_week − quarter_start_week) / quarter_duration_weeks
  if overall% ≥ expected_pace − 0.05  →  🟢
  if overall% ≥ expected_pace − 0.15  →  🟡
  else                                →  🔴
        ↓
Annual Goal page: linked DB1 view shows all KR statuses live
```

**Milestone % formula:** `tasks_done_this_month / tasks_total_this_month` where "this month" = all DB3 tasks where `month = Apr` (or May, Jun) AND `project = NEON`. No manual tagging to milestones required — month tag on each task is sufficient.

**The founder-adjusted milestone %:** the raw % is computed automatically, but the founder can override it in step 3 of `/update` if the raw count misrepresents reality (e.g. two large tasks remain that count as 2 but represent 60% of remaining work). The adjusted value is what gets written to DB4 and displayed in the EOD log.

---

## 6. Workspace Architecture

```
XC Gradient OS (Notion workspace)
│
├── 🏠 Home                          ← everyone's landing page, always open
├── 🎯 Goals & OKRs                  ← full cascade from yearly to weekly
├── 📓 Daily Logs                    ← bot-generated, one entry per person per day
├── 📅 Weekly Syncs                  ← meeting outputs, AI summaries
├── 🧠 Company Brain                 ← permanent knowledge, never changes week to week
└── 📁 Archive                       ← anything older than 2 quarters
```

### 🏠 Home

```
PHASE BANNER              big callout block, updated manually at phase gates
NORTH STAR                current phase's north star metric + live value
BIG 3 THIS WEEK           #1 / #2 / #3 with owner and current value
STREAKS                   Oriol 🔥N  Arnau 🔥N  Adam 🔥N
COMPANY CALENDAR          2-week rolling view
QUICK LINKS               → This week's sprint card
                          → Decision Log
                          → PoC Pipeline
                          → Latest weekly sync
```

### 🎯 Goals & OKRs

```
├── 🏆 2026 Annual Goal              frozen single page — linked DB1 views per quarter
│   ├── Q2 OKR view                  DB1 filtered to Q2 · KR title, %, status, last note
│   ├── Q3 OKR view                  DB1 filtered to Q3 · stub
│   └── Q4 OKR view                  DB1 filtered to Q4 · stub
│
├── Q2 2026  (CURRENT)
│   ├── Company OKRs                 DB1 view
│   ├── Project NEON                 DB2 row + linked DB3 task view
│   └── Monthly milestones
│       ├── April   ← fully detailed + gate date Apr 30
│       ├── May     ← direction only
│       └── June    ← direction only
│
├── Q3 2026  stub
├── Q4 2026  stub
│
└── 📋 Sprint Goals
    └── one page per week (W15, W16, ...)
```

### 🧠 Company Brain

```
├── Strategy
│   ├── Mission & Vision
│   ├── ICP Definition
│   └── Qualifying Question
│
├── Decision Log                  DATABASE — permanent
├── PoC Pipeline                  DATABASE — Kanban + table
│
├── Finance
│   ├── Personal Monthly Closes   DATABASE
│   ├── Company Monthly Closes    DATABASE
│   └── Runway model              link to Drive
│
└── Product
    ├── Architecture overview     Arnau owns
    └── Deployment runbook        populates during Q2
```

---

## 7. Operating Procedures

### Daily EOD Routine

The founder does **not** write the EOD log. The bot writes it. The founder's job is to run `/update` in Discord.

1. Open Discord, run `/update`
2. Complete the 3-step bot flow (see §9)
3. Bot writes the EOD page to Notion and updates DB4
4. Bot updates streak counter on Home

Total time: ~3 minutes. If `/update` is not run before midnight, streak resets to zero.

---

### Weekly Sync Format

Fixed format, ~60 minutes, every Tuesday morning.

```
0:00  ARNAU presents  (10 min)
      → Week card review: what shipped, what didn't
      → One key demo or output shown live
      → Blockers needing resolution in this meeting

0:10  ADAM presents   (10 min)
      → Week card review
      → Customer interactions, network updates
      → Operational blockers

0:20  ORIOL presents  (15 min)
      → Week card review
      → Scoreboard read aloud: NEON-CEO / NEON-CTO / NEON-COO milestone %
      → Financial / runway update if relevant

0:35  JOINT DECISIONS  (15 min)
      → Resolve all blockers from steps 1–3
      → Align on next week's sprint cards
      → Log decisions in Decision Log

0:50  NEXT WEEK SPRINT CARDS  (10 min)
      → Built together live in Notion before leaving the room
```

**Weekly scoreboard (read aloud at 0:20):**

```
┌──────────────┬───────────┬────────────┬─────────────────┐
│  Founder     │ KR target │ Milestone% │ Status          │
├──────────────┼───────────┼────────────┼─────────────────┤
│  Arnau       │ A > 0.80  │  38%       │  🟡 behind pace │
│  Adam        │ 1 meeting │  20%       │  🔴 at risk      │
│  Oriol       │ 2 leads   │  55%       │  🟢 on track     │
└──────────────┴───────────┴────────────┴─────────────────┘
Running streak: Arnau 🔥3  Adam ⚠️0 (missed yesterday)  Oriol 🔥5
```

---

### Meeting Archive Pipeline

Every weekly sync produces a permanent AI-processed record.

**Drive folder structure:**
```
Drive/
└── Weekly Syncs/
    └── 2026-W15_2026-04-07/
        ├── oriol_w15.pptx
        ├── arnau_w15.pptx
        ├── adam_w15.pptx
        └── adam_notes_w15.txt
```

**AI processing (run after each meeting):**

Feed 3 PPTs + Adam's raw notes to Claude:

```
Output:
  1. Executive summary (5 bullets, decisions only)
  2. Full meeting writeup (structured, ~400 words)
  3. Action items (owner + deadline + linked goal)
  4. Decision log entries (pre-formatted for Notion paste)
```

---

### Gamification & Streaks

**Streak Tracker (Home page):**

```
👤 Person    🔥 Current Streak    📅 Last Log      🏆 Best Streak
Oriol        12 days              Today            18 days
Arnau        7 days               Today            7 days
Adam         3 days               Yesterday ⚠️     9 days
```

**Rules:**
- A day counts if `/update` completed before midnight
- Missing a day resets to zero
- Weekends optional but count if submitted
- ⚠️ warning appears if someone has not run `/update` by 7pm

**What is not gamified:** output quality, goal achievement rate, comparison between founders. The streak measures discipline only.

---

## 8. Notion Build Order

Build in this sequence. Each block ~15–20 minutes.

```
Block 1  Workspace root — 6 top-level pages                  15 min
Block 2  DB1 OKRs — Q2 KRs (3 rows), annual goal stub,
         Q3/Q4 stubs                                          20 min
Block 3  DB2 Projects — NEON row, CORE row                    10 min
Block 4  DB3 Tasks — master table, no rows yet
         (bot populates these during /update)                 15 min
Block 5  DB4 Execution Log — empty, bot writes only           10 min
Block 6  Home page — phase banner, north star,
         big 3, streaks, quick links, calendar                20 min
Block 7  Goals & OKRs — annual goal page with linked
         DB1 views, Q2 page with NEON view,
         monthly milestone stubs                              25 min
Block 8  Daily Logs — 3 subfolders (Oriol/Arnau/Adam)
         no templates needed (bot generates pages)            10 min
Block 9  Weekly Syncs — W15 stub ready                        10 min
Block 10 Company Brain — Strategy, Decision Log DB,
         PoC Pipeline DB (Kanban), Finance stubs,
         Product stubs                                        20 min
Block 11 Archive — empty folder                               5 min
```

**What to leave blank intentionally:**
- Arnau and Adam's personal Q2 KR details → they fill these in the first sync
- Sprint goals → built live in the sync
- DB3 Tasks → bot populates; never pre-fill manually
- Q3/Q4 OKR details → populated at quarter boundaries only

---

## 9. Automation System

### Vision

Two complementary automation layers:

1. **Discord bot** — the active interface founders use daily (`/update`)
2. **Polling daemon** — passive background process that reacts to Notion changes

Together they ensure zero manual overhead above task level. Founders interact only with Discord. Notion updates itself.

---

### Discord Bot — /update Flow

Triggered by the founder. Three sequential steps delivered as a Discord modal.

**Step 1 — Completed tasks**

```
Bot:  "Today you completed: NEON-COO-15, NEON-COO-16.
       Anything else to add?"

Founder options:
  A) types free text describing additional work
     → bot creates new DB3 tasks with auto-generated IDs + marks them done
  B) clicks skip / confirms nothing more
```

**Step 2 — Tomorrow's plan**

```
Bot:  shows multiselect of all open DB3 tasks for this founder
      this month (not done, current sprint week first)

Founder:  clicks which tasks to do tomorrow
          (no typing — pure multiselect)
```

**Step 3 — Milestone delta**

```
Bot:  "April milestone: 9/24 tasks done → 38%.
       Does this feel right? Adjust if needed."

Founder:  confirms as-is (one click)
          OR enters a different % if raw count misrepresents reality
          OR adds a short qualitative note (optional)
```

**Step 4 — Bot writes to Notion**

```
→ Marks selected tasks done in DB3 (step 1 completions)
→ Creates any new tasks from free text (step 1 additions), with auto-generated IDs
→ Flags tomorrow's tasks in DB3 (step 2 selections)
→ Writes EOD entry to DB4 (milestone %, adjusted %, note)
→ Generates Daily EOD Log page in Notion (human-readable surface)
→ Updates streak counter on Home page
→ Patches last_eod_note on the relevant DB1 KR row
```

**ID generation logic (step 1 new tasks):**

```python
# Bot queries DB3:
count = query_db3(project="NEON", role="COO", quarter="Q2", year=2026)
new_id = f"NEON-COO-{count + 1}"
# Writes new task to DB3 with display_id = new_id, status = done, done_date = today
```

---

### Polling Daemon

Passive background process. Polls Notion API on fixed intervals and triggers handlers on detected changes.

**Polling targets:**

| Database | Poll interval | Detection method |
|---|---|---|
| DB3 Tasks | Every 15 min | `last_edited_time` change (checkbox ticked outside bot) |
| Decision Log | Every 30 min | New pages created since last poll |
| PoC Pipeline | Every 30 min | `Stage` property change |
| Company Finance | Every 60 min | New pages created since last poll |

**State file:** `~/.xcg_notion_state.json`

```json
{
  "tasks": {
    "last_poll": "2026-04-09T10:00:00Z",
    "last_edited": {"page_id_1": "2026-04-09T09:30:00Z"}
  },
  "decision_log": {
    "last_poll": "2026-04-09T10:00:00Z",
    "seen_page_ids": []
  },
  "poc_pipeline": {
    "last_poll": "2026-04-09T10:00:00Z",
    "stages": {"Decfa": "Demo scheduled", "Paver": "Contacted"}
  }
}
```

---

### Script Architecture

```
xcg-notion/
├── bot.py                ← Discord bot entry point (Pycord)
├── daemon.py             ← polling daemon entry point
├── config.py             ← tokens, DB IDs, webhook URLs
├── state.py              ← read/write ~/.xcg_notion_state.json
├── notion_client.py      ← thin wrapper: query, patch, create pages
├── discord_client.py     ← post to Discord channels via webhook
│
├── bot_handlers/
│   ├── update.py         ← /update flow: steps 1-2-3 → Notion writes
│   └── id_generator.py   ← query DB3 count → return next NEON-COO-N
│
├── poll_handlers/
│   ├── tasks.py          ← on task edit outside bot: recompute rollups
│   ├── decision_log.py   ← on new decision: post to #announcements
│   ├── poc_pipeline.py   ← on stage change: notify #gtm
│   └── finance.py        ← on new monthly close: update Home north star
│
└── utils/
    ├── streak.py         ← given list of log dates → current + best streak
    ├── milestone.py      ← tasks_done / tasks_total filtered by month + project
    ├── pace.py           ← expected_pace formula → 🔴/🟡/🟢 status
    └── notion_updater.py ← helpers: patch properties, create pages, append blocks
```

**`config.py`:**

```python
NOTION_TOKEN = "secret_..."
DISCORD_BOT_TOKEN = "..."
POLL_INTERVAL_SECONDS = 900

# Database IDs
DB_OKRS            = "..."    # DB1
DB_PROJECTS        = "..."    # DB2
DB_TASKS           = "..."    # DB3
DB_EXEC_LOG        = "..."    # DB4
DB_DECISION_LOG    = "..."
DB_POC_PIPELINE    = "..."
DB_COMPANY_FINANCE = "..."

# Notion page IDs
PAGE_HOME          = "..."

# Discord webhook URLs
DISCORD_ANNOUNCEMENTS = "https://discord.com/api/webhooks/..."
DISCORD_GTM           = "https://discord.com/api/webhooks/..."
```

---

### Implementation Plan

**Phase 1 — Foundation:**
1. `notion_client.py` — wrap `GET /v1/databases/{id}/query` and `PATCH /v1/pages/{id}`
2. `state.py` — read/write state JSON; handle missing file on first run
3. `config.py` — fill all IDs and tokens

**Phase 2 — /update bot (highest priority):**
4. `id_generator.py` — query DB3, return next sequential ID per project/role/quarter
5. `bot_handlers/update.py` — step 1 (detect + create tasks), step 2 (multiselect), step 3 (milestone %)
6. `utils/milestone.py` — compute tasks_done/tasks_total filtered by month + project
7. `notion_updater.py` — write DB3 tasks, DB4 exec log entry, Daily EOD log page, Home streak patch

**Phase 3 — Streak + scoreboard:**
8. `utils/streak.py` — compute current + best streak from DB4 log dates
9. `utils/pace.py` — expected_pace formula → status emoji
10. Wire streak update to Home page after each `/update` call

**Phase 4 — Polling daemon:**
11. `daemon.py` — poll loop
12. `poll_handlers/decision_log.py` — new decision → post to `#announcements`
13. `poll_handlers/poc_pipeline.py` — stage change → post to `#gtm`
14. `poll_handlers/finance.py` — new monthly close → patch Home north star

**Running:**

```bash
pip install requests pycord

# Bot (foreground or screen session)
python bot.py

# Daemon (separate screen session)
python daemon.py
```

---

*For strategic planning, phases, OKRs, and growth model, see [planning-system.md](./planning-system.md).*
*For company overview, product description, and technical IP, see [overview.md](../company/overview.md).*
