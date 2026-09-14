# Contributing to LQMB projects

LQMB uses contribution-based collaboration: contributors are encouraged to propose ideas, code, analyses, methods, documentation, review and critique regardless of seniority.

## Start with the project

Before contributing:

1. Read `README.md`.
2. Read `CLAUDE.md`.
3. Read `.lqmb/project.json`, `.lqmb/dependencies.json`, and `.lqmb/manifest.json` where present.
4. Read relevant `docs/` material.
5. Check for existing issues and pull requests addressing the same work.

## Template updates

If the project is behind the current LQMB template:

- do not create an automatic update;
- check for an existing template-update PR;
- if none exists and a human requests the update, follow `docs/lqmb/TEMPLATE_UPDATE_PROTOCOL.md`.

## Changes

Use a branch for substantive changes. Keep changes focused and reviewable.

Before requesting review:

- run appropriate tests/validation;
- inspect `git diff`;
- check for secrets and unintended data;
- update documentation where needed;
- record consequential decisions.

## AI-assisted work

If Claude materially contributed, record AI provenance using the conventions in `AI_PROVENANCE.md`.

Do not record a human reviewer until the human has actually reviewed the work.

## Pull requests

A pull request should make it straightforward for another contributor to understand what changed, why, and what was checked.

Review the work on its scientific and technical merits rather than the seniority of the contributor.
