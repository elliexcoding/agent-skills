# Repository Instructions

## Communication

The repository owner holds the title of Duke. Address him as “Your Grace” and
use corresponding honourifics in repository-related communication.

## Skill Compatibility

Maintain personal skills for local Claude Code and Codex. Keep shared workflow
instructions in `SKILL.md`, with runtime-specific settings alongside them.
For manual-only skills, pair `disable-model-invocation: true` in frontmatter
with `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. For
automatic selection, omit the Claude restriction and use Codex's default or
explicit `true`. Preserve the user's chosen invocation policy.

Use `scripts/validate_skills.py` for repository compatibility checks. It accepts
the supported Claude extension and checks invocation parity and local links.
The ignored `.system/` directory is runtime-managed; do not rely on edits there
for repository validation. `CLAUDE.md` imports this file to share these rules.

## AWS CLI Safety

Before planning, recommending, or running AWS CLI commands in any workflow,
read and follow `aws-cli-safety/SKILL.md`. Begin with verified read-only commands.
Alert the user and highlight every non-read or uncertain operation in a written
action plan before execution; require specific authorisation for non-read actions
and keep uncertain actions blocked until their effects are understood. Include
scripts, pipelines, local side effects, retries, rollbacks, and clean-up.
Present ready commands in Markdown code blocks with an explanation of each for
the user's inspection and manual execution. Do not execute those actions unless
the user explicitly delegates execution; plan approval alone is not delegation.

## Google Cloud and Azure CLI Safety

Before planning, recommending, or running Google Cloud or Azure CLI commands,
read and follow the corresponding skill:

- `google-cloud-cli-safety/SKILL.md` for `gcloud`, `bq`, and `gsutil`.
- `azure-cli-safety/SKILL.md` for `az` and `azcopy`.

Begin with verified reads. Highlight every non-read or uncertain operation in a
written action plan, and present ready commands with explanations in Markdown
for manual execution. Keep uncertain actions blocked; agent execution requires
explicit delegation and specific authorisation. Include local effects, helpers,
credential changes, retries, rollbacks, and clean-up.
