# Review Playbook

## Review sequence

Review broad intent and acceptance criteria first, then trace the architectural main path. Inspect the complete available diff, changed tests, compatibility boundaries, and operational effects before forming findings.

## Risk triage

Prioritize impact, reachability, reversibility, blast radius, and uncertainty. Increase scrutiny where the change crosses authentication, authorization, data ownership, network, deployment, persistence, or other trust boundaries.

## General lenses

Check correctness; data handling; concurrency; errors and partial failure; API, schema, and configuration compatibility; performance; observability; rollout and rollback; maintainability; documentation; and scope. Treat tests as reviewed code, not proof by themselves.

## Leadership judgement

Support the user's development towards L5 and beyond through explicit reasoning about system and team outcomes. Use a supplied company competency framework when available; level names vary between organisations, and a PR review alone cannot establish readiness for a role.

Select the lenses relevant to the change:

- **Software architect:** examine system boundaries, contracts, data ownership, coupling and failure propagation. Relate complexity, cost and future flexibility to known requirements; explain when the existing design is sufficient and when an alternative is justified.
- **Tech lead:** examine compatibility, dependencies, delivery sequencing and operational readiness. Surface concrete migration, rollout, recovery or observability decisions where the change warrants them, including coordination needed across components or teams.
- **Engineering manager:** connect technical decisions to user impact, delivery priorities, maintenance and support burden. Consider effort against risk reduction and clarify ownership or coordination gaps supported by the context. Keep feedback about the work; do not infer an author's competence, motives or team performance.

For each useful observation, connect repository evidence or documented constraints to an outcome, explain the relevant trade-off, and recommend a proportionate next step. Distinguish work needed in this PR from a possible follow-up; suggest an owner only when ownership is established in the available context. Use focused questions for uncertainty that could change a decision.

Scale this analysis to the change. A small PR may warrant only a brief explanation of why its scope and design are appropriate. Avoid speculative redesigns, process demands and comments added merely to sound senior. Apply the existing evidence threshold and severity rules to any proposed finding; leadership suggestions alone do not justify blocking a merge.

## Test review

Verify that tests exercise the claimed behavior and relevant failure paths, use realistic inputs and environments, remain deterministic, and would fail without the change. Identify missing evidence without promoting it to a finding unless the evidence threshold is met.

## Finding calibration

Use repository severity when defined; otherwise use `P0` for immediate catastrophic security, availability, or data impact; `P1` for likely serious defects, vulnerabilities, contract breaks, or unsafe rollouts; `P2` for material correctness, test, performance, or operational weaknesses; and `P3` for bounded, non-blocking improvements. State confidence separately. Disconfirm candidates before reporting them, and do not report style-only findings.

### Example finding

**P1 — Enforce tenant ownership before serving report downloads**

- **Location:** `app/reports.py`, `download_report`.
- **Trigger:** An authenticated user from tenant A requests a known report ID owned by tenant B.
- **Consequence:** The handler returns tenant B's report, bypassing tenant isolation.
- **Evidence:** The existing details path calls `get_report(report_id, user.tenant_id)`, while the new download path calls `report_repository.get(report_id)` and checks only that a user exists; no cross-tenant test covers the handler.
- **Smallest remediation:** Reuse the tenant-scoped helper (or enforce equivalent ownership) before returning the file, and add a cross-tenant regression test.

## Coverage limits

For oversized, generated, binary, dependency-heavy, or incomplete PRs, state the reviewed subset, unreviewed surface, and next highest-value review step. Inspect source and generation paths where available; otherwise report the limit and lower confidence rather than claiming complete coverage.

## Report contract

Follow the report order in [the skill's output contract](../SKILL.md#output). Order findings by severity and then confidence. Each finding contains a concise imperative title, location, trigger, consequence, evidence, and smallest remediation. Use `No findings.` when none meet the threshold.

## Review response quality

Explain why each finding matters, distinguish requirements from suggestions, remain respectful, and keep one concern per finding.

### Actionable recommendations

Include recommendations that help the user make a decision. Cite the relevant location or explain the scope of a system-wide observation, connect the observed behaviour to its impact, and offer a bounded recommendation or focused question. Explain the cost or trade-off when proposing an alternative. Use plain, collaborative language that makes the reasoning easy to discuss within the harness response.

Distinguish required changes, non-blocking suggestions and questions. A required change must be supported by a finding; an unanswered question is not proof of a defect. Specific acknowledgement of a sound design decision can be useful when it explains why the trade-off is appropriate. Do not manufacture concerns or praise to fill a quota.

### Explain the leadership judgement

Briefly explain the leadership judgement exercised by a specific observation in this review, such as reasoning across system boundaries, prioritising delivery risk or helping a team make a trade-off. Where useful, suggest a next question or action that would deepen the user's understanding or help resolve a decision.

Integrate this explanation into the response's leadership perspective, grounded in the reviewed evidence and reasoning. Attribute leadership impact to the user only when their actual actions and outcomes are known. Keep the entire review and development guidance in the current harness conversation.
