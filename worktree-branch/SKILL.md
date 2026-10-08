---
name: worktree-branch
description: Create a meaningful task branch when starting implementation in a new or detached agent worktree. Preserve existing named branches.
---

# Worktree Branch

When starting implementation in a new agent worktree, create a task-based branch
at the current commit if HEAD is detached. Preserve an existing named branch.
A read-only review or deliberate detached inspection does not need a branch.

## Use the helper

Verify the intended worktree, branch/commit and working-tree status. Run the
helper from that worktree, resolving the script path from this skill directory:

```sh
python3 <skill-dir>/scripts/ensure_worktree_branch.py --task "<task summary>"
```

Use `--dry-run` to preview. The default prefix is `codex/`; use `--prefix` when
the user or repository specifies another convention. Use `--rename-current`
only when the user explicitly requests renaming an existing branch.

Keep the slug short and tied to the outcome, such as
`codex/fix-seed-harness-existing-docs`. Include a ticket ID when the task or
repository convention calls for it. Exclude secrets, customer information and
sensitive incident details; do not pass a raw private prompt as the task text.

## Fallback and boundaries

If the helper is unavailable, create the branch with `git switch -c` at the
verified current commit (`git checkout -b` on older Git). For a name collision,
choose a focused suffix; do not overwrite or reset an existing branch.

Create the branch before implementation edits. Do not delete, reset or rename
other branches, change the base, or operate on the parent worktree by mistake.
If the repository or commit is unclear, resolve that before changing Git state.

Report whether HEAD was detached, the branch created or retained and its commit,
or the reason no branch was created. This skill does not install startup hooks
or create a new worktree.
