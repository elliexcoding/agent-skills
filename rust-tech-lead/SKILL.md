---
name: rust-tech-lead
description: Implement or design Rust APIs and crate changes, or investigate Rust performance. For review-only or failing-test requests, use the focused review or debugging skill.
---

# Rust Technical Lead

Deliver the requested Rust change within the crate's existing contracts. Keep
ownership, error and API boundaries clear and preserve edition, MSRV, features
and workspace conventions unless the task explicitly changes them.

## Establish relevant constraints

Read the affected package and workspace manifests, toolchain/configuration and
repository instructions. Inspect callers and tests for the changed path. Read
other crate or architecture documentation when the change crosses its boundary;
do not require a full workspace tour for a local edit.

Confirm crate type, supported targets, default/optional features, async runtime
and local error/logging conventions where they affect the work. Use targeted
search; `cargo metadata --no-deps` and `cargo tree -e features` can resolve
workspace and feature questions when needed.

## Rust-specific decisions

- Preserve public ownership, lifetime and trait-bound contracts. Avoid adding
  generics or macros without a concrete reuse or type-safety benefit.
- Use existing domain and error types. Keep recoverable failures in `Result`;
  an `unwrap` or `expect` in a production path needs a demonstrable invariant.
- Match dependency and error-handling conventions; do not introduce `thiserror`,
  `anyhow` or a new runtime merely as a style preference.
- Gate APIs and imports consistently with optional dependencies. Check supported
  feature combinations and targets; not every workspace supports all features
  together or compiles with no default features.
- Check cancellation, task ownership, `Send`/`Sync` and lock lifetimes at async
  boundaries. Avoid blocking the executor or holding a lock across `.await`.
- Keep unsafe code local, with soundness invariants documented and exercised at
  relevant boundaries. Use Miri or sanitiser evidence where it answers a real
  safety concern; do not assume it proves all paths sound.

For async/concurrency, unsafe/FFI, runtime debugging or performance work, read
only the matching section of [Rust workflows](references/rust-workflows.md).
For review-only or failing-test requests, prefer the available focused review
or debugging skill instead of stacking complete workflows.

## Validation and delivery

Use repository-documented checks. Start with the affected package, test, feature
and target; run required broader checks and broaden further for a demonstrated
risk. Check formatting when code changes, documentation when public examples
change, and supported feature combinations when feature-gated paths change.
Do not default to an all-features/full-workspace/doc/audit command sweep.

For a bug fix, use a regression test that distinguishes the failure from the
correct behaviour when practical. For performance work, compare representative
before/after measurements before claiming improvement. Keep temporary probes
out of the patch.

Report the behaviour delivered, consequential API/feature/target decisions and
validation results. State omitted checks and their practical limitations. Carry
implementation requests through relevant verification rather than stopping at
an initial patch.
