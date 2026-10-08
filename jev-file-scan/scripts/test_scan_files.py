#!/usr/bin/env python3
"""Exercise coverage, credential handling, and API contracts without network access."""

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import scan_files as scan


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "repo"
        self.root.mkdir()

    def args(self, *extra):
        return scan.parse_args(["--root", str(self.root), "--query", "access decisions", *extra])

    def write(self, name, text="ordinary source\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    @staticmethod
    def response(values):
        return {
            "model": "jev-test",
            "answers": {f"s{i}": {"type": "noul", "noul": value} for i, value in enumerate(values)},
            "usage": {"input_tokens": 50, "output_tokens": 10},
        }

    def test_credentials_binary_outside_and_symlinks_never_enter_payload(self):
        self.write("ok.py")
        self.write(".env", "TYPESAFE_API_KEY=never-upload-this\n")
        self.write(".ssh/settings", "private-value\n")
        (self.root / "image.bin").write_bytes(b"binary\0data")
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.py").write_text("outside-private-value\n")
        (self.root / "alias").symlink_to(outside, target_is_directory=True)
        (self.root / "link.py").symlink_to(self.root / "ok.py")
        chunks, skipped, count, candidates = scan.select_chunks(
            self.root, ["ok.py", ".env", ".ssh/settings", "image.bin", "alias/secret.py", "link.py", "../outside/secret.py"], self.args()
        )
        self.assertEqual(count, 1)
        self.assertEqual(candidates, 7)
        self.assertEqual(len(skipped), 6)
        payload = scan.make_payload(chunks, "access", "jev-test")
        for secret in (b"never-upload-this", b"private-value", b"binary"):
            self.assertNotIn(secret, payload)

    def test_unicode_chunking_preserves_all_source_lines_and_overlap(self):
        text = "".join(f"{i}: Résumé 日本語\n" for i in range(1, 201))
        chunks = scan.chunk_text("example.py", text)
        lines = text.splitlines(keepends=True)
        covered = set()
        for chunk in chunks:
            self.assertEqual(chunk.content, "".join(lines[chunk.start_line - 1:chunk.end_line]))
            self.assertLessEqual(len(chunk.content.encode()), scan.CHUNK_BYTES)
            covered.update(range(chunk.start_line, chunk.end_line + 1))
        self.assertEqual(covered, set(range(1, 201)))
        self.assertLess(chunks[1].start_line, chunks[0].end_line)

    def test_long_line_and_oversized_file_are_reported(self):
        self.write("long.py", "x" * 4_001)
        self.write("big.py", "x" * 20)
        report = scan.run(self.args("--dry-run", "--max-file-bytes", "10", "big.py"))
        self.assertEqual(report["skipped"][0]["reason"], "file size limit")
        report = scan.run(self.args("--dry-run", "long.py"))
        self.assertIn("line exceeds", report["skipped"][0]["reason"])

    def test_file_and_chunk_budgets_stop_before_network(self):
        self.write("a.py")
        self.write("b.py")
        self.write("many.py", "line\n" * 200)
        with patch.object(scan, "call_jev") as api:
            for options in (
                ["--max-files", "1", "a.py", "b.py"],
                ["--max-chunks", "1", "many.py"],
            ):
                with self.assertRaisesRegex(scan.ScanError, "No request was sent"):
                    scan.run(self.args(*options))
            api.assert_not_called()

    def test_request_budget_accounts_for_unicode_and_preserves_every_chunk(self):
        text = ("日本語" * 300 + "\n") * 15
        chunks = scan.chunk_text("cjk.md", text)
        args = self.args("--batch-size", "100")
        batches = scan.pack_requests(chunks, args)
        self.assertEqual([c for batch, _ in batches for c in batch], chunks)
        self.assertGreater(len(batches), 1)
        for batch, payload in batches:
            self.assertLessEqual(len(payload), scan.REQUEST_BYTES)
            body = json.loads(payload)
            self.assertEqual(len(body["questions"]), len(batch))

    def test_dry_run_never_reads_credentials_or_calls_api(self):
        self.write("a.py")
        with patch.object(scan, "load_key") as key, patch.object(scan, "call_jev") as api:
            report = scan.run(self.args("--dry-run", "a.py"))
        key.assert_not_called()
        api.assert_not_called()
        self.assertEqual(report["coverage"]["chunks"], 1)
        self.assertNotIn("content", report["snippets"][0])

    def test_env_precedence_literal_fallback_and_no_shell_execution(self):
        env = self.base / "test.env"
        env.write_text("export TYPESAFE_API_KEY='fallback-value' # comment\n")
        with patch.dict(os.environ, {"TYPESAFE_API_KEY": "exported-value"}, clear=True):
            self.assertEqual(scan.load_key(env), "exported-value")
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(scan.load_key(env), "fallback-value")
            marker = self.base / "must-not-exist"
            env.write_text(f"TYPESAFE_API_KEY=$(touch {marker})\n")
            with self.assertRaises(scan.ScanError):
                scan.load_key(env)
            self.assertFalse(marker.exists())

    def test_default_xdg_credential_location(self):
        env = self.base / "config/typesafe/env"
        env.parent.mkdir(parents=True)
        env.write_text("TYPESAFE_API_KEY=xdg-value\n")
        with patch.dict(os.environ, {"XDG_CONFIG_HOME": str(self.base / "config")}, clear=True):
            self.assertEqual(scan.load_key(), "xdg-value")

    def test_null_delimited_candidates_and_ignored_file_discovery(self):
        self.write("name with spaces.py")
        self.write("ignored.py")
        self.write(".gitignore", "ignored.py\n")
        automatic = scan.discover_files(self.root, self.args("--glob", "*.py"))
        self.assertIn("./name with spaces.py", automatic)
        self.assertNotIn("./ignored.py", automatic)
        candidates = self.base / "candidates"
        candidates.write_bytes(b"name with spaces.py\0ignored.py\0")
        report = scan.run(self.args("--dry-run", "--files-from", str(candidates), "--null"))
        self.assertEqual(report["coverage"]["selected_files"], 2)

    def test_valid_results_rank_by_probability_and_report_omissions(self):
        self.write("a.py", "alpha\n")
        self.write("b.py", "beta\n")
        with patch.object(scan, "load_key", return_value="dummy"), patch.object(
            scan, "call_jev", return_value=self.response([0.1, 0.9])
        ) as api:
            report = scan.run(self.args("--top", "1", "a.py", "b.py"))
        self.assertEqual(api.call_count, 1)
        self.assertEqual(report["results"][0]["path"], "b.py")
        self.assertEqual(report["results_omitted"], 1)
        self.assertEqual(report["models"], ["jev-test"])
        self.assertEqual(report["usage"]["input_tokens"], 50)

    def test_missing_invalid_and_nonfinite_answers_are_rejected(self):
        chunks = [scan.Chunk("a.py", 1, 1, "alpha\n")]
        for value in (True, -0.1, 1.1, float("nan"), "0.9"):
            with self.subTest(value=value), self.assertRaises(scan.ScanError):
                scan.validate_response(self.response([value]), chunks)
        with self.assertRaises(scan.ScanError):
            scan.validate_response(self.response([]), chunks)

    def test_later_api_failure_never_becomes_a_complete_scan(self):
        self.write("a.py")
        self.write("b.py")
        with patch.object(scan, "load_key", return_value="dummy"), patch.object(
            scan, "call_jev", side_effect=[self.response([0.9]), scan.ScanError("offline")]
        ):
            with self.assertRaisesRegex(scan.ScanError, "Request 2/2 failed.*complete scan was not produced"):
                scan.run(self.args("--batch-size", "1", "a.py", "b.py"))

    def test_http_error_does_not_print_key_or_response_body(self):
        error = urllib.error.HTTPError(scan.ENDPOINT, 401, "no", {}, io.BytesIO(b"sensitive-body"))
        with patch("urllib.request.OpenerDirector.open", side_effect=error):
            with self.assertRaises(scan.ScanError) as result:
                scan.call_jev(b"{}", "sensitive-key", 1)
        self.assertNotIn("sensitive", str(result.exception))
        self.assertIn("401", str(result.exception))
        self.assertIsNone(scan.NoRedirect().redirect_request(None, None, 302, "", {}, "https://example.com"))

    def test_cli_dry_run_works_without_exported_credentials(self):
        self.write("a.py")
        environment = os.environ.copy()
        environment.pop("TYPESAFE_API_KEY", None)
        environment["XDG_CONFIG_HOME"] = str(self.base / "missing")
        completed = subprocess.run(
            [sys.executable, str(Path(scan.__file__)), "--root", str(self.root),
             "--query", "access decisions", "--dry-run", "a.py"],
            env=environment, capture_output=True, text=True,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["status"], "dry_run")

    def test_no_candidates_is_distinct_from_a_successful_jev_scan(self):
        self.write(".env", "TYPESAFE_API_KEY=do-not-submit\n")
        with patch.object(scan, "load_key") as key, patch.object(scan, "call_jev") as api:
            report = scan.run(self.args(".env"))
        self.assertEqual(report["status"], "no_candidates")
        self.assertEqual(report["coverage"]["requests"], 0)
        key.assert_not_called()
        api.assert_not_called()

    def test_glob_exclusions_are_applied_after_inclusions(self):
        self.write("a.py")
        self.write("b.py")
        self.write("notes.md")
        candidates = scan.discover_files(self.root, self.args("--glob", "*.py", "--glob", "!b.py"))
        self.assertEqual(candidates, ["./a.py"])


if __name__ == "__main__":
    unittest.main()
