# LQMB Living Project Framework

## The idea

LQMB treats a research project as a living scientific object rather than as a
temporary container for a paper.

Projects can persist through changing people, questions, datasets, models,
methods and publications.

The repository therefore records both the project's scientific work and its
relationships to upstream templates and external dependencies.

## Three layers

### 1. The living project

Contains the project's own scientific and computational work.

### 2. The LQMB template

Defines common laboratory infrastructure and working conventions.

### 3. Dependencies

Record specific versions of other research/software/data/citation objects on
which the project depends.

## Template relationship

A project does not inherit a permanent static copy of the template.

Instead it records:

```text
template release
template commit
```

and can later propose an explicit update.

This keeps the project historically reproducible while allowing the LQMB
framework itself to evolve.

## Why updates are not automatic

Template changes can affect project workflows, provenance, AI instructions,
repository hygiene and documentation. An apparently harmless change may have
scientific or computational consequences.

Therefore:

```text
detect
  ↓
inform
  ↓
human decides
  ↓
prepare update
  ↓
review diff
  ↓
PR
  ↓
merge
```

## Contribution model

Changes to the template itself are ordinary LQMB contributions. Any authorised
member should be able to propose a change through a branch and pull request.

The template is therefore itself a living project.

## Long-term model

The same mechanism can support:

- LQMB project-to-project dependencies;
- shared LQMB software;
- external software dependencies;
- datasets;
- protocols;
- publications and methods;
- future external research collaborations.

The result is a versioned network of living research objects rather than a set
of isolated paper repositories.
