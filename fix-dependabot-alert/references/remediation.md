# Dependabot remediation and verification

Read before changing files for the selected alert. The one-alert scope, three
materially different attempts and human merge gate from `SKILL.md` apply.

## Contents

- [Discover the update](#3-discover-the-smallest-safe-update)
- [Implement](#4-implement-one-bounded-attempt)
- [Verify locally](#5-verify-from-narrow-to-broad)
- [Observe CI](#6-observe-the-slow-ci-gate)
- [Independent checker](#7-run-an-independent-checker)
- [Persist evidence and stop](#8-persist-evidence-and-stop)

### 3. Discover the smallest safe update

1. Inspect the affected manifest, lockfile, dependency graph, repository update
   policy, and supported runtime versions.
2. Search open pull requests for an existing Dependabot security update for the
   same package, manifest, and alert. Prefer reviewing or repairing that branch
   over creating a duplicate.
3. Establish a pre-change baseline with the narrowest useful install, audit,
   build, or test command. Record failures that predate the update.
4. Determine whether the dependency is direct or transitive and identify the
   package-manager-native command that can update only the required package.
5. Target the lowest version that is both outside the vulnerable range and
   compatible with repository constraints. Do not jump to the newest release by
   default.
6. For a non-patch bump or any compatibility change, read primary release notes
   and migration guidance before editing.
7. State one testable hypothesis, for example: “Updating package X from A to B
   will remove GHSA-Y without application changes.”

Stop and request a human decision when no patched version exists, the only fix
requires a major upgrade, generated/vendor files would need unsupported manual
editing, or repository policy conflicts with the secure version.

### 4. Implement one bounded attempt

1. Use the ecosystem's package manager to update the selected dependency and
   regenerate its lockfile. Do not hand-edit generated lock data.
2. Inspect the diff immediately. Revert accidental churn through a
   package-manager-supported narrower update rather than editing generated
   output by hand.
3. Change application code or tests only when the secure version requires a
   compatibility adjustment. Tie every such change to release guidance or a
   reproduced failure.
4. Keep each retry materially different: use the latest evidence to revise the
   hypothesis, then run the narrowest discriminating check.

Never make a second alert part of the attempt, upgrade an unrelated package,
delete or skip a test, weaken lint/type/audit policy, dismiss the alert, or
enable auto-merge to make the run appear successful.

### 5. Verify from narrow to broad

Run and record:

1. dependency resolution or install with the updated lockfile;
2. proof that the resolved version is outside the alert's vulnerable range;
3. the targeted audit/test/build command associated with the change;
4. repository-required lint, type, test, and build checks; and
5. `git diff --check`, the final diff, and the final changed-file list.

Do not claim that the GitHub alert is closed before merge and GitHub's dependency
graph has processed the new default-branch state. Before merge, report the
accurate state: the patch is locally verified and expected to resolve the alert.

If a baseline check already failed, prove that the update did not introduce the
failure and report the residual risk. Do not convert a pre-existing red build
into a false green claim.

### 6. Observe the slow CI gate

When push and pull-request creation are authorised:

1. Push the bounded branch and create or update one draft pull request.
2. Wait for the repository's required remote checks. With the GitHub CLI, use
   `gh pr checks --watch` when appropriate.
3. Read the complete failing job log before changing code. Distinguish a
   dependency regression from flaky infrastructure, permissions, secrets, and
   failures already present on the base branch.
4. Count a code change prompted by CI as another fix attempt. Do not spend an
   attempt merely rerunning a clearly flaky or externally blocked job.
5. Re-run relevant local checks after every CI-driven edit, then observe CI
   again.

Treat remote required CI as the slow, non-bypassable quality gate. If the user
did not authorise a push or pull request, mark remote CI as pending and stop
with a locally verified patch; do not report `READY_FOR_REVIEW`.

### 7. Run an independent checker

Use a separate review agent when available and permitted; otherwise designate a
human reviewer as the independent checker. Give the checker the alert record,
final diff, and raw command results, not the maker's conclusion.

Require the checker to reject:

- a resolved version still inside any vulnerable range for the alert;
- an unexplained major bump or unrelated dependency churn;
- hand-edited lockfile content;
- deleted, skipped, or weakened validation;
- compatibility code not justified by evidence;
- missing full-suite evidence required by repository policy; or
- claims that the alert is closed before GitHub confirms it.

Address checker findings within the same three-attempt limit. If no independent
checker is available, label that gate as pending rather than self-approving it.

### 8. Persist evidence and stop

Use the commit and pull-request description as the durable run note unless the
repository specifies another location. Include:

```markdown
## Dependabot alert
- Alert: <URL and number>
- Advisory: <GHSA/CVE>
- Package and manifest: <package>, <path>
- Vulnerable range: <range>
- Resolved version: <version>

## Change
- Hypothesis: <what this update was expected to prove>
- Scope: <manifest, lockfile, required compatibility changes>

## Validation
- `<exact command>` — <result>
- Version-range proof — <result>
- Remote required CI — <result or pending>
- Independent check — <result or pending>

## Boundaries
- Unrelated changes: none / <explain>
- Residual risk: none known / <explain>
- Merge gate: human approval required
```

Create at most one small pull request when authorised. Prefer draft status until
all local checks and the independent check pass. Never merge it as part of this
skill.

End in exactly one state:

- `READY_FOR_REVIEW`: the bounded patch, remote required CI, and independent
  check are complete;
- `BLOCKED`: name the missing permission, incompatible constraint, failed gate,
  or human decision needed;
- `NO_ACTION`: the alert is absent, stale, already fixed, or already covered by
  an equivalent pull request; or
- `ATTEMPT_LIMIT`: three materially different attempts did not satisfy the
  verifier; preserve evidence and recommend the smallest next diagnostic step.

After merge, a later read-only follow-up may confirm that GitHub marked the alert
fixed. Treat that confirmation as a separate observation, not permission for
another dependency change.
