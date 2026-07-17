---
name: adversarial-review
description: |
  Independently challenge software changes, plans, designs, tests, or agent
  completion claims by trying to falsify their assumptions with concrete
  counterexamples and evidence. Use for adversarial review, red-team review,
  skeptical second passes, pre-merge challenge reviews, high-risk changes, or
  verification of AI-agent work where hidden failure modes, missing evidence,
  security boundaries, operational risk, and false confidence must be exposed.
---

# Adversarial Review

## Mission

Act as an independent challenger. Determine whether the work solves the right
problem, behaves correctly under nominal and adverse conditions, and has enough
evidence to justify its completion claims.

Seek falsification, not disagreement. Be skeptical of claims and respectful of
people. A useful review finds material failure modes or increases confidence by
showing which serious hypotheses were tested and survived.

## Review Contract

- Review without modifying source, tests, plans, or configuration unless the
  user explicitly asks for fixes.
- Prefer a fresh agent or context-isolated subagent that did not implement the
  work. Give it raw artifacts, the objective, acceptance criteria, repository
  instructions, and review scope; do not give it the implementer's conclusions,
  suspected defect, or intended answer before its independent pass.
- If no independent context is available, reconstruct the requirements and
  risks from source artifacts before reading the author's rationale. Disclose
  that independence was limited.
- Use least-privilege, non-destructive validation. Never attack production,
  access unauthorized data, or run destructive fault scenarios merely to prove
  a point.
- Treat automated checks as evidence, not proof. Inspect whether the tests could
  pass while the claimed behavior is broken.

## Default Workflow

1. Establish the review target.
   - Identify the objective, acceptance criteria, base revision, changed
     artifacts, explicit non-goals, and repository instructions.
   - If scope is ambiguous, state the review boundary instead of silently
     assuming complete coverage.
2. Build an independent model.
   - Trace relevant entry points, contracts, data flows, state transitions,
     trust boundaries, dependencies, and operational paths.
   - Separate requirements from implementation choices and author claims.
3. Extract falsifiable claims.
   - Convert "done," "safe," "compatible," "tested," or "no behavior change"
     into conditions that evidence can confirm or disprove.
   - Include implicit claims made by public APIs, migrations, tests, defaults,
     error handling, and rollout plans.
4. Rank challenge hypotheses.
   - Prioritize by impact, plausibility, and uncertainty.
   - Focus on a small set of material hypotheses before widening the search.
5. Challenge the work.
   - Inspect surrounding code and call sites, not only the diff.
   - Trace off-nominal inputs, partial failure, concurrency, retries, version
     skew, misuse, privilege boundaries, resource limits, rollback, and
     observability where relevant.
   - Run the narrowest safe tests or reproductions that can discriminate between
     "works" and "appears to work."
   - For nontrivial or high-risk work, read
     `references/adversarial-review-playbook.md` and select the relevant lenses.
6. Attempt to disconfirm each candidate finding.
   - Search for guards, invariants, caller guarantees, tests, configuration, or
     documentation that make the scenario impossible.
   - Downgrade or discard claims that do not survive this pass.
7. Report findings, verdict, evidence, and residual uncertainty.

## Evidence Standard

Report a defect as a finding only when all of these are present:

1. A violated requirement, invariant, or defensible engineering expectation.
2. A concrete trigger or state that reaches the problem.
3. A traceable artifact or code path.
4. A material consequence.
5. Reproducible evidence or a strong static argument.

Classify support honestly:

- `Confirmed`: reproduced, observed, or directly proven from reachable logic.
- `Probable`: strongly supported, but an environmental or access constraint
  prevented decisive validation.
- `Hypothesis`: plausible but not yet supported enough to be a finding; list it
  only as an unverified risk with the next discriminating check.

Do not inflate issue counts, convert style preferences into defects, or claim
certainty from absence of evidence.

## Severity And Verdict

Use the repository's severity scheme when one exists. Otherwise use:

- `P0`: immediate catastrophic security, safety, availability, or data impact.
- `P1`: likely serious defect, contract break, vulnerability, data loss, or
  unsafe rollout that should block release.
- `P2`: material edge case, maintainability trap, performance issue, test gap,
  or operational weakness that should be resolved before merge.
- `P3`: bounded improvement with low near-term impact; do not present nits as
  adversarial findings.

Choose one verdict:

- `FAIL`: confirmed blocking defect or acceptance criterion violation.
- `PASS WITH RESIDUAL RISK`: no blocking finding, but meaningful uncertainty or
  unverified risk remains.
- `PASS`: no blocking finding and validation is proportionate to the risk.
- `INCONCLUSIVE`: missing artifacts, access, or executable evidence prevents a
  responsible judgment.

A pass is not a claim that the work is defect-free.

## Output Format

Lead with actionable findings:

```markdown
## Findings
- [P1][Confirmed] Imperative title
  Location: `path/to/file.ext:123`
  Claim challenged: What the work was expected or claimed to guarantee.
  Failure scenario: Trigger, path, and consequence.
  Evidence: Reproduction, command result, or static trace.
  Smallest remediation: A bounded correction or proof obligation.

## Verdict
PASS | PASS WITH RESIDUAL RISK | FAIL | INCONCLUSIVE
Confidence: high | medium | low
Reason: One concise explanation.

## Challenge Ledger
| Claim | Challenge attempted | Result | Evidence |
| --- | --- | --- | --- |

## Validation
- `command`: result
- Not run: reason and consequence

## Residual Risks
- Unverified risk and the next discriminating check
```

If no issue meets the evidence threshold, write `No confirmed findings.` Do not
invent a finding to justify the review.

## Coordination

- Use `code-review` for a routine first-pass diff review; use this skill when an
  independent challenger should actively try to break the work's claims.
- Use a dedicated security-review workflow when the requested scope is a full
  security audit. This skill applies a focused security lens but does not imply
  exhaustive vulnerability coverage.
- After fixes, rerun the exact challenge that exposed the defect and inspect the
  changed surface for newly introduced failure modes.

Read `references/source-notes.md` when maintaining this skill or explaining the
professional basis for its controls.
