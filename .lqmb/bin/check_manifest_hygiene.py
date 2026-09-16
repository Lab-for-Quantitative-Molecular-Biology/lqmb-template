#!/usr/bin/env python3
"""Check the internal hygiene of .lqmb/manifest.json.

manifest.json sorts every repository path into one of four classes
(template_managed_paths, project_configured_paths, protected_paths,
shared_paths). That classification is the mechanism that lets shared
infrastructure evolve without ever overwriting project-owned content, so
this script checks the properties it depends on:

- every declared path actually exists;
- the four classes are pairwise disjoint (no path, and no directory/file
  pair, is claimed by more than one class);
- every tracked file in the repository is covered by exactly one class;
- no template-managed file appears to run a script that lives under a
  protected path.

The last check is a best-effort static scan, not a proof: it is aimed
squarely at the class of defect fixed in template v0.2.3, where
.github/workflows/ci.yml (template-managed, shipped verbatim to every
downstream project) invoked a test file under tests/ (protected,
project-owned) that a downstream project would never have been given.
It scans .yml/.yaml/.py/.sh files under template_managed_paths, with
comments and Python docstrings stripped first to reduce false positives
from prose that merely discusses such a path rather than running it. It
deliberately excludes .lqmb/tests/: that directory's own purpose is to
exercise this detection logic, so it legitimately contains crafted
"bad" example strings as test fixtures, not real invocations. The
regex matches embedded shell-command text (e.g. a YAML `run:` block, or
a Python script using os.system/subprocess with a literal command
string), not Python's list-argument subprocess form
(subprocess.run(["python3", path])), which is a real gap in this
heuristic, not something it claims to cover.

This file is itself a template-managed path (.lqmb/bin/) shipped verbatim
to every downstream project, so it must not assume anything about the
repository it runs in beyond what manifest.json and `git ls-files` report.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATH_CLASSES = (
    "template_managed_paths",
    "project_configured_paths",
    "protected_paths",
    "shared_paths",
)

# Matches `python3 <path>` / `bash <path>` / `sh <path>` / `source <path>`
# invocations, e.g. inside a YAML workflow's `run:` script blocks or a
# Python script's own subprocess calls written as plain shell text.
SCRIPT_EXEC_RE = re.compile(r"\b(?:python3?|bash|sh|source)\s+([\w.][\w./-]*\.(?:py|sh))\b")

# File types scanned by check_no_managed_file_references_a_protected_path.
SCANNED_SUFFIXES = {".yml", ".yaml", ".py", ".sh"}

# template_managed_paths entries excluded from that scan: this directory's
# purpose is to test the detection logic itself, so its fixtures legitimately
# contain example "bad" invocation strings that are not real invocations.
SCAN_EXCLUDED_PREFIXES = (".lqmb/tests/",)

_PY_DOCSTRING_RE = re.compile(r'("""|\'\'\')(?:(?!\1).)*?\1', re.DOTALL)


def _strip_comments_and_docstrings(text: str, suffix: str) -> str:
    """Best-effort removal of prose before scanning for real invocations.

    This is a heuristic, not a parser: a '#' or a triple-quote inside an
    unrelated string literal can still confuse it. Good enough to keep this
    checker's own explanatory docstrings from self-triggering.
    """

    if suffix == ".py":
        text = _PY_DOCSTRING_RE.sub("", text)
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def declared_paths(manifest: dict) -> list[tuple[str, str]]:
    """Return (class_name, path) pairs across all four path classes."""

    return [(cls, path) for cls in PATH_CLASSES for path in manifest.get(cls, [])]


def _overlaps(path_a: str, path_b: str) -> bool:
    """Whether two declared paths claim any of the same repository content."""

    if path_a == path_b:
        return True
    if path_a.endswith("/") and (path_b == path_a.rstrip("/") or path_b.startswith(path_a)):
        return True
    if path_b.endswith("/") and (path_a == path_b.rstrip("/") or path_a.startswith(path_b)):
        return True
    return False


def check_paths_exist(manifest: dict, root: Path) -> list[str]:
    errors = []
    for cls, path in declared_paths(manifest):
        if not (root / path.rstrip("/")).exists():
            errors.append(f"{cls}: declared path {path!r} does not exist")
    return errors


def check_classes_disjoint(manifest: dict) -> list[str]:
    errors = []
    entries = declared_paths(manifest)
    for i, (cls_a, path_a) in enumerate(entries):
        for cls_b, path_b in entries[i + 1 :]:
            if cls_a == cls_b:
                continue
            if _overlaps(path_a, path_b):
                errors.append(
                    f"{path_a!r} ({cls_a}) and {path_b!r} ({cls_b}) overlap, "
                    "but path classes must be disjoint"
                )
    return errors


def _covering_classes(tracked_file: str, manifest: dict) -> list[str]:
    covering = []
    for cls in PATH_CLASSES:
        for path in manifest.get(cls, []):
            if path.endswith("/"):
                matches = tracked_file == path.rstrip("/") or tracked_file.startswith(path)
            else:
                matches = tracked_file == path
            if matches:
                covering.append(cls)
                break
    return covering


def check_full_coverage(manifest: dict, tracked_files: list[str]) -> list[str]:
    errors = []
    for tracked_file in tracked_files:
        covering = _covering_classes(tracked_file, manifest)
        if not covering:
            errors.append(f"tracked file {tracked_file!r} is not classified under any path class")
        elif len(covering) > 1:
            errors.append(
                f"tracked file {tracked_file!r} is classified under multiple "
                f"path classes: {covering}"
            )
    return errors


def _files_under(manifest_path: str, tracked_files: list[str]) -> list[str]:
    if manifest_path.endswith("/"):
        return [f for f in tracked_files if f == manifest_path.rstrip("/") or f.startswith(manifest_path)]
    return [manifest_path] if manifest_path in tracked_files else []


def check_no_managed_file_references_a_protected_path(
    manifest: dict, tracked_files: list[str], root: Path
) -> list[str]:
    protected_entries = manifest.get("protected_paths", [])
    errors: list[str] = []

    for managed_entry in manifest.get("template_managed_paths", []):
        if managed_entry.startswith(SCAN_EXCLUDED_PREFIXES):
            continue
        for file_path in _files_under(managed_entry, tracked_files):
            if file_path.startswith(SCAN_EXCLUDED_PREFIXES):
                continue
            suffix = Path(file_path).suffix
            if suffix not in SCANNED_SUFFIXES:
                continue
            full_path = root / file_path
            if not full_path.is_file():
                continue
            text = _strip_comments_and_docstrings(full_path.read_text(), suffix)
            for match in SCRIPT_EXEC_RE.finditer(text):
                referenced = match.group(1)
                if referenced.startswith("./"):
                    referenced = referenced[2:]
                for protected_entry in protected_entries:
                    if _overlaps(referenced, protected_entry):
                        errors.append(
                            f"{file_path!r} (template_managed_paths) appears to "
                            f"run {referenced!r}, which falls under the "
                            f"protected path {protected_entry!r}; a downstream "
                            "project's copy of this file would reference "
                            "content it was never given"
                        )
    return errors


def _git_ls_files(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"], cwd=root, capture_output=True, text=True, check=True
    )
    return [line for line in result.stdout.splitlines() if line]


def main() -> int:
    manifest = json.loads((ROOT / ".lqmb" / "manifest.json").read_text())
    tracked_files = _git_ls_files(ROOT)

    errors: list[str] = []
    errors += check_paths_exist(manifest, ROOT)
    errors += check_classes_disjoint(manifest)
    errors += check_full_coverage(manifest, tracked_files)
    errors += check_no_managed_file_references_a_protected_path(manifest, tracked_files, ROOT)

    if errors:
        print("Manifest hygiene check failed:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(
        "Manifest hygiene checks passed: declared paths exist, path classes "
        "are disjoint, every tracked file is classified exactly once, and no "
        "template-managed file appears to run a protected-path script."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
