"""Regression tests for .lqmb/bin/check_manifest_hygiene.py.

Exercises the pure classification/comparison functions against synthetic
manifests and file lists, plus regression cases for the exact v0.2.3
defect (a template-managed file running a test file that actually lives
under a protected path) and for two bugs the tests themselves originally
caught while widening that scan from YAML-only to .py/.sh as well.
"""
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

spec = importlib.util.spec_from_file_location(
    "check_manifest_hygiene", ROOT / ".lqmb" / "bin" / "check_manifest_hygiene.py"
)
check_manifest_hygiene = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = check_manifest_hygiene
spec.loader.exec_module(check_manifest_hygiene)

check_paths_exist = check_manifest_hygiene.check_paths_exist
check_classes_disjoint = check_manifest_hygiene.check_classes_disjoint
check_full_coverage = check_manifest_hygiene.check_full_coverage
check_no_managed_file_references_a_protected_path = (
    check_manifest_hygiene.check_no_managed_file_references_a_protected_path
)


def sample_manifest(**overrides) -> dict:
    manifest = {
        "schema_version": "0.2",
        "template_version": "0.2.4",
        "template_managed_paths": [".github/workflows/ci.yml", ".lqmb/bin/"],
        "project_configured_paths": [".lqmb/project.json"],
        "protected_paths": ["tests/", "README.md"],
        "shared_paths": [],
    }
    manifest.update(overrides)
    return manifest


class CheckPathsExistTests(unittest.TestCase):
    def test_passes_when_every_declared_path_exists(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("x")
            (root / "tests").mkdir()
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text("x")
            (root / ".lqmb/bin").mkdir(parents=True)
            (root / ".lqmb/project.json").write_text("{}")

            errors = check_paths_exist(sample_manifest(), root)
            self.assertEqual(errors, [])

    def test_flags_missing_declared_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # README.md deliberately not created.

            errors = check_paths_exist(sample_manifest(), root)
            self.assertTrue(any("README.md" in e for e in errors))


class CheckClassesDisjointTests(unittest.TestCase):
    def test_passes_when_disjoint(self) -> None:
        self.assertEqual(check_classes_disjoint(sample_manifest()), [])

    def test_flags_exact_duplicate_across_classes(self) -> None:
        manifest = sample_manifest(protected_paths=["tests/", "README.md", ".lqmb/project.json"])

        errors = check_classes_disjoint(manifest)
        self.assertTrue(any(".lqmb/project.json" in e for e in errors))

    def test_flags_directory_prefix_overlap(self) -> None:
        manifest = sample_manifest(protected_paths=["tests/", "README.md", ".lqmb/bin/helper.py"])

        errors = check_classes_disjoint(manifest)
        self.assertTrue(any(".lqmb/bin/helper.py" in e for e in errors))


class CheckFullCoverageTests(unittest.TestCase):
    def test_passes_when_every_tracked_file_is_classified_once(self) -> None:
        tracked = [
            ".github/workflows/ci.yml",
            ".lqmb/bin/validate_metadata.py",
            ".lqmb/project.json",
            "tests/test_something.py",
            "README.md",
        ]

        errors = check_full_coverage(sample_manifest(), tracked)
        self.assertEqual(errors, [])

    def test_flags_unclassified_tracked_file(self) -> None:
        tracked = ["CHANGELOG.md"]

        errors = check_full_coverage(sample_manifest(), tracked)
        self.assertTrue(any("CHANGELOG.md" in e and "not classified" in e for e in errors))

    def test_flags_tracked_file_classified_twice(self) -> None:
        manifest = sample_manifest(project_configured_paths=[".lqmb/project.json", "tests/"])
        tracked = ["tests/test_something.py"]

        errors = check_full_coverage(manifest, tracked)
        self.assertTrue(any("multiple path classes" in e for e in errors))


class CheckNoManagedFileReferencesAProtectedPathTests(unittest.TestCase):
    def test_passes_when_workflow_only_runs_managed_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text(
                "run: |\n  python3 .lqmb/bin/validate_metadata.py\n"
            )
            tracked = [".github/workflows/ci.yml"]

            errors = check_no_managed_file_references_a_protected_path(
                sample_manifest(), tracked, root
            )
            self.assertEqual(errors, [])

    def test_does_not_mistake_a_managed_dotted_path_for_a_bare_protected_one(self) -> None:
        """A referenced path starting with '.' (e.g. .lqmb/bin/x.py) must not
        be compared against protected_paths with its leading '.' stripped --
        that would make it collide with an unrelated bare entry such as
        'lqmb/' and produce a false positive.
        """

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text(
                "run: |\n  python3 .lqmb/bin/validate_metadata.py\n"
            )
            tracked = [".github/workflows/ci.yml"]
            manifest = sample_manifest(protected_paths=["lqmb/", "README.md"])

            errors = check_no_managed_file_references_a_protected_path(
                manifest, tracked, root
            )
            self.assertEqual(errors, [])

    def test_flags_reference_with_explicit_relative_prefix(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text(
                "run: |\n  python3 ./tests/test_validate_metadata.py\n"
            )
            tracked = [".github/workflows/ci.yml"]

            errors = check_no_managed_file_references_a_protected_path(
                sample_manifest(), tracked, root
            )
            self.assertTrue(errors)
            self.assertIn("tests/test_validate_metadata.py", errors[0])

    def test_flags_v0_2_3_style_defect(self) -> None:
        """Regression test for the exact bug fixed in template v0.2.3.

        ci.yml (template-managed) ran a regression test file addressed as
        tests/test_validate_metadata.py, but tests/ is a protected,
        project-owned path -- a downstream project's tests/ would never
        contain that file.
        """

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text(
                "run: |\n  python3 tests/test_validate_metadata.py -v\n"
            )
            tracked = [".github/workflows/ci.yml"]

            errors = check_no_managed_file_references_a_protected_path(
                sample_manifest(), tracked, root
            )
            self.assertTrue(errors)
            self.assertIn("tests/test_validate_metadata.py", errors[0])

    def test_does_not_flag_the_check_manifest_hygiene_module_itself(self) -> None:
        """The scan now covers .py files too, so check_manifest_hygiene.py's
        own source (under .lqmb/bin/, not excluded like .lqmb/tests/) is
        actually scanned here -- this is a real self-check, not a vacuous
        one: its docstring discusses the v0.2.3 bug in prose only, with no
        literal `python3 <protected-path>` invocation text, so it passes.
        """

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".lqmb/bin").mkdir(parents=True)
            (root / ".lqmb/bin/check_manifest_hygiene.py").write_text(
                (ROOT / ".lqmb" / "bin" / "check_manifest_hygiene.py").read_text()
            )
            tracked = [".lqmb/bin/check_manifest_hygiene.py"]

            errors = check_no_managed_file_references_a_protected_path(
                sample_manifest(), tracked, root
            )
            self.assertEqual(errors, [])

    def test_flags_defect_in_a_managed_python_script_too(self) -> None:
        """The scan is no longer YAML-only: a template-managed .py script
        that shells out to a protected-path file via a literal command
        string (e.g. os.system, or subprocess with shell=True) must be
        caught as well. The regex matches embedded shell-command text, not
        Python's list-argument subprocess form -- see docstring note on the
        scan being a best-effort heuristic, not a full parser.
        """

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".lqmb/bin").mkdir(parents=True)
            (root / ".lqmb/bin/helper.py").write_text(
                "import os\n"
                'os.system("python3 tests/test_validate_metadata.py")\n'
            )
            tracked = [".lqmb/bin/helper.py"]
            manifest = sample_manifest(template_managed_paths=[".lqmb/bin/"])

            errors = check_no_managed_file_references_a_protected_path(
                manifest, tracked, root
            )
            self.assertTrue(errors)
            self.assertIn("tests/test_validate_metadata.py", errors[0])

    def test_excludes_lqmb_tests_directory_even_with_matching_suffix(self) -> None:
        """.lqmb/tests/ is declared template-managed and its fixtures
        legitimately contain example 'bad' invocation strings as plain data
        (see this very test suite) -- it must be excluded from the scan
        entirely, not merely rely on comment/docstring stripping, since
        those strings are ordinary string literals, not comments.
        """

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".lqmb/tests").mkdir(parents=True)
            (root / ".lqmb/tests/test_fixture_example.py").write_text(
                'BAD_EXAMPLE = "run: |\\n  python3 tests/test_validate_metadata.py -v\\n"\n'
            )
            tracked = [".lqmb/tests/test_fixture_example.py"]
            manifest = sample_manifest(template_managed_paths=[".lqmb/tests/"])

            errors = check_no_managed_file_references_a_protected_path(
                manifest, tracked, root
            )
            self.assertEqual(errors, [])

    def test_ignores_a_bad_invocation_written_only_in_a_comment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".github/workflows").mkdir(parents=True)
            (root / ".github/workflows/ci.yml").write_text(
                "run: |\n"
                "  # do not do this: python3 tests/test_validate_metadata.py\n"
                "  python3 .lqmb/bin/validate_metadata.py\n"
            )
            tracked = [".github/workflows/ci.yml"]

            errors = check_no_managed_file_references_a_protected_path(
                sample_manifest(), tracked, root
            )
            self.assertEqual(errors, [])

    def test_ignores_a_bad_invocation_written_only_in_a_python_docstring(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".lqmb/bin").mkdir(parents=True)
            (root / ".lqmb/bin/helper.py").write_text(
                '"""Explains why we no longer run python3 tests/foo.py here."""\n'
                "print('nothing protected referenced')\n"
            )
            tracked = [".lqmb/bin/helper.py"]
            manifest = sample_manifest(template_managed_paths=[".lqmb/bin/"])

            errors = check_no_managed_file_references_a_protected_path(
                manifest, tracked, root
            )
            self.assertEqual(errors, [])


class LiveRepositoryTests(unittest.TestCase):
    """Sanity check against this repository's actual current state."""

    def test_current_manifest_is_hygienic(self) -> None:
        import json
        import subprocess

        manifest = json.loads((ROOT / ".lqmb" / "manifest.json").read_text())
        tracked = subprocess.run(
            ["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True
        ).stdout.splitlines()

        errors = []
        errors += check_paths_exist(manifest, ROOT)
        errors += check_classes_disjoint(manifest)
        errors += check_full_coverage(manifest, tracked)
        errors += check_no_managed_file_references_a_protected_path(manifest, tracked, ROOT)

        self.assertEqual(errors, [], msg="\n".join(errors))


if __name__ == "__main__":
    unittest.main()
