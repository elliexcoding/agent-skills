---
name: fix-dependabot-alert
description: Fix one GitHub Dependabot security alert or its linked PR with a minimal verified update and a human merge gate.
---

# Fix Dependabot Alert

## Purpose

Resolve exactly one Dependabot security alert with a deliberate outer loop:
discover one signal, isolate one change, verify it, obtain an independent check,
persist the evidence, and stop for human review. Optimise for a small trustworthy
pull request, not throughput.

For a triage-only request, inspect and report the alert without starting a fix.
For remediation, continue through the bounded patch and verification below.
Read [slow-loop rationale](references/slow-loop.md) when maintaining this skill
or explaining its quality gates.

## Inputs

Obtain or infer:

- the selected repository as a local path, `OWNER/REPO`, or GitHub URL;
- one Dependabot alert URL or number, linked Dependabot pull request, or GitHub
  issue that identifies the alert;
- permission boundaries for commits, pushes, and pull-request creation; and
- repository-specific instructions and required validation commands.

If the repository is not identified, ask for it. If the repository is selected
but the alert is not, list a small set of open alerts and ask the user to choose.
Only choose autonomously when the user explicitly delegates prioritisation; then
prefer an alert with an available patch, followed by runtime scope, severity,
and exploitability evidence. State the selection rule.

Treat a Dependabot alert as a security record, not as an ordinary GitHub issue.
If an issue or pull request is supplied, trace it to the referenced alert before
editing. If it only describes a routine version update with no security alert,
report that mismatch and ask whether to proceed as a non-security dependency
update.

## Slow-Loop Contract

Define the run before changing files:

```text
Signal: one open Dependabot alert
Goal: move the affected dependency outside the vulnerable range
Workspace: one isolated branch or worktree
Change budget: affected manifest and lockfile, plus compatibility code/tests only when required
Attempt limit: 3 materially different fix attempts
Checker: repository checks plus an independent review pass
Success: local and remote required checks are green and one small PR is ready for human review
Human gate: required before merge
```

Do not expand the run to a second alert. A single dependency update may close
multiple alerts for the same package and manifest; record that side effect, but
do not add unrelated packages to the patch.

## Workflow

### 1. Resolve the repository and authority

1. Read `AGENTS.md` and other repository instructions before task-specific
   edits.
2. Inspect `git status --short --branch`, remotes, the current branch, and the
   default branch.
3. Preserve user changes. Use a separate worktree when the selected checkout is
   dirty or is being used for other work.
4. Work on a concise task branch such as
   `codex/dependabot-<package>-<alert-number>`. Do not replace an existing named
   branch merely to match this suggestion.
5. Confirm GitHub authentication and repository identity. With the GitHub CLI,
   prefer:

   ```sh
   gh auth status
   gh repo view OWNER/REPO --json nameWithOwner,defaultBranchRef,url
   ```

6. Confirm whether the user authorised committing, pushing, or opening a pull
   request. Never infer authority to merge.

### 2. Capture one alert

Use an available GitHub connector that exposes Dependabot alerts, or use the
authenticated GitHub CLI. For example:

```sh
gh api --method GET repos/OWNER/REPO/dependabot/alerts \
  -f state=open -f per_page=100 \
  --jq '.[] | [.number, .security_advisory.severity, .dependency.scope, .dependency.package.ecosystem, .dependency.package.name, .dependency.manifest_path, (.security_vulnerability.first_patched_version.identifier // "no patch"), .html_url] | @tsv'

gh api repos/OWNER/REPO/dependabot/alerts/ALERT_NUMBER
```

Capture the alert number and URL, GHSA/CVE, severity, dependency scope,
ecosystem, package, manifest path, vulnerable range, first patched version, and
current state. Re-read the exact alert immediately before implementation so a
stale or already-fixed alert does not start a new change.

If access fails, distinguish missing authentication or Dependabot-alert
permission from an absent alert. Stop with the precise missing permission;
Dependabot alert reads commonly require repository access plus Dependabot-alert
read permission or an appropriate token scope.

## Remediate the selected alert

For an authorised fix, read [remediation and verification](references/remediation.md)
before editing. It covers minimal version selection, lockfile generation,
compatibility changes, local checks, remote CI, the independent checker and the
final evidence record. Do not load it for read-only triage.

Preserve the three-attempt limit. Never weaken checks, dismiss the alert or
merge the PR. `READY_FOR_REVIEW` requires local verification, remote required CI
and an independent check; report pending gates honestly. Do not claim the alert
closed before GitHub confirms it after merge.
