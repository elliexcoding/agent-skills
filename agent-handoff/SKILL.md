---
name: agent-handoff
description: Prepare feature handoffs or continuation notes when transferring work between people, agents, sessions or worktrees.
---

# Agent Handoff

Write for a reader who has not seen the conversation. They should understand
the intended outcome, expected behaviour, decisions, current progress, and next
action. Human readability is an acceptance criterion for every handoff.

## Choose the Depth

| Request | Document |
| --- | --- |
| Feature development, design-to-engineering transfer, or a rich handoff | Read [Feature handoffs](references/feature-handoff.md). Lead with purpose and experience; put execution evidence in an appendix. |
| Pause, context transfer, worktree move, blocker, or routine continuation | Use the concise continuation structure below. |
| Both | Write one feature handoff with a continuation appendix. |

Infer the audience and depth from the request and existing context. Ask only
when missing information materially changes the deliverable.

## Shared Workflow

1. Gather the request, relevant source material, decisions, implementation, and
   evidence. For repository work, inspect status, branch/worktree, commit, and
   relevant diffs. Identify supplied evidence separately from checks performed
   during preparation.
2. Distinguish agreed requirements, observed behaviour, proposals, assumptions,
   and unresolved questions. Explain important decisions and their reasons.
   Name completed, partial, unverified, and blocked work precisely.
3. Write in plain language with descriptive headings and connected paragraphs.
   Use lists for actions and tables for comparisons. Define unfamiliar terms.
   Keep detailed commands and logs beside their evidence in the technical
   section; summarise their practical implications in the main narrative.
4. Save in the user's requested location or the repository's established
   convention. For feature handoffs without a convention, use
   `docs/handoffs/<feature-slug>/handoff.md` with companion `assets/`.
   For brief continuation notes without a file request or convention, the
   final response is sufficient.
5. Read the result independently of the chat. Verify factual claims, links,
   visual labels, completion status, and actionable next steps. Return a link
   to the saved document and identify consequential gaps.

## Concise Continuation

Use these headings, combining empty or overlapping sections:

- **Objective:** requested outcome and scope.
- **Current state:** branch/worktree, commit, completed and unfinished work.
- **Changed files:** relevant paths and why they changed.
- **Validation:** commands or manual checks, results, omissions and impact.
- **Decisions and rationale:** choices the next person must preserve.
- **Blockers or risks:** impact and the input or action needed.
- **Next steps:** immediate action, follow-up, and verification.
- **Notes for the recipient:** applicable instructions and context traps.

The optional helper collects Git evidence:

```sh
python3 <skill-dir>/scripts/collect_handoff_context.py --objective "<task summary>"
```

Use `--help` for options. Its output is an unfinished mechanical scaffold;
curate it into the document or appendix before delivery.

## Receiving a Handoff

Read it fully, verify current state against its evidence, and inspect or rerun
the relevant check before editing when practical. Preserve newer user changes
and record material differences.

## Common Mistakes

- A transcript or raw helper output in place of a readable document.
- Proposed screens presented as screenshots or approved requirements.
- A passing check treated as proof of untested behaviour.
- Visuals or essential context available only in temporary session storage.

Read [Handoff principles](references/handoff-principles.md) when maintaining
this skill or assessing its evidence standards.
