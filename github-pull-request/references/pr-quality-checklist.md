# Pull Request Quality Checklist

Use this checklist as a final review pass before drafting or creating a GitHub
pull request. Apply it pragmatically: the goal is better review quality and
lower change risk, not ceremony.

## Diff Hygiene

- The diff is limited to the requested work.
- Generated files, build outputs, caches, and local-only configuration are
  excluded unless intentionally versioned.
- Formatting-only churn is separated from behavior changes when practical.
- Temporary debug logs, print statements, commented-out experiments, and local
  notes are removed.
- File moves or renames are intentional and easy to identify.

## Correctness

- The implementation addresses the actual problem rather than only the observed
  symptom.
- Important edge cases are handled.
- Error paths are explicit and useful to callers or operators.
- Data validation happens at appropriate boundaries.
- Public API or behavior changes are intentional and documented.

## SOLID And Design Principles

- Single Responsibility: changed modules, classes, functions, or components have
  focused reasons to change.
- Open/Closed: extension points are used only when real variation exists; simple
  direct code is preferred for one-off behavior.
- Liskov Substitution: implementations honor the expectations of the interfaces
  or base types they satisfy.
- Interface Segregation: callers are not forced to depend on methods, fields, or
  concepts they do not use.
- Dependency Inversion: high-level policy is not tightly coupled to volatile
  implementation details without a good reason.
- DRY: duplication is removed when it represents shared knowledge, but
  incidental similarity is not abstracted prematurely.
- KISS: the design is understandable from local context.
- YAGNI: speculative features, flags, parameters, and abstractions are avoided.

## Tests And Validation

- There is a focused test for new behavior or a clear reason one is unnecessary.
- Regression tests fail without the fix when practical.
- Existing tests that cover touched behavior still pass.
- Manual validation is described when automated coverage is not feasible.
- Skipped checks are called out honestly with the reason and residual risk.

## Security And Privacy

- Secrets, tokens, credentials, private keys, and personal data are not included
  in code, logs, fixtures, screenshots, or PR text.
- Inputs that cross trust boundaries are validated or constrained.
- Path, shell, SQL, HTML, URL, deserialization, and template handling avoid
  injection risks.
- Authentication, authorization, and tenant or user boundaries are preserved.
- Dependency changes are necessary and come from trusted packages.

## Operations And Performance

- Logging and errors provide useful diagnostics without leaking sensitive data.
- Expensive work is bounded, cached, streamed, or moved off hot paths when
  necessary.
- Database, network, filesystem, and external-service behavior is considered.
- Rollout, rollback, migration, and compatibility concerns are documented.
- Configuration changes have sensible defaults and clear failure modes.

## Documentation And Reviewability

- README, API docs, changelogs, migration notes, or runbooks are updated when
  the user or operator experience changes.
- The PR description explains why the change exists, not just what files
  changed.
- Review notes point to the parts of the diff that deserve attention.
- Screenshots or before/after examples are included for UI or output changes
  when they would reduce reviewer ambiguity.
