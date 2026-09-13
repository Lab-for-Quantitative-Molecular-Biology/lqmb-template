# LQMB Living Research Project

**Laboratory for Quantitative Molecular Biology (LQMB)**  
*Mathematical and computational approaches to molecular biology*

This repository is a **living research project**. It is intended to remain useful before, during, and after individual analyses, papers, software releases, datasets, or changes in project membership.

The project—not the paper—is the persistent scientific object. Papers and other outputs are products of the project.

## Start here

1. Read [`CLAUDE.md`](CLAUDE.md) for the LQMB working conventions and Claude Code instructions.
2. Read [`AI_PROVENANCE.md`](AI_PROVENANCE.md) for the LQMB approach to AI-assisted work.
3. Read [`docs/research-question.md`](docs/research-question.md) to understand the scientific purpose of the project.
4. Read [`docs/analysis-plan.md`](docs/analysis-plan.md) for the current planned analysis.
5. Check [`docs/research-log.md`](docs/research-log.md) and [`docs/decisions.md`](docs/decisions.md) for recent history and consequential decisions.
6. Read [`docs/contributions.md`](docs/contributions.md) to see how people are contributing.
7. Read [`data/README.md`](data/README.md) before introducing or linking research data.

## Repository structure

```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── configs/
├── data/
├── docs/
├── examples/
├── manuscript/
├── notebooks/
├── outputs/
├── scripts/
├── src/
├── tests/
├── workflows/
├── AI_PROVENANCE.md
├── CLAUDE.md
└── README.md
```

Not every project will use every directory. Add or remove components according to the scientific problem.

## Data

Research data are **not stored in this repository by default**. The `data/` directory is ignored by `.gitignore`, and CI checks that unexpected files have not been committed there.

Use [`data/README.md`](data/README.md) to document where approved project data are stored. Small, non-sensitive example datasets should normally live under `examples/`.

Before every commit, inspect `git status` and `git diff --stat` and verify that no research data, generated outputs, secrets, or other sensitive files are included.

## Reproducibility

Important analyses should be executable from documented code and configuration. Project-specific instructions for environments, commands, and validation belong in `CLAUDE.md` and `docs/`.

## Collaboration

LQMB is contribution-oriented. Ideas, analyses, code, methods, documentation, critique, and scientific interpretation are contributions regardless of seniority. Changes to the shared project should normally be made on branches and incorporated through pull requests.

See [`docs/contributions.md`](docs/contributions.md).

## AI-assisted work

AI assistance is recorded separately from human authorship. See [`AI_PROVENANCE.md`](AI_PROVENANCE.md) and the pull-request template for the project's provenance conventions.

## Living-project lifecycle

Existing paper-centred work can be migrated gradually:

```text
paper-centred project
        ↓
repository
        ↓
reproducible repository
        ↓
living research project
        ↓
multiple outputs / follow-up research
```

The repository should remain useful even when a particular paper is finished.

## Licence

The template is distributed under the MIT License. This is a licence for the template/code in this repository; individual research projects should choose appropriate licences for code, documentation, data, and manuscripts according to institutional and funder requirements.
