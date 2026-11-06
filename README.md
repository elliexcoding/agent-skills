# Agent Skills

Personal agent skills for use with Claude Code, Codex, and other coding-agent
workflows that understand a `SKILL.md` entry point.

This repository is intentionally small and portable. Each skill lives in a
top-level directory that can be copied or symlinked into the agent runtime.
Shared validation helpers live in `scripts/`.

## Skills

| Skill | Purpose |
| --- | --- |
| `agent-handoff` | Creates human-readable feature handoffs with supporting visuals and technical appendices, plus concise evidence-backed notes for resuming work across agents, sessions, or worktrees. |
| `adversarial-review` | Independently challenges software changes and agent completion claims with counterexamples, adverse-condition analysis, and evidence-backed findings. |
| `aws-cli-safety` | Starts AWS CLI work with verified reads, highlights every non-read operation in a written action plan, and presents ready commands with explanations in Markdown for manual execution. |
| `azure-cli-safety` | Applies read-only-first safeguards to Azure CLI and AzCopy, highlights every non-read operation in a written plan, and explains ready commands in Markdown for manual execution. |
| `code-review` | Performs senior-engineer code reviews with severity-ranked findings, concrete file references, validation gaps, and risk-focused review discipline. |
| `deslop` | Removes AI writing habits from prose while preserving meaning and tone; automatically polishes PR titles and descriptions before publication. |
| `eli5` | Explains topics, code, concepts, and errors at a requested level or for a specific audience, using familiar examples while preserving accuracy. |
| `fix-dependabot-alert` | Resolves one GitHub Dependabot security alert with a bounded slow loop, minimal dependency changes, explicit validation evidence, independent checking, and a human merge gate. |
| `github-pull-request` | Prepares, creates or updates GitHub pull requests with comment cleanup and prose editing before publication, impact and validation evidence, and visual walkthroughs for significant implementations. |
| `google-cloud-cli-safety` | Applies read-only-first safeguards to gcloud, bq, and gsutil, highlights every non-read operation in a written plan, and explains ready commands in Markdown for manual execution. |
| `grill-me` | Interviews the user about a plan, resolving design decisions one by one; available only through manual invocation. |
| `jev-file-scan` | Uses Jev with Codex and Claude Code to rank source snippets by semantic relevance, with local file selection and file/line references. |
| `harness-engineering` | Seeds shared Codex and Claude Code guidance through `AGENTS.md` and a `CLAUDE.md` import, plus architecture notes, quality gates, plans, decisions and technical-debt tracking. |
| `leetcode-coach` | Coaches LeetCode-style interview practice with questions, a graduated hint ladder, debriefs and mock interviews, withholding solutions unless the user asks to see them. |
| `no-comments` | Cleans redundant or stale comments before PR creation or branch pushes, preserving useful rationale, contracts and functional directives. |
| `refactor-safely` | Guides behavior-preserving refactors with explicit scope, characterization tests, small steps, validation, and reviewable change discipline. |
| `refreshing-linear-issues` | Records timestamped implementation updates in Linear issue bodies and posts a confirmation comment after the body change is verified. |
| `review-pull-request` | Returns read-only pull-request reviews directly in Codex, Claude Code or Pi, with evidence-backed findings and architecture and leadership guidance for development towards L5 and beyond. Includes Python, Rust, Kubernetes, Terraform and security lenses. |
| `rust-tech-lead` | Provides senior Rust engineering guidance for architecture, debugging, testing, performance work, and review. |
| `scope-software-task` | Turns ambiguous software changes into repository-grounded task contracts and independently verifiable implementation plans. |
| `show-me` | Provides general visual explanations on request using HumanLayer's unchanged skill, with diagrams, code sketches, and focused HTML artefacts. |
| `tdd` | Implements features and bug fixes through red, green and refactor cycles, with behaviour-focused tests and controlled external dependencies. |
| `teach` | Guides study through explicit probing, an evidence-based plan and dependency map, then adaptive teaching, transfer checks and reinforcement, with portable conversation fallbacks. |
| `temporary-claude-header-privacy` | Temporary instruction safeguard against private data in Claude-generated User-Agent headers; stops unsafe requests and defines verification before retirement. It is not a network filter. |
| `worktree-branch` | Creates meaningful task-based branches for new or detached agent worktrees so temporary work directories remain identifiable. |
| `writing-feature-comments` | Keeps feature comments concise and useful to human readers, explaining purpose, rationale, and verified concerns. |

## Repository Layout

```text
.
├── AGENTS.md
├── CLAUDE.md
├── agent-handoff/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── adversarial-review/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── aws-cli-safety/
│   ├── SKILL.md
│   └── agents/
├── azure-cli-safety/
│   ├── SKILL.md
│   └── agents/
├── code-review/
│   ├── SKILL.md
│   └── references/
├── deslop/
│   ├── SKILL.md
│   ├── LICENSE
│   └── agents/
├── eli5/
│   ├── SKILL.md
│   └── agents/
├── fix-dependabot-alert/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── github-pull-request/
│   ├── SKILL.md
│   └── references/
├── google-cloud-cli-safety/
│   ├── SKILL.md
│   └── agents/
├── grill-me/
│   ├── SKILL.md
│   └── agents/
├── harness-engineering/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── references/
│   └── scripts/
├── leetcode-coach/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── no-comments/
│   ├── SKILL.md
│   ├── LICENSE
│   └── agents/
├── refactor-safely/
│   ├── SKILL.md
│   └── references/
├── refreshing-linear-issues/
│   ├── SKILL.md
│   └── agents/
├── review-pull-request/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── rust-tech-lead/
│   └── SKILL.md
├── scope-software-task/
│   ├── SKILL.md
│   ├── agents/
│   └── references/
├── scripts/
│   ├── validate_skills.py
│   └── test_validate_skills.py
├── show-me/
│   ├── SKILL.md
│   ├── LICENSE
│   └── agents/
├── tdd/
│   ├── SKILL.md
│   ├── LICENSE
│   ├── agents/
│   └── references/
├── teach/
│   ├── SKILL.md
│   └── references/
├── temporary-claude-header-privacy/
│   ├── SKILL.md
│   └── agents/
├── worktree-branch/
│   ├── SKILL.md
│   └── scripts/
└── writing-feature-comments/
    ├── SKILL.md
    └── agents/
```

Each skill should keep `SKILL.md` as the main entry point. Supporting material is
optional and should live beside it:

- `references/` for longer guidance that should only be loaded when needed.
- `scripts/` for repeatable commands or helpers used by the skill.
- `assets/` for templates, starter files, examples, or reusable static content.
- `agents/` for tool-specific agent definitions or adapter metadata.

## Using These Skills

Use the skill directory as the unit of installation. For each agent runtime:

1. Copy or symlink the desired top-level skill directory into that tool's skills
   location.
2. Keep the directory name stable; it is the skill identifier for humans and
   tooling.
3. Make sure the entire directory is available, not just `SKILL.md`, when the
   skill depends on `references/`, `scripts/`, `assets/`, or `agents/`.

The skills are written to be readable by both Claude Code and Codex-style
systems. Tool-specific metadata should be additive and should not replace the
portable `SKILL.md` instructions.

The **temporary** `temporary-claude-header-privacy` skill addresses
[Claude Code issue #107757](https://github.com/anthropics/claude-code/issues/107757).
It is eligible for automatic selection; explicitly invoke
`/temporary-claude-header-privacy` in Claude Code before network work to load it.
It provides behavioural instructions, not guaranteed interception. Retire it
only after verifying the upstream fix and installed runtime as described in its
[SKILL.md](temporary-claude-header-privacy/SKILL.md).

## Claude Code and Codex Compatibility

Use `/skill-name` in Claude Code and `$skill-name` in Codex. Both read the shared
`SKILL.md`; Codex-specific UI settings belong in `agents/openai.yaml`.

Automatic selection is the default in both runtimes. To keep a skill manual-only,
set `disable-model-invocation: true` in its `SKILL.md` frontmatter and
`policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Keep the two
settings consistent. The [Claude Code invocation reference](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill)
and [Codex metadata reference](https://learn.chatgpt.com/docs/build-skills#optional-metadata)
describe the runtime-specific settings.

For shared project instructions, `CLAUDE.md` imports `AGENTS.md` using
`@AGENTS.md`. The harness template includes this bridge for older Claude Code
versions and configurations that do not load `AGENTS.md` directly. Existing
instruction files are preserved when seeding; merge a missing import during
an authorised update. See [Claude Code's shared instruction guidance](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).

These conventions target local Claude Code and Codex. Packaging for a different
product needs its own schema check; Claude-specific fields are not part of the
base Agent Skills upload schema. External tools, MCP connections and credentials
still need to be available in the runtime running the skill.

## Lazy Loading

This repository is designed for lazy loading:

- Agent runtimes should index skill names and descriptions for discovery.
- A skill's `SKILL.md` should be loaded only when the task matches that skill.
- Files in `references/`, `scripts/`, `assets/`, and `agents/` should be loaded
  or executed only when the active skill explicitly needs them.
- Do not paste every `SKILL.md` into a global `AGENTS.md`, `CLAUDE.md`, startup
  prompt, or tool configuration. That defeats the purpose of using skills and
  wastes context-window tokens.

When installing these skills, prefer copying or symlinking the top-level skill
directories into a tool-supported skills location over importing their full text
into a single global instruction file.

## Authoring Conventions

- Put one skill per top-level directory.
- Start every skill with `SKILL.md`.
- Keep the front matter concise: `name` and `description` should be enough for
  discovery.
- Keep default instructions practical and short. Move long rationale,
  background, examples, and optional workflows into `references/`.
- Prefer scripts for repeatable repository changes instead of long prompt-only
  procedures.
- Avoid committing generated caches, local environment files, logs, secrets, or
  model output transcripts.

## Maintaining Skill Performance

Optimise for useful instructions and reliable selection, not a word-count
target. Names and descriptions are loaded for discovery; bodies and references
should be loaded only when needed. Keep descriptions specific enough to separate
neighbouring workflows. Avoid loading generic review, PR review and language
review workflows together when one already covers the request.

Keep purpose, essential constraints, completion conditions and reference routing
in `SKILL.md`. Put substantial conditional procedures beside it and state when
they must be read. Preserve authorisation boundaries and fragile workflow
details; remove repeated advice and unconditional document or test sweeps.

This approach follows OpenAI's
[Astra skills guidance](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)
and Anthropic's
[skill authoring guidance](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
Anthropic's 500-line recommendation is an upper guideline, not a target or proof
that shorter always performs better. Its
[Opus 5.5 guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)
also recommends testing effort settings on actual tasks; prompt trimming alone
does not establish a latency or quality improvement.

For substantial changes, check explicit invocation, implicit selection, a nearby
request that should not trigger the skill, and a boundary or failure case. Check
the resulting decisions and artefacts, not just wording or file size. Compare
success, unnecessary reads/tool calls, latency and token use on the same tasks
and model settings before claiming performance gains. See OpenAI's
[skill evaluation guide](https://developers.openai.com/blog/eval-skills).

Keep existing explicit-only invocation policies intact. Treat upstream copies
and external symlinks as separate maintenance boundaries; local edits can be
lost on an upstream update.

## Validation

Before committing changes:

```sh
uv run --script scripts/validate_skills.py
git status --short
git diff --check
```

The checker declares its PyYAML dependency for `uv`. It can also run with
`python3 scripts/validate_skills.py` in an environment that has PyYAML installed.
Pass skill directories to check a subset, for example
`uv run --script scripts/validate_skills.py deslop github-pull-request`.

The checker validates names, descriptions, the supported shared frontmatter
fields, invocation parity and local Markdown links in `SKILL.md`. It includes
symlinked personal skills and excludes the runtime-managed `.system/` directory.
It does not execute workflows or prove service access. Use this checker for
repository compatibility instead of interpreting the bundled validator's
rejection of Claude-specific fields as a runtime failure.

When changing the validation or seeding helpers, run their regression checks
with PyYAML available for the compatibility tests:

```sh
python3 -B -m unittest discover -s scripts -p 'test_*.py'
python3 -B -m unittest discover -s harness-engineering/scripts -p 'test_*.py'
```

For skills that include scripts, also run the script's dry-run or help command
when available. For example:

```sh
python3 harness-engineering/scripts/seed_harness.py --help
python3 harness-engineering/scripts/seed_harness.py --target /path/to/repo --dry-run
```

## Notes

This is a personal skills repository rather than a packaged library. Stability
comes from keeping each skill self-contained, versioned, and easy to inspect.

The `show-me` skill files are copied unchanged from
[HumanLayer's skills repository at revision ca7c808](https://github.com/humanlayer/skills/tree/ca7c8088db69e315a8b2deea43820270457f8f3c/plugins/show-me/skills/show-me),
with its MIT licence included. It retains upstream's explicit-invocation policy.
The `github-pull-request` skill keeps its own context-sensitive presentation
guidance and significance gate.

The `tdd` skill is adapted from
[Matt Pocock's TDD skill at revision 5beb35b](https://github.com/mattpocock/skills/tree/5beb35b040e3de97e54fa9e386d7e42d15c295c2/skills/engineering/tdd),
with its MIT licence included. It adds refactoring after green, uses established
contracts to infer test boundaries without routine confirmation gates, and
keeps examples and guidance on test doubles in optional references.

The `deslop` skill is adapted from
[backnotprop/pstack's unslop skill at revision f51fdeb](https://github.com/backnotprop/pstack/blob/f51fdeba3d803ef90e4eaa4a95ffb4e76008ab37/skills/unslop/SKILL.md),
with its MIT licence included. It retains the upstream rule numbers, enables
automatic selection for PR preparation as well as explicit invocation, uses
British English, and preserves facts, necessary uncertainty, code, URLs and
exact quotations when editing prose. Required PR template fields and validation
evidence are preserved.

The `no-comments` skill is adapted from
[backnotprop/pstack's no-comments skill at revision f51fdeb](https://github.com/backnotprop/pstack/blob/f51fdeba3d803ef90e4eaa4a95ffb4e76008ab37/skills/no-comments/SKILL.md)
and its comment-review guidance, with the MIT licence included. It is
self-contained and automatically selectable. Unlike upstream, it preserves
useful internal rationale, unverified constraints and functional directives,
and keeps structural fixes within the authorised scope.

Install `github-pull-request` together with `no-comments` and `deslop`. The PR
workflow checks code comments before committing and pushing, then polishes the
PR title and description before creation or publication of revised text.
This is an agent workflow instruction, not a Git hook; it does not intercept
pushes made directly in a terminal.
