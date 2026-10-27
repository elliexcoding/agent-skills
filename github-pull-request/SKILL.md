---
name: github-pull-request
description: Prepare, create or update GitHub PRs, including pushing branch updates, with impact and validation evidence. Use for PR preparation and publication, not code review alone.
---

# GitHub Pull Request

Prepare a PR that explains the problem, resulting behaviour and evidence to a
reviewer who has not seen the conversation. Assess blast radius for every PR.

## Prepare the evidence

Establish the repository, current branch, working-tree state and comparison
base. Prefer the user-specified base, otherwise verify the remote default;
branch names alone are not evidence. Inspect the final diff, relevant commits,
consumers and existing validation results. Preserve unrelated user changes.

## Check comments before publication

Before creating a PR or pushing code to a new or existing PR, apply
[no-comments](../no-comments/SKILL.md) to the scoped change. Run it before the
final commit and validation so accepted cleanup is included in the commits
being published. Verify the outgoing commit diff; working-tree edits alone
will not be pushed. Do not rewrite published history merely for this cleanup.
Reuse a completed comment pass when its scoped diff is unchanged.

For requests for PR text only or read-only reviews, report suggestions without
editing source. Creating a GitHub draft PR still calls for this pass. Skip
comment cleanup for PR-metadata-only changes. If the skill is unavailable,
report that the pass was skipped rather than claiming it ran. Keep the source
change, validation and PR description consistent after any accepted edits.

## Validate the final change

Run missing checks required by the repository or justified by the change. Avoid
repeating successful checks on unchanged code without a new concern. Record
exact commands, results and material omissions without implying they ran.

## Blast radius and review depth

Assess reach, consequences, recovery and uncertainty from code and consumers.
Include downstream contracts, persisted state, external effects, rollout
exposure and what reverting code cannot undo. A disabled flag does not make a
new feature routine. Use the highest applicable depth for mixed work.

| Depth | Evidence and review focus |
| --- | --- |
| **Routine** | Bounded maintenance with understood reach, no material behavioural, contract, data, security or operational change, relevant checks and straightforward recovery. Keep review concise. |
| **Focused** | A bounded feature or behaviour change, nontrivial refactor, or uncertainty that prevents routine treatment. Identify decisions and affected paths needing judgement. |
| **Critical** | Material risk to permissions, isolation, data integrity, payments, public compatibility, shared infrastructure or availability; broad impact or difficult recovery. Explain failure modes, missing evidence and rollout decisions for domain reviewers. |

Size, package versions and labels do not determine risk. Before treating a
compatible dependency update as routine, inspect release notes, lockfile changes
and affected usage. Unknown reach or material missing validation prevents routine
classification. Give a short evidence-backed reason for the selected depth.

Classification is a recommendation, not merge authority. Preserve CODEOWNERS,
required checks, branch protection and human merge gates. Do not request
reviewers, enable auto-merge or change protections merely because of a category.
Use [the quality checklist](references/pr-quality-checklist.md) for focused or
critical changes, applying only its relevant checks.

## Walkthrough gate

Include a **Reviewer walkthrough** for:

- A new endpoint, public interface or materially changed API contract.
- A substantial user journey, business rule, algorithm or state transition.
- A structural change to service interactions, ownership, data flow or trust
  boundaries that reviewers need to understand.

For these changes, or an explicit request, read
[the walkthrough guide](references/reviewer-walkthrough.md) and produce the
smallest useful view. Otherwise omit it. A version upgrade or high risk alone
does not require a visual; assess any associated contract or architecture change
against the gate separately.

## Write the PR

Use a specific title describing the main outcome, ideally within 72 characters.
Follow repository title and issue-ID conventions. Describe the final diff,
including scope changes, rather than the conversation or abandoned approaches.

Use the repository template, preserving required fields. Always include
**Blast radius** (or a labelled subsection of the template's risk section) and
**Validation**. Without a template, a short summary plus those two sections is
enough for routine work. Expand only where review needs it:

- **Summary:** Problem and resulting behaviour.
- **Blast radius:** Review depth and reason, affected users/systems,
  consequences, recovery and uncertainty.
- **Validation:** Checks actually run and results; omitted checks and impact.
- **Review notes:** Consequential decisions and paths, when useful.
- **Reviewer walkthrough:** Only when the gate applies or requested.

Remove empty sections and drafting comments. Summarise logs; use screenshots or
before/after examples when they clarify behaviour. Do not claim uninspected
consumers are unaffected.

## Polish the PR text

After drafting the title and body, apply [deslop](../deslop/SKILL.md) before
creating the PR, including a GitHub draft PR. Apply it again to revised PR text
before publishing an update; reuse the previous pass if the text is unchanged.
For a request for PR text only, return the polished draft without publishing it.

Keep required template headings and fields, issue identifiers, links, code,
commands, validation results, risk statements and necessary uncertainty intact.
Remove filler and awkward phrasing without inventing evidence, weakening a
caveat or dropping a required section. Check that the polished text still
describes the final diff and checks actually run. This pass covers the PR title
and body; it does not authorise rewriting unrelated repository documentation.
If the skill is unavailable, report the skipped pass rather than claiming it ran.

## Create, update or deliver

For a request for PR text only, return the proposed title and body with remaining
material gaps. When creation is requested, establish the base/head and use an
available GitHub tool or CLI. With the CLI, write the exact body to a file:

```sh
gh pr create --title "<title>" --body-file <body-file>
```

For a requested update, identify the existing PR, its base/head branches and the
intended remote before pushing. Complete the comment pass and affected checks
on the outgoing changes. Use the authorised commit and push workflow, then
verify the remote head matches the intended local commit. Refresh the PR title
and body when the resulting scope or validation evidence has changed, applying
the prose pass above before publishing the revised text.

Report the created or updated PR link, branches, validation and remaining review
risks. Creating or updating the PR does not authorise merging it.
