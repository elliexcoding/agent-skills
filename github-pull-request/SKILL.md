---
name: github-pull-request
description: |
  Prepare high-quality GitHub pull requests from completed work. Use when
  drafting or creating PR titles and descriptions, summarizing diffs, checking
  validation evidence, or doing a final engineering-quality review before a PR
  is opened or handed off.
---

# GitHub Pull Request

## Role

Prepare pull requests that are easy to review, accurately describe the work,
and include a final quality check against sound engineering practices.

## Default Workflow

1. Inspect repository state:
   - `git status --short`
   - `git branch --show-current`
   - `git remote -v`
   - `git log --oneline --decorate -n 12`
2. Determine the comparison base:
   - Prefer the PR base branch requested by the user.
   - Otherwise infer the default branch from `origin/HEAD`, `main`, or
     `master`.
3. Understand the work:
   - `git diff --stat <base>...HEAD`
   - `git diff --name-status <base>...HEAD`
   - `git diff <base>...HEAD`
   - relevant commits with `git log --oneline <base>..HEAD`
4. Identify user-facing behavior, internal refactors, migrations, docs, tests,
   and operational risks.
5. Run or report validation:
   - Prefer project-documented commands.
   - Otherwise run targeted tests first, then broader checks when practical.
   - If a check cannot run, state the reason and residual risk.
6. Perform the final quality check. Read
   `references/pr-quality-checklist.md` when doing this review.
7. Draft the PR title and description.
8. If asked to create the PR, use the GitHub CLI when available:

   ```sh
   gh pr create --title "<title>" --body-file <body-file>
   ```

   Do not create a PR until the title, body, base branch, and target branch are
   clear.

## PR Title

Write a title that is specific, reviewable, and tied to the main outcome.

- Use imperative mood when the change is action-oriented:
  `Add harness seeding dry-run output`.
- Prefer a concrete noun or subsystem up front when it improves scanning:
  `Rust skill: Add async review guidance`.
- Keep it short enough to scan in GitHub lists, ideally 72 characters or fewer.
- Avoid vague titles such as `Fix bugs`, `Update files`, `Improve code`, or
  `Changes`.
- Do not overstate the work. If the change is preparatory, say so.
- Include issue IDs only when the repository convention expects them.

## PR Description

Use the repository's pull request template when one exists. Otherwise use this
structure and omit sections that genuinely do not apply:

```markdown
## Summary
- 

## Changes
- 

## Validation
- 

## Risks
- 

## Review Notes
- 
```

### Summary

Explain the outcome in one to three bullets. Focus on what changed and why, not
on every file touched.

### Changes

Group related implementation details by behavior or subsystem. Call out API,
schema, configuration, dependency, migration, and documentation changes.

### Validation

List commands that were actually run and their results. Do not imply checks ran
when they did not.

Good examples:

- `npm test`
- `cargo test --workspace --all-features`
- `python -m pytest tests/test_seed_harness.py`
- `Not run: integration tests require staging credentials.`

### Risks

Call out compatibility, rollout, data, performance, security, and operational
risks. If risk is low, explain the concrete reason.

### Review Notes

Point reviewers to the highest-value files or decisions. Include screenshots,
logs, or before/after notes only when they help review.

## Final Quality Gate

Before finalizing a PR, check:

- Correctness: the change solves the stated problem and handles relevant edge
  cases.
- Simplicity: the design is no more complex than the problem requires.
- SOLID: responsibilities are focused, dependencies are pointed in stable
  directions, and abstractions have a clear reason to exist.
- Maintainability: naming, structure, and boundaries match the surrounding
  codebase.
- Tests: important behavior has focused coverage, and risky paths are verified.
- Safety: secrets, generated artifacts, debug code, and unrelated churn are not
  included.
- Documentation: user-facing behavior, operations, and setup changes are
  documented where the repository expects them.

Use the detailed checklist in `references/pr-quality-checklist.md` for larger
or riskier changes.

## Output Expectations

When drafting only, provide:

- Proposed PR title.
- Proposed PR description.
- Validation performed or still needed.
- Quality-gate notes and any concerns.

When creating a PR, report:

- PR URL.
- Base and head branches.
- Validation performed.
- Any remaining review risks.
