---
name: refreshing-linear-issues
description: Use when refreshing or updating a Linear issue after a code change, implementation, fix, or follow-up needs to be recorded for engineers. Do not use for ordinary triage or status-only changes.
---

# Refreshing Linear Issues

## Overview

Make the issue body the durable implementation record and use a separate comment
to announce that the refresh succeeded. Preserve the original issue content and
calibrate every completion claim to evidence.

## Refresh Contract

1. Resolve one exact issue and fetch its latest body immediately before editing.
   A direct request to refresh that issue authorises the body update and one
   confirmation comment, but not changes to status, labels, assignee, or scope.
2. Gather the implemented behaviour, affected components, validation results,
   references such as a commit or pull request, and any remaining work. Do not
   infer evidence from the requested wording.
3. Generate the current timestamp at write time in ISO 8601 format, including
   seconds and a numeric timezone offset, for example
   `2026-09-01T14:30:00+09:00`. Never reuse a stale or invented timestamp.
4. Prepend the block below with a partial description patch. Preserve the
   existing body and earlier implementation blocks exactly beneath it.
5. Read the issue back and verify both the new block and preserved content.
6. Only after verification, post one top-level comment using the same timestamp,
   status, and summary.

## Body Block

```markdown
## Implementation update — <YYYY-MM-DDTHH:MM:SS±HH:MM>

**Status:** <Implemented | Partially implemented | Implementation unverified>
**Summary:** <concise engineer-facing outcome>
**Changes:** <behaviour or components changed>
**Validation:** <checks and results, or Not run>
**References:** <PR, commit, deployment, or None>
**Outstanding:** <None or remaining work and risks>
```

Choose the status from evidence:

| Status | Use when |
| --- | --- |
| `Implemented` | The described work is complete and relevant validation passed. |
| `Partially implemented` | Some requested work remains; name it under `Outstanding`. |
| `Implementation unverified` | A change exists or is reported, but validation is absent, failing, or inconclusive. |

## Confirmation Comment

```markdown
Issue refreshed at <timestamp> — **<status>**. <summary> Details, validation, references, and outstanding work are recorded in the issue body.
```

Use `refreshed`, not `shipped` or `deployed`, unless release evidence supports
that stronger claim.

## Example

```markdown
## Implementation update — 2026-09-01T14:30:00+09:00

**Status:** Implemented
**Summary:** Worker retries now stop before they overload the downstream service.
**Changes:** Updated the retry policy in `src/worker.ts`.
**Validation:** `npm test -- worker` passed.
**References:** Commit `abc123`.
**Outstanding:** None.
```

## Failure Handling

- If the body update fails, do not post the comment.
- If the comment fails after a verified body update, report partial completion.
- When an outcome is ambiguous, re-fetch the issue and recent comments before
  retrying; never create duplicate blocks or comments speculatively.

## Common Mistakes

Do not replace the whole body when a prepend patch is available, rewrite
acceptance criteria, erase prior update blocks, omit the timezone, report
`Implemented` without passed validation, or post the comment before readback.
