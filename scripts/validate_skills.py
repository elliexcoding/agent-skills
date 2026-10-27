#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML>=6,<7"]
# ///
"""Check shared skill metadata, invocation policies and local reference links."""

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

import yaml


FRONTMATTER_FIELDS = {
    "name", "description", "license", "compatibility", "metadata",
    "allowed-tools", "disable-model-invocation",
}
REPOSITORY = Path(__file__).resolve().parents[1]


def validate_skill(directory: Path) -> list[str]:
    errors = []
    try:
        content = (directory / "SKILL.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return [f"cannot read SKILL.md: {exc}"]
    match = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", content, re.DOTALL)
    if not match:
        return ["SKILL.md must start with YAML frontmatter"]
    try:
        metadata = yaml.safe_load(match[1])
    except yaml.YAMLError as exc:
        return [f"invalid frontmatter YAML: {exc}"]
    if not isinstance(metadata, dict):
        return ["frontmatter must be a mapping"]

    unsupported = set(metadata) - FRONTMATTER_FIELDS
    if unsupported:
        errors.append("unsupported shared frontmatter fields: " +
                      ", ".join(sorted(map(str, unsupported))))
    name = metadata.get("name")
    if (not isinstance(name, str) or len(name) > 64 or
            not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name)):
        errors.append("name must be 1-64 lowercase letters, digits or single hyphens")
    elif name != directory.name:
        errors.append(f"name {name!r} does not match directory {directory.name!r}")
    description = metadata.get("description")
    if (not isinstance(description, str) or not description.strip() or
            len(description) > 1024):
        errors.append("description must be a non-empty string of at most 1024 characters")
    if "metadata" in metadata and not isinstance(metadata["metadata"], dict):
        errors.append("metadata must be a mapping")
    if "compatibility" in metadata:
        compatibility = metadata["compatibility"]
        if not isinstance(compatibility, str) or len(compatibility) > 500:
            errors.append("compatibility must be a string of at most 500 characters")

    claude_manual = metadata.get("disable-model-invocation", False)
    if not isinstance(claude_manual, bool):
        errors.append("disable-model-invocation must be a YAML boolean")

    adapter = directory / "agents" / "openai.yaml"
    codex_automatic = True
    if adapter.exists():
        try:
            settings = yaml.safe_load(adapter.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            errors.append(f"cannot read agents/openai.yaml: {exc}")
            settings = None
        if not isinstance(settings, dict):
            errors.append("agents/openai.yaml must be a mapping")
            codex_automatic = None
        else:
            policy = settings.get("policy", {})
            if not isinstance(policy, dict):
                errors.append("agents/openai.yaml policy must be a mapping")
                codex_automatic = None
            else:
                codex_automatic = policy.get("allow_implicit_invocation", True)
                if not isinstance(codex_automatic, bool):
                    errors.append("allow_implicit_invocation must be a YAML boolean")

    if (isinstance(claude_manual, bool) and isinstance(codex_automatic, bool)
            and claude_manual == codex_automatic):
        errors.append("invocation mismatch: Claude disable-model-invocation and "
                      "Codex allow_implicit_invocation must be opposites")

    for target in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", content[match.end():]):
        target = target.strip().split(' "', 1)[0].strip("<>")
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        if not (directory / unquote(parsed.path)).exists():
            errors.append(f"missing local reference: {target}")
    return errors


def discover_skills(root: Path) -> list[Path]:
    return sorted(path for path in root.iterdir()
                  if not path.name.startswith(".") and (path / "SKILL.md").is_file())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skills", nargs="*", type=Path,
                        help="Skill directories; defaults to this repository's personal skills.")
    args = parser.parse_args()
    directories = args.skills or discover_skills(REPOSITORY)
    if not directories:
        print("No skills found.", file=sys.stderr)
        return 1
    failures = 0
    for directory in directories:
        errors = validate_skill(directory)
        if errors:
            failures += 1
            for error in errors:
                print(f"FAIL {directory}: {error}", file=sys.stderr)
    print(f"Validated {len(directories)} skills; {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
