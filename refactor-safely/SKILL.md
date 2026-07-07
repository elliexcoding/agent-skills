---
name: refactor-safely
description: |
  Guide behavior-preserving refactors with senior-engineer discipline. Use when
  restructuring code, reducing duplication, improving names, extracting
  abstractions, moving files, simplifying control flow, or preparing a larger
  change while preserving existing behavior.
---

# Refactor Safely

## Role

Refactor code without changing behavior unless an intentional behavior change is
explicitly requested and documented. Prefer small, verifiable steps over broad
rewrites.

The purpose of this skill is to improve structure, clarity, boundaries, or
maintainability while protecting users, tests, public contracts, and operational
behavior.

## When To Use

Use this skill when asked to:

- Clean up, simplify, reorganize, or restructure code.
- Extract functions, classes, modules, components, packages, or services.
- Rename symbols, files, routes, configuration, or public APIs.
- Remove duplication or consolidate similar logic.
- Split a large function or module.
- Prepare code for a feature without changing behavior yet.
- Reduce coupling, clarify ownership, or improve testability.

If the request includes both a refactor and behavior changes, separate the two
in the plan and verification.

## Default Workflow

1. Define the refactor boundary:
   - what may change
   - what behavior must remain the same
   - public APIs, schemas, CLI flags, configuration, files, and data formats
     that must stay compatible
2. Inspect existing behavior:
   - read nearby code, call sites, tests, docs, and usage examples
   - identify edge cases and implicit contracts
   - run the narrowest relevant existing test when practical
3. Add characterization coverage when needed:
   - prefer focused tests that lock current behavior
   - cover risky edge cases before changing structure
   - avoid overfitting to implementation details
4. Make small mechanical changes:
   - rename, move, extract, inline, or simplify one concept at a time
   - keep formatting-only churn separate when practical
   - avoid opportunistic rewrites outside the refactor boundary
5. Validate after each meaningful step:
   - run targeted tests first
   - broaden to project checks before finishing
   - inspect the diff for unintended behavior changes
6. Document intentional changes and residual risks.

For larger refactors, read `references/refactor-checklist.md` before editing.

## Refactor Types

### Mechanical

Examples: renames, moves, import updates, formatting, extraction without logic
changes.

Quality bar:

- Tool-assisted where possible.
- Easy to review.
- No semantic changes mixed in.

### Structural

Examples: module boundaries, dependency direction, class or function extraction,
shared utilities, interface cleanup.

Quality bar:

- Behavior characterized before the change.
- New boundaries have a clear responsibility.
- Abstractions are justified by real complexity or variation.

### Preparatory

Examples: making code testable, isolating side effects, introducing a seam for a
future feature, moving logic behind a stable boundary.

Quality bar:

- The future change is named.
- The preparation is useful even if the future feature changes shape.
- No speculative configuration or unused extension points.

## Safety Rules

- Do not change behavior accidentally.
- Do not combine unrelated cleanup with the requested refactor.
- Do not remove tests unless they are obsolete and replaced by equal or better
  coverage.
- Do not hide breaking API, schema, migration, or configuration changes under
  "refactor".
- Do not add abstractions only because code looks similar.
- Do not use broad formatting changes to obscure logic changes.
- Preserve user edits and untracked work.

## Validation

Prefer repository-documented commands. Otherwise use this pattern:

```sh
# Narrow check for touched behavior
<targeted test command>

# Broader confidence before finishing
<project test/build/lint/typecheck command>
```

If validation cannot run, state:

- command not run
- reason
- residual risk
- best next verification step

## Output Expectations

When planning a refactor, provide:

- refactor boundary
- behavior that must be preserved
- test or characterization strategy
- step order
- risks

When completing a refactor, report:

- what changed structurally
- what behavior was intentionally preserved
- validation run
- any intentional behavior changes
- any remaining risks or follow-up cleanup
