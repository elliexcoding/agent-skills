#!/usr/bin/env python3
"""Create a task-named branch when an agent worktree is detached."""

from __future__ import annotations

import argparse
import re
import subprocess
import unicodedata
from pathlib import Path


def git(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=cwd,
        check=check,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def git_text(args: list[str], cwd: Path, check: bool = True) -> str:
    return git(args, cwd=cwd, check=check).stdout.strip()


def current_branch(cwd: Path) -> str | None:
    result = git(["symbolic-ref", "--quiet", "--short", "HEAD"], cwd=cwd, check=False)
    branch = result.stdout.strip()
    return branch or None


def short_sha(cwd: Path) -> str:
    return git_text(["rev-parse", "--short", "HEAD"], cwd=cwd)


def slugify(text: str, max_length: int) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = ascii_text.lower()
    slug = re.sub(r"[^a-z0-9._-]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug)
    slug = slug.strip("-. _/")
    slug = slug.replace("..", "-")
    slug = slug.replace("@{", "-")
    slug = slug[:max_length].strip("-. _/")
    return slug or "task"


def normalize_prefix(prefix: str) -> str:
    prefix = prefix.strip().strip("/")
    if not prefix:
        return "codex"
    parts = [slugify(part, max_length=24) for part in prefix.split("/") if part.strip()]
    return "/".join(parts) or "codex"


def valid_branch_name(branch: str, cwd: Path) -> bool:
    result = git(["check-ref-format", "--branch", branch], cwd=cwd, check=False)
    return result.returncode == 0


def branch_exists(branch: str, cwd: Path) -> bool:
    result = git(["rev-parse", "--verify", "--quiet", f"refs/heads/{branch}"], cwd=cwd, check=False)
    return result.returncode == 0


def unique_branch_name(base: str, cwd: Path) -> str:
    if not branch_exists(base, cwd):
        return base

    sha = short_sha(cwd)
    candidate = f"{base}-{sha}"
    if not branch_exists(candidate, cwd):
        return candidate

    index = 2
    while True:
        candidate = f"{base}-{sha}-{index}"
        if not branch_exists(candidate, cwd):
            return candidate
        index += 1


def create_branch(branch: str, cwd: Path, rename_current: bool) -> None:
    if rename_current:
        git(["branch", "-m", branch], cwd=cwd)
    else:
        git(["switch", "-c", branch], cwd=cwd)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create a task-named branch when the current Git worktree is detached."
    )
    parser.add_argument("--task", required=True, help="Task or request summary.")
    parser.add_argument(
        "--prefix",
        default="codex",
        help="Branch prefix without trailing slash. Defaults to 'codex'.",
    )
    parser.add_argument(
        "--cwd",
        default=".",
        help="Worktree path. Defaults to the current directory.",
    )
    parser.add_argument(
        "--max-slug-length",
        type=int,
        default=56,
        help="Maximum length for the generated task slug.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the branch action without changing Git state.",
    )
    parser.add_argument(
        "--rename-current",
        action="store_true",
        help="Rename the current named branch. Use only when explicitly requested.",
    )
    args = parser.parse_args()

    cwd = Path(args.cwd).resolve()
    git(["rev-parse", "--is-inside-work-tree"], cwd=cwd)

    branch = current_branch(cwd)
    sha = short_sha(cwd)
    prefix = normalize_prefix(args.prefix)
    slug = slugify(args.task, max_length=args.max_slug_length)
    base_branch = f"{prefix}/{slug}"

    if not valid_branch_name(base_branch, cwd):
        base_branch = f"{prefix}/task-{sha}"

    target_branch = unique_branch_name(base_branch, cwd)

    if branch and not args.rename_current:
        print(f"already on branch: {branch} ({sha})")
        return

    action = "rename" if branch and args.rename_current else "create"
    if args.dry_run:
        print(f"would {action} branch: {target_branch} at {sha}")
        return

    create_branch(target_branch, cwd=cwd, rename_current=bool(branch and args.rename_current))
    print(f"{action}d branch: {target_branch} at {sha}")


if __name__ == "__main__":
    main()
