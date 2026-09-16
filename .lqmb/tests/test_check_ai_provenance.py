"""Regression tests for .lqmb/bin/check_ai_provenance.py.

Uses a disposable synthetic Git repository per test so the checker's own
behaviour is verified independently of this repository's real commit
history. Includes a regression case for the exact defect flagged in the
organisation's "Future directions" notes: a blank line between the
AI-Assisted/AI-Role block and a trailing Co-Authored-By line causes Git to
read only the last paragraph as trailers.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

spec = importlib.util.spec_from_file_location(
    "check_ai_provenance", ROOT / ".lqmb" / "bin" / "check_ai_provenance.py"
)
check_ai_provenance = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = check_ai_provenance
spec.loader.exec_module(check_ai_provenance)

commits_in_range = check_ai_provenance.commits_in_range
check_commit = check_ai_provenance.check_commit


class GitRepoTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        self._git("init", "-q", "-b", "main")
        self._git("config", "user.email", "test@example.invalid")
        self._git("config", "user.name", "Test User")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def _git(self, *args: str) -> str:
        result = subprocess.run(
            ["git", *args], cwd=self.repo, capture_output=True, text=True, check=True
        )
        return result.stdout

    def _commit(self, message: str) -> str:
        (self.repo / "file.txt").write_text(message)
        self._git("add", "file.txt")
        self._git("commit", "-q", "-m", message)
        return self._git("rev-parse", "HEAD").strip()

    def _base(self) -> str:
        return self._commit("base commit\n\nAI-Assisted: None")


class WellFormedTrailerTests(GitRepoTestCase):
    def test_ai_assisted_none_passes(self) -> None:
        base = self._base()
        head = self._commit("a human-only change\n\nAI-Assisted: None")

        self.assertEqual(check_commit(head, cwd=self.repo), [])
        self.assertEqual(commits_in_range(base, head, cwd=self.repo), [head])

    def test_ai_assisted_claude_generated_passes(self) -> None:
        base = self._base()
        head = self._commit(
            "an AI-generated change\n\nAI-Assisted: Claude\nAI-Role: Generated"
        )

        self.assertEqual(check_commit(head, cwd=self.repo), [])

    def test_contiguous_trailer_block_with_co_authored_by_passes(self) -> None:
        base = self._base()
        head = self._commit(
            "an AI-generated change\n\n"
            "AI-Assisted: Claude\n"
            "AI-Role: Generated\n"
            "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
        )

        self.assertEqual(check_commit(head, cwd=self.repo), [])


class MalformedTrailerTests(GitRepoTestCase):
    def test_missing_ai_assisted_trailer_fails(self) -> None:
        base = self._base()
        head = self._commit("a change with no provenance trailer at all")

        errors = check_commit(head, cwd=self.repo)
        self.assertTrue(errors)
        self.assertIn("AI-Assisted", errors[0])

    def test_invalid_ai_assisted_value_fails(self) -> None:
        base = self._base()
        head = self._commit("a change\n\nAI-Assisted: Sometimes")

        errors = check_commit(head, cwd=self.repo)
        self.assertTrue(errors)

    def test_claude_without_ai_role_fails(self) -> None:
        base = self._base()
        head = self._commit("a change\n\nAI-Assisted: Claude")

        errors = check_commit(head, cwd=self.repo)
        self.assertTrue(errors)
        self.assertIn("AI-Role", errors[0])

    def test_invalid_ai_role_value_fails(self) -> None:
        base = self._base()
        head = self._commit("a change\n\nAI-Assisted: Claude\nAI-Role: Wrote")

        errors = check_commit(head, cwd=self.repo)
        self.assertTrue(errors)

    def test_blank_line_before_co_authored_by_hides_provenance_trailers(self) -> None:
        """Regression test for the organisation's documented mock-project defect.

        A blank line between the provenance block and Co-Authored-By ends the
        trailer block early, so Git reports only Co-Authored-By as a trailer
        and the (intended) AI-Assisted/AI-Role lines are silently demoted to
        body prose -- this must be caught, not silently accepted.
        """

        base = self._base()
        head = self._commit(
            "a change\n\n"
            "AI-Assisted: Claude\n"
            "AI-Role: Generated\n"
            "\n"
            "Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"
        )

        errors = check_commit(head, cwd=self.repo)
        self.assertTrue(errors)
        self.assertIn("AI-Assisted", errors[0])


class CommitRangeTests(GitRepoTestCase):
    def test_empty_range_reports_no_commits(self) -> None:
        base = self._base()

        self.assertEqual(commits_in_range(base, base, cwd=self.repo), [])

    def test_range_excludes_base_and_is_oldest_first(self) -> None:
        base = self._base()
        first = self._commit("first\n\nAI-Assisted: None")
        second = self._commit("second\n\nAI-Assisted: None")

        self.assertEqual(commits_in_range(base, second, cwd=self.repo), [first, second])


if __name__ == "__main__":
    unittest.main()
