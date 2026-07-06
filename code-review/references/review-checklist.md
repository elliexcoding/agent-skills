# Code Review Checklist

Use this checklist for pull requests, branch diffs, commits, patches, or
selected files. It is intentionally risk-focused: prioritize issues that can
cause bugs, regressions, security problems, operational incidents, or expensive
future maintenance.

## Correctness

- Does the change solve the stated problem?
- Is the previous behavior preserved where it should be?
- Are edge cases handled: empty input, missing data, duplicates, invalid data,
  large payloads, partial failure, retries, timeouts, and concurrency?
- Are error paths explicit, observable, and actionable?
- Are invariants enforced at the right boundary?
- Are date, time zone, locale, encoding, precision, overflow, and ordering
  assumptions safe?

## Tests

- Is there coverage for the behavior being added or changed?
- Would a test fail without the fix?
- Are important error paths and edge cases covered?
- Do tests use stable behavior rather than brittle implementation details?
- Are fixtures realistic enough to catch the intended issue?
- Are slow, flaky, environment-dependent, or destructive tests isolated?

## API And Compatibility

- Are public APIs, CLI flags, configuration keys, schemas, events, files, and
  serialized formats compatible with existing users?
- Are breaking changes intentional and documented?
- Are migrations forward-compatible and rollback-aware?
- Are defaults safe for existing deployments?
- Are deprecations, feature flags, and version gates handled consistently?

## Security And Privacy

- Are authentication and authorization checks preserved?
- Are tenant, workspace, account, role, and ownership boundaries enforced?
- Are inputs crossing trust boundaries validated or constrained?
- Are SQL, shell, path, URL, HTML, template, regex, and deserialization paths
  protected from injection or resource abuse?
- Are secrets, tokens, credentials, private keys, and personal data excluded
  from code, logs, errors, tests, screenshots, and documentation?
- Are dependency additions necessary, maintained, and from trusted sources?

## Maintainability

- Does the structure match nearby code and project conventions?
- Are names specific enough to explain intent?
- Is the control flow easy to follow?
- Are responsibilities focused and boundaries clear?
- Is duplication removed only when it represents shared knowledge?
- Are abstractions justified by real variation or complexity reduction?
- Are comments used to explain non-obvious intent rather than restating code?

## Performance And Scalability

- Does the change add unbounded loops, memory growth, buffering, retries, or
  polling?
- Does it introduce N+1 database, filesystem, network, or service calls?
- Does it block an event loop or async executor?
- Are caches invalidated correctly and bounded where needed?
- Are large inputs streamed, paginated, chunked, or constrained?
- Is the performance impact measured when the change is performance-sensitive?

## Operations

- Are logs, metrics, traces, and errors useful for diagnosing failures?
- Do logs avoid sensitive data?
- Are rollout, rollback, migration, and backfill steps clear?
- Are failure modes safe and recoverable?
- Are external service, filesystem, network, and database assumptions explicit?
- Are config changes documented with safe defaults?

## Documentation

- Are README, API docs, examples, runbooks, architecture notes, or changelogs
  updated when behavior changes?
- Is new behavior discoverable for users and operators?
- Are limitations, migration steps, and compatibility notes documented where
  maintainers expect them?

## Review Calibration

- Prefer one precise high-impact finding over many weak comments.
- Avoid blocking on taste unless it affects comprehension or consistency.
- Ask a question when intent is unclear, but state the suspected risk.
- If the issue is hypothetical and low impact, mark it as non-blocking.
- If no issues are found, say that directly and identify any residual test or
  context gaps.
