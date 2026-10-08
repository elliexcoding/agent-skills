---
name: rust-code-review
description: Review Rust code for ownership, unsafe, concurrency and API risks. Use for Rust-focused reviews outside a PR review workflow.
---

# Rust Code Review

## Purpose

Find concrete risks in Rust changes before style advice. Prefer small,
actionable findings tied to behaviour, safety, API contracts, maintainability,
or missing verification.

Remain read-only unless fixes are requested. If `review-pull-request` is already
active, use its Rust reference instead of loading this second workflow.
Use `debug-failing-tests` only when a failure needs a separate diagnosis;
reproducing a defect during review does not authorise fixing it.

## Review Priorities

1. Correctness and edge cases.
2. Ownership, borrowing, lifetimes, and trait-bound complexity.
3. Error handling, panics, cancellation/drop behaviour, and resource cleanup.
4. Async, threading, locking, channels, atomics, and blocking calls.
5. `unsafe` blocks, FFI boundaries, aliasing, pinning, and invariants.
6. Public API shape, semver compatibility, feature flags, and crate metadata.
7. Allocation, cloning, copying, and avoidable work on hot paths.
8. Tests that prove behaviour, not just coverage.

## Workflow

1. Inspect the diff first, then read the surrounding code needed to understand
   intent.
2. Identify externally visible behaviour, invariants, and failure modes.
3. Inspect existing validation evidence. Run a targeted check when it resolves
   a concrete concern, selecting the affected package, test, feature and target.
4. Follow repository-required checks. Do not assume all features can be enabled
   together, all targets are available, or Clippy warnings must become errors.
5. Avoid broad rewrites unless the current design creates a concrete risk.
6. Treat missing tests as findings only when a realistic bug could escape.

## Output

Lead with findings, ordered by severity. Use file and line references when
available.

```text
Findings
- [severity] path:line - Concrete issue, impact, and suggested fix.

Open Questions
- Product or API intent that could change the recommendation.

Verification
- Commands run, or "not run" with a reason.
```

If there are no findings, say that clearly and mention any remaining test gaps
or residual risk.
