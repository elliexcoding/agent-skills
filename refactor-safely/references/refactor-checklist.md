# Safe Refactor Checklist

Use this checklist for behavior-preserving refactors. It is designed to keep
AI-assisted refactoring reviewable, reversible, and grounded in evidence.

## Scope

- The refactor has a clear goal.
- The affected files, modules, packages, services, or components are named.
- Public contracts that must remain stable are identified.
- Behavior changes are either out of scope or explicitly listed.
- Unrelated cleanup is deferred.

## Existing Behavior

- Nearby tests, examples, docs, and call sites were inspected.
- Important edge cases are understood.
- Implicit contracts are identified, including:
  - null, empty, malformed, duplicate, partial, large, and slow inputs
  - error messages and error types
  - ordering, timing, retries, and concurrency
  - path, encoding, timezone, locale, and precision behavior
  - public API, CLI, schema, event, and file-format compatibility

## Characterization Tests

- Existing tests cover the risky behavior, or new focused tests were added.
- Tests assert externally visible behavior, not private implementation details.
- Tests cover the edge cases most likely to regress.
- If no tests were added, the reason is concrete and defensible.

## Change Discipline

- Mechanical moves and renames are separate from logic edits when practical.
- Each extraction or abstraction has a clear responsibility.
- Shared code represents shared knowledge, not coincidental similarity.
- New interfaces are introduced only when there is real variation, isolation, or
  testability value.
- Dependency direction improves or stays stable.
- The diff remains reviewable.

## Compatibility

- Public APIs remain compatible or the breaking change is intentional.
- Serialized formats, migrations, events, config keys, CLI flags, and file names
  remain compatible.
- Imports, package exports, generated files, docs, and examples are updated.
- Rollout and rollback concerns are considered for deployed systems.

## Validation

- Targeted tests for touched behavior pass.
- Broader project checks pass when practical.
- Static analysis, type checks, formatters, and linters are run when relevant.
- Manual validation is documented when automated checks are insufficient.
- Failed or skipped checks are reported with exact commands and residual risk.

## Reviewability

- The final summary distinguishes:
  - pure refactor
  - intentional behavior change
  - test-only change
  - documentation or tooling update
- The most important files are called out for reviewers.
- The diff does not contain debug code, generated junk, or local-only artifacts.
- Follow-up cleanup is listed instead of silently bundled.

## Stop Conditions

Stop and reassess if:

- Tests begin failing for reasons not understood.
- The refactor requires changing public behavior to proceed.
- The diff grows beyond the original boundary.
- A new abstraction becomes more complex than the duplicated code.
- Repository state changes unexpectedly.
- User input is needed to choose between competing designs.
