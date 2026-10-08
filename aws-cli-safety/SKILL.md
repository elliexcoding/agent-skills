---
name: aws-cli-safety
description: Apply read-only-first safeguards whenever planning, recommending, reviewing, or running AWS CLI commands, including scripts, pipelines, incidents, and deployments. Highlight every non-read or uncertain action in a written action plan. Present ready commands in Markdown with explanations for the user to inspect and execute manually.
---

# AWS CLI Safety

Start every AWS CLI task with read-only investigation. Before running any command,
classify its complete behaviour as `READ`, `NON-READ`, or `UNKNOWN`. Only verified
`READ` commands may run during investigation. Every other operation must first
be alerted to the user, highlighted in a written action plan, and specifically
authorised. Apply this rule in every environment, including development accounts.

When commands are ready, hand them to the user in Markdown for inspection and
manual execution. Read-only investigation may proceed within scope, but preparing
or approving a plan does not instruct the agent to execute the ready actions.

These are agent instructions, not a technical command blocker or an IAM policy.
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
- Resolve profile, account, role, region, endpoint, arguments, input files, and
  target resources before execution. Inspect only relevant non-secret settings;
  never dump credential files or tokens. Include credential helpers and session
  creation/refresh when assessing side effects. Unresolved behaviour is
  **UNKNOWN**; do not silently log in or alter configuration to unblock a read.
- Consult the installed command's help and the matching official AWS CLI/API
  documentation when effects are uncertain. Do not probe safety by running a
  command and hoping IAM denies it. If evidence is unavailable, keep it blocked.
- Dry-run flags differ by command. A documented preview may be `READ` only when
  the exact invocation and all surrounding steps have no non-read effects. Never
  remove a dry-run flag or fall back to a real operation after a preview fails.
- Include preparation, backups, snapshots, temporary resources, rollbacks,
  retries, and clean-up in the classification. Safety-related purpose does not
  make a write into a read. Do not bypass this boundary through an SDK, console,
  infrastructure tool, subprocess, or another agent.

## Read-only investigation first

1. Establish the intended environment and use existing credentials. Verify the
   caller/account with `aws sts get-caller-identity` once credential resolution
   itself has been checked. Make profile and region explicit where applicable;
   stop on an unexpected account, endpoint, role, region, or resource owner.
2. Inspect current state and dependencies with verified reads. Bound queries,
   pagination, and time ranges appropriately, and state when evidence is partial.
   Prefer metadata to downloading payloads or exposing secrets. Keep output in
   the tool response unless a local export has been planned as **NON-READ**.
3. If a change is needed, complete the safe investigation and prepare the exact
   proposal for manual execution. Request execution approval only if the user
   wants the agent to run it. A failed read does not authorise a fix, login,
   broader permissions, or a mutating diagnostic.

## Highlight every non-read action

Before any proposed **NON-READ** or **UNKNOWN** operation, give a visible warning
in the conversation: **AWS NON-READ ACTION — NOT EXECUTED**, followed by the
action, target, and consequence. Flag destructive or irreversible effects with
**DESTRUCTIVE** or **IRREVERSIBLE**. Put this above command blocks, not only in a
tool call or collapsed log. Apply the same labelling to commands recommended for
the user to run.

Write the action plan using the project's existing plan convention. If there is
none, use a clearly named local `aws-action-plan.md` without overwriting an
unrelated file. Link it in the conversation and summarise the highlighted actions.
If a file cannot be written, present the complete plan in the conversation and
state that it was not saved. Writing the plan and its execution record is the
necessary documentation step; identify that local path, and do not treat it as
permission to write exports, credentials, configuration, or AWS resources.

Keep verified reads separate from highlighted non-read actions. Give each
non-read action its own stable ID and the following details; no catch-all steps
such as "apply the fixes" or "clean up afterwards":

```markdown
# AWS CLI action plan

Objective and read-only findings: ...
Context: profile, verified account/role, region, endpoint, environment
Plan file: ...
Execution mode: MANUAL — commands prepared for the user; not run by the agent
READ checks: commands, results, limitations

## A1 — **NON-READ — NOT EXECUTED** — action name
- Authorisation: REQUIRED, or the user's existing specific approval and scope
- Exact command: full arguments, resolved targets, and any input payload/diff
- Target and scope: resource IDs/ARNs, local paths, count and selection bounds
- Effect: before/after state, dependencies, cost, availability and access impact
- Risk: highlight **DESTRUCTIVE** / **IRREVERSIBLE** where applicable
- Preconditions: evidence and checks required immediately before execution
- Recovery: exact reversal steps and their own action IDs, or no safe reversal
- Verification: read-only checks and success/abort conditions
- Execution record: not run; later record time, result, and observed state
```

Use **UNKNOWN — BLOCKED — NOT EXECUTED** for unresolved actions and record what
must be established. Redact secrets without leaving target scope ambiguous. If
the exact command or affected set cannot yet be bounded, the plan is not ready
for execution. For bulk changes, record the reviewed target list or bounded
selection and counts; refresh it before execution and stop on unexpected drift.

## Present ready commands for manual execution

Show the commands directly in the conversation as Markdown, and include them in
the same action-plan file when one is required. A file link or a summary alone is
not enough. Mark the hand-off **READY FOR MANUAL EXECUTION — NOT EXECUTED**;
readiness describes a reviewed proposal, not permission for the agent to run it.

- Present commands in execution order, each in its own fenced `sh` code block
  without shell prompt characters. Above each block, give its action ID,
  `READ` / **`NON-READ`** classification, and a plain-language explanation of
  what it does, which targets it affects, and any writes or deletions. Keep the
  required non-read warning and destructive/irreversible labels prominent.
- Include the working directory, applicable profile and region, expected
  account/role, prerequisites, exact arguments, and required payloads. Resolve
  non-secret values and quote them for the intended shell. Never publish secrets.
  If values, payloads, permissions, or effects remain unresolved, label the
  affected command **DRAFT — NOT READY**, explain what is missing, and keep it
  separate from executable commands; do not present placeholders as ready code.
- Explain the expected result and when to stop after each command. Separate
  identity/preflight reads, previews, changes, and read-only verification so the
  user can inspect each result before proceeding. Keep conditional recovery and
  clean-up clearly separate from the normal sequence; never combine inspection
  and mutation into one paste-and-run block.
- For manual execution, finish the hand-off without running its actions or
  asking for permission to run them. Wait for the user to execute them or
  explicitly delegate execution.
  Record manual execution only from the user's report or observed evidence;
  providing commands is not evidence that they ran or succeeded.

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

## Examples that defeat name-based checks

These examples illustrate effects, not a complete allow-list. Recheck the exact
command, parameters, credential path, and surrounding shell before use.

| Command or pattern | Classification and reason |
| --- | --- |
| `aws ec2 describe-instances`, `aws s3api list-objects-v2` | `READ` when limited to inspection with verified context and no surrounding writes. |
| `aws sqs receive-message` | **NON-READ**: receiving affects message visibility and processing state; it is not a passive peek. See [AWS receive-message](https://docs.aws.amazon.com/cli/latest/reference/sqs/receive-message.html). |
| `aws s3api get-object ... output.bin`, S3 downloads, `... > file`, `... \| tee file` | **NON-READ**: local creation/overwrite counts even when the AWS API reads data. See [AWS get-object](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-object.html). |
| `aws s3 sync ... --delete` | **NON-READ**, **DESTRUCTIVE**: may copy, overwrite, and delete destination files/objects. A verified `--dryrun` is a separate preview, never approval for the real command. See [AWS sync](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html). |
| `aws cloudformation deploy ... --no-execute-changeset` | **NON-READ**: still creates a change set. See [AWS deploy](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/deploy.html). |
| `aws lambda invoke`, remote execution, job/query starts | **NON-READ** when they execute work, create jobs/results, or write files. A Lambda `DryRun` requires separate review, including its output destination. See [AWS invoke](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html). |
| `aws sso login`, credential/configuration changes | **NON-READ**: authentication/session and local configuration/cache effects must be planned. See [AWS login](https://docs.aws.amazon.com/cli/latest/reference/sso/login.html). |
