# Action plan and command hand-off

Read before proposing any non-read or uncertain action, or presenting ready
commands for manual execution. These requirements also apply when execution
has already been delegated.

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
