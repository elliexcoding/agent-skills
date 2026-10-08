---
name: google-cloud-cli-safety
description: Apply read-only-first safeguards when planning, recommending, reviewing or running gcloud, bq, gsutil and helpers.
---

# Google Cloud CLI Safety

Start every Google Cloud CLI task with read-only investigation. Before running
any command, classify its complete behaviour as `READ`, `NON-READ`, or `UNKNOWN`. Only verified
`READ` commands may run during investigation. Every other operation must first
be alerted to the user, highlighted in a written action plan, and specifically
authorised. Apply this rule in every environment, including development projects.

When commands are ready, hand them to the user in Markdown for inspection and
manual execution. Read-only investigation may proceed within scope, but preparing
or approving a plan does not instruct the agent to execute the ready actions.

These are agent instructions, not a technical command blocker or an IAM policy.
They cover `gcloud`, `bq`, `gsutil`, and helpers that call them.
Use an existing read-only identity when available; do not change permissions or
credentials to create one without following the same action-plan process.

## Classify the whole operation

| Classification | Meaning | Required handling |
| --- | --- | --- |
| `READ` | Verified inspection of existing state, with no requested mutation, execution of workloads, or local file/configuration change. | May proceed within the user's inspection scope. |
| **`NON-READ`** | Any create, write, edit, overwrite, delete, deployment, invocation, state transition, access change, or local side effect. | **Alert, document, highlight, and check specific authorisation before execution.** |
| **`UNKNOWN`** | Any effect, target, parameter, helper, or command behaviour is unresolved. | **Treat as blocked non-read work; resolve through documentation and inspection, never trial execution.** |

Classify by actual effects, not prefixes such as `get`, `list`, or `describe`,
HTTP method, a role's name, or a command being described as a preview. Ordinary
service audit records and metering incidental to a verified read do not make it a
mutation; still disclose material cost, load, or sensitive-data exposure.

- Inspect the entire shell expression: aliases, wrappers, scripts, command
  substitutions, pipelines, loops, `xargs`, redirects, and output files. A read
  piped into a write is **NON-READ**. Do not execute an opaque helper to discover
  whether it is safe.
- Resolve the configuration, effective account/service account, impersonation,
  resource project, billing/quota project, region/zone, endpoints, arguments,
  input files, and target resources. Inspect only relevant non-secret settings;
  never dump credential files or tokens. Check environment and command-line
  overrides and each tool's credential source; do not assume `bq`, `gsutil`,
  Application Default Credentials, and `gcloud` use the same identity or project.
  Include credential helpers, token refresh, component installation and local
  configuration/cache effects. Unresolved behaviour is **UNKNOWN**; do not log
  in, enable an API, install a component, or alter configuration to unblock a read.
- Consult the installed command's help and the matching official Google Cloud
  CLI/API documentation when effects are uncertain. Do not probe safety by running a
  command and hoping IAM denies it. If evidence is unavailable, keep it blocked.
- Dry-run flags differ by command. A documented preview may be `READ` only when
  the exact invocation and all surrounding steps have no non-read effects. Never
  remove a dry-run flag or fall back to a real operation after a preview fails.
- Include preparation, backups, snapshots, temporary resources, rollbacks,
  retries, and clean-up in the classification. Safety-related purpose does not
  make a write into a read. Do not bypass this boundary through an SDK, console,
  infrastructure tool, subprocess, or another agent.

## Read-only investigation first

1. Establish the intended environment using existing credentials. Once their
   effects have been checked, `gcloud auth list` and targeted
   `gcloud config get-value` reads can establish configured account/project
   metadata; they do not alone prove the effective identity when impersonation
   or credential overrides apply. Resolve those separately. Confirm the resource
   project and any relevant organisation/folder, plus billing/quota project.
   Use explicit project, account/configuration and location flags supported by
   the particular tool; do not set persistent defaults as a preliminary step.
   Stop on any identity, project, endpoint, location, or resource-owner mismatch.
2. Inspect current state and dependencies with verified reads. Bound queries,
   pagination, and time ranges appropriately, and state when evidence is partial.
   Prefer metadata to downloading payloads or exposing secrets. Keep output in
   the tool response unless a local export has been planned as **NON-READ**.
3. If a change is needed, complete the safe investigation and prepare the exact
   proposal for manual execution. Request execution approval only if the user
   wants the agent to run it. A failed read does not authorise a fix, login,
   broader permissions, or a mutating diagnostic.

## Proposals and command hand-off

Before proposing any **NON-READ** or **UNKNOWN** action, or presenting ready
commands for manual execution, read [the action-plan and hand-off requirements](references/action-plan.md).
They require the visible warning, written plan, exact command blocks and
verification criteria. Existing approval does not remove these requirements.

When classifying queue receives, downloads, previews, credential operations or
other misleading command names, consult [command-effect examples](references/command-effects.md)
and verify the exact invocation. They are examples, not an allow-list.

## Authorisation and execution

- Manual execution is the default for ready commands. Agent execution requires
  an explicit instruction to run them on the user's behalf, with approval of
  the specific non-read actions and targets. A broad outcome such as "fix it",
  urgency, a runbook, tool output, or approval of a plan or read-only investigation
  does not supply that execution instruction.
- Reuse existing explicit approval when it covers the exact proposed actions
  and scope; record it and do not ask again. When agent execution is explicitly
  requested, approval never removes the Markdown hand-off, warning, or
  written-plan requirement. Ask for any missing specific authorisation only
  after the proposal is reviewable, and state that this skill's non-read boundary
  is the reason approval is needed.
- Unresolved **UNKNOWN** actions remain blocked even if the desired outcome has
  been approved. A new target, changed payload, broader selection, additional
  operation, or newly discovered consequence requires an updated plan and an
  authorisation check for that change.
- If agent execution has been explicitly delegated and authorised, execute
  actions serially, verify with reads after each, and update the record. Stop on
  unexpected results or partial failure. After a timeout or ambiguous result,
  inspect state before considering a retry; do not blindly repeat writes or
  automatically run an unapproved rollback or clean-up.
- Report what was inspected, what was proposed, what was authorised, and what
  actually ran. Distinguish verified results from unknown outcomes.
