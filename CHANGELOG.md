# Changelog

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
