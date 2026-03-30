# SAN Repo OS / RaaOS Criteria v2

A fresh-pass criteria document for a **Stateless Agent Native Repo Operating System**.

Date: 2026-03-28

## 1. What this is

This is **not** a repo blueprint.

It is a **constitution-level criteria set** for judging whether a repository actually behaves like an operating system for stateless coding agents.

The key test is simple:

> Can a fresh stateless agent enter cold, discover authority, reconstruct state, take bounded work, change code safely, verify reality, publish durable progress, and leave the repo in a better state without relying on hidden chat memory or human cleanup?

If the answer is no, the repo is not yet functioning as a true SAN Repo OS.

This framing is grounded in current agent engineering practice. OpenAI describes the human role in agent-first software as designing environments, specifying intent, and building feedback loops rather than hand-writing code; Anthropic describes the core long-running-agent problem as discrete sessions where each new session begins with no memory; OpenAI, GitHub, and Anthropic all now treat repo-local instruction surfaces and reusable workflows as first-class control mechanisms.[R1][R2][R3][R4][R5][R6]

## 2. Scope and non-goals

This criteria set is deliberately:

- agent-agnostic
- operating-system-agnostic
- VCS-host-agnostic
- framework-agnostic
- language-agnostic
- repo-age-agnostic

It does **not** require GitHub, Codex, Claude Code, Copilot, MCP, Nx, LangGraph, or Temporal.

But it **does** require that any implementation stack provide the underlying behaviors those tools are examples of: layered control, restartable state, diffable change control, bounded permissions, runtime verification, and durable handoff artifacts.[R1][R2][R4][R5][R7][R8][R9][R10]

## 3. Core definition

A **SAN Repo OS / RaaOS** is a repository-local operating environment that gives fresh stateless agents the equivalent of:

- a boot sequence
- a kernel / control plane
- a memory model
- a filesystem model
- a process model
- a syscall / tool surface
- a protection model
- a change-control layer
- a verification layer
- a recovery layer
- an observability / debugger layer
- an outward-safe export layer

The “OS” language here is an analogy, but a useful one: the repo must do for agents what an operating system does for programs — make execution structured, bounded, resumable, inspectable, and governable.

## 4. The twelve constitutional criteria

## Criterion 1 — Cold-start bootability

A SAN Repo OS **MUST** let a fresh stateless agent get oriented without relying on prior chat/session memory.

The repo must expose a discoverable entry path that tells the agent:

- where authority lives
- how to understand the current state of work
- how to find the next bounded task
- how to verify the environment before making changes
- how to publish durable progress before leaving

Why this is constitutional:

Anthropic’s long-running-agent work explicitly states that each new session begins with no memory and therefore needs artifacts that bridge sessions. OpenAI similarly emphasizes that agents only know what they can access in-context while running.[R2][R1]

Pass condition:

A fresh agent can reconstruct repo state and begin useful work from repo-local artifacts alone.

Fail smell:

The agent must ask humans what happened last, or guess.

## Criterion 2 — Canonical control plane

A SAN Repo OS **MUST** have one canonical control plane.

That means there is one authoritative in-repo surface that defines:

- operator doctrine
- tasking rules
- validation rules
- safety rules
- escalation rules
- precedence between local and broader guidance

The implementation may use different filenames or layouts, but the invariant is singular authority, not a specific path.

Why this is constitutional:

OpenAI’s current guidance shows layered instruction discovery for `AGENTS.md`, with local overrides nearer the work, and GitHub documents repository-wide, path-specific, and nearest-agent-instruction precedence. OpenAI’s harness writeup also shows that one giant instruction file fails and that a short map plus deeper structured sources works better.[R3][R4][R1]

Pass condition:

If two agents enter cold, they identify the same authoritative control surface and the same precedence rules.

Fail smell:

Multiple competing “truths” or informal doctrine living mainly in chat, people’s heads, or stale side docs.

## Criterion 3 — Repo-local system of record

A SAN Repo OS **MUST** make the repository itself the primary operational memory surface.

The repo must hold versioned, inspectable artifacts for:

- current plans
- feature state
- decisions
- technical debt
- operating doctrine
- verification status
- known risks

Why this is constitutional:

OpenAI explicitly says repository-local, versioned artifacts are what the agent can see, and describes a structured knowledge base as the system of record rather than one large instruction file. Anthropic’s harness approach similarly depends on progress logs, feature lists, and git history.[R1][R2]

Pass condition:

A future agent can recover intent, progress, and rationale from repo-local evidence.

Fail smell:

Critical truth lives in Slack, docs outside the repo, or prior chat threads.

## Criterion 4 — Durable handoff memory

A SAN Repo OS **MUST** preserve restartable state across stateless sessions.

This requires durable handoff artifacts that capture at minimum:

- what was attempted
- what changed
- what passed
- what failed
- what is next
- what remains risky

The exact storage format is an adapter decision; the criterion is restartable handoff state.

Why this is constitutional:

Anthropic recommends an initializer phase, a coding phase, progress notes, feature state, git history, and clean end-of-session state specifically because agents lose session memory. Durable execution systems such as LangGraph and Temporal likewise treat persisted state and replay as first-class for long-running, interruptible workflows.[R2][R9][R10]

Pass condition:

After interruption, a fresh agent can resume without re-discovering everything or corrupting prior work.

Fail smell:

Frequent rework, duplicate work, or undocumented half-implemented changes.

## Criterion 5 — Versioned, diffable, reversible change control

A SAN Repo OS **MUST** operate on a versioned change-control surface.

It must support:

- diffable changes
- attributable checkpoints
- reviewable change units
- selective acceptance/rejection
- rollback/revert
- isolated change contexts when parallel work is needed

Git is the current best default adapter, not the constitutional requirement.

Why this is constitutional:

OpenAI’s harness engineering work started from an empty git repository and scaled through large numbers of pull requests. Codex’s review tooling is explicitly Git-based and supports diff review, staging, and reverting. Git’s own worktree model supports multiple isolated working trees attached to the same repository, sharing history while separating per-worktree state. Google’s review guidance also explains why small changes improve review speed, quality, rollback, and mergeability.[R1][R11][R12][R13]

Pass condition:

Every meaningful change can be inspected, reviewed, partially accepted, reverted, and resumed from a known checkpoint.

Fail smell:

In-place opaque edits, giant unreviewable change sets, or no clean rollback path.

## Criterion 6 — Bounded task/process model

A SAN Repo OS **MUST** give agents bounded work, not amorphous ambition.

It should decompose work into units small enough that an agent can:

- understand the goal
- change one coherent thing
- verify it
- publish state
- exit cleanly

The repo must discourage one-shotting whole applications or sprawling mixed-purpose edits.

Why this is constitutional:

Anthropic’s harness research found one-feature-at-a-time progress critical; OpenAI’s harness writeup describes working depth-first through smaller building blocks; Anthropic’s general agent guidance argues that the most successful teams use simple, composable patterns rather than complex frameworks.[R2][R1][R14]

Pass condition:

Work naturally collapses into bounded units with clear acceptance conditions.

Fail smell:

Agents repeatedly try to do too much, run out of context, or leave multi-surface messes.

## Criterion 7 — Deterministic execution surface

A SAN Repo OS **MUST** provide a stable, obvious way to run the code and validate changes.

The repo should expose deterministic commands or equivalent callable operations for:

- setup/bootstrap
- build
- test
- lint/format/typecheck where relevant
- local runtime start
- smoke verification
- cleanup / teardown where relevant

Where multi-surface updates are repetitive and high-risk, the repo should prefer **command-first mutation** over scattered manual edits.

Why this is constitutional:

OpenAI’s Codex best practices explicitly call out build, test, lint commands and verification expectations in project guidance. Anthropic’s harness research recommends verifying the app before new work and using init/start scripts. OpenAI’s live agent engineering also emphasizes standard development tools and local scripts as direct agent interfaces.[R6][R2][R1]

Pass condition:

A fresh agent can execute the canonical operations without improvising hidden steps.

Fail smell:

“Works on my machine” setup, tribal shell knowledge, or manual multi-file sync tasks that agents routinely miss.

## Criterion 8 — Agent-legible architecture and topology

A SAN Repo OS **MUST** make the codebase navigable for agents.

That means:

- explicit module boundaries
- limited cross-boundary leakage
- named domains/features
- predictable directory semantics
- minimal need to load the entire repo at once
- architecture that supports progressive disclosure

For medium and large repos, a machine-readable topology graph **SHOULD** exist. Exact graph format is an adapter choice; the invariant is machine-readable navigability, not JSON specifically.

Why this is constitutional:

OpenAI says agent legibility is the goal and that the repo should let the agent reason about the business domain directly from the repository. Anthropic’s context-engineering guidance says context is finite and argues for the smallest possible high-signal context, just-in-time retrieval, and lightweight references rather than loading everything up front. Nx’s project graph JSON is one concrete example of a machine-readable graph adapter.[R1][R15][R16]

Pass condition:

Agents can find the right neighborhood quickly and operate locally.

Fail smell:

Huge god-modules, ambiguous ownership, overloaded directories, or architecture that only longtime humans understand.

## Criterion 9 — Security, permissions, and trust boundaries

A SAN Repo OS **MUST** support bounded autonomy rather than blind autonomy.

The repo/runtime pair must define:

- writable scope
- read scope
- network policy
- approval policy
- destructive action rules
- external tool trust rules
- secret-handling rules
- escalation boundaries

“Hands-free” means autonomous **inside a declared trust envelope**, not unbounded by policy.

Why this is constitutional:

OpenAI’s Codex security model defaults to workspace-limited writes, no network unless enabled, and approval policies for network or out-of-workspace actions. MCP’s specification likewise emphasizes user consent, data privacy, tool safety, and explicit authorization flows.[R7][R8]

Pass condition:

An agent can act autonomously within a clear envelope, and exceptions are policy decisions rather than surprises.

Fail smell:

Either everything is blocked, or everything is effectively YOLO.

## Criterion 10 — Tool / I-O bus and adapter discipline

A SAN Repo OS **MUST** have a disciplined way to connect agents to external systems.

The repo should distinguish between:

- internal repo truth
- external live context
- external action surfaces
- read tools
- write tools
- trusted tools
- untrusted tools

The system should support adapter-based integration rather than hard-coding one vendor’s surface as law.

Why this is constitutional:

MCP defines an open protocol for hosts, clients, and servers, with tools, prompts, resources, roots, progress tracking, logging, and explicit security guidance. OpenAI’s Codex customization model explicitly combines project guidance, skills, MCP, and subagents; Anthropic’s context engineering also recommends just-in-time retrieval using lightweight references and tools.[R8][R5][R15]

Pass condition:

External context and actions enter through explicit, governable adapters.

Fail smell:

Agents depend on copy-pasted chat context, ad hoc credentials, or tool sprawl with unclear trust.

## Criterion 11 — Runtime truth and verification

A SAN Repo OS **MUST** let agents prove reality, not just claim success.

Verification must be anchored in commands, tests, runtime inspection, or observable signals such as logs, metrics, traces, or UI checks as appropriate to the app.

The repo should let agents answer questions like:

- does it build?
- do tests pass?
- does the app boot?
- is the target path working?
- did performance/reliability regress?

Why this is constitutional:

OpenAI’s best practices tell teams to include how to verify work, write/update tests, run the right test suites, and review diffs. Anthropic recommends a basic end-to-end verification at the start of each session. OpenAI’s harness engineering also describes making UI, logs, metrics, and traces directly legible to agents so they can reproduce bugs and validate fixes.[R6][R2][R1]

Pass condition:

Completion claims are backed by reproducible evidence.

Fail smell:

Agents regularly say “done” without runnable proof.

## Criterion 12 — Recovery, drift control, and continuous inspection

A SAN Repo OS **MUST** be able to detect and correct its own drift.

This implies a standing inspection/governance loop — whether called Sanlock or something else — that can assess:

- control-plane health
- doc/code drift
- stale artifacts
- repeated agent failure modes
- architecture erosion
- oversized or over-coupled modules
- missing verification
- export leakage risks
- quality trend over time

It should be able to recommend hardening, softening, or refining the harness, and where safe, open narrowly-scoped repair changes.

Why this is constitutional:

OpenAI’s harness engineering describes dedicated linters, CI jobs, recurring doc-gardening, quality documents, updateable quality grades, and recurring cleanup tasks that function like garbage collection. It also describes review loops that can be largely agent-to-agent. This strongly supports a continuous-inspection criterion, even if “Sanlock” is our own name for it.[R1][R6]

Pass condition:

The repo gets more legible and reliable with repeated agent use.

Fail smell:

Agent usage makes the repo noisier, less coherent, and more fragile over time.

## 5. Cross-cutting criteria

These are not separate constitutional pillars, but they apply across all twelve.

### A. Outward-safe export surfaces

A SAN Repo OS should distinguish internal operator doctrine, machine recovery state, verification evidence, and outward-facing product/client artifacts. Git already provides one useful adapter mechanism: `export-ignore` can exclude files and directories from archive outputs.[R12]

### B. Process isolation for parallel work

When the repo is large or throughput is high, isolated parallel work contexts become important. Git worktrees are one current adapter; subagents with separate context windows are another. The constitutional invariant is isolation with shared authority and resumable state, not a specific mechanism.[R11][R17]

### C. Runtime durability for long-running work

For short work, repo-local artifacts plus version control may be enough. For long-running or interruptible workflows, durable execution patterns become more important. LangGraph and Temporal are current examples of systems that persist state and enable replay/resume.[R9][R10]

### D. Machine-readable topology is a SHOULD+, not an absolute MUST

Fresh research does **not** support hard-coding one graph format or one node budget into the constitution. The strong conclusion is narrower:

- large repos should expose machine-readable topology
- modules should remain agent-legible and bounded
- hotspot/oversize policies can be added as governance rules

But numeric thresholds such as “5% of app load” belong in policy, not constitutional law, unless validated by repeated operational evidence in a specific environment.

## 6. Hard-fail conditions

A repo should **not** be considered a true SAN Repo OS if any of these are missing:

1. No canonical control plane
2. No repo-local system of record
3. No durable handoff state
4. No versioned diff/revert path
5. No deterministic verify path
6. No explicit permission model
7. No way to recover from interrupted work
8. No ongoing drift inspection

If one of these is absent, the system may still be “agent-assisted,” but it is not yet “stateless-agent-native.”

## 7. What “human hands-free” should actually mean

The strongest defensible definition is:

> Human hands-free means a fresh stateless agent can complete routine coding work end-to-end without live human intervention **inside a declared trust envelope**.

That includes:

- implementation
- maintenance
- refactoring
- remediation
- upgrading
- regression checking
- progress publishing
- rollback where needed

It does **not** imply:

- unrestricted destructive access
- unrestricted network access
- skipping review/evidence for high-risk changes
- relying on hidden memory

This interpretation matches current approval/sandbox models from Codex and the security/consent principles in MCP.[R7][R8]

## 8. A practical scoring model for comparison against any blueprint

Use a 0–5 maturity score per constitutional criterion:

- **0** — absent
- **1** — ad hoc / human-dependent
- **2** — partially present, brittle
- **3** — reliable for routine supervised agent work
- **4** — reliable for bounded autonomous work
- **5** — self-auditing, drift-resistant, continuously improving

A repo is:

- **not SAN-native** if any hard-fail criterion is 0 or 1
- **SAN-capable** if all hard-fail criteria are at least 3
- **SAN-operational** if most criteria are 4
- **true RaaOS / Repo OS** only when the repo can reliably onboard fresh agents, absorb repeated autonomous work, and improve through inspection rather than decay

## 9. Fresh conclusion

From a fresh research pass, the heart of a SAN Repo OS is **not** “better prompts.”

It is:

- repo-local authority
- restartable state
- diffable change control
- bounded autonomy
- agent-legible architecture
- deterministic verification
- continuous drift correction

Or in one line:

> A SAN Repo OS is a repo that can cold-start, constrain, inform, validate, recover, and tune stateless agents repeatedly without depending on hidden human memory.

That is the standard I would now use to judge any SAN blueprint.

## References

[R1] OpenAI — Harness engineering: leveraging Codex in an agent-first world
https://openai.com/index/harness-engineering/

[R2] Anthropic — Effective harnesses for long-running agents
https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents

[R3] OpenAI Developers — Custom instructions with AGENTS.md
https://developers.openai.com/codex/guides/agents-md/

[R4] GitHub Docs — Adding repository custom instructions for GitHub Copilot
https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions

[R5] OpenAI Developers — Customization (project guidance, skills, MCP, subagents)
https://developers.openai.com/codex/concepts/customization/

[R6] OpenAI Developers — Codex best practices and review docs
https://developers.openai.com/codex/learn/best-practices/
https://developers.openai.com/codex/app/review/

[R7] OpenAI Developers — Agent approvals & security
https://developers.openai.com/codex/agent-approvals-security/

[R8] Model Context Protocol — Specification
https://modelcontextprotocol.io/specification/2025-06-18

[R9] LangGraph Docs — Persistence / durable execution
https://docs.langchain.com/oss/javascript/langgraph/persistence
https://docs.langchain.com/oss/javascript/langgraph/durable-execution

[R10] Temporal Docs / Temporal site — durable execution
https://docs.temporal.io/
https://temporal.io/

[R11] Git — git-worktree documentation
https://git-scm.com/docs/git-worktree

[R12] Git — gitattributes documentation (`export-ignore`)
https://git-scm.com/docs/gitattributes

[R13] Google Engineering Practices — Small CLs
https://google.github.io/eng-practices/review/developer/small-cls.html

[R14] Anthropic — Building effective agents
https://www.anthropic.com/engineering/building-effective-agents

[R15] Anthropic — Effective context engineering for AI agents
https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

[R16] Nx Docs — GraphJson / project graph
https://nx.dev/docs/reference/devkit/GraphJson

[R17] Anthropic Docs — Subagents in Claude Code
https://docs.anthropic.com/en/docs/claude-code/sub-agents
