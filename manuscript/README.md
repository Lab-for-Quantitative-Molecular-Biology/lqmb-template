# Manuscript

Manuscripts are outputs of the living project. They do not define the project's lifetime or structure.

Create subdirectories here when a project produces multiple manuscripts, preprints, or thesis outputs.

Keep this directory even if the project never produces a manuscript. Every LQMB project carries
the same skeleton and CI requires it (see `docs/decisions.md`, 2026-09-16). Keep this `README.md`
too: git does not track empty directories, so deleting it removes `manuscript/` from a clean
checkout and CI fails while your local working tree still looks correct.
