# Rust specialist workflows

Read the section matching the changed behaviour: async/concurrency, unsafe/FFI,
debugging or performance. Tool examples are conditional, not a command queue.

## Async And Concurrency

- Identify the runtime before changing async code (`tokio`, `async-std`,
  `smol`, custom executor, or no runtime).
- Do not block async executors with CPU-heavy work, file I/O, or synchronous
  locks; use runtime-specific blocking APIs where appropriate.
- Make cancellation and timeout behaviour explicit for long-running tasks.
- Check `Send`, `Sync`, and `'static` requirements at task boundaries.
- Prefer message passing, narrow lock scopes, and immutable sharing. When using
  `Arc<Mutex<_>>`, document or test the concurrency behaviour that matters.
- Avoid holding a lock across `.await`.

## Unsafe, FFI, And Low-Level Code

- Avoid `unsafe` unless it is required for FFI, performance, or low-level API
  contracts.
- Keep unsafe blocks small and local.
- Document each unsafe block with the invariants that make it sound.
- Add tests that exercise boundary conditions around unsafe code.
- Use `miri`, sanitisers, or platform-specific checks when available and
  relevant.

## Debugging Workflow

1. Reproduce the failure with the narrowest command possible.
2. Capture exact symptoms: error text, backtrace, failing test, input, feature
   flags, target triple, and environment variables.
3. Reduce the failing path:
   - run a single test: `cargo test <name> -- --nocapture`
   - enable backtraces: `RUST_BACKTRACE=1 cargo test <name>`
   - inspect features: `cargo tree -e features`
   - inspect dependency duplication: `cargo tree -d`
4. Instrument carefully:
   - prefer existing `tracing`, `log`, or test assertions
   - remove temporary debug output before finalising
5. Fix root cause rather than symptoms.
6. Add or update a regression test that fails without the fix.

## Performance Work

- Measure before optimising.
- Start with realistic workloads and representative inputs.
- Use existing benchmarks first; otherwise add focused Criterion benchmarks
  when the change needs repeatable measurement.
- Check algorithmic complexity, allocation volume, clone frequency, lock
  contention, and async scheduling before micro-optimising.
- Keep performance changes readable and backed by before/after data.
