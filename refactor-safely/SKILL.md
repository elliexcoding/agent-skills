---
name: refactor-safely
description: Restructure code while preserving behaviour. Use for requested renames, extraction, deduplication or changes to module boundaries.
---

# Refactor Safely

Improve the requested structure while preserving observable behaviour. If the
request also changes behaviour, identify and verify that change separately.

## Establish the boundary

Identify the affected consumers and contracts: public APIs, schemas, CLI flags,
configuration, serialised formats, ordering, errors and side effects where
relevant. Read enough callers and tests to understand the behaviour that must
survive. Keep unrelated clean-up outside the change.

Choose the approach that fits the work:

- **Mechanical:** Prefer tool-assisted renames, moves and import updates; keep
  semantic changes separate.
- **Structural:** Characterise risky behaviour before changing responsibilities
  or dependency boundaries. Abstract shared knowledge, not coincidental syntax.
- **Preparatory:** Name the future change and keep the preparation useful on its
  own; avoid unused extension points or speculative configuration.

For a larger refactor, use the relevant sections of
[the refactor checklist](references/refactor-checklist.md) to check compatibility
and stopping conditions.

## Change and verify

Make small, reviewable changes. Use existing tests where they cover the affected
contracts; add characterisation tests only for a concrete uncovered risk. Tests
should distinguish preserved behaviour from a regression, not mirror the new
implementation.

Run affected checks after meaningful changes and the checks required by the
repository. Broaden validation when changed dependencies, failures or unresolved
risks justify it. Inspect the final diff for accidental behaviour changes,
unrelated formatting and lost user edits.

Do not remove or weaken tests to accommodate a refactor, hide breaking changes
under its name, or reset unrelated work. If progress requires a behaviour change
outside the request, preserve the current work and explain the decision needed.

## Report

State the structural change, preserved contracts and validation evidence. Name
any intentional behaviour change separately. For omitted checks, state the
reason, resulting uncertainty and next useful verification step. A simple
refactor needs only a short explanation; a plan is not a mandatory deliverable.
