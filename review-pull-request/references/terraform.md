# Terraform Review Lens

Use this lens for Terraform configuration, modules, state migrations, lock
files, and supplied plan output. Ask observable failure questions; do not
assume a provider's behavior from resource naming alone.

Do not claim that a resource will be replaced unless a supplied rendered plan,
provider schema, or documented lifecycle rule supports that claim. Preserve
unknown values as uncertainty, and state the workspace, variables, provider
versions, and target environment covered by any supplied plan. (`TF-PLAN`)

## Plan and stateful blast radius

- Does the supplied plan show create, update, delete, replace, or destroy
  actions for every changed address? What attribute or lifecycle rule causes a
  replacement, and what is unknown until apply? Trace destroy/create ordering,
  dependencies, and the recovery path for stateful resources. (`TF-PLAN`,
  `TF-LIFECYCLE`)
- Would the stated production plan affect data, identity, networking, or a
  shared control plane? Is a snapshot, migration, cutover, restore, or
  rollback procedure supplied and compatible with the order shown in the plan?

## State and address continuity

- Does the backend provide the required access control, encryption, locking,
  and workspace separation for the declared environments? Can concurrent
  applies, stale state, or unreviewed drift overwrite an intended change?
  (`TF-STATE-SENSITIVE`)
- When modules, resources, `for_each` keys, or `count` indexes move, do
  `moved` or `removed` blocks, imports, and addresses preserve the existing
  remote object? Are the addressed state and workspace supplied rather than
  inferred? (`TF-REFACTOR`)

## Dependency graph and provider behavior

- Do lifecycle arguments (`create_before_destroy`, `prevent_destroy`,
  `ignore_changes`, replacement triggers), explicit dependencies, aliases,
  and eventual-consistency waits express the required ordering without hiding
  drift or making recovery impossible? (`TF-LIFECYCLE`, `TF-PROVIDERS`)
- Can a `for_each` key or `count` insertion silently reassign an existing
  object? Do provider aliases target the intended account, project, region, or
  subscription, based on supplied configuration rather than variable names?
  (`TF-STYLE`, `TF-PROVIDERS`)

## Versions and supply chain

- Are Terraform, provider, and module version constraints mutually compatible
  with the PR's declared versions? Does a lock-file change have an explained
  upgrade path and preserve checksums/source integrity? (`TF-VERSIONS`,
  `TF-LOCK`)
- Does a module source pin a trustworthy revision, and are upgrade notes or
  provider schema changes supplied where they can change plan semantics?
  (`TF-PROVIDERS`, `TF-VERSIONS`)

## Secrets and external effects

- Are IAM permissions limited to the operation and environment, and do
  credentials, sensitive/ephemeral values, state, plans, outputs, CI logs,
  provisioners, or external data sources disclose or mutate more than the PR
  intends? (`TF-STATE-SENSITIVE`)
- Can provisioners or external data make apply non-idempotent, leak secrets,
  or leave remote resources changed outside state tracking? Is the failure and
  rollback behavior evidenced?

## Module contracts and deployment safety

- Do input validation, defaults, outputs, and module interfaces preserve the
  callers' contract across environments? Are policy controls and environment
  parity evidenced for the intended apply target? (`TF-STYLE`)
- Is the proposed change reversible with the available state and operational
  evidence, or does it require an explicitly reviewed migration rather than a
  Terraform-only rollback?
