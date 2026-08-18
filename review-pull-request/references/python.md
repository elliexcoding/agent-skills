# Python Review Lens

Use this lens after the core workflow has identified changed Python files or
runtime/package behavior. Ask observable failure questions; do not require a
particular framework or library.

## Data and failure behavior

- Can an input at a trust boundary have the wrong shape, missing fields,
  unexpected nulls, duplicate keys, or values outside the supported range?
- Does validation occur before data is used for authorization, persistence, or
  external effects, and does the resulting error preserve the intended API
  contract?
- Can shared mutable values, mutable default arguments, class attributes, or
  cached objects leak state across calls, requests, or tenants?
- Do default values change the semantics of absence versus an explicit value?
  Are decimal, float, timezone, daylight-saving, monotonic-clock, and
  serialization choices correct at their boundary?
- Does the exception taxonomy distinguish expected, recoverable, and programmer
  failures, with expected failures caught at the narrowest useful type? Do
  cleanup, context managers, retries, and partial side effects leave a
  recoverable state and preserve the original failure where appropriate?

## `asyncio` and typing

- Does cancellation propagate rather than get converted into success, a retry,
  or a silently abandoned task? Are task groups, timeouts, child-task lifetime,
  and cleanup behavior correct on success, failure, and cancellation?
  (`PY-ASYNCIO`)
- Could synchronous CPU, filesystem, database, or network work block the event
  loop? Does a background task retain ownership of resources long enough to
  complete or be cancelled deliberately?
- Do annotations narrow values before use and express the actual generic,
  protocol, and variance contract? Could `Any`, an unchecked cast, an
  untyped dependency, or a dynamically assembled value bypass that contract?

## Packaging and boundaries

- Can an import or module-level initializer perform surprising I/O, mutation,
  registration, or configuration-dependent work? Are optional dependencies,
  package metadata, CLI entry points, and supported Python versions consistent
  with the changed behavior?
- At SQL, shell, path, URL, template, archive, XML, deserialization, secret,
  and log boundaries, can untrusted data change interpretation, escape its
  allowed scope, disclose sensitive values, or exhaust resources?
  (`PY-SECURITY`, `PY-SUBPROCESS`)
- Is pickle or equivalent unsafe deserialization reachable from untrusted or
  insufficiently authenticated data? (`PY-PICKLE`)

## Cost and test evidence

- Does a loop create repeated I/O or N+1 calls, accidental quadratic work,
  unnecessary materialization of generators, or an unbounded collection in a
  request, job, or service process?
- Does pytest collect and execute the intended tests? Do tests exercise normal
  and boundary cases with parametrization where it clarifies the contract,
  async success/failure/cancellation when relevant, and fixture lifetimes that
  cannot leak state?
- Would mocks still permit the production boundary to fail differently? Do
  package/install and CLI checks cover the artifact users actually consume?
