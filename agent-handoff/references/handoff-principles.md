# Agent Handoff Principles

These principles are adapted for local AI-agent engineering workflows using
Codex, Claude Code, and similar tools.

## Source Notes

- OpenAI Codex documentation says Codex works best when treated like a teammate
  with explicit context and a clear definition of done:
  https://developers.openai.com/codex/workflows
- OpenAI's Codex release notes emphasize verifiable evidence through terminal
  logs and test outputs, and the need for manual review before integration:
  https://openai.com/index/introducing-codex/
- OpenAI Codex best practices recommend asking Codex to create tests when
  needed, run checks, confirm the result, and review the work before accepting
  it:
  https://developers.openai.com/codex/learn/best-practices
- OpenAI Codex AGENTS.md guidance describes durable layered instructions for
  consistent task expectations:
  https://developers.openai.com/codex/guides/agents-md
- OpenAI Codex worktree documentation describes Local/Worktree handoff as a way
  to move work safely between checkouts:
  https://developers.openai.com/codex/app/worktrees

## What A Handoff Must Preserve

An agent handoff is not a status update. It is the execution state required to
resume work safely.

Preserve:

- Objective: what outcome the user wants.
- Scope: what repository, branch, worktree, files, and constraints matter.
- Evidence: commands run, outputs observed, tests passed or failed, and relevant
  diffs.
- Decisions: why the current approach was chosen.
- Continuation: the next safest action and how to verify it.
- Risk: blockers, uncertainty, data concerns, migrations, deploy impact, and
  unresolved review items.

## Completion States

Use precise language:

- `Complete`: implementation and relevant validation are done.
- `Ready for review`: implementation is done, but human review or PR creation
  remains.
- `Partially complete`: some implementation exists, with named remaining work.
- `Blocked`: no meaningful progress can continue without named input or an
  external-state change.
- `Abandoned approach`: a path was tried and rejected; record why so the next
  agent does not repeat it.

## Evidence Standards

For every validation claim, include the command or check.

Good:

```text
Validation:
- `cargo test --workspace`: passed
- `cargo clippy --workspace --all-targets`: not run; clippy is not installed in
  this environment
```

Weak:

```text
Validation:
- Tests look fine
```

If a command failed, preserve the exact failing command and the shortest useful
symptom. Do not paste huge logs unless they are necessary.

## Next-Agent Checklist

Before handing off, confirm:

- The current branch/worktree is named.
- `git status --short --branch` was checked.
- Changed files are listed with intent.
- Validation status is explicit.
- The next step is ordered and actionable.
- Blockers identify the owner or required input.
- No secrets or private data are included in the handoff.
- The handoff can be read independently of the previous conversation.
