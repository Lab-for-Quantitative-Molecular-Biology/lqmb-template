# LQMB Template Update Protocol

This is the standard procedure for proposing an update of a living LQMB project to a newer template release.

## Before starting

1. Confirm the project contains `.lqmb/project.json` and `.lqmb/manifest.json`.
2. Read the recorded template version and commit.
3. Check the canonical `lqmb-template` repository for the latest release.
4. Check GitHub for an existing open template-update PR for the same target release.

## If an existing update PR exists

Do not create another branch for the same update. Review, comment on or contribute to the existing PR.

## If no update PR exists

Create:

```text
chore/lqmb-template-vX.Y.Z
```

Then:

1. Obtain the original template version recorded by the project.
2. Obtain the target template version.
3. Read the target template's `.lqmb/manifest.json`.
4. Compare only template-managed paths.
5. Never overwrite protected paths.
6. For a managed file changed upstream but not locally, adopt the upstream file.
7. For a managed file changed locally but not upstream, preserve the project file.
8. For a managed file changed both locally and upstream, stop and request human resolution.
9. Update `.lqmb/project.json` to the new template version and exact commit.
10. Record the update in `CHANGELOG.md` or `docs/decisions.md`.
11. Run the project's normal validation.
12. Review `git diff` and `git status`.
13. Open a pull request describing the old and new template versions, files affected, conflicts resolved and validation performed.
14. Merge only after human review.

## Important safety rule

Never copy the complete template repository over a living project. Template updates are selective and manifest-driven.

## Historical provenance

The project must retain the exact template version/commit used before and after an update through ordinary Git history and the project metadata file.
