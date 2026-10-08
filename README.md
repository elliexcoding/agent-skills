# Agent Skills

Personal agent skills for use with Claude Code, Codex, and other coding-agent
workflows that understand a `SKILL.md` entry point.

This repository is intentionally small and portable. Each top-level directory is
a standalone skill that can be copied, symlinked, or packaged into whichever
agent runtime is being used.

## Skills

| Skill | Purpose |
| --- | --- |
| `agent-handoff` | Creates human-readable feature handoffs with supporting visuals and technical appendices, plus concise evidence-backed notes for resuming work across agents, sessions, or worktrees. |
| `adversarial-review` | Independently challenges software changes and agent completion claims with counterexamples, adverse-condition analysis, and evidence-backed findings. |
| `aws-cli-safety` | Starts AWS CLI work with verified reads, highlights every non-read operation in a written action plan, and presents ready commands with explanations in Markdown for manual execution. |
| `azure-cli-safety` | Applies read-only-first safeguards to Azure CLI and AzCopy, highlights every non-read operation in a written plan, and explains ready commands in Markdown for manual execution. |
| `code-review` | Performs senior-engineer code reviews with severity-ranked findings, concrete file references, validation gaps, and risk-focused review discipline. |
| `fix-dependabot-alert` | Resolves one GitHub Dependabot security alert with a bounded slow loop, minimal dependency changes, explicit validation evidence, independent checking, and a human merge gate. |
| `github-pull-request` | Drafts or creates GitHub pull requests with evidence-backed blast-radius assessments, proportionate review depth, and visual walkthroughs for significant implementations. |
| `google-cloud-cli-safety` | Applies read-only-first safeguards to gcloud, bq, and gsutil, highlights every non-read operation in a written plan, and explains ready commands in Markdown for manual execution. |
| `grill-me` | Interviews the user about a plan, resolving design decisions one by one; available only through manual invocation. |
| `jev-file-scan` | Uses Jev with Codex and Claude Code to rank source snippets by semantic relevance, with local file selection and file/line references. |
| `harness-engineering` | Seeds or improves agent-first project harness files such as `AGENTS.md`, architecture notes, quality gates, execution-plan folders, decision records, and technical-debt tracking. |
| `refactor-safely` | Guides behavior-preserving refactors with explicit scope, characterization tests, small steps, validation, and reviewable change discipline. |
| `refreshing-linear-issues` | Records timestamped implementation updates in Linear issue bodies and posts a confirmation comment after the body change is verified. |
| `review-pull-request` | Performs read-only, L5-calibrated pull-request reviews with evidence-backed findings and deep Python, Rust, Kubernetes, Terraform, and security lenses. |
| `rust-tech-lead` | Provides senior Rust engineering guidance for architecture, debugging, testing, performance work, and review. |
| `scope-software-task` | Turns ambiguous software changes into repository-grounded task contracts and independently verifiable implementation plans. |
| `show-me` | Provides general visual explanations on request using HumanLayer's unchanged skill, with diagrams, code sketches, and focused HTML artefacts. |
| `worktree-branch` | Creates meaningful task-based branches for new or detached agent worktrees so temporary work directories remain identifiable. |
| `writing-feature-comments` | Keeps feature comments concise and useful to human readers, explaining purpose, rationale, and verified concerns. |

## Repository Layout

```text
.
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
├── show-me/
│   ├── SKILL.md
│   ├── LICENSE
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
git status --short
rg --files -g 'SKILL.md'
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
