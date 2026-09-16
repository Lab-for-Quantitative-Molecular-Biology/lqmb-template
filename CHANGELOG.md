# Changelog

## 0.2.4 — patch release

### Fixed

- `examples/` was unusable for its documented purpose. `CLAUDE.md` and `data/README.md` both direct contributors to keep small, non-sensitive example datasets in `examples/`, but the scientific-format patterns in the template-managed `.gitignore` are unanchored and therefore match at every depth. `examples/mini.bam`, `examples/demo.vcf`, `examples/demo.h5ad`, `examples/demo.parquet` and similar fixtures were silently ignored: `git add` succeeded with no output, CI passed, and the fixture was absent from the repository, surfacing only on another contributor's clone. `.csv` and `.tsv` were unaffected, so the failure appeared intermittent and depended on the fixture's file type.
- Added a `!examples/**` negation to `.gitignore`, positioned after the scientific-format block and before the secrets, log, OS and cache patterns. Git applies the last matching pattern, so data formats are now trackable under `examples/` while `examples/.DS_Store`, `examples/secrets.json`, `examples/*.key`, `examples/.env`, `examples/*.log` and `examples/__pycache__/` remain ignored. A negation placed at the end of the file would instead have re-included `.DS_Store` and tripped the existing tracked-artefact check. Protection of `data/`, `outputs/` and the repository root is unchanged.
- `.lqmb/manifest.json` was missing a classification for `CHANGELOG.md` and `LICENSE`: neither fell under any of the four path classes, even though `ci.yml` requires both to exist. Both are now `protected_paths` (project-owned, like `docs/decisions.md` and `docs/research-log.md`), and this gap is exactly what the new manifest hygiene check below now catches mechanically.

### Enforcement

Addresses two of the three items listed under "Close the loop between policy and enforcement" in the organisation's Future directions notes (the third, a local commit-msg hook, was tried and then deliberately dropped -- see below):

- **AI provenance in CI.** `AI_PROVENANCE.md` requires `AI-Assisted`/`AI-Role` to be real Git trailers, not body prose — a blank line before an adjacent trailer such as `Co-Authored-By` silently breaks Git's trailer detection, so only the last paragraph is read as a trailer. Added `.lqmb/bin/check_ai_provenance.py`, wired into `ci.yml` over each push or PR's commit range. A local commit-msg hook was also built and tried, but dropped before merge: this framework's actual enforcement point is CI at the PR boundary, the hook could not be mandated (a contributor still has to opt in to install it, and `--no-verify` bypasses it trivially), and it added real operational complexity — including breaking against a checked-out tree from before its own dependency existed, discovered while testing it against this branch's own history. The CI check alone already fully closes the loop that matters.
  - **Incident and fix.** This bundle was first merged to `main` as PR #6 (merge commit `e7930e1`). `ci.yml`'s `push`-event range then spans `before..after`, which for a "Create a merge commit" merge includes the merge commit itself — a commit GitHub generates, not a contributor, carrying no trailer of its own. `check_ai_provenance.py` correctly flagged it as missing `AI-Assisted`, so `main`'s CI failed immediately after a fully green PR run (whose `pull_request`-event range only ever spanned the PR branch's own commits, never the merge commit that didn't exist yet). PR #6 was reverted (PR #7) rather than left red. `check_ai_provenance.py` now exempts any commit with more than one parent from the trailer requirement, with regression tests covering both the exemption and that genuinely malformed non-merge commits still fail; see `AI_PROVENANCE.md`.
- **Manifest hygiene checks.** Added `.lqmb/bin/check_manifest_hygiene.py`, verifying that every path `.lqmb/manifest.json` declares actually exists, that the four path classes are pairwise disjoint, that every tracked file is classified under exactly one of them, and that no template-managed file (YAML workflow, or `.py`/`.sh` script) appears to run a script that lives under a protected path — the exact class of defect fixed in v0.2.3, now checked mechanically so it cannot recur silently.
- **Derive CI assertions from metadata.** `ci.yml` no longer hard-codes the template version literal; `validate_metadata.py` already asserted `TEMPLATE_VERSION` against `manifest.json` and, for the template itself, `project.json`, so the hard-coded comparison was a fourth, unnecessary place to hand-edit at every release. Version duplication is now three files (`TEMPLATE_VERSION`, `.lqmb/manifest.json`, `.lqmb/project.json`) plus `README.md`'s prose mention, rather than five.

### CI

- Added a "Check example dataset sizes" step, warning when a tracked file under `examples/` exceeds 1 MiB. This restores a deliberate size limit in place of the accidental one the ignore patterns previously provided. The step emits a GitHub warning and exits 0 rather than failing, because `examples/` is a `protected_path` while `.github/workflows/ci.yml` is a `template_managed_path`; a hard failure would repeat the managed-versus-protected defect fixed in v0.2.2 and v0.2.3.
- Checkout now uses `fetch-depth: 0` so the AI-provenance check has the commit range available to walk.
- `.github/workflows/ci.yml`'s "Validate template self metadata" step no longer hard-codes a `TEMPLATE_VERSION` comparison (see "Derive CI assertions from metadata" above); `validate_metadata.py` alone now covers that assertion.

## 0.2.3 — patch release

### Fixed

- Relocated the metadata-validation regression tests from `tests/test_validate_metadata.py` to `.lqmb/tests/test_validate_metadata.py`. `tests/` is a `protected_path` — project-owned and never synced from the template — yet the v0.2.2 fix added the CI step `python3 -m unittest tests/test_validate_metadata.py -v` to the template-managed `.github/workflows/ci.yml`, so any downstream project adopting v0.2.2 verbatim would get a CI step referencing a test file the sync process has no mandate to provide, breaking CI again for a new reason.
- `.lqmb/tests/` is now a declared `template_managed_path` in `.lqmb/manifest.json`, so the regression tests travel with `.lqmb/bin/validate_metadata.py` and `.github/workflows/ci.yml` as one consistent, adoptable unit.

### CI

- `.github/workflows/ci.yml`'s "Validate template self metadata" step now checks `TEMPLATE_VERSION` against `0.2.3` and its regression-test step runs `.lqmb/tests/test_validate_metadata.py` directly as a script (`python3 .lqmb/tests/test_validate_metadata.py -v`) rather than via `python3 -m unittest <path>`: unittest's module loader converts the path to a dotted module name, and the leading `.lqmb` component (a dot-prefixed directory) produces an invalid empty module name.
- Added `.lqmb/tests/test_validate_metadata.py` to the required-files check, mirroring the existing entry for `.lqmb/bin/template-status.py`.

## 0.2.2 — patch release

### Fixed

- Fixed a CI bug where the "Validate template self metadata" step in `.github/workflows/ci.yml` unconditionally asserted the *template's own* self-referential invariants (`project.type == "lqmb-template"`, `template.commit == "self"`, a top-level `release` key), even though `.github/workflows/ci.yml` is a template-managed path shipped verbatim to every downstream project. Every downstream project's `.lqmb/project.json` has a different, equally legitimate shape (a real adopted `template.version`/`commit`, no `release` key), so this step failed on every downstream repository that adopted v0.2.1.
- The validation now branches on `project.project.type`: `"lqmb-template"` keeps the self-referential checks; any other type validates downstream invariants instead (real non-`"self"` `template.version`/`commit`, `manifest.template_version` matching `TEMPLATE_VERSION`, no `release` key required).
- Corrected `README.md`'s "This template is **v0.2.0**." version line, which had already fallen one release behind at the v0.2.1 tag.

### CI

- Extracted the metadata-validation logic from an inline CI heredoc into `.lqmb/bin/validate_metadata.py` (already a template-managed path) so it is testable and shared between the template and downstream projects that adopt this release.
- Added `tests/test_validate_metadata.py`, covering both template-shaped and a synthetic downstream-shaped `project.json`/`manifest.json`, including regression cases for the bug above.
- Added a CI step running these regression tests.

## 0.2.1 — patch release

### Fixed

- Corrected the canonical LQMB GitHub organisation URL to `Lab-for-Quantitative-Molecular-Biology`.
- Corrected the template repository's self-referential metadata so it does not pin itself to a downstream release.
- Fixed invalid JSON in `.lqmb/project.json`.
- Clarified the distinction between template-managed and project-configured `.lqmb` paths.
- Added read-only upstream release checking to `template-status.py`.
- Added explicit dependency/update protocol guidance.
- Strengthened Claude instructions so commits, pushes and pull requests require explicit human authorisation.
- Clarified that `Human-Reviewer` may only be recorded after actual human review.

### CI

- Updated `actions/checkout` to `v7`, which uses the current Node 24 runtime. GitHub's checkout release history documents the Node 24 migration in the newer releases.
- Added validation that template self-metadata are internally consistent.
- Added validation for required `.lqmb` files.
- Added detection of tracked `.DS_Store` and `__MACOSX` artefacts.
- Improved JSON metadata validation.
- Added validation of the read-only template-status tool.

## 0.2.0

- Added explicit AI provenance policy and pull-request disclosure.
- Added research-data commit prevention in `.gitignore` and CI.
- Added data-storage guidance.
- Added `.lqmb` metadata and template/dependency framework.
- Added living-project framework documentation.
- Added template update protocol.

## 0.1.0

- Initial LQMB living research project template.
