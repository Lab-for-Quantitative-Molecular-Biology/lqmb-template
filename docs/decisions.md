# Decisions

Record consequential scientific, analytical, computational, or organisational decisions.

## 2026-09-16 — CI requires the full project skeleton, including unused directories

### Decision

`.github/workflows/ci.yml` hard-requires the directories `src/`, `tests/`, `scripts/`,
`workflows/`, `configs/`, `notebooks/` and `manuscript/`, and the file `README.md`, even though
all eight are `protected_paths` in `.lqmb/manifest.json` and therefore owned by the project
rather than the template. This is deliberate. Every LQMB project keeps the full skeleton, and an
unused directory keeps its placeholder `README.md` rather than being deleted.

### Rationale

A `template_managed_path` asserting a requirement about a `protected_path` is normally a defect:
it lets the template dictate the shape of project-owned space, and it caused three consecutive
patch releases (v0.2.1 to v0.2.3). This case is different in two ways.

First, it cannot break a project. The only adoption path the framework provides is GitHub
"Use this template" or a fork, so every project starts with all seven directories and their
placeholder `README.md` files. CI passes from the first commit.

Second, the cost of compliance is one directory holding a one-line README, set against a real
benefit: `src/` means the same thing in every LQMB repository, so any lab member can navigate an
unfamiliar project without reading its layout first.

### Alternatives considered

Dropping the seven directories from `required_dirs`, or downgrading them from hard failures to
warnings. Both were rejected: they would make the skeleton advisory, and a
skeleton that half the projects follow provides none of the navigational benefit that justifies
it.

### Consequences

A project that produces no manuscript still carries `manuscript/`, and one that keeps its code
outside `src/` still carries an empty `src/`. Those directories must keep their placeholder
`README.md`: git does not track empty directories, so removing the placeholder makes the
directory vanish from a clean checkout and CI fails in Actions while the local working tree still
looks correct. `manuscript/README.md` states this.

This decision covers directory existence only. It does not license the template to assert
anything else about protected paths, and it does not apply to `LICENSE` or `CHANGELOG.md`, which
`ci.yml` also requires but which belong to no manifest path class at all — an unresolved gap.

### Revisit when

A project has a substantive reason to restructure that the skeleton blocks — for example adopting
a language whose packaging conventions conflict with `src/` — or when a bootstrap step exists that
can generate a per-project skeleton, at which point CI could check the project's declared
structure instead of a fixed list.

<!-- Format template for new entries: -->

## YYYY-MM-DD — Decision title

### Decision

### Rationale

### Alternatives considered

### Consequences

### Revisit when

<!-- Optional: state what new evidence would justify revisiting the decision. -->
