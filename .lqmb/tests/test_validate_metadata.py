"""Regression tests for .lqmb/bin/validate_metadata.py.

Guards against the bug where the CI metadata-validation step unconditionally
asserted the *template's own* self-referential invariants (project.type ==
"lqmb-template", template.commit == "self", a top-level "release" key) even
though .github/workflows/ci.yml is a template-managed path shipped verbatim
to every downstream project, whose .lqmb/project.json has a different,
equally legitimate shape (see docs/lqmb/TEMPLATE_UPDATE_PROTOCOL.md).
"""
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

spec = importlib.util.spec_from_file_location(
    "validate_metadata", ROOT / ".lqmb" / "bin" / "validate_metadata.py"
)
validate_metadata = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validate_metadata
spec.loader.exec_module(validate_metadata)

validate = validate_metadata.validate


def downstream_project(**overrides):
    project = {
        "schema_version": "0.2",
        "project": {"name": "mock-project", "type": "lqmb-research-project"},
        "template": {
            "repository": "https://github.com/Lab-for-Quantitative-Molecular-Biology/lqmb-template",
            "version": "0.2.1",
            "commit": "6d58cb61b262e8098678844b01ab30b51ae5c861",
            "sync_policy": "prompt",
        },
        "dependencies_file": ".lqmb/dependencies.json",
    }
    project.update(overrides)
    return project


def downstream_manifest(template_version="0.2.1"):
    return {
        "schema_version": "0.2",
        "template_version": template_version,
        "template_managed_paths": [".lqmb/manifest.json", ".lqmb/bin/"],
        "project_configured_paths": [".lqmb/project.json", ".lqmb/dependencies.json"],
        "protected_paths": [],
        "shared_paths": [],
    }


class TemplateSelfMetadataTests(unittest.TestCase):
    def test_current_template_metadata_is_valid(self):
        project = json.loads((ROOT / ".lqmb" / "project.json").read_text())
        manifest = json.loads((ROOT / ".lqmb" / "manifest.json").read_text())
        template_version_file = (ROOT / "TEMPLATE_VERSION").read_text().strip()

        validate(project, manifest, template_version_file)

    def test_template_release_must_match_template_version_file(self):
        project = json.loads((ROOT / ".lqmb" / "project.json").read_text())
        manifest = json.loads((ROOT / ".lqmb" / "manifest.json").read_text())

        with self.assertRaises(AssertionError):
            validate(project, manifest, "9.9.9")


class DownstreamProjectMetadataTests(unittest.TestCase):
    """This is the regression coverage for the reported bug."""

    def test_downstream_shaped_project_is_valid(self):
        project = downstream_project()
        manifest = downstream_manifest()

        validate(project, manifest, "0.2.1")

    def test_downstream_project_needs_no_release_key(self):
        project = downstream_project()
        self.assertNotIn("release", project)
        manifest = downstream_manifest()

        validate(project, manifest, "0.2.1")

    def test_downstream_project_rejects_self_template_version(self):
        project = downstream_project()
        project["template"]["version"] = "self"
        manifest = downstream_manifest()

        with self.assertRaises(AssertionError):
            validate(project, manifest, "0.2.1")

    def test_downstream_project_rejects_self_template_commit(self):
        project = downstream_project()
        project["template"]["commit"] = "self"
        manifest = downstream_manifest()

        with self.assertRaises(AssertionError):
            validate(project, manifest, "0.2.1")

    def test_downstream_project_rejects_self_sync_policy(self):
        project = downstream_project()
        project["template"]["sync_policy"] = "self"
        manifest = downstream_manifest()

        with self.assertRaises(AssertionError):
            validate(project, manifest, "0.2.1")

    def test_downstream_manifest_template_version_must_match_file(self):
        project = downstream_project()
        manifest = downstream_manifest(template_version="0.2.0")

        with self.assertRaises(AssertionError):
            validate(project, manifest, "0.2.1")


if __name__ == "__main__":
    unittest.main()
