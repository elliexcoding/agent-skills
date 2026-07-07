#!/usr/bin/env python3
"""Collect a markdown scaffold for an AI-agent engineering handoff."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def run_git(args: list[str], cwd: Path, check: bool = False) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def git_output(args: list[str], cwd: Path, fallback: str = "unavailable") -> str:
    code, stdout, stderr = run_git(args, cwd=cwd)
    if code == 0:
        return stdout or "(none)"
    return stderr or fallback


def section(title: str, body: str) -> str:
    return f"## {title}\n{body.strip()}\n"


def fenced(text: str) -> str:
    return f"```text\n{text.strip() or '(none)'}\n```"


def build_handoff(cwd: Path, objective: str, base: str | None, max_commits: int) -> str:
    branch_status = git_output(["status", "--short", "--branch"], cwd)
    branch = git_output(["branch", "--show-current"], cwd)
    commit = git_output(["rev-parse", "--short", "HEAD"], cwd)
    changed_files = git_output(["status", "--short"], cwd)
    recent_commits = git_output(["log", "--oneline", f"-n{max_commits}"], cwd)

    if base:
        diff_stat = git_output(["diff", "--stat", f"{base}...HEAD"], cwd)
        diff_names = git_output(["diff", "--name-status", f"{base}...HEAD"], cwd)
    else:
        diff_stat = git_output(["diff", "--stat"], cwd)
        diff_names = git_output(["diff", "--name-status"], cwd)

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    base_line = base if base else "not specified"

    parts = [
        f"# Agent Handoff\n\nGenerated: {generated}\nRepository: `{cwd}`\n",
        section("Objective", objective),
        section(
            "Current State",
            "\n".join(
                [
                    f"- Branch: `{branch}`",
                    f"- Commit: `{commit}`",
                    f"- Base: `{base_line}`",
                    "- Completed: TODO",
                    "- In progress: TODO",
                ]
            ),
        ),
        section("Git Status", fenced(branch_status)),
        section("Changed Files", fenced(changed_files)),
        section("Diff Summary", fenced(diff_stat)),
        section("Diff Names", fenced(diff_names)),
        section("Recent Commits", fenced(recent_commits)),
        section(
            "Validation",
            "- TODO: list commands run and results\n- Not run: TODO",
        ),
        section("Decisions And Rationale", "- TODO"),
        section("Blockers Or Risks", "- TODO"),
        section(
            "Next Steps",
            "1. TODO\n2. TODO\n3. TODO",
        ),
        section("Notes For Next Agent", "- TODO"),
    ]
    return "\n".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collect a markdown scaffold for an AI-agent handoff."
    )
    parser.add_argument("--objective", required=True, help="Current task objective.")
    parser.add_argument(
        "--cwd",
        default=".",
        help="Repository path. Defaults to the current directory.",
    )
    parser.add_argument(
        "--base",
        help="Optional base branch or commit for diff summary.",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=8,
        help="Number of recent commits to include.",
    )
    parser.add_argument(
        "--output",
        help="Optional markdown file to write. Defaults to stdout.",
    )
    args = parser.parse_args()

    cwd = Path(args.cwd).resolve()
    code, _, stderr = run_git(["rev-parse", "--is-inside-work-tree"], cwd=cwd)
    if code != 0:
        raise SystemExit(stderr or f"not a Git worktree: {cwd}")

    markdown = build_handoff(
        cwd=cwd,
        objective=args.objective,
        base=args.base,
        max_commits=args.max_commits,
    )

    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = cwd / output
        output.write_text(markdown + "\n")
        print(f"wrote handoff scaffold: {output}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
