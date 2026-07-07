---
name: agent-handoff
description: |
  Create production-quality handoffs between AI agents, Codex threads, Claude
  Code sessions, worktrees, or humans. Use when pausing work, switching context,
  handing off between local and worktree environments, compacting context,
  escalating a blocker, or leaving durable execution notes for another agent.
---

# Agent Handoff

## Role

Create a concise, evidence-backed handoff that lets the next agent or engineer
continue without rediscovering the task from scratch.

The handoff must preserve execution state, not just summarize conversation. It
should state what was requested, what changed, what was verified, what remains,
and the safest next action.

## When To Use

Use this skill when:

- Pausing before the task is complete.
- Switching between Codex, Claude Code, another agent, or a human engineer.
- Moving a thread between local checkout and worktree.
- Context is about to be compacted or lost.
- A task is blocked by missing input, failing infrastructure, permissions, or
  unclear product intent.
- Work is complete but the next step is review, PR creation, deployment, or
  follow-up validation.

## Source-Informed Principles

This skill follows these production agent practices:

- Treat the agent like a teammate: give explicit context and a clear definition
  of done.
- Preserve verifiable evidence: include commands run, outputs observed, changed
  files, and validation status.
- Keep durable instructions small and reusable; put repeatable workflows in
  skills or repository guidance instead of relying on long prompts.
- Make uncertainty explicit. If tests failed, could not run, or were skipped,
  say exactly why.
- Keep human review in the loop for agent-generated code before integration.

For the rationale and source links, read
`references/handoff-principles.md` when changing this skill.

## Default Workflow

1. Capture repository state:
   - `git status --short --branch`
   - `git branch --show-current`
   - `git rev-parse --short HEAD`
   - `git diff --stat`
   - relevant `git diff` or file reads
2. Reconstruct the task:
   - original request
   - current objective
   - constraints and decisions made
   - user preferences or project instructions that still matter
3. Capture execution evidence:
   - files changed
   - commands run
   - tests, linters, type checks, builds, manual checks
   - failures and partial results
4. Identify continuation state:
   - completed work
   - remaining work
   - known blockers
   - risks and assumptions
   - safest next command or action
5. Write the handoff using the template below.
6. If the handoff will be consumed later, save it in the repository's preferred
   planning or notes location. If no convention exists, put it in the final
   response instead of creating a random file.

## Helper Script

Use the helper script to collect mechanical git context:

```sh
python3 <skill-dir>/scripts/collect_handoff_context.py --objective "<task summary>"
```

Useful options:

```sh
# Compare against a base branch or commit
python3 <skill-dir>/scripts/collect_handoff_context.py --objective "<task>" --base main

# Save a markdown scaffold
python3 <skill-dir>/scripts/collect_handoff_context.py --objective "<task>" --output handoff.md
```

The script produces a scaffold. Fill in the human judgment sections before
handing off.

## Handoff Format

Use this structure:

```markdown
## Objective
One sentence describing the requested outcome.

## Current State
- Branch/worktree:
- Commit:
- Status:
- Completed:
- In progress:

## Changed Files
- `path`: what changed and why

## Validation
- `command`: result
- Not run: reason and residual risk

## Decisions And Rationale
- Decision: reason

## Blockers Or Risks
- Risk/blocker: impact and recommended handling

## Next Steps
1. Immediate next action
2. Follow-up action
3. Final verification or handoff target

## Notes For Next Agent
- Relevant instructions, assumptions, user preferences, or context traps
```

## Quality Bar

A good handoff is:

- Specific: names files, commands, branches, commits, and concrete next steps.
- Honest: distinguishes done, partial, unverified, and blocked work.
- Short: enough to continue, not a transcript.
- Ordered: next action is obvious.
- Verifiable: points to evidence, not vague confidence.
- Safe: warns about destructive commands, secrets, migrations, deploys, and
  user-visible behavior changes.

## Receiving A Handoff

When continuing from a handoff:

1. Read the handoff fully before editing.
2. Verify current repository state against the handoff.
3. Re-run or inspect the most relevant failing or passing check before changing
   more code when practical.
4. Preserve user changes that happened after the handoff.
5. Update the handoff or final response with anything that changed.

## Anti-Patterns

- "Mostly done" without listing what remains.
- "Tests pass" without command names.
- "Need to fix errors" without the exact failing command or symptom.
- Large conversation summaries that omit current git state.
- Hiding uncertainty to make the work sound cleaner.
- Creating a handoff file in an unexpected location when a final response would
  be clearer.
