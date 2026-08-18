# Review Playbook

## Review sequence

Review broad intent and acceptance criteria first, then trace the architectural main path. Inspect the complete available diff, changed tests, compatibility boundaries, and operational effects before forming findings.

## Risk triage

Prioritize impact, reachability, reversibility, blast radius, and uncertainty. Increase scrutiny where the change crosses authentication, authorization, data ownership, network, deployment, persistence, or other trust boundaries.

## General lenses

Check correctness; data handling; concurrency; errors and partial failure; API, schema, and configuration compatibility; performance; observability; rollout and rollback; maintainability; documentation; and scope. Treat tests as reviewed code, not proof by themselves.

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

Write the report in this exact order: findings; recommended verdict and confidence; review coverage; CI and local-validation evidence; open questions; residual risks and limitations. Order findings by severity and then confidence. Each finding contains a concise imperative title, location, trigger, consequence, evidence, and smallest remediation. Use `No findings.` when none meet the threshold.

## Comment quality

Explain why each finding matters, distinguish requirements from suggestions, remain respectful, and keep one concern per finding.
