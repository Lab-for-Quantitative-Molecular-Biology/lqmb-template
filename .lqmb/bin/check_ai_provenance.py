#!/usr/bin/env python3
"""Verify AI provenance Git trailers on a range of commits.

AI_PROVENANCE.md requires ``AI-Assisted`` / ``AI-Role`` (or
``AI-Assisted: None``) to be real Git trailers, detectable with
``git show -s --format='%(trailers:unfold)'`` -- not merely lines that look
like trailers somewhere in the commit message body. A blank line between the
provenance block and an adjacent trailer such as ``Co-Authored-By`` breaks
Git's trailer detection: only the last *contiguous* block of trailer-shaped
lines at the end of the message counts, so everything above the blank line
is read back as body prose instead. This script is a template-managed path
shipped verbatim to every downstream project, so it must not assume
anything about that project's own commit history beyond the base/head range
it is given.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

TRAILER_LINE_RE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*): (.*)$")
VALID_AI_ASSISTED = {"Claude", "None"}
VALID_AI_ROLE = {"Generated", "Modified", "Assisted"}


def _run_git(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout


def commits_in_range(base: str, head: str, cwd: Path | None = None) -> list[str]:
    """Return commit SHAs reachable from ``head`` but not from ``base``, oldest first."""

    out = _run_git(["rev-list", "--reverse", f"{base}..{head}"], cwd=cwd)
    return [line for line in out.splitlines() if line]


def trailers_for(commit: str, cwd: Path | None = None) -> dict[str, list[str]]:
    """Return the real Git trailers of ``commit`` as ``{key: [values]}``."""

    raw = _run_git(["show", "-s", "--format=%(trailers:unfold)", commit], cwd=cwd)
    trailers: dict[str, list[str]] = {}
    for line in raw.splitlines():
        match = TRAILER_LINE_RE.match(line)
        if match:
            trailers.setdefault(match.group(1), []).append(match.group(2))
    return trailers


def check_commit(commit: str, cwd: Path | None = None) -> list[str]:
    """Return a list of provenance errors for ``commit`` (empty if compliant)."""

    trailers = trailers_for(commit, cwd=cwd)
    errors: list[str] = []

    ai_assisted = trailers.get("AI-Assisted")
    if not ai_assisted:
        errors.append(
            "missing 'AI-Assisted' Git trailer (AI_PROVENANCE.md requires "
            "'AI-Assisted: Claude' or 'AI-Assisted: None')"
        )
        return errors

    if len(ai_assisted) > 1:
        errors.append("'AI-Assisted' trailer given more than once")
        return errors

    if ai_assisted[0] not in VALID_AI_ASSISTED:
        errors.append(
            f"'AI-Assisted: {ai_assisted[0]}' is not one of {sorted(VALID_AI_ASSISTED)}"
        )
        return errors

    if ai_assisted[0] == "Claude":
        ai_role = trailers.get("AI-Role")
        if not ai_role:
            errors.append(
                "'AI-Assisted: Claude' requires an 'AI-Role' trailer "
                f"(one of {sorted(VALID_AI_ROLE)})"
            )
        elif len(ai_role) > 1:
            errors.append("'AI-Role' trailer given more than once")
        elif ai_role[0] not in VALID_AI_ROLE:
            errors.append(
                f"'AI-Role: {ai_role[0]}' is not one of {sorted(VALID_AI_ROLE)}"
            )

    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="exclusive start of the commit range")
    parser.add_argument("--head", default="HEAD", help="inclusive end of the commit range")
    args = parser.parse_args(argv)

    commits = commits_in_range(args.base, args.head)
    if not commits:
        print(f"No commits in range {args.base}..{args.head}; nothing to check.")
        return 0

    failed = False
    for commit in commits:
        errors = check_commit(commit)
        subject = _run_git(["show", "-s", "--format=%s", commit]).strip()
        short = commit[:12]
        if errors:
            failed = True
            print(f"ERROR: {short} {subject!r}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK: {short} {subject!r}")

    if failed:
        print()
        print(
            "See AI_PROVENANCE.md. Trailers must be real Git trailers with no "
            "blank line separating them from each other or from an adjacent "
            "trailer such as Co-Authored-By -- a blank line ends the trailer "
            "block early and everything above it is read back as body prose."
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
