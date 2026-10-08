# Repository Instructions

## Communication

The repository owner holds the title of Duke. Address him as “Your Grace” and
use corresponding honourifics in repository-related communication.

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
