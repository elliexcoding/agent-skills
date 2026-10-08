---
name: harness-engineering
description: Create or improve repository guidance, knowledge maps and quality checks when asked to set up an agent development harness.
---

# Harness Engineering

## Overview

Seed repositories with a small, agent-legible harness: a concise `AGENTS.md`,
versioned docs as the system of record, architecture and quality maps, and
places to capture plans, decisions, and technical debt.

## Context Discipline

- Use the seeding script for a requested scaffold. For a narrow guidance edit,
  change the relevant existing file without seeding unrelated documents.
- Read `references/harness-principles.md` only when adapting the principles or
  explaining the rationale.
- Read `references/seeding-guide.md` only when changing the seeded file set,
  handling an existing repo, or customizing the workflow.
- Do not paste the full OpenAI article into project files. Distill its ideas
  into local, project-specific operating rules.

## Default Workflow

1. Inspect the target repository:
   - `pwd`
   - `rg --files -g 'AGENTS.md' -g 'ARCHITECTURE.md' -g 'docs/**'`
   - project package/config files relevant to the stack
2. Decide whether this is a fresh seed, an existing-repo upgrade or a targeted
   guidance edit. Keep the artefact set proportionate to the request.
3. Seed missing files with:

   ```sh
   python3 <skill-dir>/scripts/seed_harness.py --target <repo-root>
   ```

   Add `--project-name "<name>"` when the repository directory name is not the
   right project name.
4. For existing repos, keep local truth authoritative:
   - Do not overwrite existing docs unless explicitly asked.
   - Merge concepts into existing docs when they already serve the same role.
   - Keep `AGENTS.md` short and link to deeper docs.
5. Review the diff and adapt placeholders to the real project.
6. Add project-specific validation commands, architecture boundaries, and
   recurring cleanup expectations.

## Seeded Harness

The default script creates missing files from `assets/starter/`:

- `AGENTS.md`: short entry point and map for Codex.
- `ARCHITECTURE.md`: current architecture, boundaries, and invariants.
- `docs/harness/README.md`: harness purpose and maintenance loop.
- `docs/harness/principles.md`: local golden principles.
- `docs/harness/quality-gates.md`: validation and review gates.
- `docs/exec-plans/README.md`: durable plan format for complex work.
- `docs/decisions/README.md`: lightweight decision records.
- `docs/tech-debt.md`: visible debt and cleanup queue.

## Commands

```sh
# Preview what would be created
python3 <skill-dir>/scripts/seed_harness.py --target <repo-root> --dry-run

# Seed missing files only
python3 <skill-dir>/scripts/seed_harness.py --target <repo-root>

# Overwrite existing harness files only when explicitly requested
python3 <skill-dir>/scripts/seed_harness.py --target <repo-root> --force
```

## Validation

- Run the script with `--dry-run` before seeding a non-empty repository.
- After seeding, inspect `git diff`.
- Confirm `AGENTS.md` is a map, not a manual.
- Confirm deeper docs are linked and discoverable.
- Confirm validation commands are executable or clearly marked as TODOs.
