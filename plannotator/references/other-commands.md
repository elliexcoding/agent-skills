# Other Plannotator commands and integration details

Read only the section needed for the requested operation.

## plannotator annotate-last

```bash
plannotator annotate-last [--stdin] [--tailscale] [--gate] [--json] [--hook]
plannotator last
```

Opens the latest rendered assistant message from the current agent session in the annotation UI (`last` is an alias). The session log is discovered per host automatically; `--stdin` reads the content from stdin instead.

Do not print a commentary or status message immediately before running it: the command targets the latest rendered assistant message, so a preamble becomes the thing being annotated.

## plannotator copilot-last

```bash
plannotator copilot-last [--gate] [--json] [--hook]
```

The annotate-last variant for live GitHub Copilot CLI sessions (reads Copilot's session-state events). Normally invoked by the Copilot plugin's /plannotator-last command; use it only inside a Copilot CLI session.

## plannotator archive

```bash
plannotator archive
```

Opens a read-only browser over saved plan decisions (approved/denied badges) from the Plannotator data directory. No feedback comes back; the session ends when the user clicks Done.

## plannotator guide

```bash
plannotator guide list
plannotator guide export --id <savedGuideId> [--out <file.html>]
plannotator guide export --guide <guide.json> --patch <diff.patch> [--out <file.html>]
plannotator guide export --snapshot <snapshot.json> [--out <file.html>]
plannotator guide share --id <savedGuideId> [--public] [--ttl <7d|24h|30m|3600>] [--json]
plannotator guide unshare <id> --token <deleteToken>
```

Guided Reviews are AI-generated walkthroughs of a diff, produced inside the code review UI. The CLI works with saved ones:

- `list` shows guides Plannotator has persisted for the current repo.
- `export` writes one portable, self-contained HTML file (the viewer loads from guides.show). `--guide` + `--patch` exports a guide you authored yourself against a unified diff (`--patch -` reads stdin; validation is strict and names any file the guide references that the patch lacks). `--out -` writes to stdout. `--viewer-url` overrides the pinned viewer base.
- `share` uploads the guide and prints a link. Encrypted by default: the key lives only in the URL fragment and the host stores ciphertext. `--public` stores it unencrypted so chat apps can unfurl a preview. `--ttl` sets an expiry; otherwise the link stays until `unshare`. A saved guide records its link, and a second `share --id` refuses rather than orphaning the first link's delete token.
- `unshare <id> --token <t>` removes a link using the delete token printed at share time.

## plannotator sessions

```bash
plannotator sessions [--open [N]] [--clean]
```

Lists active Plannotator server sessions. `--open` reopens session N (default 1) in the browser, useful when a tab was closed mid-review. `--clean` drops stale entries.

## Other subcommands

```bash
plannotator setup-goal <interview|facts> <bundle.json | -> [--json]
plannotator uninstall [--purge] [--yes] [--dry-run]
plannotator improve-context
```

- `setup-goal` opens the interview or facts-acceptance UI for /goal workflows; it is driven by the `plannotator-setup-goal` skill and takes a bundle JSON (`-` reads stdin). Do not hand-build bundles.
- `uninstall` removes Plannotator-installed components (`--purge` also deletes local data; `--yes` is required without a TTY; `--dry-run` previews).
- `improve-context` and `install-runtime` are internal integration commands (hook plumbing and managed runtime install). Never run `improve-context` directly; `plannotator install-runtime agent-terminal` exists for reinstalling the optional annotate-terminal runtime and is normally run by the installer.
- Additional host-internal subcommands (the `opencode-*` and `copilot-plan` family) are invoked by their plugins, not by you.

## Environment variables that change behavior

| Variable | Use |
| --- | --- |
| `PLANNOTATOR_REMOTE=1` | Force remote mode (fixed port 19432, wide bind) for SSH/devcontainer sessions; `0` forces local. Unset means SSH auto-detection. |
| `PLANNOTATOR_PORT` | Fix the port instead of a random one. |
| `PLANNOTATOR_ORIGIN` | Override agent-origin detection (`claude-code`, `codex`, `opencode`, `pi`, `oh-my-pi`, `amp`, `droid`, `copilot-cli`, `gemini-cli`, `kiro-cli`, `mistral-vibe`). Set it when launching Plannotator from a wrapper the detection cannot see through. |
| `PLANNOTATOR_AI=disabled` | Disable Ask AI and agent-launched review surfaces in the UI. |
| `PLANNOTATOR_SHARE=disabled` | Disable URL sharing, including guide share links. |
| `PLANNOTATOR_DATA_DIR` | Move the data directory (default `~/.plannotator`): plans, history, drafts, config. |
| `PLANNOTATOR_BROWSER` | Open sessions in a specific browser. |

## Posting annotations into a live session

A running plan-review session exposes a small HTTP API on its base URL for external annotations: `POST /api/external-annotations` adds inline annotations the reviewer sees immediately, with PATCH/DELETE for updates and an SSE stream at `/api/external-annotations/stream`. The UI's "copy agent instructions" action puts the full API contract for the current session, with the correct base URL, on the clipboard for handing to an agent or script. If the user pastes such instructions, follow them; do not invent endpoints beyond that contract.


## Session model

Every review or annotate command starts a local web server, opens the browser, and blocks until the human decides. That can take minutes, or more than an hour for a large pull request. Launch it with a long (or no) command timeout, or in the background, then read stdout when the process exits. In Claude Code, a background command is stopped after 30 minutes unless you pass `run_in_background` with a longer `timeout` (up to `7200000` ms). Do not kill the process to "finish" a review; a session that ends without a decision reads as no feedback. If a session was stopped by a time limit, run the same command again: annotation drafts are restored.

Stdout is the interface, but its contract is command-specific. For `annotate` and its last-message variants:

- Plaintext (default): empty output on close, `The user approved.` on approve, otherwise the feedback text. Address returned feedback in the same conversation.
- `--json`: one JSON record with `decision` (`approved`, `dismissed`, or `annotated`) and optional raw `feedback`. An approval may still carry notes in `feedback`; treat those as guidance, not a change request.
- `--hook`: hook-native output for real PostToolUse/Stop hook contexts only. Approve/close emits nothing (hook passes); annotations emit `{"decision":"block","reason":"..."}`. `--hook` implies the gate UI. Never use it for a normal interactive invocation.

`plannotator <command> --help` prints usage without launching anything. Bare `plannotator` is the hook entry point and expects hook JSON on stdin.
