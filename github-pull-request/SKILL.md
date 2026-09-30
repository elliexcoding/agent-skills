---
name: github-pull-request
description: |
  Prepare high-quality GitHub pull requests from completed work. Use when
  drafting or creating PR titles and descriptions, summarising diffs, assessing
  blast radius, checking validation evidence, or preparing proportionate human
  review before a PR is opened or handed off.
---

# GitHub Pull Request

## Role

Prepare pull requests that are easy to review, accurately describe the work,
and direct human attention towards consequential changes. Assess blast radius
for every PR; add a visual walkthrough only when the change warrants one.

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
4. Assess blast radius and choose review depth using the guidance below. Trace
   affected callers and consumers beyond the changed files where needed.
5. Run or report validation:
   - Prefer project-documented commands.
   - Otherwise run targeted tests first, then broader checks when practical.
   - If a check cannot run, state the reason and residual risk.
6. Perform the final quality check. For focused or critical changes, read
   `references/pr-quality-checklist.md`.
7. Draft the PR title and description, always including **Blast radius**. Apply
   the visual walkthrough gate below before loading its reference or creating
   any visual artefact.
8. If asked to create the PR, use the GitHub CLI when available:

   ```sh
   gh pr create --title "<title>" --body-file <body-file>
   ```

   Do not create a PR until the title, body, base branch, and target branch are
   clear.

## Blast Radius And Review Depth

Determine impact from behaviour and reach, not line count, file count, a PR
label, or a version number. A one-line permission change can be critical.
Consider the whole PR; use the highest applicable review depth for mixed work.

Ground the assessment in the diff, relevant consumers, configuration, and
validation evidence:

- **Reach:** affected entry points, shared modules, downstream consumers, users,
  tenants, and services. Distinguish current rollout exposure from eventual
  reach; a disabled feature flag does not make a new feature routine.
- **Consequences:** changes to contracts, persisted data, permissions, external
  effects, availability, performance, or deployment behaviour. State what could
  fail and who would experience it.
- **Recovery:** compatibility, rollout controls, rollback practicality, and any
  state or external effects that reverting code would not undo.
- **Evidence and uncertainty:** relevant checks and concrete limits on the
  assessment. Do not claim no downstream impact without inspecting the relevant
  consumers. Unknown reach or missing material validation rules out routine
  treatment; investigate or state the gap and escalate proportionately.

Choose a review depth and give a short reason:

| Review depth | When it applies | Human review experience |
| --- | --- | --- |
| **Routine** | Bounded, understood maintenance with no material contract, behaviour, data, security, or operational change; relevant checks support the assessment and recovery is straightforward. Examples include prose corrections and compatible package upgrades after checking release notes, lockfile changes, and affected usage. | Keep the PR concise: outcome, blast radius, and validation. Recommend the repository's lightweight review or established automated path when policy permits; do not add discretionary reviewers or review ceremony. Skip the visual walkthrough. |
| **Focused** | A new endpoint, feature, or meaningful behaviour change with bounded impact; a nontrivial refactor; or uncertainty that prevents routine treatment. | Identify the decisions and code paths needing human judgement. Add a walkthrough only if the significance gate below applies. |
| **Critical** | Material risk to authentication or authorisation, tenant isolation, data integrity, payments, public compatibility, shared infrastructure, or service availability; failures with broad impact or difficult recovery. | Prioritise substantive review by the relevant domain owners. Explain failure modes, validation gaps, and rollout/recovery decisions. Add a walkthrough only if the significance gate below applies. |

A package version upgrade alone does not warrant a visual walkthrough. Assess
breaking changes, transitive dependencies, runtime usage, and migrations before
calling it routine. A risky upgrade can need critical review without a visual;
if it also changes application contracts or architecture, assess those changes
against the gate in their own right.

These are review recommendations, not merge authorisation. Preserve repository
approval requirements, CODEOWNERS, required checks, and any workflow-specific
human merge gate. Do not change branch protection, request reviewers, or enable
auto-merge merely because a PR receives a particular classification.

## Visual Walkthrough Gate

Include a **Reviewer walkthrough** for significant implementation changes:

- A new endpoint, public interface, or materially changed API contract, even
  when the implementation is small.
- A substantial user journey, business rule, algorithm, or state transition.
- A structural change to service interactions, ownership, data flow, or trust
  boundaries that reviewers need to understand to judge correctness.

For these changes, read [references/reviewer-walkthrough.md](references/reviewer-walkthrough.md)
and produce the smallest useful view of the changed behaviour. For other PRs,
omit the walkthrough and do not load the reference or generate visual artefacts.
A reviewer or user can explicitly request an explanation for any change.
High risk alone does not require a diagram; a short permission change may need
careful human scrutiny with a clear textual explanation.

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

Use the repository's pull request template when one exists, preserving its
required fields. Add **Blast radius**, or a clearly labelled subsection within
its existing impact/risk section. Otherwise use this structure and omit optional
sections that genuinely do not apply. Always retain **Blast radius** and
**Validation**; keep routine PRs to those sections and a short summary.

```markdown
## Summary
- 

## Blast radius
- Review depth: Routine / Focused / Critical — reason supported by evidence.
- Affected users/systems and possible consequences:
- Recovery and remaining uncertainty:

## Changes
- 

## Validation
- 

## Review Notes
- 

## Reviewer walkthrough
<!-- Only when the significance gate applies or explicitly requested. -->
```

### Summary

Explain the outcome in one to three bullets. Focus on what changed and why, not
on every file touched.

### Changes

Group related implementation details by behaviour or subsystem. Call out API,
schema, configuration, dependency, migration, and documentation changes.

### Validation

List commands that were actually run and their results. Do not imply checks ran
when they did not.

Good examples:

- `npm test`
- `cargo test --workspace --all-features`
- `python -m pytest tests/test_seed_harness.py`
- `Not run: integration tests require staging credentials.`

### Blast Radius

State review depth, affected users and systems, plausible consequences, and
recovery/uncertainty using the assessment above. Use a compact paragraph for
routine work and expand only where the impact needs explanation. Refer to
validation results without repeating logs. If the repository also requires a
Risks section, cross-reference it rather than duplicating the assessment.

### Review Notes

Point reviewers to the highest-value files or decisions. Include screenshots,
logs, or before/after notes only when they help review. For significant changes,
use the conditional walkthrough to orient reviewers, then ask concrete review
questions about the consequential decisions. Remove empty sections and template
comments from the finished description.

## Final Quality Gate

Before finalising a PR, check:

- Correctness: the change solves the stated problem and handles relevant edge
  cases.
- Simplicity: the design is no more complex than the problem requires.
- SOLID: responsibilities are focused, dependencies are pointed in stable
  directions, and abstractions have a clear reason to exist.
- Maintainability: naming, structure, and boundaries match the surrounding
  codebase.
- Tests: important behaviour has focused coverage, and risky paths are verified.
- Safety: secrets, generated artefacts, debug code, and unrelated churn are not
  included.
- Documentation: user-facing behaviour, operations, and setup changes are
  documented where the repository expects them.
- Review effort: blast radius is evidenced, review depth is proportionate, and
  a walkthrough is included only when the significance gate applies or requested.

Use the detailed checklist in `references/pr-quality-checklist.md` for larger
or riskier changes.

## Output Expectations

When drafting only, provide:

- Proposed PR title.
- Proposed PR description.
- Blast radius and recommended review depth.
- Validation performed or still needed.
- Quality-gate notes and any concerns.

When creating a PR, report:

- PR URL.
- Base and head branches.
- Validation performed.
- Blast radius, recommended review depth, and any remaining review risks.
