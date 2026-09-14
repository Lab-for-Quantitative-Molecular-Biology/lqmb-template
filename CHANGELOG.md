# Changelog

## 0.2.0 — 2026-09-14

### Added

- `.lqmb/project.json` for explicit project identity and exact template provenance.
- `.lqmb/dependencies.json` for versioned research/software/publication dependencies and living citations.
- `.lqmb/manifest.json` defining template-managed, protected and future shared paths.
- Human-readable LQMB Living Project Framework documentation.
- Explicit Template Update Protocol.
- Local metadata inspection script for first-interaction checks.

### Changed

- `CLAUDE.md` now requires first-interaction template/dependency checks and human approval before updates.
- `CLAUDE.md` clarifies that `data/` is not a default raw-data store.
- AI provenance now requires structured Git trailers and forbids claiming human review before it occurs.
- Template updates are defined as ordinary, reviewable project changes rather than silent synchronisation.
- `CONTRIBUTING.md` now describes template-update and AI-provenance workflows.
- CI and repository hygiene are aligned with the living-project metadata.

### Important compatibility note

Version 0.2 is a framework update from v0.1. Existing projects should migrate deliberately using the supplied migration guide. Do not replace an existing project by copying the v0.2 template over it.

## 0.1.0

Initial LQMB living research repository template.
