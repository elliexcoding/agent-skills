---
name: worktree-branch
description: |
  Ensure new agent worktrees use meaningful task-based Git branches instead of
  detached HEAD commits. Use immediately after creating or entering a worktree,
  especially when the prompt, task, or request can be summarized as a branch
  name.
---

# Worktree Branch

## Role

When an agent starts work in a new Git worktree, make the worktree identifiable
by creating a task-based branch if the checkout is detached.

This is intended for Codex, Claude Code, and similar tools that create temporary
worktrees such as:

```text
/Users/kraise/.codex/worktrees/6902/rust-lab cd2f4ae (detached HEAD)
```

After this skill runs, the worktree should be on a branch such as:

```text
codex/add-rust-lab-test-harness
```

## Trigger Guidance

Use this skill at the beginning of a task when any of these are true:

- A new worktree was just created.
- `git status` or the shell prompt shows `detached HEAD`.
- The worktree path is under an agent-managed worktree directory.
- The user asks to start a task, implement a request, fix a bug, or prepare a
  change in a fresh worktree.

The skill cannot force Codex, Claude Code, or another agent runtime to call it
automatically. To get automatic behavior, configure the agent or its startup
instructions to load this skill whenever a worktree is created or entered.

## Default Workflow

1. Inspect the worktree:
   - `git status --short --branch`
   - `git rev-parse --abbrev-ref HEAD`
   - `git rev-parse --short HEAD`
2. If already on a named branch, keep it unless the user asks to rename it.
3. If detached, derive a concise branch name from the task or request.
4. Create a branch at the current commit before editing files.
5. Report the branch name to the user.

## Helper Script

Prefer the helper script from this skill directory:

```sh
python3 <skill-dir>/scripts/ensure_worktree_branch.py --task "<task summary>"
```

Useful options:

```sh
# Preview the generated branch without changing Git state
python3 <skill-dir>/scripts/ensure_worktree_branch.py --task "<task summary>" --dry-run

# Use a different prefix
python3 <skill-dir>/scripts/ensure_worktree_branch.py --task "<task summary>" --prefix claude

# Allow renaming the current named branch when explicitly requested
python3 <skill-dir>/scripts/ensure_worktree_branch.py --task "<task summary>" --rename-current
```

## Branch Naming Rules

- Default prefix: `codex/`.
- Use the repository or user convention when one exists.
- Use lowercase kebab-case for the task slug.
- Keep names specific but short:
  - Good: `codex/add-pr-quality-skill`
  - Good: `codex/fix-seed-harness-existing-docs`
  - Bad: `codex/update`
  - Bad: `codex/fix-stuff`
- Avoid ticket IDs unless the task or repository convention includes them.
- Avoid secrets, customer names, private data, or sensitive incident details in
  branch names.

## Manual Fallback

If the helper script is unavailable, use this pattern:

```sh
git switch -c codex/<task-slug>
```

If `git switch` is unavailable:

```sh
git checkout -b codex/<task-slug>
```

If the branch already exists, add a short commit hash or focused suffix:

```sh
git switch -c codex/<task-slug>-<short-sha>
```

## Safety Rules

- Create the branch before making edits.
- Do not overwrite, delete, reset, or rename an existing branch unless the user
  explicitly asks.
- Do not create a branch from the wrong repository or parent worktree.
- Do not include raw user prompts when they contain private or sensitive data.
- If the current state is confusing, report the current branch, commit, and
  working tree status before changing anything.

## Output Expectations

After running this skill, report:

- Whether the worktree was detached.
- The branch name created or reused.
- The commit the branch points to.
- Any reason a branch was not created.
