# Review Pull Request Skill Design

## Objective

Create a standalone `review-pull-request` skill for an L5-equivalent engineer
performing general pull-request reviews. The skill must find material defects,
security issues, compatibility risks, and operational hazards while providing
deeper guidance for Python, Rust, Kubernetes, and Terraform changes.

The skill must be read-only. It may recommend an approve, comment, request
changes, or inconclusive verdict, but it must not publish review comments,
submit a verdict, edit source, or mutate cloud CI state.

## Scope

The skill covers pull requests in any language or stack. It provides a general
review workflow and conditionally loads specialist references for:

- Python
- Rust
- Kubernetes
- Terraform
- application security and software supply-chain risk

The existing `code-review` skill remains unchanged. Deprecating it may be
considered only after the new skill has been exercised on real pull requests
and shown to cover the older skill's use cases. Deprecation is not part of this
change.

## Repository Structure

Create one top-level skill:

```text
review-pull-request/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── review-playbook.md
    ├── python.md
    ├── rust.md
    ├── kubernetes.md
    ├── terraform.md
    ├── security.md
    └── source-notes.md
```

`SKILL.md` contains only the core workflow, evidence standard, CI policy,
severity calibration, reference-routing rules, and output contract. Detailed
domain checks live in the relevant reference so unrelated material is not
loaded. No scripts or assets are needed because the workflow is judgment-heavy
and should use repository-native tools.

Update the repository skill catalog to include `review-pull-request` without
marking `code-review` as deprecated.

## Review Workflow

1. Establish the PR objective, acceptance criteria, base and head revisions,
   repository instructions, and changed-file inventory.
2. Inspect the PR description, linked context, dependency changes, and existing
   CI results without changing remote state.
3. Classify risk and identify the architectural main path before reviewing
   line-level details.
4. Review the complete diff and enough surrounding implementation, call sites,
   configuration, documentation, and tests to understand the change.
5. Load only the specialist references relevant to the changed technologies.
6. Trace each candidate issue from a reachable trigger through the affected
   path to a concrete consequence. Search for guards, tests, or caller
   guarantees that disprove it before reporting it.
7. Run targeted local checks only when they can confirm or disprove a concrete
   concern or fill an important evidence gap.
8. Produce the read-only review report defined below.

The workflow reviews tests as production-quality code. Passing CI is evidence,
not proof that the change or its tests are correct.

## CI and Local Validation Policy

The default is CI-first and evidence-driven:

- Read existing CI status, check summaries, and relevant failure logs when
  available.
- Never trigger, rerun, approve, cancel, or otherwise mutate cloud CI jobs.
- Do not run a blanket local test suite merely to duplicate green CI.
- Run a targeted local test, reproduction, static check, or build only when it
  distinguishes a concrete concern from speculation or covers a material CI
  gap.
- Report every local command actually run and its result. State why an
  important check was not run and what uncertainty remains.

## Review Standard

The general lens covers:

- correctness and edge cases
- security, privacy, and trust boundaries
- API, schema, data, and configuration compatibility
- concurrency, error handling, resource management, and partial failure
- performance and scalability
- observability, rollout, rollback, and operational safety
- maintainability, design complexity, documentation, and PR scope
- test quality and whether tests would detect the claimed regression

The review examines every changed line within the declared scope, but spends
the most effort on high-impact and uncertain paths. Large, incoherent,
generated, binary, or dependency-heavy changes receive explicit coverage
limits rather than a false claim of completeness.

### Specialist Lenses

- **Python:** typing and data shapes; async, cancellation, and blocking work;
  exception and resource handling; packaging and imports; serialization,
  injection, and runtime edge cases.
- **Rust:** ownership and lifetimes; unsafe and FFI invariants; panic, drop, and
  cancellation behavior; concurrency; feature flags and semver; allocation and
  hot-path costs.
- **Kubernetes:** RBAC and workload identity; pod and container security;
  secrets; probes and resources; scheduling and disruption; networking;
  rollout safety; selectors and API compatibility.
- **Terraform:** destructive replacement; state and drift; lifecycle rules;
  provider and module versions; IAM and secret exposure; import and move
  semantics; rollback feasibility.
- **Security:** authentication and authorization; injection, SSRF, path, and
  deserialization risks; cryptography and sensitive data; dependency and
  supply-chain exposure.

## Finding and Verdict Calibration

A finding requires:

1. A violated requirement, invariant, or defensible engineering expectation.
2. A reachable trigger or state.
3. A precise code or configuration path.
4. A concrete and material consequence.
5. A bounded remediation or proof obligation.

Each finding has separate severity and confidence. Confirmed or strongly
supported issues are findings. Plausible but unsupported possibilities belong
under open questions or residual risks. Personal style preferences and nits are
not findings.

Use repository-defined severity when available. Otherwise use:

- `P0`: immediate catastrophic security, availability, or data impact.
- `P1`: likely serious defect, vulnerability, data loss, contract break, or
  unsafe rollout that should block merge.
- `P2`: material correctness edge case, maintainability trap, performance
  issue, test gap, or operational weakness that should normally be addressed
  before merge.
- `P3`: bounded, non-blocking improvement with low near-term impact.

The skill recommends one verdict without submitting it:

- `APPROVE`
- `COMMENT`
- `REQUEST CHANGES`
- `INCONCLUSIVE`

A clean review does not imply certainty. The verdict must reflect remaining
coverage and evidence gaps.

## Output Contract

The report uses this order:

1. Findings, ordered by severity and then confidence.
2. Recommended verdict and confidence.
3. Review coverage, including files and risk areas examined.
4. CI and local-validation evidence.
5. Open questions.
6. Residual risks and limitations.

Each finding includes a concise imperative title, precise location, trigger,
consequence, evidence, and smallest practical remediation. If there are no
findings, the report states that directly. The skill must not invent findings
to appear thorough.

## Missing Information and Failure Handling

When PR metadata, linked requirements, CI logs, repository instructions, or
surrounding code are unavailable, state exactly what is missing and how it
limits confidence. Continue with available evidence unless the missing context
prevents a responsible verdict; in that case recommend `INCONCLUSIVE`.

For an oversized PR, identify the reviewed subset, unreviewed surface, and the
next highest-value review step. For generated or binary changes, review the
source and generation path when available and disclose what could not be
inspected.

## Validation Strategy

Develop the skill with a RED-GREEN-REFACTOR cycle using fresh, isolated review
scenarios:

1. A mixed Python and Terraform PR with an application defect and destructive
   infrastructure risk.
2. A Rust and Kubernetes PR with concurrency or unsafe assumptions and rollout
   hazards.
3. A benign PR that tests whether the reviewer fabricates findings.
4. A CI scenario that tests read-only evidence gathering and prohibits cloud
   job mutation.
5. A large or incomplete PR that tests honest coverage and confidence.

First record baseline behavior without the skill. Then repeat the same
scenarios with the skill, identify gaps or rationalizations, revise the skill,
and rerun until the output satisfies the review contract. Keep scenario
artifacts outside the skill unless a reusable reference is demonstrably needed.

Finally:

- validate the skill structure and frontmatter with the repository's skill
  validation tooling;
- verify every reference route and `agents/openai.yaml` metadata;
- inspect the complete diff;
- run an independent final review of the finished skill.

These evaluations must not access production systems or mutate cloud state.

## Professional Basis

The source notes will cite primary guidance, including Google's Engineering
Practices for review sequencing, code health, test inspection, and comment
quality; GitHub documentation for pull-request reviews and status checks; OWASP
secure-code-review guidance; and official Python, Rust, Kubernetes, and
Terraform documentation for the specialist lenses.
