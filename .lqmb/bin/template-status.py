#!/usr/bin/env python3
"""Inspect the local LQMB template dependency metadata.

This command is deliberately read-only. It does not fetch, modify or update files.
Use Claude/GitHub tooling to compare the recorded version/commit with the canonical
lqmb-template repository before preparing an update.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / ".lqmb" / "project.json"
DEPS = ROOT / ".lqmb" / "dependencies.json"
MANIFEST = ROOT / ".lqmb" / "manifest.json"


def load(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    missing = [str(p.relative_to(ROOT)) for p in (META, DEPS, MANIFEST) if not p.exists()]
    if missing:
        print("ERROR: missing LQMB metadata: " + ", ".join(missing))
        return 1

    project = load(META)
    deps = load(DEPS)
    manifest = load(MANIFEST)
    template = project.get("template", {})
    print("LQMB project status")
    print(f"  Project: {project.get('project', {}).get('name', '<unknown>')}")
    print(f"  Template repository: {template.get('repository', '<missing>')}")
    print(f"  Recorded template version: {template.get('version', '<missing>')}")
    print(f"  Recorded template commit: {template.get('commit') or '<not recorded>'}")
    print(f"  Sync policy: {template.get('sync_policy', '<missing>')}")
    print(f"  Declared dependencies: {len(deps.get('dependencies', []))}")
    print(f"  Managed paths: {len(manifest.get('managed_paths', []))}")
    print(f"  Protected paths: {len(manifest.get('protected_paths', []))}")
    try:
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        print(f"  Current project commit: {head}")
    except Exception:
        print("  Current project commit: unavailable")
    print("\nRead-only check complete. Compare the recorded template/dependency identifiers with their upstream sources before proposing updates.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
