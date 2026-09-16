# Changelog

## 0.2.4 — patch release

### Fixed

- `examples/` was unusable for its documented purpose. `CLAUDE.md` and `data/README.md` both direct contributors to keep small, non-sensitive example datasets in `examples/`, but the scientific-format patterns in the template-managed `.gitignore` are unanchored and therefore match at every depth. `examples/mini.bam`, `examples/demo.vcf`, `examples/demo.h5ad`, `examples/demo.parquet` and similar fixtures were silently ignored: `git add` succeeded with no output, CI passed, and the fixture was absent from the repository, surfacing only on another contributor's clone. `.csv` and `.tsv` were unaffected, so the failure appeared intermittent and depended on the fixture's file type.
- Added a `!examples/**` negation to `.gitignore`, positioned after the scientific-format block and before the secrets, log, OS and cache patterns. Git applies the last matching pattern, so data formats are now trackable under `examples/` while `examples/.DS_Store`, `examples/secrets.json`, `examples/*.key`, `examples/.env`, `examples/*.log` and `examples/__pycache__/` remain ignored. A negation placed at the end of the file would instead have re-included `.DS_Store` and tripped the existing tracked-artefact check. Protection of `data/`, `outputs/` and the repository root is unchanged.

### CI

- Added a "Check example dataset sizes" step, warning when a tracked file under `examples/` exceeds 1 MiB. This restores a deliberate size limit in place of the accidental one the ignore patterns previously provided. The step emits a GitHub warning and exits 0 rather than failing, because `examples/` is a `protected_path` while `.github/workflows/ci.yml` is a `template_managed_path`; a hard failure would repeat the managed-versus-protected defect fixed in v0.2.2 and v0.2.3.
- `.github/workflows/ci.yml`'s "Validate template self metadata" step now checks `TEMPLATE_VERSION` against `0.2.4`.

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
