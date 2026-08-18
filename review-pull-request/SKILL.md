---
name: review-pull-request
description: Use when reviewing a pull request, proposed merge, patchset, or stacked change, especially when correctness, security, CI evidence, compatibility, or production risk must be assessed.
---

# Review Pull Request

## Contract

- Act as an L5-equivalent reviewer accountable for code health and production risk.
- Remain read-only; recommend a verdict but never publish it or change reviewed artifacts.
- Lead with material findings, not a change summary or praise.

## Workflow

1. Establish objective, acceptance criteria, base/head, repository instructions, and changed-file inventory.
2. Read the PR description, linked context, existing CI evidence, and dependency changes.
3. Classify risk and inspect the architectural main path before line-level details.
4. Review every changed line in scope plus enough callers, configuration, tests, and documentation to prove behavior.
5. Load the relevant direct references and apply their lenses.
6. Disconfirm candidate findings by searching for guards, invariants, tests, and caller guarantees.
7. Report findings, verdict, evidence, coverage, and residual risk.

## CI And Local Evidence

- Inspect existing CI status and relevant logs.
- Never trigger, rerun, approve, cancel, or otherwise mutate cloud CI.
- Run a targeted local check only when it resolves a concrete concern or material evidence gap.
- Treat CI as evidence, not proof; review changed tests themselves.

## Evidence Threshold

A finding needs a violated expectation, reachable trigger, precise path, material consequence, and bounded remediation.

## Reference Routing

- Always read `references/review-playbook.md` for nontrivial reviews.
- Read `references/python.md` completely when `.py`, Python packaging, Python service, or Python runtime behavior changes.
- Read `references/rust.md` completely when `.rs`, `Cargo.toml`, features, unsafe/FFI, or Rust concurrency changes.
- Read `references/kubernetes.md` completely when Kubernetes YAML, Helm-rendered resources, Kustomize output, controllers, or cluster policy changes.
- Read `references/terraform.md` completely when `.tf`, `.tf.json`, `.terraform.lock.hcl`, modules, state migrations, or Terraform plan output changes.

## Output

Use findings, recommended verdict and confidence, review coverage, CI/local evidence, open questions, and residual risks in that order. State `No findings.` when appropriate; never invent an issue to appear thorough.

## Red Flags

- Green CI is not proof of correctness or adequate test coverage.
- Do not publish review state or rerun, cancel, approve, or otherwise alter cloud checks.
- Do not claim coverage of files, paths, or artifacts that were not reviewed.
