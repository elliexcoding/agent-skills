---
name: plannotator
description: Use the Plannotator CLI when the user requests its plan, code or document review UI, annotations, saved decisions or Guided Reviews.
---

# Plannotator

Plannotator opens a local review UI and returns the human's decision or feedback
on stdout. Use the CLI contract, not browser scraping. Launch only the surface
the user requested; read its reference before selecting flags.

## Choose the workflow

| Request | Entry point and required reference |
| --- | --- |
| Review a plan through the host's native plan flow | Let the configured plan-exit hook launch it; never run bare `plannotator`. |
| Review local code or a PR/MR | `plannotator review`; read [review options and output](references/review.md). |
| Annotate a file, URL, folder or running app | `plannotator annotate <target>`; read [annotation options](references/annotate.md). |
| Approve or gate a saved plan/spec/document | `plannotator annotate <file> --gate --json`; read [annotation decisions and gates](references/annotate.md). |
| Annotate the last assistant message | `plannotator last`; read [last-message commands](references/other-commands.md#plannotator-annotate-last). Do not send a preamble first: it would become the selected message. |
| Browse archived decisions, manage sessions, export/share a guide or adjust integration | Read the relevant section of [other commands](references/other-commands.md). |

Use `plannotator <command> --help` when unsure. Do not guess flags. Source files
belong in code review; `.env` files must not be submitted for annotation because
history copies the content. Plain `annotate` has no approval button.

## Sessions and decisions

For host timeouts, plaintext output or hook integration, consult the
[session contract](references/other-commands.md#session-model).

A review session can remain open for a long time. Use a background-capable tool
or suitable process timeout and await its output; do not terminate it merely to
finish the agent turn. If a time limit ends a session, say so. Reopening the same
command restores annotation drafts; a closed session supplies no approval.

With `--json`, classify the outcome using `decision`, not text matching:

- Review returns `decision` and CLI-rendered `message`.
- Annotate returns `decision` and optional raw `feedback`.
- Decisions are `approved`, `annotated` or `dismissed`. Approval can include
  guidance; notes alone do not turn approval into rejection.

Use `--hook` only in a real hook context. Do not start a strict approval gate
unless a human is available to review. Read the annotation reference for strict
exit-code semantics; an exit code alone normally does not convey a decision.

Address returned feedback in the same conversation. Uploading a guide, exposing
a session through Tailscale, changing configuration or uninstalling software
requires scope covering that action; opening a local review alone does not.
