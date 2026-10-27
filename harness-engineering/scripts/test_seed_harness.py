"""Check shared instructions and preservation of an existing repository."""

import contextlib
import io
from pathlib import Path
import tempfile
import unittest

from seed_harness import seed


class SharedHarnessTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def run_seed(self, dry_run=False):
        with contextlib.redirect_stdout(io.StringIO()):
            return seed(self.root, "Example", dry_run=dry_run, force=False)

    def test_fresh_seed_imports_shared_instructions_and_is_repeatable(self):
        self.run_seed()
        self.assertEqual((self.root / "CLAUDE.md").read_text(), "@AGENTS.md\n")
        self.assertTrue((self.root / "AGENTS.md").is_file())
        self.assertNotIn("{{PROJECT_NAME}}", (self.root / "AGENTS.md").read_text())
        self.assertEqual(self.run_seed(), 0)

    def test_existing_instruction_files_are_preserved(self):
        existing = {"CLAUDE.md": "Keep the Claude-specific instructions.\n",
                    "AGENTS.md": "Keep the shared project rules.\n"}
        for name, content in existing.items():
            (self.root / name).write_text(content)
        self.run_seed()
        for name, content in existing.items():
            self.assertEqual((self.root / name).read_text(), content)

    def test_dry_run_creates_nothing(self):
        self.assertGreater(self.run_seed(dry_run=True), 0)
        self.assertEqual(list(self.root.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
