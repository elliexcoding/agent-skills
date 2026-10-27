"""Exercise compatibility failures without invoking either agent runtime."""

from pathlib import Path
import tempfile
import unittest

import yaml

from validate_skills import discover_skills, validate_skill


class CompatibilityTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.skill = self.root / "example"
        self.skill.mkdir()

    def write_skill(self, extra=None, body="Follow the requested workflow.\n"):
        metadata = {"name": "example", "description": "An example workflow."}
        metadata.update(extra or {})
        (self.skill / "SKILL.md").write_text(
            "---\n" + yaml.safe_dump(metadata) + "---\n\n" + body,
            encoding="utf-8",
        )

    def write_policy(self, value):
        directory = self.skill / "agents"
        directory.mkdir(exist_ok=True)
        (directory / "openai.yaml").write_text(
            yaml.safe_dump({"policy": {"allow_implicit_invocation": value}}),
            encoding="utf-8",
        )

    def test_default_automatic_and_explicit_only_skills_are_accepted(self):
        self.write_skill()
        self.assertEqual(validate_skill(self.skill), [])
        self.write_skill({"disable-model-invocation": True})
        self.write_policy(False)
        self.assertEqual(validate_skill(self.skill), [])

    def test_invocation_mismatch_is_detected_in_both_directions(self):
        for manual, automatic in ((False, False), (True, True)):
            with self.subTest(manual=manual):
                self.write_skill({"disable-model-invocation": manual})
                self.write_policy(automatic)
                self.assertTrue(any("invocation mismatch" in error
                                    for error in validate_skill(self.skill)))

    def test_quoted_booleans_are_rejected(self):
        self.write_skill({"disable-model-invocation": "false"})
        self.write_policy("true")
        errors = validate_skill(self.skill)
        self.assertTrue(any("disable-model-invocation must" in e for e in errors))
        self.assertTrue(any("allow_implicit_invocation must" in e for e in errors))

    def test_typo_does_not_silently_enable_invocation(self):
        self.write_skill({"disable_model_invocation": True})
        self.assertTrue(any("unsupported shared frontmatter" in error
                            for error in validate_skill(self.skill)))

    def test_malformed_metadata_is_reported(self):
        (self.skill / "SKILL.md").write_text("---\nname: [broken\n---\n")
        self.assertTrue(any("invalid frontmatter YAML" in error
                            for error in validate_skill(self.skill)))
        self.write_skill({"description": ""})
        self.assertTrue(any("description must" in error
                            for error in validate_skill(self.skill)))

    def test_missing_dependency_is_reported_until_installed(self):
        self.write_skill(body="Read [other](../other/SKILL.md) and [docs](https://example.com).\n")
        self.assertEqual(validate_skill(self.skill),
                         ["missing local reference: ../other/SKILL.md"])
        other = self.root / "other"
        other.mkdir()
        (other / "SKILL.md").write_text("Supporting instructions.\n")
        self.assertEqual(validate_skill(self.skill), [])

    def test_discovery_includes_linked_skills_but_excludes_bundled_system_files(self):
        self.write_skill()
        system = self.root / ".system"
        system.mkdir()
        (system / "SKILL.md").write_text("Bundled content.\n")
        (self.root / "linked").symlink_to(self.skill, target_is_directory=True)
        self.assertEqual([p.name for p in discover_skills(self.root)],
                         ["example", "linked"])


if __name__ == "__main__":
    unittest.main()
