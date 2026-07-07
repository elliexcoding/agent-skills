#!/usr/bin/env python3
"""Seed agent-first harness engineering files into a repository."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


def render_template(text: str, project_name: str) -> str:
    return (
        text.replace("{{PROJECT_NAME}}", project_name)
        .replace("{{DATE}}", date.today().isoformat())
    )


def iter_templates(template_root: Path) -> list[Path]:
    return sorted(path for path in template_root.rglob("*") if path.is_file())


def seed(target: Path, project_name: str, dry_run: bool, force: bool) -> int:
    skill_root = Path(__file__).resolve().parents[1]
    template_root = skill_root / "assets" / "starter"
    if not template_root.exists():
        raise SystemExit(f"template root not found: {template_root}")

    target = target.resolve()
    if not target.exists() or not target.is_dir():
        raise SystemExit(f"target must be an existing directory: {target}")

    created_or_updated = 0
    for template in iter_templates(template_root):
        rel_path = template.relative_to(template_root)
        dest = target / rel_path
        exists = dest.exists()
        action = "update" if exists and force else "create"

        if exists and not force:
            print(f"skip existing {rel_path}")
            continue

        print(f"{action} {rel_path}")
        created_or_updated += 1
        if dry_run:
            continue

        content = render_template(template.read_text(), project_name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content)

    if dry_run:
        print(f"dry run complete: {created_or_updated} file(s) would change")
    else:
        print(f"complete: {created_or_updated} file(s) changed")
    return created_or_updated


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Seed OpenAI-style harness engineering docs into a repo."
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Repository root to seed. Defaults to the current directory.",
    )
    parser.add_argument(
        "--project-name",
        help="Project name for templates. Defaults to the target directory name.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print intended changes without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files. Use only when explicitly requested.",
    )
    args = parser.parse_args()

    target = Path(args.target)
    project_name = args.project_name or target.resolve().name
    seed(target=target, project_name=project_name, dry_run=args.dry_run, force=args.force)


if __name__ == "__main__":
    main()
