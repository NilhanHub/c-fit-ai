---
title: SAN Repo OS Blueprint
edition: 3.7
date: 2026-03-28
status: current-working-edition
audience: coding agents, human maintainers, repo stewards
mode: operational doctrine + bootstrap + retrofit + continuous alignment
compatibility: agent-agnostic, project-agnostic, repo-age-agnostic, OS-agnostic, VCS-agnostic
canonical_model: five-plane SAN model with cross-cutting overlays
san_supervisor: Sanlock
---

# SAN Repo OS Blueprint
## Edition 3.7 — March 28, 2026
## Stateless-Agent-Native Repository Operating System

## 0. Executive delta

This edition keeps the **five-plane SAN model** from the earlier books, but hardens it with stronger invariants and better cross-cutting doctrine.

The biggest upgrade is this:

**SAN is not just an internal repo hygiene pattern.  
SAN is an operating system for stateless agents that must survive cold entry, long-horizon work, repeated handoffs, outward sharing, and continuous tuning.**

Edition 3.7 therefore strengthens or formalizes all of the following:

- singular canonical control-plane authority,
- equivalent manifestations / same invariant,
- session / thread / tool memory as non-authoritative,
- artifact-class separation and outward exposure boundaries,
- command-first mutation for deterministic multi-surface updates,
- recurring-failure memory and escalation,
- versioned change stewardship with diffable checkpoints, review surfaces, and rollback paths,
- default code-control adapter guidance for Git and GitHub-like forges,
- machine-readable topology graphs or equivalent structured node maps,
- node-budget governance with a default 5 percent effective-load target,
- Sanlock checks for oversized gravity wells, topology drift, and dispersion readiness,
- conditional purpose-scoped execution contexts,
- conditional rehydration truth contracts for stateful systems,
- Sanlock as the standing SAN debugger / inspector / tuner,
- SAN as a continuous alignment system, not a one-shot bootstrap ritual.

This blueprint is deliberately **abstract at the invariant level** and **adapter-friendly at the implementation level**.

It does not assume:
- one agent vendor,
- one repo layout,
- one instruction filename everywhere,
- one shell,
- one task runner,
- one orchestration runtime,
- one packaging strategy,
- one export mechanism,
- one version-control workflow.

It does define:
- what MUST be true,
- what SHOULD be true,
- what MAY vary,
- what is adapter-specific,
- what is conditional,
- what must be scored every run.

---

## 1. Normative language

The words **MUST**, **SHOULD**, **MAY**, **MUST NOT**, and **SHOULD NOT** are normative.

---

## 2. Primary mission

A repo is SAN-aligned when a fresh stateless agent can:

1. identify governing doctrine,
2. determine which doctrine actually applies,
3. recover current durable repo truth,
4. discover the current bounded work surface,
5. discover the real execution and verification entrypoints,
6. perform bounded work without hidden tribal context,
7. prove what happened with evidence,
8. update durable repo truth,
9. hand off cleanly,
10. leave the SAN harness intact or stronger,
11. survive resumed work after cold restart,
12. support outward sharing without leaking internal operator doctrine when outward sharing is active.

If those conditions are not true, the repo is not yet operating as a SAN repo OS.

---

## 3. Compatibility envelope

This blueprint is intentionally:

- **agent-agnostic**
- **project-agnostic**
- **repo-age-agnostic**
- **OS-agnostic**
- **VCS-agnostic**
- **runtime-agnostic**
- **layout-agnostic**
- **tool-vendor-agnostic**

That means the blueprint is built from **invariants, roles, planes, overlays, classes, and adapters**.

It is not built from:
- one hard-coded directory structure,
- one fixed branching pattern,
- one fixed state-file naming scheme,
- one mandatory orchestration runtime,
- one mandatory export/archive mechanism.

---

## 4. Core model

### 4.1 The repo is an agent operating system

A SAN repo is not merely a code folder.

It is an **agent operating system**:
- it carries doctrine,
- it carries memory,
- it packages capabilities,
- it routes tools and runtime behavior,
- it defines trust boundaries,
- it exposes a resumable control plane,
- it can be inspected and tuned.

### 4.2 The five-plane model remains

Edition 3.7 keeps the five-plane model:

1. **Doctrine plane**
2. **State plane**
3. **Capability plane**
4. **Tool / runtime plane**
5. **Trust plane**

No new base plane is required.

Instead, Edition 3.7 adds stronger **cross-cutting overlays** that operate across multiple planes.

### 4.3 Cross-cutting overlays

The main cross-cutting overlays are:

- singular canonical control-plane authority,
- session memory non-authority,
- artifact-class separation,
- outward exposure governance,
- command-first mutation,
- recurring-failure memory,
- topology graph and node-budget governance,
- Sanlock supervisory inspection.

These are not separate planes.
They are cross-cutting operating laws.

### 4.4 Invariants vs adapters

Edition 3.7 makes an explicit distinction:

- **Invariant** = what MUST be true
- **Adapter** = how a given toolchain or repo manifests that truth
- **Conditional doctrine** = applies only when the repo or workflow has the relevant property
- **Example** = a current common implementation, not a timeless law

A future-proof SAN blueprint must prefer invariants over adapters.

---

## 5. Core architectural axioms

### 5.1 Canonical doctrine is not the same as client load order

A shared repo doctrine surface SHOULD exist.

Today, common implementations include `AGENTS.md` for Codex-style instruction discovery, `CLAUDE.md` for Claude Code, and repository/path-specific instruction files for GitHub Copilot. But the invariant is not the filename. The invariant is that the repo can explain:
- what doctrine is canonical,
- what other instruction surfaces exist,
- what precedence rules apply,
- which layers are shared versus tool-specific.

### 5.2 The repo must carry the memory

Durable repo truth MUST outrank:
- chat memory,
- thread memory,
- tool auto-memory,
- session assumptions,
- stale conversational context.

Transient memory is advisory only.

### 5.3 Deterministic work belongs in code, commands, hooks, workflows, or generators

If a step is:
- repeated,
- derivable,
- mechanically checkable,
- cross-surface,
- likely to recur,

then it SHOULD NOT live only in prose.

### 5.4 Capability packaging beats prompt bloat

Reusable workflows SHOULD be packaged as skills, plugins, subagents, hooks, scripts, generators, typed workflows, or equivalent reusable capability surfaces.

Do not solve recurring work by making one giant root prompt fatter forever.

### 5.5 One canonical control plane, not many plausible ones

The repo MUST present one write-authoritative control plane for operational truth.

Mirrors, generated views, local overlays, convenience views, and transitional legacy surfaces MAY exist.
Competing authorities MUST NOT.

### 5.6 Equivalent manifestations, same invariant

Different repos MAY manifest the same SAN invariant differently.

Examples:
- one repo may use a dedicated SAN root,
- another may use an existing state-docs surface,
- another may use a generated control-plane index,
- another may use layered instruction surfaces plus a durable state store.

These are acceptable only if they preserve the invariant.

**Shape is negotiable.  
Authority is not.**

### 5.7 Command-first mutation beats hand synchronization

When a change spans coupled or derived surfaces, SAN prefers a rerunnable mutation path anchored to declared source truth.

Human memory is not a synchronization system.

### 5.8 Versioned change stewardship is part of SAN, not optional garnish

A SAN repo MUST provide a **versioned change-control surface** with:
- diffable history,
- reviewable checkpoints,
- reversible or rollback-capable change paths,
- bounded work isolation when concurrency or risk requires it,
- promotion or merge semantics that do not depend on tribal memory alone.

Git is the default contemporary adapter.
GitHub, GitLab, Bitbucket, Forgejo, Gitea, or equivalent forges are collaboration adapters.
The invariant is not the vendor.
The invariant is durable, inspectable, reviewable change stewardship.

### 5.9 Reviewability is part of correctness

A change is not SAN-correct if it is:
- hard to review,
- hard to reproduce,
- hard to verify,
- hard to revert,
- impossible to resume from.

### 5.10 The dry-run or re-entry run is the real gate

A beautiful doctrine file does not prove SAN alignment.

The real proof is whether a fresh agent can:
- enter,
- orient,
- act,
- verify,
- update state,
- hand off,
without tribal intervention.

### 5.11 SAN is continuous

Bootstrap is not the end of SAN.

Every serious agent run is a chance to:
- detect drift,
- tighten weak doctrine,
- soften overbuilt ceremony,
- add missing automation,
- repair stale control-plane surfaces,
- improve recovery and handoff quality.



### 5.12 The repo SHOULD remain legible as a bounded node graph

A SAN repo SHOULD expose a machine-readable topology graph or equivalent structured map of bounded nodes and edges.

The invariant is not one specific file path.
The invariant is that the repo can explain, inspect, and progressively improve:
- what the bounded nodes are,
- how they relate hierarchically,
- what they directly depend on,
- what they verify,
- which nodes are oversized or hotspot-prone,
- which nodes are ready to disperse further.

JSON is the default contemporary adapter because modern graph tooling can emit or consume JSON representations, but the law is the structured graph, not the serialization.

### 5.13 No node should become an unexamined gravity well

A SAN repo SHOULD avoid letting one node silently absorb too much of the app’s structural burden.

The default doctrine is:
- target each node at no more than **5 percent of effective app load**,
- treat more than **5 percent** as a review trigger,
- treat more than **10 percent**, or repeated hotspot gravity, as a mandatory dispersion review unless the node is explicitly justified as exceptional.

Effective app load is not raw LOC alone.
It is a weighted structural burden combining factors such as:
- code-surface share,
- dependency centrality,
- fan-in / fan-out pressure,
- affected radius,
- change frequency,
- runtime or business criticality,
- verification span,
- hidden-state risk.

Splitting by line count alone is not SAN.
Truthful boundedness is SAN.

---

## 6. Plane model

## 6.1 Doctrine plane

### Purpose
The doctrine plane tells agents how to behave.

### It MUST define
- canonical doctrine surface,
- precedence assumptions,
- verification expectations,
- update obligations,
- authority rules,
- anti-patterns,
- required scoring or inspection expectations.

### It SHOULD define
- bounded work style,
- preferred review granularity,
- permission posture,
- escalation expectations,
- conditionally activated doctrines.

### It MAY include
- tool-specific overlays,
- environment-specific overlays,
- path-scoped rules,
- specialization rules,
- mode-specific instructions.

### Current common adapters
Examples only, not invariants:
- `AGENTS.md`
- `AGENTS.override.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`
- path-scoped instruction files
- imported or nested instruction fragments

### Core rule
The doctrine plane MUST be thin enough to remain durable and thick enough to prevent drift.

---

## 6.2 State plane

### Purpose
The state plane carries durable repo truth.

### It MUST hold durable answers for
- current state,
- current work,
- current decisions,
- open questions,
- verification truth,
- re-entry / resume truth,
- next-step truth,
- authority mapping.

### It SHOULD expose
- repo map,
- seam map,
- bounded node topology graph,
- affected-radius map,
- hotspot map,
- current risk areas,
- active work mode,
- current verification posture.

### It MAY include
- generated memory indexes,
- machine-readable summaries,
- vector or database-backed memory stores,
- state snapshots,
- delta summaries,
- generated dashboards.

### Core rule
The state plane MUST be auditable, versionable or inspectable, resumable, and recoverable by a fresh agent.

---

## 6.3 Capability plane

### Purpose
The capability plane packages reusable workflows and narrow expertise.

### It SHOULD contain
- repeatable operating knowledge,
- reusable checklists,
- deterministic wrappers,
- narrow subagents,
- hooks for reliable automation,
- specialized command or generation surfaces.

### It MUST avoid
- giant “do everything” blobs,
- hidden capability behavior with no discoverable trigger boundary,
- duplicate authority with the doctrine plane.

### Core rule
One capability = one operational pattern with clear trigger, boundary, verification, and exit conditions.

---

## 6.4 Tool / runtime plane

### Purpose
The tool / runtime plane connects agents to tools, execution environments, orchestration logic, and durable long-horizon work surfaces.

### It MAY include
- MCP or equivalent tool protocols,
- tool adapters,
- runtime graphs,
- durable execution engines,
- subgraphs,
- approval interceptors,
- execution isolation mechanisms,
- typed command wrappers.

### Core rule
The runtime plane MUST NOT smuggle ungoverned authority outside the control plane.

The repo must still know:
- what work is happening,
- what state matters,
- what was verified,
- what approvals were used,
- where resumable truth lives.

---

## 6.5 Trust plane

### Purpose
The trust plane governs verification, tracing, evals, review, approvals, release gating, handoff quality, and outward exposure readiness.

### It MUST cover
- verification entrypoints,
- test / lint / typecheck / build or equivalent validation,
- review expectations,
- merge / release gating,
- provenance or traceability expectations,
- approval boundaries.

### It SHOULD cover
- evals,
- trace grading,
- recurrence clustering,
- outward sharing gates,
- release / checkpoint provenance.

### Core rule
The trust plane converts “the agent says it worked” into evidence-backed truth.

---

## 7. Cross-cutting invariant: singular canonical control plane

### 7.1 Definition
A SAN repo MUST have one authoritative control plane that owns:
- doctrine truth,
- current operational truth,
- execution truth,
- verification truth,
- handoff truth,
- authority mapping.

### 7.2 What singular means
“Singular” does not mean only one file or one folder exists.

It means:
for any operational question, the repo has one deterministically preferred write-authoritative answer at decision time.

### 7.3 Allowed non-canonical surfaces
The repo MAY have:
- mirrors,
- generated views,
- local convenience overlays,
- transitional legacy surfaces,
- read-optimized summaries.

But they MUST be explicitly non-canonical or transitional.

### 7.4 Failure modes
Control-plane singularity is broken when:
- two surfaces both appear authoritative,
- different agents update different truths,
- mirrors drift silently,
- legacy docs still behave like shadow authority,
- no one can answer “where should this truth be written?”

### 7.5 Future-proof rule
Edition 3.7 explicitly adopts:

**Equivalent manifestations, same invariant.**

The invariant is mandatory.
The manifestation is adaptable.

---

## 8. Cross-cutting invariant: session / thread / tool memory is non-authoritative

### 8.1 Rule
Transient session memory MUST yield immediately to:
- durable repo truth,
- live observed repo state,
- actual verification outcomes,
- actual approvals,
- actual current execution context.

### 8.2 Operational consequence
When ambient tool or thread memory drifts, the correct fix is often:
- refresh,
- restart,
- re-enter,
- re-orient from repo truth,

not repo mutation to satisfy stale memory.

### 8.3 Anti-pattern
Do not mutate repo reality to match a stale session belief.

### 8.4 Why this matters
Stateless systems fail when the agent trusts remembered context more than durable truth.

---

## 9. Cross-cutting invariant: artifact classes and exposure boundaries

### 9.1 Rule
Artifacts MUST be classified by:
- role,
- audience,
- authority,
- exposure level.

### 9.2 Minimum abstract artifact classes

A SAN repo SHOULD distinguish at least these classes:

1. **Doctrine**
2. **Machine recovery state**
3. **Execution state**
4. **Verification evidence**
5. **Governance / audit**
6. **Product source truth**
7. **Outward narrative / handoff**
8. **Release / provenance summary**

### 9.3 Private-by-default classes
The following SHOULD be private by default:
- doctrine,
- machine recovery state,
- execution state,
- internal verification evidence,
- supervisory tuning history,
- internal governance / audit detail.

### 9.4 Potentially outward-facing classes
The following MAY become outward-facing when curated:
- product source truth,
- outward narrative / handoff,
- release / provenance summary,
- sanitized examples and public run instructions.

### 9.5 Export boundary rule
No artifact whose primary purpose is:
- internal recovery,
- supervision,
- tuning,
- unresolved internal reasoning,
- private verification detail,

MAY cross an outward boundary unless it is explicitly:
- reclassified,
- sanitized,
- reviewed,
- approved for outward use.

### 9.6 Important consequence
When outward sharing is active, the outward-facing source surface itself SHOULD be safe to inspect.
Do not rely only on “final zip cleanup” if the outward-facing working surface is itself unsafe.

### 9.7 Anti-patterns
- ad hoc panic deletion before handoff,
- mixing internal evidence with client truth,
- exposing operator doctrine as if it were product documentation,
- outward sharing from unsafe mutable surfaces.

---

## 10. Cross-cutting invariant: command-first mutation of coupled surfaces

### 10.1 Rule
If an update is:
- deterministic,
- repeated,
- derived,
- mechanically checkable,
- cross-surface,
- likely to recur,

it MUST prefer a rerunnable mutation path anchored to declared source truth.

### 10.2 Examples of command-worthy update classes
Abstract classes:
- generated views,
- mirrors,
- indexes,
- summary refreshes,
- coordinated migrations,
- repeated state-surface updates,
- coupled metadata refreshes,
- codemods,
- scaffolding expansions,
- release / export manifest refreshes.

### 10.3 Safeguards
A command-first mutation path SHOULD provide:
- declared source truth,
- rerunnability,
- safe replay behavior,
- explicit side-effect boundary,
- verification after mutation,
- provenance recording,
- idempotence where practical,
- human approval when destructive.

### 10.4 Anti-pattern
Hand-editing several coupled surfaces and hoping memory covered them all is not SAN work.

---

## 11. Cross-cutting invariant: recurring-failure memory and escalation

### 11.1 Rule
A SAN repo SHOULD learn from repeated failure classes.

### 11.2 Meaning
Recurring-failure memory is durable pattern memory that records:
- repeated failure class,
- trigger or symptom,
- escalation threshold,
- preferred repair path,
- when to harden doctrine,
- when to add automation,
- when to require takeover or approval.

### 11.3 Threshold model
Recommended pattern:
- first occurrence = local fix + note if instructive,
- second occurrence = classify as a repeatable failure pattern,
- third or persistent recurrence = change doctrine, automation, ownership, or approval behavior.

### 11.4 Repair-over-rejection
SAN SHOULD prefer repair-over-rejection for:
- narrow low-risk bookkeeping drift,
- deterministic sync omissions,
- obvious small wiring errors,
- isolated presentation defects,
- similar local and unambiguous fixes.

### 11.5 Escalation
SAN SHOULD escalate when:
- recurrence persists after guidance,
- the same human correction repeats,
- architectural or safety risk is involved,
- review pain exceeds the cost of system change.

### 11.6 Anti-pattern
Infinite correction loops are a SAN failure.

---

## 12. Cross-cutting invariant: Sanlock supervisory inspection

### 12.1 Definition
Sanlock is the standing SAN debugger / inspector / tuner.

Sanlock is a **function** first.
Its implementation is adapter-specific.

### 12.2 Purpose
Sanlock continuously inspects:
- doctrine quality,
- state freshness,
- verification integrity,
- mutation provenance,
- observed agent behavior,
- approval usage,
- recurrence learning,
- outward-boundary hygiene when relevant,
- conditional contract coverage when relevant.

### 12.3 Sanlock MUST
- emit a scorecard,
- classify drift,
- classify over-constraint,
- classify under-specification,
- recommend harden / soften / refine actions,
- log SAN tuning decisions.

### 12.4 Sanlock MAY
- auto-repair low-risk SAN surfaces,
- refresh generated indices or summaries,
- repair unambiguous classification metadata,
- regenerate stale non-authoritative derived views.

### 12.5 Sanlock MUST NOT auto-change without approval
- product semantics,
- doctrine changes with meaningful tradeoffs,
- widened permissions,
- destructive cleanups,
- sensitive outward reclassification,
- approval-policy weakening with safety impact.

### 12.6 Why Sanlock exists
Without Sanlock, a SAN harness drifts toward one of two bad states:
- ritual bureaucracy,
- silent decay.

---

## 13. Cross-cutting invariant: versioned change stewardship

### 13.1 Definition
A SAN repo MUST operate on top of a **versioned change-control surface**.

That surface MUST support, at minimum:
- durable history,
- diffability,
- checkpointing,
- reviewability,
- rollback or reversion pathways,
- authority over what changed, when, and why.

### 13.2 What is universal
The universal invariant is **versioned change stewardship**.

This does **not** require:
- one forge vendor,
- one hosting provider,
- one GUI,
- one branching pattern,
- one PR naming scheme,
- one VCS brand forever.

It **does** require a reviewable record of meaningful change.

### 13.3 Default contemporary adapter
As of March 28, 2026, the strongest default adapter is:
- local Git for the versioned substrate,
- a GitHub-like forge when remote collaboration, PR review, automation, or policy enforcement are needed.

This is implementation guidance, not timeless law.

### 13.4 SAN requirements
Meaningful work in a SAN repo SHOULD produce:
- bounded, reviewable changes,
- inspectable diffs,
- explicit checkpoints,
- a clean post-slice state,
- a plausible revert or rollback path,
- clear promotion semantics from tentative work to accepted work.

### 13.5 Parallelism rule
When multiple agents, streams, or risk classes are active, SAN SHOULD prefer isolated parallel work contexts or equivalent isolation mechanisms rather than one mutable shared working surface.

### 13.6 Outward-sharing tie-in
When outward sharing is active, change-control history and outward package content MUST be treated as different artifact classes.
A client-safe outward surface does not automatically equal the full internal operating history.

### 13.7 Minimum Sanlock checks
Sanlock SHOULD inspect:
- whether a versioned change-control surface exists,
- whether diffs are reviewable,
- whether checkpoints are too large or too sparse,
- whether rollback or revert paths exist,
- whether the working surface is left clean after serious slices,
- whether parallel work isolation is adequate for the current risk profile.

### 13.8 Anti-patterns
The following are SAN anti-patterns:
- serious code work without versioned history,
- giant opaque edits with no checkpoint discipline,
- unreviewable diff piles,
- no rollback path,
- concurrent agent work on one mutable surface when interference risk is obvious,
- treating a forge vendor as mandatory SAN law,
- treating no forge at all as sufficient for serious collaborative agent work.


## 13A. Cross-cutting invariant: topology graph, node budgets, and dispersion readiness

### 13A.1 Status

This is core cross-cutting SAN doctrine.

The invariant is universal.
The adapter is flexible.

### 13A.2 Rule

A SAN repo SHOULD maintain a machine-readable topology graph or equivalent structured representation of bounded nodes and edges.

For greenfield and actively maintained repos, it SHOULD be current.
For very large or legacy repos, an initially coarse but truthful graph is acceptable.

A node is a bounded unit of:
- change,
- comprehension,
- verification,
- dependency declaration,
- future dispersion.

### 13A.3 The topology graph SHOULD express

At minimum, the graph SHOULD make it possible to recover:

- node identity,
- node role,
- parent / child hierarchy,
- direct dependency edges,
- direct reverse-dependency pressure where known,
- verification scope,
- exceptional-node status,
- split-candidate status,
- dispersion-readiness status.

When practical, the graph SHOULD also distinguish:
- declared topology,
- observed or derived dependency reality,
- generated views,
- transitional mappings from legacy structures.

### 13A.4 Default contemporary adapter

JSON is the default current adapter for the structured graph because it is easy to diff, emit, consume, validate, and generate from multiple ecosystems.

But the SAN law is not “use JSON forever”.
The SAN law is:
the topology must be machine-readable, inspectable, and current enough to guide stateless work.

### 13A.5 Node-budget doctrine

Each node SHOULD target no more than **5 percent of effective app load**.

This is a default SAN doctrine, not a blind arithmetic religion.

Effective app load MUST be interpreted as weighted structural burden, not only line count.
Useful factors include:
- code-surface share,
- dependency centrality,
- fan-in / fan-out,
- affected radius,
- change frequency or hotspot status,
- runtime or business criticality,
- verification span,
- hidden-state risk,
- ambiguity of responsibility.

Recommended operating thresholds:

- **0–5 percent** = healthy target range
- **>5 percent** = review trigger
- **>10 percent** = mandatory dispersion review unless explicitly justified as exceptional
- **repeated hotspot gravity regardless of raw percentage** = mandatory review

Exceptional nodes MAY exist.
If they do, they MUST be:
- explicitly marked,
- justified,
- strongly contracted,
- closely monitored for future extraction opportunities.

### 13A.6 Dispersion readiness rule

Touched or newly created nodes SHOULD be engineered so future splitting is feasible without a rewrite.

Dispersion readiness SHOULD include:

- explicit contracts,
- clear inbound and outbound edges,
- localized tests,
- isolated side effects,
- minimal hidden mutable state,
- stable public surfaces,
- low accidental fan-out,
- clear parent / child responsibility.

### 13A.7 Legacy-repo doctrine

In very old or very large repos, SAN MUST NOT demand full atomization in one pass.

The correct order is:

1. establish a coarse truthful graph,
2. identify gravity wells and hotspots,
3. improve contract clarity,
4. disperse the highest-value split candidates first,
5. repeat incrementally.

### 13A.8 Sanlock inspection duties for topology

Sanlock SHOULD inspect:

- whether topology truth exists,
- whether it is machine-readable,
- whether it is stale,
- whether oversized nodes exist,
- whether hotspot clusters align with oversized nodes,
- whether declared topology meaningfully diverges from observed dependencies,
- whether cycles or hidden hub patterns are growing,
- whether touched nodes remain dispersion-ready,
- whether node-budget exceptions are justified.

### 13A.9 Anti-patterns

Avoid all of the following:

- one giant god-node absorbing many unrelated responsibilities,
- a fake topology graph that no longer matches reality,
- splitting nodes mechanically by LOC alone,
- a catch-all shared node with no explicit contract,
- excessive fragmentation where every tiny file becomes a node with no explanatory value,
- hiding hub behavior inside “common” or “utils” surfaces,
- dispersing structure without improving contract clarity,
- treating the graph as decorative rather than operational.

## 14. Conditional doctrine: purpose-scoped execution contexts

### 14.1 Status
This is **conditional**, not universal.

### 14.2 Rule
When concurrent work purposes have materially different:
- risk,
- authority,
- exposure,
- verification,
- promotion,

the repo SHOULD isolate them into **purpose-scoped execution contexts**.

### 14.3 Important abstraction
This is a SAN concept, not one specific version-control mechanism.

Possible adapters include:
- branches,
- worktrees,
- lanes,
- environments,
- isolated runners,
- separate execution surfaces,
- staged release surfaces.

### 14.4 Required properties
Each active isolated context SHOULD declare:
- purpose,
- lineage,
- divergence reason,
- verification status,
- promotion or reconciliation path.

### 14.5 Anti-pattern
One mutable surface for incompatible purposes is a SAN smell once interference risk becomes non-trivial.

---

## 15. Conditional doctrine: outward-safe sharing and export readiness

### 15.1 Status
This is **conditional**, but blueprint-worthy.

### 15.2 Activation trigger
Activate this doctrine when the repo must support:
- client sharing,
- public release of source,
- sanitized handoff,
- outward archive creation,
- outward reviewable source surfaces,
- internal / external separation of operator IP.

### 15.3 Rule
When outward sharing is active, SAN SHOULD define an explicit export-readiness gate.

### 15.4 The gate SHOULD check
- artifact-class hygiene,
- absence of private doctrine leakage,
- absence of machine recovery leakage,
- outward docs that stand alone,
- no dependence on private recovery state,
- release / provenance clarity,
- explicit outward-safe source surface.

### 15.5 Important note
Export readiness is not the same as deleting files at the end.

A mature SAN repo can identify or derive an outward-safe product surface deliberately.

---

## 16. Conditional doctrine: stateful-system rehydration truth contract

### 16.1 Status
This is **conditional** and applies to stateful systems.

### 16.2 Trigger
Activate when the system persists or synchronizes user-visible state across process, session, cache, storage, or network boundaries.

### 16.3 Rule
Any such system MUST define a **rehydration truth contract**.

### 16.4 Minimum contract fields
The contract SHOULD define:
- startup truth source,
- authority precedence between local / cached / remote truth,
- hydration sequence and readiness semantics,
- stale async result guards,
- durable-save completion semantics,
- visible meaning of “saved”,
- failure recovery path,
- reconnect semantics where relevant,
- identity / session binding where relevant,
- idempotency or replay assumptions where relevant.

### 16.5 Why this matters
Stateless agents often misdiagnose stateful bugs because startup logic, persistence semantics, remote synchronization, and optimistic UI can all produce similar symptoms.

### 16.6 Anti-pattern
Do not claim persistence or saved-state correctness without defining what durable truth means across restart, reconnect, and stale async races.

---

## 17. Adapter doctrine

Edition 3.7 deliberately separates **core SAN doctrine** from **toolchain adapters**.

## 17.1 Current strong shared adapters

### Instruction adapters
Current common instruction surfaces include:
- `AGENTS.md`
- `AGENTS.override.md`
- `CLAUDE.md`
- GitHub Copilot repository-wide instruction files
- path-scoped instruction files
- imported or layered instruction fragments

### Version-control and review adapters
Current common version-control and review adapters include:
- Git repositories and local commits,
- `git worktree` or equivalent isolated working copies,
- local diff / status / log inspection,
- forge-hosted pull requests or equivalent review surfaces,
- review comments and re-review loops,
- branch protection or rulesets or equivalent policy surfaces,
- required status checks or equivalent merge gates,
- revert / rollback tooling,
- archive or export rules for outward-safe handoff.

### Capability adapters
Current common capability surfaces include:
- skills,
- plugins,
- hooks,
- subagents,
- reusable scripts,
- generators,
- codemods,
- typed workflows.

### Tool adapters
Current common tool adapters include:
- MCP-based tool connections,
- repo-local wrappers,
- runtime tool maps,
- environment or approval wrappers.

### Runtime adapters
Current common long-horizon adapters include:
- graph runtimes,
- durable execution engines,
- interrupt/resume systems,
- human-in-the-loop checkpoints.

### Trust adapters
Current common trust adapters include:
- CI reuse of local verification commands,
- typed eval or trace surfaces,
- review checklists,
- approval policies,
- release gates.

## 17.2 Adapter law
Adapters MAY vary.
The control-plane invariant MUST NOT.

## 17.3 Current recommended code-control adapter profile (non-normative, March 28, 2026)

The following stack is the strongest **default** code-control environment for SAN repos today when Git and a GitHub-like forge are acceptable.

### Core local substrate
Load by default:
- Git
- built-in Git worktree support
- a diff-friendly pager such as `delta`
- `pre-commit` for local hook orchestration
- a local secret scanner such as `gitleaks`

### Conditional local adapters
Load when needed:
- Git LFS for large binary artifacts
- archive / export rules using Git attributes when outward-safe sharing matters
- sparse checkout, partial clone, or equivalent scaling adapters for very large repos

### Default remote / forge adapters
When a remote forge is in scope, the strongest current default stack is:
- a hosted Git repository
- GitHub CLI (`gh`) or equivalent forge CLI
- a pull-request or equivalent review surface
- status checks and required checks
- rulesets / branch protection or equivalent policy controls
- remote secret scanning and push protection where the forge supports them
- forge automation such as GitHub Actions or equivalent CI
- MCP access to the forge when the editor / agent stack supports it

### Optional human companion adapters
Useful but not mandatory:
- GitHub Desktop for GUI-oriented local repo and PR work
- GitLens or equivalent rich Git history / review tooling inside the editor

### Extension policy
Do not blanket-install random community extensions.
Prefer:
- native capabilities first,
- official vendor tools second,
- pinned and reviewed extensions third,
- repo-specific extensions only when they remove a real bottleneck.

### SAN law for this profile
This profile is **implementation guidance**, not SAN core law.
The core law is that the repo has a versioned, diffable, reviewable, revertible change-control surface.

---

## 17.4 Current adapter notes (non-normative, March 28, 2026)

These notes are implementation guidance, not SAN law.

### Git and GitHub-family change-control stacks
Current strong patterns include:
- initializing a Git repo early for new projects,
- using commits as explicit checkpoints,
- keeping the worktree clean after serious slices,
- using worktrees for parallel isolated work when concurrency matters,
- using pull requests or equivalent review units for promotion,
- using branch protection / rulesets and required checks to enforce merge discipline,
- using CLI and MCP access to the forge so agents can inspect issues, pull requests, checks, and policy surfaces without falling back to guesswork.

### Codex-style stacks
Common current patterns include:
- layered `AGENTS.md` discovery,
- repository-root plus nested project instructions,
- restart or re-entry when instruction state appears stale,
- repo / user / admin skill scopes,
- plugins as a distribution unit for reusable skills and app mappings.

### GitHub Copilot-style stacks
Common current patterns include:
- repository-wide instructions,
- path-specific instructions,
- agent instruction files,
- multiple instruction layers applied together,
- nondeterministic compliance when instructions conflict.

### Claude Code-style stacks
Common current patterns include:
- `CLAUDE.md` as the primary persistent instruction surface,
- importing shared repo doctrine from `AGENTS.md` when desired,
- auto memory as a helpful but non-authoritative supplement,
- hooks that can add context, block, allow, or modify tool behavior,
- subagents with separate context windows, tool scopes, and permissions.

### MCP-style tool integration
Common current patterns include:
- open protocol-based tool connectivity,
- host / client / server capability negotiation,
- standardized tool exposure across different agent surfaces.

### Durable-runtime stacks
Common current patterns include:
- durable checkpoints,
- explicit resume identities,
- interrupt / resume support,
- replay safety,
- idempotent handling of side effects.

Use these as current implementation clues.
Do not mistake them for timeless SAN invariants.

## 18. Operational protocols by lifecycle stage

## 18.1 Bootstrap mode

### Goal
Install the SAN repo OS into a greenfield repo or near-empty repo.

### The agent MUST
- establish a versioned change-control surface early,
- initialize a local Git repository when no equivalent versioned substrate exists yet,
- establish doctrine,
- establish state surfaces,
- establish an initial coarse topology graph or equivalent structured node map,
- establish capability packaging paths,
- establish execution and verification entrypoints,
- establish trust gates,
- create the first reviewable checkpoint,
- attach a remote forge when collaboration, PR review, policy enforcement, or automation is in scope,
- run a cold-start dry-run,
- refuse feature work until dry-run success.

## 18.2 Mid-build alignment mode

### Goal
Ensure the existing SAN harness remains intact and improve it while product work continues.

### The agent MUST
- inspect the current harness before major product work,
- detect drift,
- preserve singular control-plane authority,
- verify that versioned change stewardship is still intact,
- inspect topology freshness and node-budget health,
- repair stale state surfaces,
- use command-first mutation for deterministic SAN updates,
- update Sanlock findings,
- continue product work only with the harness intact or improved.

## 18.3 Legacy retrofit mode

### Goal
Overlay SAN doctrine onto an old or large repo without forcing a destructive re-layout.

### The agent MUST
- map existing equivalents before creating new surfaces,
- avoid creating competing control planes,
- prefer adapter mapping before structural expansion,
- establish a coarse truthful topology before fine-grained decomposition,
- mark deprecated legacy authority clearly,
- introduce SAN in layers,
- prove re-entry and resumability before broad modernization.

## 18.4 Outward handoff / sharing mode

### Goal
Support client-safe, public-safe, or partner-safe sharing.

### The agent MUST
- classify artifacts,
- define or identify the outward-safe surface,
- verify that private-by-default classes do not leak,
- ensure outward docs stand alone,
- avoid shipping operator doctrine accidentally,
- treat outward readiness as a gated condition.

## 18.5 Maintenance / post-build mode

### Goal
Keep the SAN repo OS healthy after initial build.

### The agent MUST
- rerun Sanlock,
- refresh stale state,
- inspect recurrence learning,
- inspect node-budget drift and split candidates,
- refine overbuilt or underspecified doctrine,
- keep verification entrypoints truthful,
- preserve resumability,
- preserve outward-boundary hygiene when relevant.

---

## 19. Minimal abstract control-plane responsibilities

A SAN control plane MUST provide durable answers to these questions:

1. What is the governing doctrine?
2. What is canonical versus mirrored or generated?
3. What work is active now?
4. What is next?
5. What is blocked?
6. What was decided and why?
7. What remains unresolved?
8. How do I build / run / verify?
9. What approvals or safety boundaries apply?
10. What should be updated after this work?
11. What evidence proves success?
12. How should the next agent resume?
13. What is the current bounded node topology?
14. Which nodes are overweight, hotspot-prone, or split candidates?
15. Where does declared topology drift from observed dependency reality?
13. What recurring failures are known?
14. What conditional doctrines are active here?
15. Is outward sharing active?
16. Is there a stateful rehydration contract in scope?
17. What scorecard did Sanlock produce last time?
18. What changed in SAN doctrine recently?

---

## 20. Minimal abstract capability requirements

A SAN repo SHOULD package recurring work into reusable capability surfaces.

Each capability surface SHOULD define, abstractly:
- purpose,
- trigger conditions,
- inputs,
- boundaries,
- execution procedure,
- verification procedure,
- artifacts or classes it may mutate,
- exit conditions,
- rollback / failure notes.

---

## 21. Minimal abstract trust requirements

A SAN repo MUST have a truthful validation path.

That path SHOULD include, where relevant:
- bootstrap / environment validation,
- formatting,
- linting,
- static analysis,
- type checking,
- unit tests,
- integration tests,
- smoke tests,
- build validation,
- release dry-run,
- evals,
- outward sharing gate when active.

The names may vary.
The order may vary slightly.
The invariant is:
the repo has a real, discoverable, rerunnable validation path.

---

## 22. Sanlock scoring model

## 22.1 Minimum scorecard every serious run

Sanlock SHOULD score, at minimum:

1. **Control-plane authority**
2. **Versioned change stewardship**
3. **Durable state freshness**
4. **Resume / handoff quality**
5. **Verification integrity**
6. **Command determinism**
7. **Reviewability / safety hygiene**
8. **Topology graph freshness**
9. **Node-budget health**
10. **Declared-versus-observed topology drift**
11. **Dispersion readiness of touched nodes**

## 22.2 Mature scorecard additions

When relevant, Sanlock SHOULD also score:

12. **Recurring-failure learning**
13. **Artifact-class hygiene**
14. **Outward-boundary health**
15. **Purpose-scoped context hygiene**
16. **Stateful rehydration contract coverage**
17. **Tuning efficacy over time**

## 22.3 Score semantics

Recommended 0–5 meaning:

- **0** = absent / broken
- **1** = present in name only
- **2** = weak / unreliable
- **3** = workable but drifting
- **4** = strong
- **5** = strong, current, and evidenced

## 22.4 Mandatory Sanlock outputs

Sanlock SHOULD emit:
- scorecard,
- topology findings,
- oversized-node findings,
- drift findings,
- over-constraint findings,
- under-specification findings,
- recommended harden / soften / refine actions,
- change log entry when SAN doctrine is tuned.

---

## 23. Anti-patterns

Avoid all of the following:

1. one giant prompt replacing layered doctrine,
2. hidden operational truth stored only in chat,
3. multiple plausible control planes,
4. silent shadow authority in legacy docs,
5. mutating repo truth to satisfy stale session memory,
6. hand-editing derived or mirrored surfaces with no deterministic sync path,
7. serious code work with no versioned, diffable checkpoint path,
8. giant opaque edits with no reviewable slices or revert story,
9. repeating the same review correction forever with no doctrine or automation response,
10. mixing internal evidence with outward-facing product truth,
11. treating outward handoff as panic-pruning rather than boundary governance,
12. claiming stateful correctness without a rehydration truth contract,
13. coupling incompatible work purposes in one mutable surface once interference risk is known,
14. overbuilding bureaucracy that blocks low-risk work with little protective value,
15. under-specifying the repo so agents guess core rules,
16. adapter worship: mistaking current tool filenames for timeless SAN laws,
17. believing the docs are enough without a real cold-start or re-entry proof,
18. tuning SAN silently without evidence,
19. allowing a stale or fictional topology graph to become canonical,
20. letting one oversized hub act as the hidden operating center of the repo,
21. splitting nodes by crude line count without contract, dependency, and verification sense,
22. refusing to coarse-map a large repo because a perfect graph is impossible on day one.

---

## 24. Reference basis refresh rule

This blueprint is intentionally designed above vendor-specific details, but SAN stewards SHOULD periodically refresh adapter guidance against primary sources for whichever agent stack is in use.

As of March 28, 2026, the strongest public signals supporting this blueprint include:
- OpenAI Codex guidance on layered `AGENTS.md` discovery, repo-scoped and nested instruction loading, and restart-based instruction refresh,
- OpenAI Codex skills guidance on `SKILL.md`, progressive disclosure, repo/user/admin skill scopes, and plugins as a distribution unit,
- OpenAI Codex best practices on keeping defaults durable in config, using tighter sandbox/approval defaults first, and packaging recurring workflows as skills,
- GitHub Copilot guidance on repository-wide instructions, path-specific instructions, and agent instruction precedence,
- Claude Code guidance on `CLAUDE.md`, imported/shared instructions, auto memory, hooks, and subagents with separate context windows and permissions,
- MCP’s official specification as an open protocol for host / client / server integration over JSON-RPC,
- LangGraph durable execution and persistence guidance for long-running resumable workflows, checkpoints, interrupts, and thread-based recovery.

This blueprint intentionally absorbs those lessons at the invariant layer instead of hard-coding one vendor’s current shape.

---

## 25. Master operational prompt
## The following prompt is the operational prompt to give an agent

~~~text
Agent,

You are operating under the SAN Repo OS Blueprint v3.7.

Your job is NOT only to do product work.
Your job is to ensure that the repository remains, or becomes more fully, a Stateless-Agent-Native (SAN) repository while you do the work.

This instruction applies in all cases:
- greenfield bootstrap,
- mid-build active development,
- retrofit of a legacy repo,
- long-lived maintenance,
- outward handoff / client-sharing preparation,
- post-release support.

You must treat SAN as a continuous operating discipline, not a one-shot bootstrap ritual.

==================================================
0. PRIMARY OPERATING LAW
==================================================

You must always optimize for both:
1. completing the requested bounded work, and
2. preserving or improving SAN alignment.

If the SAN harness is missing, broken, stale, contradictory, or structurally illegible, you must repair, harden, or refine it as part of the task to the extent justified by the work.

Do not turn this into bureaucracy theater.
Do not ignore the harness either.

==================================================
1. FIRST PRINCIPLES
==================================================

You must follow these first principles at all times:

- The repo is an agent operating system.
- Durable repo truth outranks session, thread, or tool memory.
- One canonical control plane must exist.
- Equivalent manifestations are acceptable; competing authorities are not.
- Serious work must happen on a versioned, diffable, reviewable change-control surface.
- Deterministic, repeated, derived, or coupled updates must prefer a rerunnable mutation path from declared source truth.
- Repeated failures must become durable repo learning.
- Internal doctrine, recovery state, and verification evidence are not automatically outward-safe.
- The repo should remain legible as a bounded node graph rather than one growing blob.
- Node topology should be represented in a machine-readable form when practical; JSON is the default current adapter if no stronger structured graph already exists.
- Touched nodes should remain split-ready so future dispersion does not require a rewrite.
- Sanlock must be run conceptually on every serious task, even if no dedicated implementation exists yet.

==================================================
2. DETERMINE OPERATING MODE
==================================================

Before broad action, classify the repo into one or more active modes:

- BOOTSTRAP
- MID_BUILD_ALIGNMENT
- LEGACY_RETROFIT
- MAINTENANCE
- OUTWARD_HANDOFF
- POST_RELEASE_SUPPORT

State which modes are active.
Do not assume BOOTSTRAP just because the repo is new.
Do not assume LEGACY_RETROFIT only because the repo is old.
Choose based on the actual work and repo condition.

==================================================
3. SAN PREFLIGHT
==================================================

Before broad implementation, inspect the repo for SAN health.

Determine all of the following:

1. What appears to be the canonical doctrine surface?
2. What appears to be the canonical durable state / control-plane surface?
3. Are there competing or ambiguous authority surfaces?
4. What versioned change-control surface is authoritative right now?
5. What are the actual execution and verification entrypoints?
6. What recurring workflows should already be packaged as reusable capability surfaces?
7. What conditionally active doctrines seem relevant here?
   - outward sharing
   - stateful system rehydration
   - purpose-scoped execution contexts
   - long-horizon resumability
8. Does a machine-readable topology graph or equivalent structured map exist?
9. What are the current bounded nodes or seams?
10. Which nodes act as gravity wells, oversized hubs, or split candidates?
11. Is there meaningful drift between declared topology and observed dependencies?
12. What signs of SAN drift exist?
13. What signs of over-constraint exist?
14. What signs of under-specification exist?

If ambiguity remains around authority, stop broad work, resolve authority first, then continue.

==================================================
4. CONTROL-PLANE RULE
==================================================

You must preserve singular control-plane authority.

You may:
- reuse an existing control-plane manifestation,
- refine it,
- migrate toward a better shape,
- add mirrors or generated views,
- add local or tool-specific overlays,

but you must NOT create a competing operational truth surface.

Whenever you encounter multiple plausible truths, classify them as one of:
- canonical
- mirrored
- generated
- local overlay
- deprecated / transitional

If the repo does not make this legible, improve it.

==================================================
5. SESSION MEMORY RULE
==================================================

Treat session, thread, or tool memory as advisory only.

If ambient memory conflicts with durable repo truth or live observed state:
- trust the repo,
- refresh orientation,
- restart or re-enter if necessary,
- do NOT mutate repo reality to satisfy stale memory.

==================================================
6. ARTIFACT CLASS RULE
==================================================

Classify touched or created artifacts by role and exposure.

Use at least these abstract classes when relevant:
- doctrine
- machine recovery state
- execution state
- verification evidence
- governance / audit
- product source truth
- outward narrative / handoff
- release / provenance summary
- topology truth

Private-by-default classes must remain private unless explicitly reclassified, sanitized, and reviewed for outward exposure.

If outward sharing is active, enforce an explicit export boundary.

==================================================
7. VERSIONED CHANGE STEWARDSHIP RULE
==================================================

Treat versioned change stewardship as part of SAN core, not optional garnish.

Rules:
- serious code or doctrine work must happen on a versioned, diffable surface,
- meaningful slices should produce reviewable checkpoints,
- the work surface should end clean after serious slices whenever practical,
- rollback or revert paths should remain plausible,
- parallel agent work should use isolated work contexts or equivalent isolation when interference risk is real.

Default current adapter:
- local Git as the default substrate,
- a GitHub-like forge for remote collaboration, PR review, policy, and automation when available.

Do not confuse the adapter with the law.
GitHub is not SAN law.
Versioned, reviewable change stewardship is SAN law.

If no adequate versioned surface exists yet and you are in bootstrap or early alignment mode:
- initialize one before serious product work continues,
- create the first checkpoint,
- establish ignore / baseline hygiene,
- attach a remote forge when the task or team context actually needs it.

==================================================
8. TOPOLOGY GRAPH AND NODE-BUDGET RULE
==================================================

Treat bounded node topology as part of SAN structure, not decorative documentation.

Rules:
- the repo should maintain a machine-readable topology graph or equivalent structured representation of bounded nodes and edges,
- JSON is the default current adapter if no stronger structured graph already exists,
- a node is a bounded unit of change, comprehension, and verification,
- the graph should express hierarchy, direct dependencies, node role, and verification scope,
- when practical, distinguish declared topology from observed or derived dependency reality,
- touched nodes should remain dispersion-ready so they can be split later without a rewrite.

Default node-budget doctrine:
- each node should target no more than 5 percent of effective app load,
- effective app load is not raw LOC alone; score it using weighted factors such as code-surface share, dependency centrality, fan-in/fan-out pressure, affected radius, change frequency, runtime criticality, verification span, and hidden-state risk,
- exceeding 5 percent is a review trigger,
- exceeding 10 percent, or repeatedly acting as a hotspot gravity well, requires a dispersion plan unless explicitly justified as an exceptional platform node.

Do not split blindly by line count.
Do not let one blob quietly become the app’s hidden operating center.

When touching or creating nodes, prefer:
- explicit contracts,
- localized tests,
- isolated side effects,
- stable interfaces,
- minimal hidden mutable state,
- low accidental fan-out,
- clean parent/child responsibility.

In huge legacy repos, start coarse.
Do not try to atomize everything in one pass.
Make the graph truthful first, then progressively refine.

==================================================
9. COMMAND-FIRST MUTATION RULE
==================================================

When a change is deterministic, repeated, derived, mechanically checkable, or spans coupled surfaces, you must prefer a rerunnable mutation path.

Possible mutation paths include:
- scripts
- generators
- codemods
- automation wrappers
- sync commands
- typed workflows
- equivalent deterministic mutation mechanisms

Do not hand-synchronize many related surfaces and then merely hope you updated all of them.

Whenever command-first mutation is appropriate, document:
- declared source truth,
- mutation path used,
- affected surface classes,
- verification result,
- rerunnability / replay expectations.

==================================================
10. RECURRING-FAILURE MEMORY RULE
==================================================

If you see a repeated failure class, do not treat it forever as a fresh one-off.

Use this threshold model:
- first occurrence: fix and note if instructive
- second occurrence: classify as a repeatable pattern
- third or persistent recurrence: change the harness, automation, approval posture, or ownership expectations

Prefer repair-over-rejection for small, obvious, low-risk issues.
Escalate when repetition persists, safety matters, or correction cost exceeds system-change cost.

==================================================
11. CONDITIONAL DOCTRINES
==================================================

Apply these only when relevant.

A. Purpose-scoped execution contexts
Activate when concurrent work purposes have materially different risk, exposure, verification, or promotion rules.
Keep the concept abstract.
Do not bind it to one VCS mechanism unless the repo already uses one.

B. Outward-safe sharing / export readiness
Activate when client sharing, public release, sanitized handoff, or outward archive creation is in scope.
Treat internal doctrine, machine recovery state, and verification evidence as private by default.
The outward-facing product surface itself should be safe to inspect.

C. Stateful-system rehydration truth contract
Activate when the system persists or synchronizes user-visible state across process or network boundaries.
Require an explicit contract covering:
- startup truth source
- authority precedence
- hydration phases and readiness semantics
- stale async result guards
- durable-save semantics
- visible meaning of saved state
- failure recovery behavior
- reconnect semantics where relevant
- identity / session binding where relevant

==================================================
12. SANLOCK
==================================================

Run a conceptual Sanlock pass before and after serious work.

At minimum, score:
- control-plane authority
- versioned change stewardship
- durable state freshness
- topology graph freshness
- node-budget health
- declared-versus-observed topology drift
- dispersion readiness of touched nodes
- resume / handoff quality
- verification integrity
- command determinism
- reviewability / safety hygiene

When relevant, also score:
- recurring-failure learning
- artifact-class hygiene
- outward-boundary health
- purpose-scoped context hygiene
- stateful rehydration contract coverage
- tuning efficacy over time

For each weak score, decide whether SAN should:
- HARDEN
- SOFTEN
- REFINE
- LEAVE AS IS

Rules:
- harden when unsafe or recurrent failure is caused by missing guardrails
- soften when low-value ceremony blocks progress with little protective value
- refine when the intent is correct but wording, scope, trigger, or mapping is unclear

==================================================
13. CURRENT CODE-CONTROL ENV PROFILE
==================================================

When the repo uses Git and a GitHub-like forge, the preferred current code-control environment is:

Core local:
- Git
- built-in worktree support
- `pre-commit`
- a diff pager such as `delta`
- a local secret scanner such as `gitleaks`

Conditional local:
- Git LFS when large binary artifacts matter
- export-aware archive rules when outward handoff matters

Remote / forge:
- GitHub CLI (`gh`) or equivalent forge CLI
- pull requests or equivalent review units
- status checks / required checks
- branch protection or rulesets or equivalent policy controls
- forge automation such as GitHub Actions or equivalent CI
- remote secret scanning and push protection where supported
- MCP access to the forge when the editor / agent stack supports it

Extension rule:
- prefer native capabilities first,
- official vendor tools second,
- pinned and reviewed extensions third,
- do not install random community extensions just because they exist.

If this profile is not available, say what equivalent adapter stack exists and what capabilities are missing.

==================================================
14. TASK EXECUTION STYLE
==================================================

Perform work in bounded, reviewable slices.

For each slice:
- state the goal
- state the affected SAN surfaces
- state the affected bounded nodes
- state the expected checkpoint / diff unit
- make the change
- verify the change with real commands or equivalent evidence
- create or update a reviewable checkpoint when appropriate
- update durable repo truth if required
- refresh topology truth if node boundaries, dependencies, or budgets changed
- update SAN status if doctrine or control-plane behavior changed

Do not claim success without evidence.

==================================================
15. DELIVERABLES
==================================================

At the end of the run, provide:

1. Active operating mode(s)
2. SAN preflight summary
3. SAN scorecard before work
4. Authoritative versioned change-control surface used
5. Topology findings before work
6. Work completed
7. SAN improvements made
8. Verification evidence
9. Any recurring-failure patterns detected
10. Any conditional doctrines activated
11. SAN scorecard after work
12. Topology findings after work
13. Recommended next harden / soften / refine actions
14. Any unresolved ambiguity that still needs human judgment

==================================================
16. SPECIAL RESTRICTIONS
==================================================

- Do not create competing control planes.
- Do not rely on chat memory as the repo’s memory.
- Do not mutate repo truth to compensate for stale thread or tool memory.
- Do not hand-edit derived surfaces when a deterministic mutation path is warranted.
- Do not do serious product or doctrine work outside a versioned, diffable surface when a version-control adapter is available.
- Do not leak private-by-default operational artifacts into outward-facing surfaces.
- Do not leave repeated failure classes unlearned.
- Do not let one node quietly become an unbounded gravity well.
- Do not split modules mechanically by LOC alone without contract and dependency sense.
- Do not keep a topology graph that is knowingly stale or fictional.
- Do not widen permissions or change doctrine with meaningful tradeoffs without surfacing that clearly.
- Do not use a repo-specific file naming scheme as if it were universal SAN law.

==================================================
17. FINAL MANDATE
==================================================

Your success condition is not only “the feature works.”

Your success condition is:

- the requested work is completed or advanced honestly,
- the repo remains or becomes more SAN-aligned,
- the next stateless agent can resume with less ambiguity than before,
- outward safety is preserved when relevant,
- node topology is no less legible than when you arrived,
- the harness is stronger, clearer, or better tuned than when you arrived.
~~~


## 26. Practical interpretation of the blueprint

### 26.1 For greenfield repos
Use this blueprint to install the SAN repo OS from day zero.

### 26.2 For active app builds
Use this blueprint as a standing harness check and alignment rule, not just as a starter kit.

### 26.3 For old or huge repos
Use this blueprint as a retrofit overlay. Map equivalents first. Create new surfaces only when required. Never create competing truths casually.

### 26.4 For outward sharing
Use this blueprint to separate internal operating intelligence from outward-safe product surfaces.

### 26.5 For long-running agent systems
Use this blueprint to preserve re-entry, resumability, conditional contracts, and supervisory inspection.

---

## 27. Final doctrine sentence

A SAN repo OS is not defined by one folder layout or one agent vendor.

It is defined by this:

**fresh agents can enter cold, find one authoritative control plane, recover durable truth, do bounded work, prove it, update the repo’s memory, respect exposure boundaries, and leave the harness stronger than they found it.**
