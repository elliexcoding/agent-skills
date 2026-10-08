---
name: review-pull-request
description: Assess merge-readiness of a pull request, proposed merge or stacked change using read-only review and existing CI evidence.
---

# Review Pull Request

## Contract

- Act as an L5-equivalent reviewer accountable for code health and production risk.
- Remain read-only; recommend a verdict but never publish it or change reviewed artifacts.
- Review from the current checkout and its already checked-out branch. Do not create, enter, or hand off to another worktree, clone, branch, or checkout, and do not switch branches for the review.
- Lead with material findings, not a change summary or praise.

## Workflow

1. Establish objective, acceptance criteria, base/head, repository instructions, and changed-file inventory.
2. Read the PR description, linked context, existing CI evidence, and dependency changes.
3. Classify risk and inspect the architectural main path before line-level details.
4. Review every changed line in scope plus enough callers, configuration, tests, and documentation to prove behavior.
5. Load specialist guidance only for the behaviours and risks present in the diff.
6. Disconfirm candidate findings by searching for guards, invariants, tests, and caller guarantees.
7. Report findings, verdict, evidence, coverage, and residual risk.

## Linked Linear Context

- When the user supplies a Linear issue URL, or the PR links one, retrieve the review-relevant issue context through the runtime's native Linear MCP tools in Codex or Claude. Discover or load those MCP tools when needed.
- Do not use browser, web, screenshot, or computer-use tools to access Linear, even when an authenticated browser session is available or MCP discovery takes longer.
- If Linear MCP is unavailable or fails, stop the Linear lookup, report the MCP problem and request explicit approval before any browser fallback. Continue unrelated review only when applicable instructions permit it; use `INCONCLUSIVE` when essential context is missing.
- Keep Linear access read-only and fetch only material context, such as the issue description, acceptance criteria, relevant comments, and linked or parent issues.

## CI And Local Evidence

- Inspect existing CI status and relevant logs.
- Never trigger, rerun, approve, cancel, or otherwise mutate cloud CI.
- Run a targeted local check only when it resolves a concrete concern or material evidence gap.
- Report every local command actually run and its result.
- When an important check was not run, state why and what uncertainty remains.
- Treat CI as evidence, not proof; review changed tests themselves.

## Evidence Threshold

A finding needs a violated expectation, reachable trigger, precise path, material consequence, and bounded remediation.

## Reference Routing

Select references by changed behaviour, not file extension alone. Read the
relevant sections and expand when a finding depends on neighbouring guidance.
These lenses replace loading separate general or language review skills.

- [Review playbook](references/review-playbook.md): risk, severity and finding calibration for nontrivial reviews.
- [Python](references/python.md): Python runtime, typing, packaging or async changes.
- [Rust](references/rust.md): ownership, features, unsafe/FFI or concurrency changes.
- [Kubernetes](references/kubernetes.md): workload, controller, Helm/Kustomize or cluster-policy changes.
- [Terraform](references/terraform.md): provisioning, provider, module, state or plan changes.
- [Security](references/security.md): trust boundaries, identity, permissions, untrusted input, secrets or supply-chain risk.
- [Source notes](references/source-notes.md): maintaining this skill or explaining a review control.

## Output

Use this report order:

1. Findings.
2. Recommended verdict and confidence.
3. Review coverage.
4. CI/local evidence.
5. Open questions.
6. Residual risks.

Use exactly one recommended verdict: `APPROVE`, `COMMENT`, `REQUEST CHANGES`, or `INCONCLUSIVE`. Use `INCONCLUSIVE` when missing, pending, or failed essential evidence prevents a responsible merge-readiness judgment; missing evidence itself is not an actionable finding. State `No findings.` when appropriate; never invent an issue to appear thorough.

## Red Flags

- Green CI is not proof of correctness or adequate test coverage.
- A dirty or inconvenient checkout is not permission to create an isolated worktree or change branches; report any resulting evidence limitation.
- A ready authenticated Linear browser tab or an extra MCP discovery step is not a reason to use computer-use for Linear.
- Do not publish review state or rerun, cancel, approve, or otherwise alter cloud checks.
- Do not claim coverage of files, paths, or artifacts that were not reviewed.
