# LQMB Living Research Project Template

**Laboratory for Quantitative Molecular Biology (LQMB)**  
*Mathematical and computational approaches to molecular biology*

This repository is the **canonical LQMB living research project template**.

It is itself a living project: contributors may propose changes through ordinary Git branches and pull requests, and released changes can subsequently be adopted by active LQMB projects.

## What this template provides

- a reproducible research-project structure;
- explicit scientific documentation;
- AI-assisted development and provenance conventions;
- data-protection defaults;
- contribution-based collaboration practices;
- machine-readable links to the LQMB template and project dependencies;
- a controlled, non-destructive mechanism for proposing template updates.

## Living-project principle

A research repository persists beyond an individual paper. Papers, software, datasets, analyses, methods and follow-up questions are outputs of the project rather than its organisational centre.

## v0.2 framework

Version 0.2 introduces the `.lqmb/` metadata layer.

```text
.lqmb/
├── project.json
├── dependencies.json
├── manifest.json
└── README.md
```

`project.json` records the template version and exact commit adopted by the project.

`dependencies.json` records other software, projects, datasets, methods and publications on which the project depends.

`manifest.json` identifies which paths are governed by the template and which are protected project content.

See:

- [`docs/lqmb/LQMB_LIVING_PROJECT_FRAMEWORK.md`](docs/lqmb/LQMB_LIVING_PROJECT_FRAMEWORK.md)
- [`docs/lqmb/TEMPLATE_UPDATE_PROTOCOL.md`](docs/lqmb/TEMPLATE_UPDATE_PROTOCOL.md)
- [`AI_PROVENANCE.md`](AI_PROVENANCE.md)
- [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Version

This template is **v0.2.2**.
