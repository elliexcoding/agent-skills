---
name: rust-code-review
description:
  Review Rust changes for correctness, maintainability, tests, and idiomatic
  project fit. Use when asked to review Rust code, Rust diffs, crates, PRs, or
  unsafe/concurrency-sensitive Rust changes.
---

# Rust Code Review

## Purpose

Find concrete risks in Rust changes before style advice. Prefer small,
actionable findings tied to behaviour, safety, API contracts, maintainability,
or missing verification.

## Companion Skills

- Use `debug-failing-tests` when tests fail, reproduction is unclear, or the
  review depends on proving a suspected runtime failure.
- Use this skill before broader refactoring advice; review should establish
  whether the current change is correct.

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
3. Run targeted checks when practical:

   ```bash
   cargo fmt --check
   cargo clippy --all-targets --all-features -- -D warnings
   cargo test --all-targets --all-features
   ```

4. If the workspace uses different commands, follow the repo's documented
   commands instead.
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
