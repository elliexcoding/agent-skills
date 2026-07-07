# Harness Seeding Guide

Use this reference when changing the seeded file set, upgrading an existing
repository, or customizing the harness beyond the default script.

## File Roles

- `AGENTS.md`: Short context entry point. Keep it under roughly 100 lines and
  link to deeper docs.
- `ARCHITECTURE.md`: Current architecture, dependency boundaries, invariants,
  and known seams where future agents should look first.
- `docs/harness/README.md`: Defines the harness itself and how it is maintained.
- `docs/harness/principles.md`: Project-specific golden principles that should
  be promoted into checks when possible.
- `docs/harness/quality-gates.md`: Commands and expectations for formatting,
  tests, linting, security, performance, and review.
- `docs/exec-plans/README.md`: Durable plan format for complex work.
- `docs/decisions/README.md`: Lightweight decision records for tradeoffs.
- `docs/tech-debt.md`: Visible cleanup queue with owners or triggers.

## Fresh Repository Workflow

1. Run `seed_harness.py --dry-run`.
2. Run `seed_harness.py`.
3. Replace placeholders in the generated files.
4. Add stack-specific validation commands.
5. Add architecture boundaries once the stack is known.
6. Commit the harness before adding large features.

## Existing Repository Workflow

1. Inspect existing docs before seeding.
2. Run `seed_harness.py --dry-run`.
3. Seed only missing files by default.
4. Merge ideas into existing docs rather than creating duplicates.
5. Use `--force` only when the user explicitly requests overwriting generated
   harness files.

## Customization Guidance

- Keep permanent instructions in `AGENTS.md` minimal.
- Move detailed domain knowledge to `docs/`.
- Use mechanical checks for recurring rules.
- Prefer project-specific validation over generic best practices.
- Add examples only when they prevent repeated mistakes.
- Delete generated sections that do not apply.

## Search Patterns

Use these before changing a harness:

```sh
rg -n "harness|AGENTS|architecture|quality|exec plan|technical debt" .
rg --files -g 'AGENTS.md' -g 'ARCHITECTURE.md' -g 'docs/**'
```
