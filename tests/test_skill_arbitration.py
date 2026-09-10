from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPLICIT_ONLY_SKILLS = (
    "scope-software-task",
    "worktree-branch",
    "debug-failing-tests",
    "github-pull-request",
)


class SkillArbitrationTests(unittest.TestCase):
    def test_root_agents_declares_one_process_orchestrator(self) -> None:
        agents_file = REPO_ROOT / "AGENTS.md"
        if not agents_file.is_file():
            self.fail("root AGENTS.md must define the skill arbitration policy")

        contents = agents_file.read_text(encoding="utf-8")
        self.assertIn("## Skill arbitration", contents)
        self.assertIn(
            "Superpowers is the authoritative process workflow", contents
        )
        self.assertIn(
            "Custom skills provide domain-specific analysis or implementation steps",
            contents,
        )
        self.assertIn(
            "If a custom skill conflicts with Superpowers, follow Superpowers",
            contents,
        )

    def test_competing_repo_skills_are_explicit_only(self) -> None:
        policy_pattern = re.compile(
            r"(?m)^policy:\s*$\n(?:^[ \t]+.*\n)*?"
            r"^[ \t]+allow_implicit_invocation:\s*false\s*$"
        )

        for skill_name in EXPLICIT_ONLY_SKILLS:
            with self.subTest(skill=skill_name):
                metadata_file = REPO_ROOT / skill_name / "agents" / "openai.yaml"
                self.assertTrue(
                    metadata_file.is_file(),
                    f"{skill_name} must declare an explicit invocation policy",
                )
                if metadata_file.is_file():
                    contents = metadata_file.read_text(encoding="utf-8")
                    self.assertRegex(contents, policy_pattern)


if __name__ == "__main__":
    unittest.main()
