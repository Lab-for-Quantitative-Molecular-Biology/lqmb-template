# LQMB Claude Code instructions

## Project identity

This repository belongs to the **Laboratory for Quantitative Molecular Biology (LQMB)**.

LQMB develops mathematical and computational approaches to molecular biology, including genomics and other quantitative molecular methods.

## Core principles

### Living research

Treat the repository as a persistent scientific object rather than a temporary container for a paper.

A paper, preprint, software release, dataset, or figure set is an output of the project. Do not reorganise the project around a manuscript unless there is a clear scientific reason to do so.

Projects may continue after publication, generate multiple outputs, incorporate new data or methods, and be extended by new contributors.

### Contribution over hierarchy

Evaluate proposed changes on scientific reasoning, evidence, reproducibility, usefulness, and fit with the project—not on the seniority of the contributor.

Do not assume that the PI or most senior researcher owns the scientific idea or implementation. Encourage explicit discussion and review of consequential changes.

Scientific responsibility, institutional accountability, supervision, ethics, data governance, and other formal responsibilities remain explicit even when collaboration is contribution-based.

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
3. Read `.lqmb/project.json`, `.lqmb/dependencies.json`, and `.lqmb/manifest.json` when present.
4. On the first substantive interaction with a project, check whether the recorded LQMB template version/commit and declared dependencies are current enough to warrant informing the human user about available updates. Do not modify anything merely because an update exists.
5. Inspect the repository structure and the existing implementation.
6. For substantial tasks, propose a concise implementation plan before editing files.
7. Preserve existing behaviour unless the requested change requires otherwise.

For unfamiliar analyses or code, explain the current implementation before proposing a replacement.

## LQMB template and project framework

The `lqmb-template` repository is a living upstream project, not a one-time scaffold.

Each LQMB project records the exact template release and commit it adopted in `.lqmb/project.json`. The template defines which paths it manages in `.lqmb/manifest.json`.

If a newer template version is available:

- inform the human user;
- do not update automatically;
- check for an existing open template-update pull request before creating a new one;
- if the human requests an update, use the LQMB Template Update Protocol;
- update only template-managed paths;
- never overwrite project-protected paths automatically;
- treat simultaneous changes to a managed file as a human-resolved conflict;
- update the recorded template version and exact commit only as part of the reviewed update.

Never copy the entire template repository over a living project.

## Dependencies and living citations

When `.lqmb/dependencies.json` exists, treat it as the project's durable dependency/citation record.

Dependencies may include LQMB repositories, external software, datasets, protocols, publications, methods, and other research projects.

When a dependency has a newer release or otherwise material upstream change:

- inform the human user;
- do not silently rewrite historical versions or citations;
- propose an update only after human approval;
- preserve exact versions, commits, DOIs, or other immutable identifiers used for reproducibility.

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
- Keep important contribution information in `docs/contributions.md`.

## Data rules

Do not add raw, sensitive, patient-level, confidential, or very large datasets to Git unless the project explicitly requires it and the repository is approved for that data.

The repository `.gitignore` is configured to prevent routine tracking of the `data/` directory and common scientific data formats. Do not weaken or bypass these rules merely to make an analysis convenient.

The `data/` directory is **not the default repository location for raw research data**. It is an ignored local/project workspace that may be used where appropriate for project-linked or locally mounted data. Raw, sensitive, confidential, or large datasets should normally remain in approved institutional, HPC, or project-specific storage and should not be copied into the repository workspace unnecessarily.

Small, non-sensitive example datasets needed for tests or demonstrations should normally live under `examples/`.

Before proposing a commit, inspect `git status` and `git diff --stat` and verify that no research data, generated outputs, credentials, or other sensitive files have been included.

Do not hard-code credentials, API keys, tokens, passwords, or private URLs into code or configuration.

Use documented paths, environment variables, or approved data-storage mechanisms instead.

Never weaken `.gitignore` protections merely to make a workflow convenient without an explicit project-level decision.

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
human review of changes
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
- run the project's documented validation commands;
- verify that only intended files are included.

Claude should normally work on a branch and **should not push a branch or open a pull request unless the user has explicitly asked for that action or clearly authorised that stage of the workflow**.

Do not force-push, rewrite history, delete branches, or merge pull requests unless explicitly instructed.

## Commits and AI provenance

Use concise, informative commit messages that describe the change.

LQMB records material AI assistance using structured Git commit trailers. Follow `AI_PROVENANCE.md` and use, where applicable:

```text
AI-Assisted: Claude
AI-Role: Generated
```

```text
AI-Assisted: Claude
AI-Role: Modified
```

```text
AI-Assisted: Claude
AI-Role: Assisted
```

For work without material AI assistance, use:

```text
AI-Assisted: None
```

Where a human has actually reviewed the material change, add:

```text
Human-Reviewer: <name>
```

Claude must **never claim or record that a human has reviewed, approved, validated, or signed off work unless that review has actually occurred**.

AI provenance does not constitute scientific authorship. Human contributors remain responsible for reviewing and approving material incorporated into the repository.

GitHub or Claude Code may also add conventional attribution such as:

```text
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
```

This is supplementary. The LQMB `AI-Assisted`, `AI-Role`, and, where applicable, `Human-Reviewer` fields remain the authoritative AI-provenance record.

Prefer actual Git trailers rather than merely writing provenance fields into the prose of a commit message.

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

Scientific disagreement and constructive criticism are expected parts of the research process.

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
- never claim to have run an analysis, test, or command that was not actually run;
- stop at an appropriate human review point before making shared changes visible unless explicitly authorised to continue.

Claude should not:

- fabricate scientific evidence;
- silently change analysis definitions;
- delete valuable project history;
- commit secrets;
- assume unpublished data may be shared externally;
- push to protected/shared branches without explicit instruction;
- claim human review that has not occurred;
- bypass repository data protections.

When making changes, prefer the sequence:

```text
inspect
  ↓
understand
  ↓
plan
  ↓
implement
  ↓
test
  ↓
report
  ↓
human review
  ↓
push / pull request when authorised
```

## Definition of done

A substantive change is complete when appropriate:

1. the implementation is correct and understandable;
2. relevant tests or validation have been run;
3. important documentation is updated;
4. consequential scientific decisions are recorded;
5. `git diff` has been reviewed;
6. no secrets, research data, or unintended large files have been added;
7. AI provenance has been recorded where material AI assistance occurred;
8. `Human-Reviewer` has been recorded only after actual human review; and
9. the appropriate branch, pull request, and merge steps have been completed or explicitly handed back to the human contributor.
