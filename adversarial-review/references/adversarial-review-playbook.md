# Adversarial Review Playbook

Use this playbook selectively. Rank lenses by the change's impact, plausibility
of failure, and uncertainty; do not mechanically apply every prompt.

## Build The Challenge Set

Turn requirements and artifacts into explicit claims:

| Source | Example claim | Useful challenge |
| --- | --- | --- |
| Acceptance criterion | Requests are idempotent | Retry after a partial write |
| Public API | Existing clients remain compatible | Send old payloads and defaults |
| Migration | Rollout preserves data | Interrupt, roll back, and version-skew |
| Test | Invalid input is rejected | Find malformed input the fixture omits |
| Completion note | All callers were updated | Search imports, dispatch, and reflection |
| Refactor claim | Behavior is unchanged | Compare externally visible invariants |

Rank candidate challenges with a simple qualitative score:

- Impact: What happens if the claim is false?
- Plausibility: Is the trigger reachable in realistic use?
- Uncertainty: How weak is the current evidence?

Start with the highest combined risk. Three strong challenges are more valuable
than twenty speculative observations.

## Challenge Lenses

### Intent And Requirements

- Does the change solve the user's actual need rather than a narrower proxy?
- Are acceptance criteria missing negative, permission, lifecycle, or rollback
  requirements?
- Does a locally correct implementation violate a system-level invariant?
- Is a stated non-goal actually necessary for safe operation?

### Inputs And State

- Exercise empty, null, malformed, duplicate, stale, unordered, oversized,
  boundary, Unicode, and partially valid inputs where applicable.
- Trace first use, repeated use, restart, retry, cancellation, timeout, partial
  completion, and cleanup.
- Challenge state-machine transitions that arrive out of order or repeat.
- Look for time-of-check/time-of-use gaps and stale caches.

### Contracts And Compatibility

- Check old and new clients, stored data, serialized formats, CLI flags,
  environment variables, events, and defaults.
- Trace all callers and implementations of changed interfaces.
- Test whether optional fields, error types, ordering, timing, or side effects
  are part of the practical contract even when undocumented.
- For migrations, inspect expand/contract sequencing, mixed-version operation,
  reversibility, backfill behavior, and data preservation.

### Failure And Operations

- Inject or reason through dependency timeout, rate limit, malformed response,
  partial success, retry, and permanent failure.
- Check idempotency, transaction boundaries, compensation, and rollback.
- Look for unbounded CPU, memory, I/O, queues, recursion, cardinality, or fanout.
- Verify that logs, metrics, traces, and alerts reveal failure without leaking
  secrets or sensitive data.
- Ask whether feature flags, deploy ordering, and rollback work under version
  skew.

### Security And Misuse

- Identify assets, actors, entry points, trust boundaries, and privileged sinks.
- Trace untrusted data from source through validation and transformation to
  database, filesystem, renderer, shell, network, logger, or authorization use.
- Challenge authentication, authorization, tenant isolation, object ownership,
  secret handling, and least privilege.
- Consider spoofing, tampering, repudiation, information disclosure, denial of
  service, and elevation of privilege where relevant.
- Form one realistic misuse case: how could a malicious or merely confused user
  make the feature do something it was not intended to do?

Do not execute exploits against live or unauthorized targets. Prefer static
proof, unit-level reproduction, local fixtures, or a clearly authorized test
environment.

### Concurrency And Distribution

- Interleave reads, writes, retries, cancellation, and duplicate delivery.
- Challenge assumptions about ordering, uniqueness, atomicity, clock accuracy,
  network reliability, and exactly-once execution.
- Inspect lock scope, async blocking, races, deadlocks, starvation, and lost
  updates.
- Consider process crash or leader change between side effects.

### Design And Code Health

- Check whether responsibilities remain cohesive and dependencies point toward
  stable abstractions.
- Challenge substitutions that violate caller expectations, broad interfaces
  that force irrelevant dependencies, and abstractions that leak implementation
  details.
- Apply SOLID and similar principles only when they expose concrete coupling,
  change amplification, invalid states, or testability problems. Do not report
  principle names as findings by themselves.
- Ask whether complexity, duplication, or indirection increased without buying
  a measurable capability.

### Tests And Evidence

- Would each important test fail if the claimed behavior were broken?
- Do mocks bypass the real parser, serializer, authorization rule, transaction,
  or integration boundary under review?
- Are assertions checking outcomes and invariants rather than implementation
  details?
- Are negative, boundary, concurrent, migration, and failure-path tests
  proportionate to risk?
- Do test commands cover the changed package and configuration actually shipped?
- Are skipped, flaky, snapshot, or golden tests hiding meaningful drift?

## Disconfirm A Candidate Finding

Before reporting an issue:

1. Trace the exact trigger to the consequence.
2. Search for caller guarantees, validation, invariants, feature gates, and
   deployment constraints that block the path.
3. Read relevant tests and documentation.
4. Run a narrow reproduction when safe and practical.
5. Try the expected fix or guard mentally against the same scenario.
6. Downgrade to an unverified risk if decisive evidence is unavailable.

Avoid duplicate findings with the same root cause. Report the root defect and
list representative consequences.

## Review Packet For An Independent Agent

Provide:

- Objective and acceptance criteria.
- Repository instructions and safety constraints.
- Review scope and base revision.
- Raw diff, changed files, test output, and relevant design artifacts.
- Available commands and environment limitations.

Withhold until after the independent pass:

- The implementer's confidence statement or chain of reasoning.
- Suspected bugs and expected findings.
- Proposed fixes that could anchor the reviewer.
- Another reviewer's conclusions.

After the independent pass, provide the PR description or completion report and
ask the reviewer to challenge any additional claims it contains.

## Stop Conditions

Stop widening the review when:

- The highest-risk claims have proportionate evidence.
- New hypotheses are lower impact or duplicate established root causes.
- Further proof requires unavailable access or unsafe actions.
- The review boundary has been reached.

State the residual risk rather than implying exhaustive coverage.
