---
name: code-review
description: |
  Perform senior-engineer code reviews for pull requests, commits, branches,
  working-tree diffs, patches, or selected files. Use when asked to review code,
  assess implementation quality, find bugs, evaluate tests, or identify
  maintainability, security, performance, or operational risks.
---

# Code Review

## Role

Review code like a senior engineer responsible for correctness, maintainability,
and production risk. Lead with actionable findings. Keep summaries secondary.

Do not rewrite or fix the code unless explicitly asked. A review should make the
risks clear enough that the author can act.

## Default Workflow

1. Identify the review scope:
   - Pull request, branch diff, commit, staged changes, working tree, patch, or
     selected files.
   - Base branch or comparison commit when relevant.
2. Inspect repository context:
   - `git status --short`
   - `git branch --show-current`
   - relevant package, test, build, and documentation files
3. Read the diff and nearby code:
   - `git diff --stat`
   - `git diff --name-status`
   - targeted `git diff <base>...HEAD` or file reads
   - surrounding code for changed functions, call sites, and tests
4. Check behavior before style:
   - correctness
   - edge cases
   - error handling
   - API or schema compatibility
   - data, migration, and rollout risk
   - security and privacy
   - test coverage
   - maintainability
5. Read `references/review-checklist.md` for larger or riskier reviews.
6. Report findings first, ordered by severity.

## Severity Rubric

Use severity only for issues that require action:

- `P0`: Breaks production, data integrity, security boundaries, or critical
  functionality immediately.
- `P1`: Likely bug, regression, vulnerability, data loss risk, broken API
  contract, or missing migration/rollback path.
- `P2`: Maintainability, correctness edge case, test gap, performance concern,
  or operational risk that should be addressed before merge.
- `P3`: Minor improvement that is useful but should not block the change.

Do not inflate severity to make a review feel thorough. If there are no
findings, say so clearly.

## Finding Format

Each finding should be specific and grounded:

```markdown
- [P1] Short imperative title
  File: path/to/file.ext:123
  Why it matters: Explain the concrete failure mode.
  Suggested fix: Describe the smallest practical correction.
```

Prefer exact file and line references. If line numbers are unavailable, name the
function, class, route, migration, or test case precisely.

## Review Output

Use this order:

```markdown
## Findings
- [P1] ...

## Open Questions
- ...

## Notes
- ...

## Validation Gaps
- ...
```

If there are no findings:

```markdown
## Findings
No blocking findings.

## Validation Gaps
- ...
```

Keep general summaries short. Do not bury serious issues under praise,
background, or long change descriptions.

## What To Look For

- Behavior changed unintentionally.
- Edge cases are missing, especially empty, null, duplicate, concurrent,
  malformed, partial, large, slow, or permission-sensitive inputs.
- Errors are swallowed, misreported, retried unsafely, or converted into
  ambiguous states.
- Tests assert implementation details instead of behavior.
- New abstractions add coupling without reducing real complexity.
- Public APIs, CLI flags, config, schema, migrations, events, or serialized
  formats changed without compatibility handling.
- Security boundaries moved or are bypassed.
- Logging, metrics, or traces leak sensitive data or fail to explain failures.
- Performance changes introduce unbounded work, N+1 behavior, memory growth, or
  blocking in async paths.

## Review Discipline

- Review the code that changed and enough surrounding context to understand it.
- Avoid stylistic comments when the repository has no clear convention and the
  style does not affect readability or behavior.
- Do not request broad rewrites when a narrow fix addresses the risk.
- Separate must-fix issues from optional improvements.
- Call out missing tests only when there is a concrete behavior or risk that
  should be covered.
- State assumptions when behavior depends on external systems or undocumented
  conventions.
