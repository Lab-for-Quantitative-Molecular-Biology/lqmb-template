# Data

Research data are not stored in this repository by default.

The repository `.gitignore` is deliberately configured to prevent the contents of `data/` from being committed, except for this documentation and the placeholder file.

## Where data live

Document the approved storage location(s) for this project here. Examples include institutional storage, HPC filesystems, managed object storage, or an approved controlled-access data service.

Do not put credentials, access tokens, confidential URLs, or other secrets in this file.

## Small example data

Small, non-sensitive example datasets required for demonstrations or automated tests should normally live in `examples/`, not `data/`.

## Important warning

`.gitignore` prevents untracked files from being added accidentally; it does not remove files that have already been committed. Before committing, inspect `git status` and `git diff --stat` and verify that no research data or sensitive files are included.
