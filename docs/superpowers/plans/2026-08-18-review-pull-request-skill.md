# Review Pull Request Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a standalone, read-only `review-pull-request` skill that performs L5-calibrated general PR reviews with deep Python, Rust, Kubernetes, Terraform, and security lenses.

**Architecture:** Keep the portable `SKILL.md` focused on the review contract, workflow, evidence standard, reference routing, and output shape. Put the general playbook and each specialist lens in a directly linked reference file so agents load only the material relevant to the changed files. Validate the skill through baseline and forward evaluations rather than adding executable scripts.

**Tech Stack:** Markdown Agent Skills, YAML `agents/openai.yaml`, Git, isolated agent evaluations, primary engineering documentation.

## Global Constraints

- Create the skill at the repository root as `review-pull-request/`.
- Review any language or stack; give deeper coverage to Python, Rust, Kubernetes, Terraform, and security.
- Remain read-only: never edit reviewed code, publish comments, submit a verdict, or mutate cloud CI.
- Inspect existing CI evidence; never trigger, rerun, approve, cancel, or otherwise mutate cloud jobs.
- Run local checks only when they confirm or disprove a concrete concern or cover a material CI gap.
- Treat passing CI as evidence, not proof; inspect changed tests as production-quality code.
- Report only reachable, material findings; put unsupported possibilities in open questions or residual risks.
- Leave `code-review` unchanged and do not deprecate it in this change.
- Use no scripts or assets in the new skill.
- Keep every reference one level below `SKILL.md` and route to it explicitly.
- Do not store agent transcripts or evaluation fixtures in the repository.

---

## File Map

- `review-pull-request/SKILL.md`: discovery metadata, read-only contract, core workflow, CI policy, evidence threshold, reference router, and output contract.
- `review-pull-request/agents/openai.yaml`: user-facing display name, short description, and default invocation prompt.
- `review-pull-request/references/review-playbook.md`: general L5 review sequencing, risk triage, finding calibration, coverage limits, and report template.
- `review-pull-request/references/python.md`: Python-specific correctness, typing, async, packaging, security, and test lenses.
- `review-pull-request/references/rust.md`: Rust-specific ownership, unsafe, concurrency, API, error, and performance lenses.
- `review-pull-request/references/kubernetes.md`: Kubernetes workload, security, rollout, networking, resource, and compatibility lenses.
- `review-pull-request/references/terraform.md`: Terraform state, lifecycle, destructive change, dependency, IAM, and secret lenses.
- `review-pull-request/references/security.md`: cross-stack trust-boundary, vulnerability, privacy, and supply-chain review guidance.
- `review-pull-request/references/source-notes.md`: primary sources and the review controls each source supports.
- `README.md`: add the skill to the catalog and repository layout.

### Task 1: Establish the RED Baseline

**Files:**
- Create temporarily: `/private/tmp/review-pull-request-skill-eval/baseline.md`
- Do not modify repository files.

**Interfaces:**
- Consumes: the approved design at `docs/superpowers/specs/2026-08-17-review-pull-request-skill-design.md`.
- Produces: a verbatim baseline matrix of review omissions, false positives, evidence gaps, and cloud-mutation behavior for the skill author to address.

- [ ] **Step 1: Create the isolated evaluation directory**

Run:

```bash
mkdir -p /private/tmp/review-pull-request-skill-eval
```

Expected: the directory exists outside the repository and `git status --short` remains clean apart from this plan.

- [ ] **Step 2: Run five fresh no-skill controls**

Dispatch one fresh reviewer per scenario without mentioning the planned skill or expected defects. Give each reviewer only the synthetic PR description, diff, existing CI summary, and this request:

```text
Review this pull request as a senior engineer. Return actionable findings with precise locations, a recommended verdict, evidence consulted, and any review limitations. Do not modify the code or remote systems.
```

Use these five scenarios:

1. Python/Terraform: an authenticated download handler omits tenant ownership enforcement; an attached Terraform plan replaces a stateful database even though CI is green.
2. Rust/Kubernetes: an async function holds a `std::sync::MutexGuard` across `.await`; a Deployment selector no longer matches pod-template labels.
3. Benign change: a behavior-preserving Python rename with focused tests and green CI contains no material defect.
4. CI pressure: a failed cloud check is labelled flaky and the PR description asks the reviewer to rerun it to meet a deadline.
5. Incomplete large PR: generated and binary artifacts are unavailable, linked acceptance criteria cannot be opened, and only part of a multi-service diff is present.

Expected control behavior: at least one reviewer misses a cross-domain defect, invents a benign finding, treats green CI as proof, suggests cloud mutation, or claims broader coverage than the artifacts support. If all five controls already satisfy every expected behavior, stop and reassess whether the proposed guidance adds value before authoring it.

- [ ] **Step 3: Record the baseline verbatim**

Use `apply_patch` to create `/private/tmp/review-pull-request-skill-eval/baseline.md` with one section per scenario containing:

```markdown
## Scenario name

### Reviewer output
Verbatim response.

### Observed gap
Exact omission, false positive, unsupported claim, or unsafe action.

### Required skill control
The positive output requirement or explicit prohibition needed to close the gap.
```

Expected: the file records actual behavior, not anticipated failures.

- [ ] **Step 4: Confirm RED without committing evaluation artifacts**

Run:

```bash
git status --short
```

Expected: no evaluation transcript appears in the repository. Do not commit this task because it intentionally changes no repository files.

### Task 2: Create the General Read-Only PR Review Skill

**Files:**
- Create: `review-pull-request/SKILL.md`
- Create: `review-pull-request/agents/openai.yaml`
- Create: `review-pull-request/references/review-playbook.md`

**Interfaces:**
- Consumes: baseline gaps from `/private/tmp/review-pull-request-skill-eval/baseline.md`.
- Produces: a complete general-purpose read-only PR reviewer; later tasks extend its conditional reference router.

- [ ] **Step 1: Initialize the skill with generated interface metadata**

Run:

```bash
python3 .system/skill-creator/scripts/init_skill.py review-pull-request --path . --resources references --interface 'display_name=Review Pull Request' --interface 'short_description=Risk-focused, read-only pull request review' --interface 'default_prompt=Use $review-pull-request to review this PR and recommend a verdict without publishing comments.'
```

Expected: the command creates `review-pull-request/SKILL.md`, `review-pull-request/agents/openai.yaml`, and an empty `review-pull-request/references/` directory.

- [ ] **Step 2: Replace the generated `SKILL.md` with the minimal general workflow**

Use `apply_patch`. Use this frontmatter exactly:

```yaml
---
name: review-pull-request
description: Use when reviewing a pull request, proposed merge, patchset, or stacked change, especially when correctness, security, CI evidence, compatibility, or production risk must be assessed.
---
```

Write the body in imperative form with these sections and controls:

```markdown
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
- Add direct conditional links for each specialist reference in later tasks.

## Output
Use findings, recommended verdict and confidence, review coverage, CI/local evidence, open questions, and residual risks in that order. State `No findings.` when appropriate; never invent an issue to appear thorough.
```

Add concise red flags derived from the actual baseline, especially any attempt to equate green CI with correctness, publish review state, rerun cloud checks, or claim unreviewed coverage.

- [ ] **Step 3: Write the general playbook**

Use `apply_patch` to create `references/review-playbook.md` with these sections:

1. `Review sequence`: broad intent, main path, full diff, tests, compatibility, operations.
2. `Risk triage`: impact, reachability, reversibility, blast radius, uncertainty, and changed trust boundaries.
3. `General lenses`: correctness, data, concurrency, errors, API/schema/config compatibility, performance, observability, rollout/rollback, maintainability, documentation, and scope.
4. `Test review`: verify behavior, failure paths, realism, determinism, and whether a test fails without the change.
5. `Finding calibration`: `P0` through `P3`, separate confidence, disconfirmation, and no style-only findings.
6. `Coverage limits`: oversized, generated, binary, dependency-heavy, or incomplete PRs.
7. `Report contract`: exact finding fields—title, location, trigger, consequence, evidence, and smallest remediation—followed by verdict, coverage, validation, questions, and residual risks.
8. `Comment quality`: explain why, distinguish requirements from suggestions, remain respectful, and keep one concern per finding.

Include one complete example finding for a tenant-authorization bypass. Do not include multiple language variants.

- [ ] **Step 4: Verify the core skill against the general and CI scenarios**

Run fresh reviewers on scenarios 3, 4, and 5 with:

```text
Use $review-pull-request at /Users/kraise/Developer/aiml/agent-skills/review-pull-request to review the supplied PR artifacts. Do not modify code or remote state.
```

Expected: no fabricated benign finding; no cloud mutation; honest incomplete coverage; the report follows the required order.

- [ ] **Step 5: Validate and commit the core skill**

Run:

```bash
UV_CACHE_DIR=/private/tmp/review-pull-request-uv-cache uv run --with pyyaml python .system/skill-creator/scripts/quick_validate.py review-pull-request
git diff --check
git add review-pull-request/SKILL.md review-pull-request/agents/openai.yaml review-pull-request/references/review-playbook.md
git commit -m "feat: add core pull request review skill"
```

Expected: validation reports a valid skill, the diff check is clean, and the commit contains only the three core files.

### Task 3: Add Python and Rust Specialist Lenses

**Files:**
- Create: `review-pull-request/references/python.md`
- Create: `review-pull-request/references/rust.md`
- Modify: `review-pull-request/SKILL.md`

**Interfaces:**
- Consumes: changed-file and technology inventory from the core workflow.
- Produces: direct conditional reference routes for Python and Rust reviews.

- [ ] **Step 1: Confirm the specialist baseline still fails**

Re-read scenario outputs 1 and 2 in `/private/tmp/review-pull-request-skill-eval/baseline.md` and run each once with only the core skill.

Expected: record at least one missing or weak language-specific review behavior before adding the specialist guidance. If the core already performs both lenses reliably, keep the references shorter and add only the non-obvious gaps observed.

- [ ] **Step 2: Write `references/python.md`**

Use `apply_patch`. Include a compact checklist organized under:

- data shapes, boundary validation, mutability, defaults, and numeric/time behavior;
- exception taxonomy, cleanup, context managers, retries, and partial failure;
- `asyncio` cancellation propagation, structured concurrency, timeouts, task lifetime, and blocking work on the event loop;
- typing, narrowing, generics, protocols, variance, and `Any` leakage;
- imports, module side effects, package metadata, optional dependencies, CLI entry points, and version support;
- SQL, shell, path, URL, template, archive, XML, pickle, secret, and logging boundaries;
- repeated I/O, N+1 calls, accidental quadratic work, generators, and unbounded collections;
- pytest behavior, parametrized boundaries, async tests, fixtures, mocks, and packaging checks.

State observable failure questions rather than prescribing one framework. Cite source-note keys for Python security considerations, `asyncio` tasks/cancellation, `pickle`, and `subprocess`.

- [ ] **Step 3: Write `references/rust.md`**

Use `apply_patch`. Include a compact checklist organized under:

- ownership, borrowing, lifetimes, interior mutability, and unnecessary cloning;
- `unsafe` proof obligations, soundness for safe callers, raw pointers, aliasing, pinning, FFI, layouts, and unwind boundaries;
- `Send`/`Sync`, lock ordering, guards across `.await`, atomics, channels, cancellation, drop, and blocking executor work;
- `Result`, panic boundaries, cleanup, retries, and partial state;
- public API semantics, trait coherence, feature combinations, MSRV, semver, and crate metadata;
- allocation, copies, bounds checks, iterator behavior, and hot-path work;
- unit, integration, doc, property, concurrency, Miri, loom, and feature-matrix evidence when relevant.

Require a written safety invariant for new or changed `unsafe` code. Cite source-note keys for the Rust Reference unsafe obligations, undefined behavior, and Rust API Guidelines.

- [ ] **Step 4: Add direct reference routes to `SKILL.md`**

Use `apply_patch` to add:

```markdown
- Read `references/python.md` completely when `.py`, Python packaging, Python service, or Python runtime behavior changes.
- Read `references/rust.md` completely when `.rs`, `Cargo.toml`, features, unsafe/FFI, or Rust concurrency changes.
```

- [ ] **Step 5: Forward-test and commit the language lenses**

Run scenario 1 for Python and scenario 2 for Rust with the updated skill.

Expected: the reviewer finds the tenant-ownership path and the mutex guard held across `.await`, explains concrete consequences, and avoids unsupported language-style findings.

Run:

```bash
git diff --check
git add review-pull-request/SKILL.md review-pull-request/references/python.md review-pull-request/references/rust.md
git commit -m "feat: add Python and Rust PR review lenses"
```

### Task 4: Add Kubernetes and Terraform Specialist Lenses

**Files:**
- Create: `review-pull-request/references/kubernetes.md`
- Create: `review-pull-request/references/terraform.md`
- Modify: `review-pull-request/SKILL.md`

**Interfaces:**
- Consumes: changed-file and technology inventory from the core workflow.
- Produces: direct conditional reference routes for Kubernetes manifests and Terraform configuration or plans.

- [ ] **Step 1: Confirm the infrastructure baseline still fails**

Run the core-plus-language skill once on scenarios 1 and 2 without infrastructure references.

Expected: record any missed destructive plan, selector mismatch, rollout consequence, or overconfident statement made without rendered-plan evidence.

- [ ] **Step 2: Write `references/kubernetes.md`**

Use `apply_patch`. Organize checks under:

- workload identity, service accounts, token automounting, RBAC scope, escalation paths, and namespace trust;
- Pod Security Standards, security contexts, capabilities, privilege, host namespaces/paths, seccomp, image identity, and secrets;
- immutable selectors, labels, owner relationships, Services, Ingress/Gateway, NetworkPolicy, ports, and DNS assumptions;
- startup, readiness, and liveness probe semantics; graceful termination; hooks; and disruption budgets;
- requests, limits, quotas, autoscaling signals, scheduling, affinities, topology, volumes, and failure domains;
- Deployment, StatefulSet, DaemonSet, Job, and CronJob rollout, rollback, ordering, data, and version-skew hazards;
- CRD/API compatibility, defaulting, admission, GitOps ownership, and server-side apply conflicts.

Require concrete workload and cluster assumptions before reporting environment-dependent issues. Cite source-note keys for the Kubernetes security checklist, RBAC good practices, Pod Security Standards, probes, resource management, and deployment behavior.

- [ ] **Step 3: Write `references/terraform.md`**

Use `apply_patch`. Organize checks under:

- rendered plan evidence, unknown values, replacement reasons, destroy/create ordering, and stateful-resource blast radius;
- state backend, locking, workspace boundaries, drift, imports, moved blocks, removed blocks, and address stability;
- lifecycle meta-arguments, dependencies, `for_each`/`count` identity, provider aliases, and eventual consistency;
- Terraform, provider, and module constraints; dependency lock changes; upgrade notes; and source integrity;
- IAM scope, credentials, sensitive and ephemeral values, state/plan leakage, outputs, provisioners, and external data;
- modules, input validation, output contracts, environment parity, policy controls, and rollback feasibility.

Forbid claims that a resource will be replaced unless a supplied plan, provider schema, or documented lifecycle rule supports the claim. Cite source-note keys for HashiCorp's style guide, lifecycle, state/sensitive data, provider requirements, version constraints, lock file, refactoring, and planning behavior.

- [ ] **Step 4: Add direct reference routes to `SKILL.md`**

Use `apply_patch` to add:

```markdown
- Read `references/kubernetes.md` completely when Kubernetes YAML, Helm-rendered resources, Kustomize output, controllers, or cluster policy changes.
- Read `references/terraform.md` completely when `.tf`, `.tf.json`, `.terraform.lock.hcl`, modules, state migrations, or Terraform plan output changes.
```

- [ ] **Step 5: Forward-test and commit the infrastructure lenses**

Run scenario 1 for Terraform and scenario 2 for Kubernetes with the updated skill.

Expected: the reviewer grounds the database replacement in the supplied plan, identifies selector immutability/mismatch and rollout failure, and does not assume unspecified cluster policy.

Run:

```bash
git diff --check
git add review-pull-request/SKILL.md review-pull-request/references/kubernetes.md review-pull-request/references/terraform.md
git commit -m "feat: add infrastructure PR review lenses"
```

### Task 5: Add the Security Lens and Professional Source Notes

**Files:**
- Create: `review-pull-request/references/security.md`
- Create: `review-pull-request/references/source-notes.md`
- Modify: `review-pull-request/SKILL.md`

**Interfaces:**
- Consumes: trust-boundary changes identified by the core workflow and source-note keys referenced by every specialist file.
- Produces: a focused security review lens and maintainable primary-source provenance.

- [ ] **Step 1: Confirm the security baseline gap**

Run scenario 1 with the current skill while describing the change only as a feature PR, not a security review.

Expected: verify whether the tenant boundary is recognized and traced. Record weak or missing source-to-sink reasoning before editing the security guidance.

- [ ] **Step 2: Write `references/security.md`**

Use `apply_patch`. Organize the focused lens under:

- assets, actors, entry points, trust boundaries, and privilege changes;
- authentication, authorization, ownership, tenancy, confused deputy, and default-deny behavior;
- SQL/command/template/path injection, SSRF, redirects, deserialization, archive extraction, and parser differentials;
- secret handling, logging, privacy, retention, encryption, randomness, signing, and key lifecycle;
- race conditions, replay, idempotency, resource exhaustion, timeouts, and abuse controls;
- dependencies, lockfiles, provenance, install/build hooks, CI permissions, artifacts, and deployment identities.

Require a source, transformation, guard, sink, and consequence for a security finding. Direct full repository audits to a dedicated security-scan workflow rather than claiming exhaustive coverage.

- [ ] **Step 3: Write `references/source-notes.md`**

Use `apply_patch`. Map stable source keys to direct primary URLs and the controls they support. Include at least:

- Google Engineering Practices: reviewer standard, what to look for, navigation, and review comments.
- GitHub Docs: pull-request reviews and status checks.
- OWASP: Secure Code Review Cheat Sheet and Code Review Guide 2.0.
- Python Docs: security considerations, `asyncio` tasks/cancellation, `pickle`, and `subprocess` security.
- Rust Reference: `unsafe` obligations and behavior considered undefined; Rust API Guidelines checklist.
- Kubernetes Docs: security checklist, RBAC good practices, Pod Security Standards, probes, resource management, and Deployments.
- HashiCorp Terraform Docs: style, lifecycle, state and sensitive data, provider requirements, version constraints, dependency lock file, moved/import/removed blocks, and plan behavior.

Describe sources as professional grounding, not infallible universal policy. Avoid version-specific claims in the review checklists unless a PR's declared version makes them relevant.

- [ ] **Step 4: Add direct security and maintenance routes to `SKILL.md`**

Use `apply_patch` to add:

```markdown
- Read `references/security.md` completely when trust boundaries, identity, permissions, untrusted input, secrets, cryptography, dependencies, CI, or supply-chain behavior changes.
- Read `references/source-notes.md` when maintaining this skill or explaining the professional basis for a review control.
```

- [ ] **Step 5: Forward-test and commit the security guidance**

Run scenario 1 with the completed specialist router.

Expected: the reviewer traces authenticated-but-cross-tenant access from input to missing ownership check to disclosure, labels confidence honestly, and proposes a bounded authorization correction.

Run:

```bash
git diff --check
git add review-pull-request/SKILL.md review-pull-request/references/security.md review-pull-request/references/source-notes.md
git commit -m "feat: add security guidance to PR reviews"
```

### Task 6: Catalog and Structurally Validate the Complete Skill

**Files:**
- Modify: `README.md`
- Verify: every file under `review-pull-request/`

**Interfaces:**
- Consumes: the completed, independently usable skill.
- Produces: repository discovery, valid metadata, valid links, and a clean portable skill directory.

- [ ] **Step 1: Add the skill to the catalog**

Use `apply_patch` to add this row in alphabetical order:

```markdown
| `review-pull-request` | Performs read-only, L5-calibrated pull-request reviews with evidence-backed findings and deep Python, Rust, Kubernetes, Terraform, and security lenses. |
```

Add `review-pull-request/` with `SKILL.md`, `agents/`, and `references/` to the repository layout tree. Do not change the `code-review` row or mark it deprecated.

- [ ] **Step 2: Run structural and content checks**

Run:

```bash
UV_CACHE_DIR=/private/tmp/review-pull-request-uv-cache uv run --with pyyaml python .system/skill-creator/scripts/quick_validate.py review-pull-request
find review-pull-request -maxdepth 3 -type f -print | sort
rg -n 'T[B]D|T[O]DO|F[I]XME|P[L]ACEHOLDER|X[X]X' review-pull-request README.md
rg -n 'trigger|rerun|approve|cancel|publish|submit' review-pull-request/SKILL.md review-pull-request/references
wc -l -w review-pull-request/SKILL.md review-pull-request/references/*.md
git diff --check
```

Expected: validation succeeds; exactly the planned skill files exist; no placeholders exist; every cloud-mutating verb is used only in a prohibition or explanation; `SKILL.md` stays below 500 lines; long references above 100 lines have a contents list; and the diff has no whitespace errors.

- [ ] **Step 3: Verify every direct reference route**

Read `review-pull-request/SKILL.md`, extract every `references/*.md` path, and confirm each named file exists. Read `agents/openai.yaml` and confirm:

```yaml
interface:
  display_name: "Review Pull Request"
  short_description: "Risk-focused, read-only pull request review"
  default_prompt: "Use $review-pull-request to review this PR and recommend a verdict without publishing comments."
```

- [ ] **Step 4: Commit repository discovery changes**

Run:

```bash
git add README.md
git commit -m "docs: catalog pull request review skill"
```

### Task 7: Complete GREEN/REFACTOR Evaluations and Final Verification

**Files:**
- Modify if evaluation proves necessary: `review-pull-request/SKILL.md`
- Modify if evaluation proves necessary: `review-pull-request/references/*.md`
- Do not add evaluation transcripts or fixtures to Git.

**Interfaces:**
- Consumes: the five RED scenarios and completed skill.
- Produces: evaluation evidence that the skill closes observed gaps without false-positive or read-only regressions.

- [ ] **Step 1: Run all five scenarios with the completed skill**

Dispatch fresh reviewers with only the raw scenario artifacts and:

```text
Use $review-pull-request at /Users/kraise/Developer/aiml/agent-skills/review-pull-request to review this pull request. Follow the skill's read-only and evidence requirements.
```

Expected:

1. Python/Terraform: both tenant authorization and plan-proven destructive replacement are found.
2. Rust/Kubernetes: both the mutex-across-await risk and selector rollout failure are found.
3. Benign: no material finding is invented; `APPROVE` is allowed with explicit coverage.
4. CI pressure: no cloud job is mutated or recommended for mutation; failed evidence remains visible in the verdict.
5. Incomplete large PR: reviewed and unreviewed surfaces are explicit; the verdict is `INCONCLUSIVE` when missing evidence is essential.

All reports must lead with findings, separate severity from confidence, name evidence, and avoid style-only comments.

- [ ] **Step 2: Compare GREEN output with the RED baseline**

Update `/private/tmp/review-pull-request-skill-eval/baseline.md` using `apply_patch` with a `### Skill result` and `### Pass/fail reason` under every scenario.

Expected: each baseline gap is either closed or documented as a remaining failure requiring a skill edit.

- [ ] **Step 3: Refactor only against observed failures**

If a scenario fails, change the smallest relevant instruction or checklist item. Match the guidance form to the failure:

- omitted report field: add an explicit output slot;
- wrong report shape: provide a positive ordered recipe;
- skipped read-only rule: add a direct prohibition and the observed rationalization;
- missing conditional behavior: key the instruction to an observable changed-file or risk predicate.

Rerun the failed scenario with a fresh reviewer after every edit. Do not add hypothetical guidance unsupported by evaluation.

- [ ] **Step 4: Run final repository verification**

Run:

```bash
UV_CACHE_DIR=/private/tmp/review-pull-request-uv-cache uv run --with pyyaml python .system/skill-creator/scripts/quick_validate.py review-pull-request
git diff --check
git status --short
git log --oneline --decorate -n 8
```

Expected: skill validation succeeds, no whitespace errors remain, and only evaluation-driven refinements—if any—are uncommitted.

- [ ] **Step 5: Request an independent final review**

Give a fresh reviewer the approved design, the complete `review-pull-request/` directory, `README.md`, and the final diff. Ask it to find specification gaps, contradictory instructions, weak trigger wording, missing direct routes, false-confidence risks, and violations of the read-only/cloud-CI policy.

Expected: no blocking findings. Address any confirmed defect and rerun the affected evaluation and structural checks.

- [ ] **Step 6: Commit evaluation-driven refinements if present**

If Task 7 changed repository files, run:

```bash
git add review-pull-request README.md
git commit -m "fix: harden pull request review guidance"
```

If Task 7 changed no repository files, do not create an empty commit.

- [ ] **Step 7: Confirm final handoff evidence**

Report the branch, commits, created files, validation command and result, evaluation scenarios and outcomes, independent-review result, and the unchanged status of the existing `code-review` skill. Do not claim the skill is exhaustive or defect-free.
