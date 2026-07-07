# Harness Engineering Principles

Source: OpenAI, "Harness engineering: leveraging Codex in an agent-first world"
by Ryan Lopopolo, published February 11, 2026.
https://openai.com/index/harness-engineering/

Use this reference when adapting the harness to a specific project or explaining
why the seeded files exist. Keep project output concise and project-local.

## Distilled Principles

### Humans steer; agents execute

Treat engineering work as environment design, task specification, and feedback
loop design. The human role shifts toward choosing goals, encoding constraints,
reviewing outcomes, and improving the system that lets agents make progress.

### Missing capability beats trying harder

When Codex fails repeatedly, diagnose the missing capability: unclear docs,
absent test harness, hard-to-inspect runtime state, weak tooling, missing
schemas, or unenforced architecture. Feed the fix back into the repository.

### Repository knowledge is the system of record

Prefer repository-local, versioned knowledge over chat history, external docs,
or implicit human memory. `AGENTS.md` should be a compact table of contents that
points to deeper docs. Avoid a giant instruction file.

### Progressive disclosure is a design requirement

Agents need maps, not encyclopedias. Keep always-loaded instructions short.
Place detailed architecture, product, quality, reliability, and reference docs
in discoverable files that Codex can read only when relevant.

### Agent legibility is a product property

Optimize code, docs, tools, logs, tests, and runtime behavior so an agent can
inspect and reason about them. If Codex cannot access it during a run, it should
not be treated as operational knowledge.

### Make the application observable and controllable

Useful harnesses expose local runtime control, logs, metrics, traces, browser or
UI state, screenshots, fixtures, and repeatable workloads. The goal is to let
Codex reproduce, validate, and iterate without manual copy-paste.

### Enforce invariants mechanically

Use tests, linters, type checks, dependency-boundary checks, schema checks, and
CI jobs to enforce architecture and taste. Prefer invariant-based guardrails
over long lists of stylistic instructions.

### Encode remediation into tooling

Error messages, linters, and check failures should tell agents how to fix the
problem. The check itself becomes part of the harness.

### Use boring, inspectable technology by default

Favor tools and abstractions that are stable, composable, well represented in
the codebase, and easy for agents to inspect. Dependencies are still valuable,
but opaque behavior can reduce agent leverage.

### Capture plans and decisions as durable artifacts

For complex work, keep execution plans, progress logs, decisions, and known debt
in the repository. This lets future runs resume from structured history instead
of rediscovering context.

### Autonomy grows from feedback loops

Increase autonomy gradually: reproduce, inspect, fix, test, drive the app,
open a PR, respond to review, remediate CI, and escalate only for judgment.
Each step needs local tooling and verifiable signals.

### Garbage collect continuously

Agent-generated repositories can drift by copying existing patterns, including
bad ones. Maintain golden principles, quality grades, and recurring cleanup
tasks so small corrections happen continuously.

## Anti-Patterns

- A giant `AGENTS.md` that tries to be the whole knowledge base.
- Instructions that are not backed by checks or examples.
- External-only knowledge that Codex cannot access while working.
- Vague quality bars with no runnable validation.
- Templates copied without project-specific adaptation.
- Overwriting existing project truth with generic harness docs.
- Treating agent throughput as a reason to skip high-risk validation.

## Project Adaptation Questions

- What should Codex read first in this repository?
- Which docs are authoritative for architecture, product behavior, and quality?
- Which validation commands prove a change is safe?
- Which runtime signals can Codex inspect without human mediation?
- Which architectural boundaries should be mechanically enforced?
- Which recurring cleanup tasks prevent drift?
- Which decisions require human judgment before proceeding?
