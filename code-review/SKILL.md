---
name: code-review
description: Review commits, diffs or selected files for concrete defects and regression risks. For PR merge-readiness, use review-pull-request.
---

# Code Review

Review the requested diff or files for actionable defects. Remain read-only
unless fixes are requested. Lead with findings, ordered by severity.

## Scope and evidence

Establish the comparison base and review boundary. Inspect the changed code,
relevant callers, contracts and tests; do not imply coverage beyond what you read.
Prioritise behaviour, compatibility, error paths, security boundaries and
operational impact over style.

A finding needs a reachable trigger, precise location and material consequence.
Search for guards, caller guarantees or tests that disprove each candidate.
Report a missing test only when a concrete failure could escape. Recommend the
smallest useful correction, not a broad rewrite.

Use existing validation evidence. Run a targeted local check when it resolves a
specific concern; distinguish observed results from static arguments and checks
not run. Follow repository-required review checks without repeating completed
checks unless the code or relevant conditions changed.

## Choose the review workflow

- For a PR, proposed merge or stacked change, use `review-pull-request` when
  available; its workflow includes specialist lenses. Do not stack both general
  review workflows by default.
- For a Python- or Rust-focused review outside that workflow, use the matching
  language review skill when available. For mixed-language work, add only the
  language guidance relevant to the changed paths.
- For a larger review with uncertain coverage, consult the relevant sections of
  [the review checklist](references/review-checklist.md).
- An adversarial second pass or exhaustive security audit is a separate scope;
  do not silently turn an ordinary review into either.

## Findings and severity

Use the repository's severity scheme, otherwise:

| Level | Meaning |
| --- | --- |
| P0 | Immediate catastrophic production, security or data-integrity failure. |
| P1 | Likely serious defect, vulnerability, broken contract or unsafe rollout. |
| P2 | Material edge case, test gap, performance or operational weakness. |
| P3 | Useful, bounded improvement that need not block the change. |

For each finding give the severity, actionable title, file and line (or exact
symbol), trigger, consequence, supporting evidence and smallest remediation.
Separate uncertainty from confirmed defects and optional suggestions from
required fixes. Omit taste-based comments without a repository convention or
material readability problem.

Finish with any questions that affect the judgement and material validation
limitations. If no finding meets the evidence threshold, say so; do not invent
issues or confuse lack of evidence with proof of correctness.
