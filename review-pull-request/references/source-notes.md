# Source Notes

These primary sources provide professional grounding for review controls; they
are not infallible universal policy. Apply them to the repository's declared
requirements and versions. Do not turn version-specific guidance into a review
requirement unless the PR declares the relevant version.

## General review

### `PR-STANDARD`

[Google Engineering Practices: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) supports deciding whether a change improves the codebase and is ready to submit.

### `PR-LOOK-FOR`

[Google Engineering Practices: What to Look for in a Code Review](https://google.github.io/eng-practices/review/reviewer/looking-for.html) supports evaluating design, functionality, complexity, tests, naming, comments, style, and documentation.

### `PR-NAVIGATE`

[Google Engineering Practices: Navigating a CL in Review](https://google.github.io/eng-practices/review/reviewer/navigate.html) supports reviewing context and dependency order before relying on line-level changes.

### `PR-COMMENTS`

[Google Engineering Practices: Writing Code Review Comments](https://google.github.io/eng-practices/review/reviewer/comments.html) supports clear, respectful, actionable findings that explain impact.

### `GH-REVIEWS`

[GitHub Docs: About pull request reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/about-pull-request-reviews) supports distinguishing review feedback and review states from implementation evidence.

### `GH-STATUS`

[GitHub Docs: Status checks](https://docs.github.com/en/pull-requests/reference/status-checks) supports treating reported check state as evidence to inspect, not a substitute for review.

## Security

### `OWASP-SECURE-REVIEW`

[OWASP Secure Code Review Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secure_Code_Review_Cheat_Sheet.html) supports tracing trust boundaries, input handling, authorization, error handling, cryptography, and deployment controls.

### `OWASP-REVIEW-GUIDE`

[OWASP Code Review Guide 2.0](https://owasp.org/www-project-code-review-guide/assets/OWASP_Code_Review_Guide_v2.pdf) supports evidence-led review of implementation paths and their security consequences.

## Python

### `PY-SECURITY`

[Python documentation: Security considerations](https://docs.python.org/3/library/security_warnings.html) supports checking language and library security boundaries before relying on defaults.

### `PY-ASYNCIO`

[Python documentation: asyncio tasks](https://docs.python.org/3/library/asyncio-task.html) supports reviewing task lifetime, cancellation, timeout, and cleanup behavior.

### `PY-PICKLE`

[Python documentation: pickle](https://docs.python.org/3/library/pickle.html) supports treating untrusted pickle data as unsafe to deserialize.

### `PY-SUBPROCESS`

[Python documentation: subprocess security considerations](https://docs.python.org/3/library/subprocess.html#security-considerations) supports checking command construction and shell-invocation boundaries.

## Rust

### `RUST-UNSAFE`

[Rust Reference: unsafe](https://doc.rust-lang.org/reference/unsafe-keyword.html) supports requiring explicit safety invariants where unsafe operations are used.

### `RUST-UB`

[Rust Reference: behavior considered undefined](https://doc.rust-lang.org/reference/behavior-considered-undefined.html) supports reviewing unsafe code against Rust's undefined-behavior constraints.

### `RUST-API`

[Rust API Guidelines checklist](https://rust-lang.github.io/api-guidelines/checklist.html) supports reviewing public API consistency, documentation, testing, and compatibility expectations.

## Kubernetes

### `K8S-SECURITY`

[Kubernetes security checklist](https://kubernetes.io/docs/concepts/security/security-checklist/) supports reviewing cluster, workload, network, image, and secret security controls.

### `K8S-RBAC`

[Kubernetes RBAC good practices](https://kubernetes.io/docs/concepts/security/rbac-good-practices/) supports applying least privilege to identities, roles, bindings, and escalation-sensitive permissions.

### `K8S-POD-SECURITY`

[Kubernetes Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/) supports evaluating workload isolation controls against the declared policy level.

### `K8S-PROBES`

[Kubernetes probes](https://kubernetes.io/docs/concepts/workloads/pods/probes/) supports reviewing health checks as traffic and restart controls.

### `K8S-RESOURCES`

[Kubernetes resource management for pods and containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) supports reviewing requests and limits against scheduling and resource-exhaustion behavior.

### `K8S-DEPLOYMENTS`

[Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) supports reviewing rollout behavior, selectors, availability, and revision history.

## Terraform

### `TF-STYLE`

[Terraform style conventions](https://developer.hashicorp.com/terraform/language/style) supports reviewing configuration readability and module interface consistency.

### `TF-LIFECYCLE`

[Terraform lifecycle meta-arguments](https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle) supports reviewing replacement ordering, destruction safeguards, and drift-related tradeoffs.

### `TF-STATE-SENSITIVE`

[Terraform state and sensitive data](https://developer.hashicorp.com/terraform/language/manage-sensitive-data) supports reviewing state access, sensitive values, and disclosure paths.

### `TF-PROVIDERS`

[Terraform provider requirements](https://developer.hashicorp.com/terraform/language/providers/requirements) supports reviewing provider sources, versions, aliases, and compatibility evidence.

### `TF-VERSIONS`

[Terraform version constraints](https://developer.hashicorp.com/terraform/language/expressions/version-constraints) supports reviewing declared Terraform and provider compatibility ranges.

### `TF-LOCK`

[Terraform dependency lock file](https://developer.hashicorp.com/terraform/language/files/dependency-lock) supports reviewing locked provider selections and checksum integrity.

### `TF-REFACTOR`

[Terraform moved blocks](https://developer.hashicorp.com/terraform/language/block/moved), [import blocks](https://developer.hashicorp.com/terraform/language/block/import), and [removed blocks](https://developer.hashicorp.com/terraform/language/block/removed) support preserving state-address intent when refactoring managed infrastructure.

### `TF-PLAN`

[Terraform plan command](https://developer.hashicorp.com/terraform/cli/commands/plan) supports reviewing planned actions, unknown values, and target-environment context before apply.
