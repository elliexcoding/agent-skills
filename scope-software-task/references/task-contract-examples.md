# Task Contract Examples

Use these examples to calibrate depth and decomposition. Adapt the structure to
repository evidence; do not copy requirements that do not apply.

## Contents

1. Compact bug fix
2. Standard feature change
3. Extended schema migration

## 1. Compact Bug Fix

### Request

"Stop the CLI from crashing when the config file is empty."

### Contract

- **Outcome:** An empty configuration file produces the documented default
  configuration or a normal user-facing validation error instead of a panic.
- **Current behaviour:** Trace the config loader and reproduce the crash with
  the smallest empty-file fixture.
- **In scope:** Empty files and the loader's existing error boundary.
- **Non-goals:** Redesigning the configuration format or changing unrelated
  validation messages.
- **Invariants:** Existing valid files parse identically; malformed non-empty
  files keep their documented behaviour.
- **Acceptance criteria:** The reproduction no longer panics; valid and malformed
  fixtures retain their established results.
- **Verification:** Focused loader test plus the repository's narrow CLI test.
- **Uncertainty:** Whether the documented contract requires defaults or an
  error; resolve from docs and existing zero-value handling before editing.

### Work Unit

One unit is sufficient once the expected empty-file behaviour is established:
add a characterization or regression test, make the minimal correction, and run
the focused checks.

## 2. Standard Feature Change

### Request

"Cache successful user-profile reads."

### Contract

- **Outcome:** Repeated reads of an unchanged profile avoid the database while
  preserving API, authorization, and failure behaviour.
- **Current behaviour:** Trace the endpoint through authorization, service, and
  repository layers; locate the established cache abstraction and tests.
- **In scope:** Successful reads, expiration, update invalidation, cache failure,
  tests, and required observability.
- **Non-goals:** Negative caching, a new cache provider, public API changes, or
  unrelated user-service cleanup.
- **Invariants:** Authorization executes for every request; cache failure falls
  back safely; cached data excludes secrets and internal metadata.
- **Acceptance criteria:**
  - The first authorized read accesses the database.
  - A repeated read returns the same representation without another database
    access.
  - An update prevents stale data from being served.
  - Expiration causes a fresh database read.
  - Cache unavailability does not make the endpoint unavailable.
  - An unauthorized caller cannot infer whether a cached profile exists.
- **Verification:** Focused service tests, endpoint integration tests, failure
  injection for cache unavailability, and standard lint/type checks.
- **Uncertainty:** Cache lifetime and consistency expectation require an owner
  decision if no existing policy or neighbouring implementation establishes
  them.

### Work Units

1. Confirm current behaviour, cache conventions, and consistency requirements.
2. Add characterization coverage for API and authorization invariants.
3. Implement one end-to-end successful-read cache path.
4. Add invalidation, expiration, and cache-failure behaviour.
5. Verify observability, the full acceptance set, and the final diff.

Do not split handler, service, cache, and tests among parallel agents before the
cache contract is stable.

## 3. Extended Schema Migration

### Request

"Replace `full_name` with separate `given_name` and `family_name` columns."

### Decision Gates

Resolve before implementation:

- How existing names are split, including ambiguous single-token and
  locale-dependent names.
- Whether either new field is nullable.
- Which API versions and downstream consumers still require `full_name`.
- Whether rollback must preserve writes made after the migration begins.

### Safe Decomposition

1. **Contract and inventory**
   - Identify database, API, event, analytics, export, and batch consumers.
   - Approve transformation, compatibility, and rollback semantics.
2. **Expand**
   - Add nullable columns or an equivalent backward-compatible representation.
   - Deploy without changing read or write behaviour.
3. **Dual write**
   - Populate both representations and measure divergence.
4. **Backfill**
   - Run a resumable, observable, rate-limited transformation.
   - Record ambiguous rows rather than silently corrupting them.
5. **Read transition**
   - Move bounded consumers after completeness and consistency checks pass.
6. **Contract**
   - Remove the old representation only after the compatibility window,
     rollback obligations, and dependent migrations are complete.

### Required Evidence

- Consumer inventory and owners.
- Transformation fixtures for representative and adversarial names.
- Backfill progress, error, and divergence metrics.
- Forward- and backward-compatibility tests.
- A rehearsed pause or rollback path at each phase.

Do not package expand, backfill, consumer cutover, and column removal into one
agent task or one irreversible release.
