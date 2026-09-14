#!/usr/bin/env python3
"""Validate ``.lqmb/project.json`` against ``.lqmb/manifest.json``.

This file is a template-managed path (``.lqmb/bin/``) and is shipped
verbatim to every downstream project, so it must not assume the
repository it runs in is the canonical ``lqmb-template`` itself.

- When ``project.project.type == "lqmb-template"``, this repository is the
  canonical template and its ``.lqmb/project.json`` is expected to use the
  self-referential sentinels documented in
  ``docs/lqmb/LQMB_LIVING_PROJECT_FRAMEWORK.md`` and ``.lqmb/README.md``.
- Otherwise this is a downstream project, which records a real adopted
  template release/commit and has no top-level ``release`` key.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


def validate(project: dict[str, Any], manifest: dict[str, Any], template_version_file: str) -> None:
    """Raise ``AssertionError`` if project/manifest metadata are inconsistent."""

    project_type = project["project"]["type"]
    template = project["template"]

    assert manifest["template_version"] == template_version_file, (
        f"manifest.template_version ({manifest['template_version']!r}) does not match "
        f"TEMPLATE_VERSION ({template_version_file!r})"
    )

    if project_type == "lqmb-template":
        # The canonical template cannot pin itself to its own future release.
        assert template["version"] == "self"
        assert template["commit"] == "self"
        assert template["sync_policy"] == "self"
        assert project["release"]["version"] == template_version_file
    else:
        # Downstream projects record an immutable adopted release and commit,
        # and have no self-referential "release" key.
        assert template["version"] not in ("self", "", None), (
            "downstream project.json must record a real adopted template "
            "release, not the template's own 'self' sentinel"
        )
        assert template["commit"] not in ("self", "", None), (
            "downstream project.json must record a real adopted template "
            "commit, not the template's own 'self' sentinel"
        )
        assert template["sync_policy"] != "self", (
            "downstream project.json must not use the template's own "
            "'self' sync policy"
        )

    managed = set(manifest["template_managed_paths"])
    configured = set(manifest["project_configured_paths"])

    assert ".lqmb/project.json" in configured
    assert ".lqmb/dependencies.json" in configured
    assert ".lqmb/manifest.json" in managed
    assert ".lqmb/project.json" not in managed
    assert ".lqmb/dependencies.json" not in managed


def main() -> int:
    project = json.loads((ROOT / ".lqmb" / "project.json").read_text())
    manifest = json.loads((ROOT / ".lqmb" / "manifest.json").read_text())
    template_version_file = (ROOT / "TEMPLATE_VERSION").read_text().strip()

    validate(project, manifest, template_version_file)

    print("Project/template metadata and manifest are consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
