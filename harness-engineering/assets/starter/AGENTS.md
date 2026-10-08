# {{PROJECT_NAME}} Agent Guide

This file is the entry point for Codex. Keep it short and point to deeper,
versioned project knowledge instead of duplicating it here.

## Read When Relevant

- Service boundaries or cross-component changes: `ARCHITECTURE.md`.
- Project-specific engineering constraints: `docs/harness/principles.md`.
- Applicable validation commands: `docs/harness/quality-gates.md`.
- Complex work needing a durable plan: `docs/exec-plans/`.
- Rationale for an affected design decision: `docs/decisions/`.
- Known debt affecting the requested work: `docs/tech-debt.md`.

Read what the task needs; this is a map, not a mandatory reading sequence.

## Working Rules

- Read the relevant docs before changing behavior or architecture.
- Prefer small, reviewable changes with focused tests.
- Preserve existing public contracts unless the task explicitly changes them.
- Update docs when behavior, architecture, commands, or project assumptions
  change.
- Add or update mechanical checks when a rule is likely to recur.
- Treat repeated agent failure as a harness gap: missing docs, missing tests,
  missing runtime visibility, or missing tooling.

## Validation

Run the applicable required checks in `docs/harness/quality-gates.md`. Broaden
validation when changed dependencies, failures or unresolved risks justify it;
do not repeat successful checks on unchanged code without a new reason. If a
check cannot run, state why and identify the residual risk.

## Human Escalation

Ask for human judgement when an unresolved decision affects product direction,
security, data retention, irreversible migrations or external contracts and is
not settled by the user's request or repository evidence. Use existing scoped
authorisation; do not ask again for an already agreed action. Continue work
that does not depend on the missing decision.
