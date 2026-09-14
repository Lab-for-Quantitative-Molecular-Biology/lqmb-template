# Changelog

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
