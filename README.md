# Agent Skills

Personal agent skills for use with Claude Code, Codex, and other coding-agent
workflows that understand a `SKILL.md` entry point.

This repository is intentionally small and portable. Each top-level directory is
a standalone skill that can be copied, symlinked, or packaged into whichever
agent runtime is being used.

## Skills

| Skill | Purpose |
| --- | --- |
| `agent-handoff` | Creates concise, evidence-backed handoffs between AI agents, Codex threads, Claude Code sessions, worktrees, or humans so work can resume safely. |
| `adversarial-review` | Independently challenges software changes and agent completion claims with counterexamples, adverse-condition analysis, and evidence-backed findings. |
| `code-review` | Performs senior-engineer code reviews with severity-ranked findings, concrete file references, validation gaps, and risk-focused review discipline. |
| `github-pull-request` | Drafts or creates high-quality GitHub pull requests with clear titles, useful descriptions, validation evidence, and a final engineering-quality checklist. |
| `harness-engineering` | Seeds or improves agent-first project harness files such as `AGENTS.md`, architecture notes, quality gates, execution-plan folders, decision records, and technical-debt tracking. |
| `refactor-safely` | Guides behavior-preserving refactors with explicit scope, characterization tests, small steps, validation, and reviewable change discipline. |
| `rust-tech-lead` | Provides senior Rust engineering guidance for architecture, debugging, testing, performance work, and review. |
| `worktree-branch` | Creates meaningful task-based branches for new or detached agent worktrees so temporary work directories remain identifiable. |

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
├── code-review/
│   ├── SKILL.md
│   └── references/
├── github-pull-request/
│   ├── SKILL.md
│   └── references/
├── harness-engineering/
│   ├── SKILL.md
│   ├── agents/
│   ├── assets/
│   ├── references/
│   └── scripts/
├── refactor-safely/
│   ├── SKILL.md
│   └── references/
├── rust-tech-lead/
│   └── SKILL.md
└── worktree-branch/
    ├── SKILL.md
    └── scripts/
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

## Validation

Before committing changes:

```sh
git status --short
find . -maxdepth 2 -name SKILL.md -print
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
