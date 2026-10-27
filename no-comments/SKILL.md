---
name: no-comments
description: Remove redundant, stale and task-narrating code comments from a scoped diff while preserving useful constraints and required directives. Use for comment cleanup and before creating a PR or pushing code to a new or existing PR. Read-only reviews and PR-metadata-only edits do not authorise source changes.
---

# No comments

Keep comments only when they give readers information the code cannot clearly
provide. Remove narration and obsolete explanations without changing behaviour
or losing the reason for a constraint. This is a focused pass over the change,
not a requirement to eliminate every comment.

## Establish the scope

Use the caller's files or diff. Before PR creation or a push, identify the
current branch, working-tree state, intended remote and actual PR base. Prefer
the caller's base or the existing PR's base; otherwise verify the remote default
branch. Do not assume `main` or compare only with the branch's upstream, which
can omit changes already pushed to the PR.

Inspect the branch diff from its merge base with the target branch, together
with staged and unstaged changes that belong to the requested work. Include new
files only when they are part of that work. Preserve unrelated user changes and
partial staging. A comment can be in scope when it was added or edited, or when
the changed code makes its explanation stale; a changed file alone does not
authorise deleting all its comments.

For a read-only review, request for PR text only or request for suggestions,
report proposed edits without changing files. Creating a GitHub draft PR still
publishes code and calls for this pass. Skip it for PR title, description or
label changes that do not publish code. The skill does not itself authorise a
commit, push, PR creation or merge.

## Inspect before deleting

Read the surrounding code, relevant callers and tests. Classify each candidate
using the evidence available:

- **Remove:** Restatements of obvious code, decorative banners, duplicate
  explanations, commented-out experiments, development diaries and claims
  demonstrably made obsolete by the change. Keep section labels when they help
  readers navigate a structure that the code does not otherwise make clear.
- **Keep:** Legal notices and licence headers, public API contracts, useful
  rationale, safety or concurrency invariants, and constraints imposed by a
  dependency, platform, protocol or business rule. Keep issue or specification
  links when they explain such a constraint. A useful explanation of our own
  code can also qualify; external origin is not a prerequisite.
- **Investigate:** Workaround explanations, `IMPORTANT`, `do not remove`, TODOs
  and claims whose truth is unclear. Check the named symbol and relevant
  evidence. If the constraint is unverified, retain it and report what needs
  checking. Do not erase uncertainty by deleting its only documentation.

Treat compiler, type-checker, linter, formatter, coverage, build and code
generation directives as functional input. Shebangs, encoding declarations,
SQL hints and similar comment syntax can affect execution. Inspect their role
before changing them. Do not remove `@ts-expect-error` from a negative type test
or remove a suppression simply because suppressions look undesirable. An
obsolete directive may be removed only when relevant checks establish that it
is no longer needed; a suppression hiding a defect requires a proper fix.

Docstrings and documentation comments can be runtime data, API documentation
or executable examples. Preserve those contracts and do not treat comment-like
text in strings, fixtures or Markdown as removable source comments. Follow
repository rules for generated and third-party files.

## Make the smallest useful edit

Delete comments that add no lasting information. Shorten or correct a useful
comment when its wording is the problem. Keep the enduring reason in plain
language, consistent with the repository's comment conventions.

When a comment reveals a confusing name, hidden invariant or workaround, name
the exact code and propose the smallest improvement. Implement a refactor or
encode a constraint in a type, test or runtime check only when that change fits
the existing authorised scope and can be validated. Otherwise retain the
necessary explanation and report the follow-up. A check before pushing must
not silently become a redesign or remove a guard that still protects behaviour.

Use a fresh pass over the scoped diff after editing. Do not use a blanket regex
stripper or a deletion quota. No changes is a valid result when every comment
earns its place.

## Verify before publication

Check the final diff for lost rationale, unintended code edits, syntax changes
and whitespace errors. Run the affected checks and the checks required by the
repository. Use parsing, linting, type checking, documentation checks or tests
according to what changed. Do not add tests that merely assert comment wording.

Perform this pass before the final commit and push when possible. If the work
is already committed, include accepted cleanup in a normal follow-up commit
when committing is part of the authorised workflow. Do not amend published
history or force-push merely to tidy comments. Never stage unrelated changes.

Verify that the commits to be pushed contain the accepted cleanup; edits left
only in the working tree are not part of a push. If the workflow does not permit
including them, report the pending edits before publication. If code or
comments change after the pass, inspect those changes and refresh affected
validation before publishing. A failed check caused by cleanup must be fixed
or the affected cleanup reverted before proceeding.

Report what was removed or revised, what was deliberately retained, relevant
checks and any open constraints or suggested code fixes. Include deletion
counts only when verified. Do not claim a push or PR creation unless it was
separately requested and completed.

Adapted from [backnotprop/pstack's no-comments skill](https://github.com/backnotprop/pstack/blob/f51fdeba3d803ef90e4eaa4a95ffb4e76008ab37/skills/no-comments/SKILL.md)
and its comment-review guidance. The upstream MIT licence is included in
[LICENSE](LICENSE). This adaptation is self-contained, permits automatic
selection before PR publication, and preserves unverified constraints and
functional directives until a justified, validated change is available.
