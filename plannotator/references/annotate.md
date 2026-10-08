# Document, page and app annotations

## plannotator annotate

```bash
plannotator annotate <target> [--markdown] [--no-jina] [--app | --static] [--render-html] [--tailscale] [--gate] [--json] [--hook]
```

Opens one document, page, or app in the annotation UI and returns the human's annotations on stdout.

Plain `annotate` is feedback-only: it shows **Close** but no **Approve** button. When the user asks to review, approve, accept, or gate a generated plan/spec/document saved as a file, always add `--gate --json`. Do not tell the user they can approve a plain `annotate` session. If the plan is being handed off through the host agent's native plan flow, do not launch `annotate`; let the plan-exit hook open the approval UI automatically.

Targets:

- Markdown and text files: `.md`, `.mdx`, `.txt`.
- Plain-text config and data files, rendered as text: `.yaml`, `.yml`, `.json`, `.jsonc`, `.json5`, `.toml`, `.ini`, `.cfg`, `.conf`, `.properties`, `.csv`, `.tsv`, `.log`, `.xml`, `.env.example`. `.env` itself is deliberately refused (it commonly holds secrets, and annotate history copies file contents). Source-code files belong to `plannotator review`, not annotate.
- Diagram sources, opened in the full diagram viewer (zoom, pan, popout, click a node/edge/cluster to comment): `.mmd`, `.mermaid` (Mermaid) and `.dot`, `.gv` (Graphviz). The file is the whole diagram — no fence needed — and comments carry the part's id plus its real file line.
- HTML files (`.html`, `.htm`): rendered as the raw page by default; `--markdown` converts to markdown instead. `--render-html` is accepted for compatibility; raw rendering is already the default.
- URLs (`https://...`): fetched and converted via Jina Reader by default; `--no-jina` uses plain fetch plus Turndown instead.
- Running local apps: a loopback `http://localhost:PORT/` URL whose probe returns HTML opens in live-app mode (annotate the real running page). `--app` forces live mode and fails loudly when it cannot apply; `--static` forces the classic conversion pipeline. Non-loopback URLs always use the conversion pipeline.
- Folders: `plannotator annotate docs/` opens a file browser over the folder's supported files.

Single files are capped at 2MB. Files are read from disk at stable project paths; keep the reviewed source where it lives.

Argument tolerance: extra words are fine (`plannotator annotate look at notes.md please` opens `notes.md`), but two resolvable targets is an error naming both, and an unrecognized dashed token disables the tolerance so flag typos fail loudly. When nothing resolves in a plain multi-word invocation, the CLI prints an agent-addressed handoff on stdout and exits 0: read it, work out the concrete target, and re-run with that exact path or URL.

### Strict gates and exit codes

For a machine-checkable approval gate, add `--gate --json` plus one or both strict flags:

```bash
plannotator annotate report.md --gate --json --require-approval --result-file /tmp/decision.json
```

- `--require-approval`: exit code reports the human outcome.
- `--result-file <path>`: the stdout decision JSON is also published atomically to `<path>`. The parent directory must exist and the file must not; results resolve from the invocation cwd.

Exit codes under a strict flag (grep convention):

| Exit | Meaning |
| --- | --- |
| 0 | Approved. The only success. |
| 1 | The reviewer did not approve (annotated or dismissed); the decision record was still published. |
| 2 | The gate itself failed: bad flag combination, startup failure (missing file, unreachable URL, oversized file), or the result file could not be published. Never treat as a reviewer outcome. |
| 128+n | Killed by signal n. |

Without strict flags, startup failures exit 1 and the exit code carries no decision; parse the output instead. Both strict flags require `--gate --json` and reject `--hook`.

## Asking the reviewer questions

When a decision needs the reviewer (a trade-off you cannot settle from the code or the conversation), write it as a question block. The reviewer answers in place, and the answers come back to you in an "Answers to your questions" section at the top of their feedback, with the questions they left open listed under "Unanswered".

```markdown
:::question
Where should losing conflict versions be kept?

Last-write-wins silently drops the loser unless we keep it somewhere.

- [ ] Local only, purged after 30 days — cheap, no server change
- [ ] Server-side per user — survives reinstall, needs a retention policy
- [ ] Nowhere — accept silent loss for v1

Recommended: Local only, purged after 30 days
:::
```

- `:::question` picks one choice, `:::question-multi` picks any number, `:::question-text` asks for free text (a block with no choices is free text too).
- The first line is the question. Other prose lines are context.
- Choices are task-list items: `- [ ] label`, optionally `- [ ] label — why`. The reviewer can always answer "Other", add a note, or skip.
- `Recommended: <label>` marks your recommendation. Text that matches no choice is offered as a suggested answer.
- `- [x]` means the choice is already settled. Use it when you resubmit: keep an answered question with the chosen choice checked, or remove the block and write the decision into the prose.
- Leave blank lines between the parts so the block also reads well on GitHub.
- Ask only what you cannot decide alone, and keep a round short (about 8 questions at most). Do not ask rhetorical questions or questions the codebase answers.
- Each answer comes back under its question (`### Q2. <question> (line N)`) as `Answer: <choice>`, marked `(your recommendation)` when the reviewer took yours, or as `Other: …`, free text in a quote, or `Skipped`, plus any `Note:`. A question you marked `- [x]` is settled and only comes back if the reviewer changed it or added a note.
