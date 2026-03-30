# Colombo Jobs Pulse Night Build Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a defended jobs-product direction for Colombo youth and implement the strongest possible mobile-first web MVP slice by morning.

**Architecture:** Preserve the existing Python research foundation while adding a separate web product slice under `apps/web`. Pair evidence-backed product docs with a seeded frontend demo and tested domain logic for story expiry, trust surfacing, job relevance, and reporting hooks.

**Tech Stack:** Python repo foundation, TypeScript web app, React/Vite or Next-class app shell, Vitest/Playwright for new web checks, markdown research docs, JSON/YAML contracts.

---

### Task 1: Live governance files

**Files:**
- Create: `task_rubric.md`
- Create: `STATUS.md`
- Create: `DECISIONS.md`
- Create: `REJECTED_IDEAS.md`

**Step 1: Write the files**

- Capture mission, chosen weapons, current state, initial decisions, and first rejected ideas.

**Step 2: Keep them fresh**

- Update these files whenever the product direction changes or implementation status shifts.

### Task 2: Market and wedge research

**Files:**
- Create: `research/market_map.md`
- Create: `research/wedge_matrix.md`
- Create: `research/final_wedge_decision.md`
- Modify: `evidence/source_catalog.json`
- Modify: `EVIDENCE_INDEX.md`

**Step 1: Collect current sources**

- Use live web research for Sri Lanka labor conditions, mobile behavior, scam patterns, and incumbent platforms.

**Step 2: Write the scoring matrix**

- Compare at least 7 wedges, score them, reject weak ones explicitly, and choose a winner plus backup.

### Task 3: Product, UX, stories, trust, and architecture package

**Files:**
- Create: `product/*.md`
- Create: `ux/*.md`
- Create: `stories/*.md`
- Create: `trust/*.md`
- Create: `architecture/*.md`

**Step 1: Define the product truth**

- Lock the ICP, habit loop, content loop, trust loop, and retention model.

**Step 2: Define the execution**

- Specify end-to-end flows, story rules, moderation rules, data model, API contracts, jobs, analytics, and admin needs.

### Task 4: Web MVP slice

**Files:**
- Create: `apps/web/...`
- Create: app-level tests before custom product logic

**Step 1: Add failing tests**

- Cover at least story expiry behavior, ranking/trust utility helpers, and reporting/moderation hooks before implementing those modules.

**Step 2: Build the UI**

- Implement onboarding, profile setup, feed shell, story reel shell, job detail, story composer, trust badges, and reporting UI with seeded data.

**Step 3: Verify**

- Run unit tests, type checks, build checks, and browser-level sanity checks.

### Task 5: Demo, QA, and handoff

**Files:**
- Create: `demo/*.md`
- Create: `qa/*.md`
- Create: `HANDOFF/*.md`
- Modify: `CHANGELOG.md`

**Step 1: Capture demo assets**

- Save screenshots and write a walkthrough plus “why this wins” brief.

**Step 2: Run verification**

- Record lint, type, build, responsiveness, expiry, and moderation status honestly.

**Step 3: Ship the handoff**

- Summarize what won, what was built, what is mocked, and the next 72 hours of work.
