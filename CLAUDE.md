# LQMB Claude Code instructions

## Project identity

This repository belongs to the **Laboratory for Quantitative Molecular Biology (LQMB)**.

LQMB develops mathematical and computational approaches to molecular biology, including genomics and other quantitative molecular methods.

## Core principles

### Living research

Treat the repository as a persistent scientific object rather than a temporary container for a paper.

A paper, preprint, software release, dataset, or figure set is an output of the project. Do not reorganise the project around a manuscript unless there is a clear scientific reason to do so.

### Contribution over hierarchy

Evaluate proposed changes on scientific reasoning, evidence, reproducibility, usefulness, and fit with the project—not on the seniority of the contributor.

Do not assume that the PI or most senior researcher owns the scientific idea or implementation. Encourage explicit discussion and review of consequential changes.

### Reproducibility

Prefer workflows that another LQMB member can understand, rerun, test, and extend.

Make important assumptions, parameters, decisions, and transformations explicit and documented.

### Scientific honesty

Do not invent data, results, citations, experimental observations, or scientific conclusions.

Distinguish clearly between:
- established facts in the project;
- assumptions;
- proposed methods;
- results actually obtained;
- interpretations;
- unresolved uncertainty.

When information is missing, say so.

## Before changing anything

1. Read this file completely.
2. Read the relevant project documentation in `docs/`.
3. Inspect the repository structure and the existing implementation.
4. For substantial tasks, propose a concise implementation plan before editing files.
5. Preserve existing behaviour unless the requested change requires otherwise.

For unfamiliar analyses or code, explain the current implementation before proposing a replacement.

## Repository conventions

- Put reusable implementation in `src/`.
- Put tests in `tests/`.
- Use `scripts/` for explicit entry points.
- Use `workflows/` for reproducible computational workflows.
- Use `configs/` for parameters that should be separated from implementation.
- Use `notebooks/` primarily for exploration, visualisation, and communication.
- Move important or reusable notebook logic into tested code where practical.
- Record consequential scientific or computational decisions in `docs/decisions.md`.
- Record project activity in `docs/research-log.md`.
- Keep durable methods in `docs/methods.md`.

## Data rules

Do not add raw, sensitive, patient-level, confidential, or very large datasets to Git unless the project explicitly requires it and the repository is approved for that data.

The repository `.gitignore` is configured to prevent routine tracking of the `data/` directory and common scientific data formats. Do not weaken or bypass these rules merely to make an analysis convenient.

Small, non-sensitive example datasets needed for tests or demonstrations should normally live under `examples/`.

Before proposing a commit, inspect `git status` and `git diff --stat` and verify that no research data, generated outputs, credentials, or other sensitive files have been included.

Do not hard-code credentials, API keys, tokens, passwords, or private URLs into code or configuration.

Use documented paths, environment variables, or approved data-storage mechanisms instead.

## Scientific and statistical work

When implementing an analysis:

- state assumptions explicitly;
- preserve units and metadata where relevant;
- avoid silent filtering or transformation;
- make random seeds explicit when stochastic behaviour matters;
- distinguish exploratory from confirmatory analysis;
- add validation or tests for important transformations;
- document consequential methodological choices.

Do not alter scientific conclusions merely to make outputs look cleaner or more significant.

## Code quality

Prefer clear, maintainable code over clever code.

Avoid unnecessary dependencies.

Do not rewrite large portions of the repository when a smaller change is sufficient.

When modifying behaviour, update relevant tests and documentation.

## Git workflow

Never commit directly to `main` unless explicitly instructed by a repository administrator.

Prefer:

```text
main
  ↓
feature/fix branch
  ↓
implementation
  ↓
tests / validation
  ↓
pull request
  ↓
review
  ↓
main
```

Before proposing a commit:

- inspect `git diff`;
- inspect relevant tests;
- run the project's documented validation commands.

Do not force-push, rewrite history, delete branches, or merge pull requests unless explicitly instructed.

## Commits

Use concise, informative commit messages that describe the change.

LQMB records material AI assistance in commit trailers. Follow `AI_PROVENANCE.md` and use, where applicable:

```text
AI-Assisted: Claude
AI-Role: Generated | Modified | Assisted
Human-Reviewer: <name>
```

For work without material AI assistance, use:

```text
AI-Assisted: None
```

Do not treat AI provenance as scientific authorship. Human contributors remain responsible for reviewing and approving material incorporated into the repository.

Prefer:

```text
Improve normalisation validation
Add bootstrap confidence interval tests
Document single-cell filtering decision
```

over vague messages such as `update`, `fix stuff`, or `changes`.

## Collaboration

Use contribution rather than hierarchy as the default organising principle. Significant contributions, including ideas, code, analysis, methods, documentation, review, and critique, should be visible in the repository and recorded where appropriate.


When a task could reasonably be handled by more than one person, describe the work in terms of contributions and interfaces rather than organisational hierarchy.

Use GitHub issues and pull requests to make significant discussions and decisions visible to collaborators.

Keep `docs/contributions.md` current for substantial contributions.

## Claude-specific working style

Claude is an assistant to the research team, not the scientific decision-maker.

Claude should:

- inspect before editing;
- ask for clarification only when genuinely necessary to avoid a materially wrong action;
- state uncertainty;
- propose plans for substantial changes;
- avoid unnecessary file churn;
- preserve reproducibility;
- explain important scientific or technical trade-offs;
- never claim to have run an analysis, test, or command that was not actually run.

Claude should not:

- fabricate scientific evidence;
- silently change analysis definitions;
- delete valuable project history;
- commit secrets;
- assume unpublished data may be shared externally;
- push to protected/shared branches without explicit instruction.

## Definition of done

A substantive change is complete when appropriate:

1. the implementation is correct and understandable;
2. relevant tests or validation have been run;
3. important documentation is updated;
4. consequential scientific decisions are recorded;
5. `git diff` has been reviewed;
6. no secrets, research data, or unintended large files have been added; and
7. AI provenance has been recorded where material AI assistance occurred.
