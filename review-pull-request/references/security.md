# Security Review Lens

Use this focused lens when the change touches a trust boundary or security
control. Ask observable failure questions against the supplied diff and nearby
context; it complements, rather than replaces, the general diff review.

For every security finding, trace **source → transformations → guards → sink →
consequence**. Name the attacker-controlled or privileged source, each
meaning-changing transformation, the missing or bypassed guard, the concrete
sink, and the observable confidentiality, integrity, availability, or
authorization consequence. If a link is not evidenced, state a bounded
question or residual risk instead of a finding. (`OWASP-SECURE-REVIEW`,
`OWASP-REVIEW-GUIDE`)

This lens reviews the supplied PR and necessary context; it is not an
exhaustive repository audit. Route a requested full repository or deep
security audit to the dedicated security-scan workflow.

## Assets, actors, and boundaries

- Which assets, identities, data classifications, operations, and availability
  properties can this change expose or alter? Which human, service, workload,
  CI, or deployment identity can invoke it?
- What are the entry points and trust boundaries: request fields, queue events,
  files, URLs, configuration, environment, dependency metadata, or identity
  tokens? Can a value cross one of them and gain authority or a new
  interpretation?
- Does a role, token, service account, endpoint, workflow, or deployment
  identity gain, delegate, or retain privilege beyond the stated operation?

## Identity, authority, and ownership

- Does authentication bind the actual caller, and does each sensitive action
  authorize that caller at the object, tenant, account, and operation scope?
  Can an authenticated caller substitute another tenant's identifier or use a
  broader internal helper to bypass ownership?
- Do defaults fail closed when identity, policy data, ownership, or a required
  guard is absent or errors? Can a confused deputy use the service's authority
  to access a resource the caller could not access directly?
- Are authorization decisions repeated after redirects, asynchronous handoff,
  cache lookup, retry, or resource indirection when the protected object or
  principal can change?

## Untrusted interpretation and execution

- Can data from an untrusted source be transformed into SQL, a shell command,
  template, path, URL, redirect target, query, or downstream request whose
  interpreter grants it different meaning? Is the relevant allowlist,
  parameterization, canonicalization, or containment guard applied before the
  sink?
- Can a server-side request reach internal, link-local, metadata, or otherwise
  unauthorized network targets after parsing, redirects, DNS resolution, or
  proxy handling? Can a redirect send a user or credential to an untrusted
  destination?
- Can deserialization, archive extraction, XML/format parsing, or multiple
  parsers interpret input differently, execute code, escape an extraction
  root, or consume unbounded resources?

## Secrets, privacy, and cryptography

- Could credentials, tokens, keys, personal data, or sensitive business data
  enter source control, build output, logs, traces, errors, metrics, URLs,
  client responses, state, or backups? Are collection, access, retention, and
  deletion behavior consistent with the stated purpose?
- Are encryption, signing, randomness, nonce handling, key selection,
  rotation, revocation, and verification performed at the intended boundary?
  Can a downgrade, predictable value, stale key, or unchecked signature change
  the result?

## Stateful and availability controls

- Can concurrent requests, retries, retries after a timeout, or asynchronous
  workers race a check, duplicate an effect, replay a credential or event, or
  violate an idempotency boundary? Which persistent key or transaction makes
  the operation safe?
- Can attacker-controlled work exhaust CPU, memory, storage, file handles,
  queue capacity, connections, or downstream quotas? Are size limits, rate
  limits, quotas, timeouts, cancellation, and backpressure enforced at the
  relevant boundary?

## Dependencies and delivery chain

- Do changed dependencies, lockfiles, registries, checksums, signatures,
  provenance, install/build hooks, generated artifacts, or package scripts
  allow an unreviewed party to execute code or alter the shipped result?
- Are CI workflow permissions, action/image revisions, secrets, artifacts,
  approvals, and deployment credentials limited to the job and environment
  that need them? Can an untrusted contribution influence a privileged build,
  artifact, release, or deployment identity?
