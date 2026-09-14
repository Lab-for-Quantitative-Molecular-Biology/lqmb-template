#!/usr/bin/env python3
"""Read-only LQMB template/dependency status checks.

Default: inspect only local metadata.

--check-upstream: query the canonical template repository for release tags.
This does not modify the repository.

--json: emit machine-readable output.

The command never changes files, Git remotes, branches, commits, or tags.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
META = ROOT / ".lqmb" / "project.json"
DEPS = ROOT / ".lqmb" / "dependencies.json"
MANIFEST = ROOT / ".lqmb" / "manifest.json"
VERSION_FILE = ROOT / "TEMPLATE_VERSION"

SEMVER_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def local_status() -> dict[str, Any]:
    missing = [str(p.relative_to(ROOT)) for p in (META, DEPS, MANIFEST) if not p.exists()]
    if missing:
        return {"ok": False, "error": f"Missing LQMB metadata: {', '.join(missing)}"}

    project = load(META)
    deps = load(DEPS)
    manifest = load(MANIFEST)
    template = project.get("template", {})
    template_version = template.get("version")
    release = project.get("release", {})

    status: dict[str, Any] = {
        "ok": True,
        "project_name": project.get("project", {}).get("name", "<unknown>"),
        "project_type": project.get("project", {}).get("type", "<unknown>"),
        "template_repository": template.get("repository"),
        "template_version": template_version,
        "template_commit": template.get("commit"),
        "sync_policy": template.get("sync_policy"),
        "dependencies": len(deps.get("dependencies", [])),
        "template_managed_paths": len(manifest.get("template_managed_paths", manifest.get("managed_paths", []))),
        "project_configured_paths": len(manifest.get("project_configured_paths", [])),
        "protected_paths": len(manifest.get("protected_paths", [])),
        "shared_paths": len(manifest.get("shared_paths", [])),
        "manifest_template_version": manifest.get("template_version"),
        "root_template_version": VERSION_FILE.read_text(encoding="utf-8").strip() if VERSION_FILE.exists() else None,
        "release_version": release.get("version"),
    }

    if project.get("project", {}).get("type") == "lqmb-template":
        status["template_self_reference"] = (
            template.get("version") == "self"
            and template.get("commit") == "self"
            and template.get("sync_policy") == "self"
        )
    else:
        status["template_self_reference"] = False

    try:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        status["current_project_commit"] = head
    except Exception:
        status["current_project_commit"] = None

    return status


def semver_key(tag: str) -> tuple[int, int, int] | None:
    match = SEMVER_TAG.match(tag)
    return tuple(int(v) for v in match.groups()) if match else None


def upstream_releases(repository: str) -> list[tuple[str, str]]:
    completed = subprocess.run(
        ["git", "ls-remote", "--tags", repository],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "git ls-remote failed")

    tag_objects: dict[str, str] = {}
    peeled_commits: dict[str, str] = {}
    for line in completed.stdout.splitlines():
        if not line.strip():
            continue
        sha, ref = line.split("\t", 1)
        if ref.endswith("^{}"):
            tag_ref = ref[:-3]
            tag = tag_ref.rsplit("/", 1)[-1]
            if semver_key(tag):
                peeled_commits[tag] = sha
        else:
            tag = ref.rsplit("/", 1)[-1]
            if semver_key(tag):
                tag_objects[tag] = sha

    releases: list[tuple[str, str]] = []
    for tag in set(tag_objects) | set(peeled_commits):
        # For annotated tags, prefer the peeled commit. For lightweight tags,
        # the tag SHA is the commit SHA.
        releases.append((tag, peeled_commits.get(tag, tag_objects[tag])))

    releases.sort(key=lambda item: semver_key(item[0]) or (0, 0, 0), reverse=True)
    return releases


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-upstream", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    status = local_status()
    if not status.get("ok"):
        print(status["error"])
        return 1

    output = {"local": status}

    if args.check_upstream:
        repo = status["template_repository"]
        if status.get("project_type") == "lqmb-template":
            output["upstream"] = {"status": "skipped", "reason": "This repository is the canonical template itself."}
        else:
            try:
                releases = upstream_releases(repo)
                latest = releases[0] if releases else None
                current_version = status.get("template_version")
                current_key = semver_key(f"v{current_version}") if current_version else None
                latest_key = semver_key(latest[0]) if latest else None
                output["upstream"] = {
                    "status": "ok",
                    "latest_release": latest[0] if latest else None,
                    "latest_commit": latest[1] if latest else None,
                    "recorded_release": current_version,
                    "recorded_commit": status.get("template_commit"),
                    "update_available": bool(latest_key and current_key and latest_key > current_key),
                }
            except Exception as exc:
                output["upstream"] = {
                    "status": "unavailable",
                    "error": str(exc),
                    "message": "Upstream could not be queried. No update should be inferred from local metadata alone.",
                }

    if args.json:
        print(json.dumps(output, indent=2))
    else:
        s = output["local"]
        print("LQMB project status")
        print(f"  Project: {s['project_name']}")
        print(f"  Type: {s['project_type']}")
        print(f"  Template repository: {s['template_repository']}")
        print(f"  Recorded template version: {s['template_version']}")
        print(f"  Recorded template commit: {s['template_commit']}")
        print(f"  Sync policy: {s['sync_policy']}")
        print(f"  Template-managed paths: {s['template_managed_paths']}")
        print(f"  Project-configured paths: {s['project_configured_paths']}")
        print(f"  Protected paths: {s['protected_paths']}")
        print(f"  Declared dependencies: {s['dependencies']}")
        if "upstream" in output:
            print("\nUpstream check")
            u = output["upstream"]
            print(f"  Status: {u.get('status')}")
            if u.get("latest_release"):
                print(f"  Latest release: {u['latest_release']}")
                print(f"  Latest commit: {u['latest_commit']}")
                print(f"  Update available: {u['update_available']}")
            elif u.get("error"):
                print(f"  Error: {u['error']}")
                print("  No update should be inferred from local metadata alone.")
        print("\nRead-only check complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
