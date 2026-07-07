# {{PROJECT_NAME}} Agent Guide

This file is the entry point for Codex. Keep it short and point to deeper,
versioned project knowledge instead of duplicating it here.

## Start Here

- Architecture map: `ARCHITECTURE.md`
- Harness principles: `docs/harness/principles.md`
- Quality gates: `docs/harness/quality-gates.md`
- Execution plans: `docs/exec-plans/`
- Decisions: `docs/decisions/`
- Technical debt: `docs/tech-debt.md`

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

Before finishing, run the project-specific checks in
`docs/harness/quality-gates.md`. If a check cannot run, state why and identify
the residual risk.

## Human Escalation

Ask for human judgment when a task changes user-visible product direction,
security posture, data retention, irreversible migrations, external contracts,
or another decision not inferable from repository context.
