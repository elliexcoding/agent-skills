# Rust Review Lens

Use this lens after the core workflow has identified changed Rust files,
Cargo/package behavior, or Rust runtime behavior. Ask observable failure
questions; do not require a particular crate or runtime.

## Ownership and safety

- Do ownership, borrowing, lifetimes, and interior-mutability choices preserve
  the intended aliasing and mutation rules? Is an unnecessary clone hiding a
  lifetime, ownership, or hot-path cost problem?
- For every new or changed `unsafe` block, is there a written safety invariant
  stating the assumptions it relies on and why safe callers cannot violate
  them? Does the implementation uphold that invariant for raw pointers,
  aliasing, initialization, pinning, FFI, layout, and unwind boundaries?
  (`RUST-UNSAFE`, `RUST-UB`)

## Concurrency and failure behavior

- Are `Send` and `Sync` requirements satisfied at actual spawn and API
  boundaries? Can lock ordering, interior mutability, atomics, channels, or
  `Drop` create a race, deadlock, lost wake-up, or shutdown hazard?
- Is a synchronous guard retained across `.await`, or does cancellation leave a
  lock, channel, task, or partial update in the wrong state? Is blocking work
  isolated from the executor when it can stall async progress?
- Are `Result` values propagated with useful context and without accidental
  panic? Are panic boundaries, cleanup, retries, and partial-state recovery
  compatible with the operation's durability and idempotency requirements?

## Public surface and cost

- Do public APIs preserve their documented semantics across trait coherence,
  feature combinations, MSRV, semver, and crate metadata? Are feature-gated
  paths tested or explicitly unsupported? (`RUST-API`)
- Do allocation patterns, copies, bounds checks, iterator behavior, and work in
  hot paths change latency, memory use, or complexity at realistic sizes?

## Evidence

- Do unit, integration, and documentation tests cover changed behavior and
  errors? Where the risk warrants it, is there property, concurrency, Miri,
  loom, or feature-matrix evidence that exercises the relevant invariant?
- For `unsafe`, FFI, concurrent, or feature-sensitive changes, does the
  available evidence test the stated invariant and the combinations callers can
  actually use, rather than only a happy path?
