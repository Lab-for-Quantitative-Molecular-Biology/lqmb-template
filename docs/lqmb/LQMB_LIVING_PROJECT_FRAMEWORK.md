# LQMB Living Project Framework

## Why this exists

LQMB research repositories are living scientific projects. A repository is a persistent research object that can continue across papers, datasets, methods, contributors, funding periods and follow-up questions.

The LQMB template is therefore not a one-time scaffold. It is a versioned upstream project that defines part of the common LQMB research environment.

## 1. `lqmb-template` is itself a living project

`lqmb-template` follows the same LQMB principles as any other project. Members may propose improvements through ordinary branches and pull requests.

A template change becomes part of the canonical framework only after review and merge.

## 2. Every project records its template dependency

Every LQMB project contains `.lqmb/project.json`. It records:

- the canonical template repository;
- the template release version adopted by the project;
- the exact template commit when known;
- the project's policy for proposed template updates.

The release version is human-readable. The commit provides exact provenance.

## 3. Template updates are proposed, never silently imposed

A project does not automatically change because the upstream template changes.

When Claude or a project member first interacts substantively with the project, the recorded template version should be compared with the current canonical template.

If a newer template is available, the human should be told and asked whether to prepare an update.

No update should be applied merely because it exists.

## 4. Managed and protected paths

`.lqmb/manifest.json` defines what the template controls.

### Template-managed paths

These encode the common LQMB framework and can be updated from a newer template release.

### Project-protected paths

These contain project-specific research and must never be overwritten automatically by a template update.

### Shared paths

Shared paths require an explicit merge strategy. v0.2 defines none; this category exists to make future extensions explicit rather than accidental.

## 5. Safe update is a three-way operation

A template update compares:

1. the template version originally adopted by the project;
2. the current canonical template;
3. the project's current file.

For each managed file:

- if only the upstream template changed, the project can adopt the new file;
- if only the project changed, preserve the project version;
- if both changed, prepare a conflict for human resolution;
- protected files are never replaced by this process.

This prevents template updates from overwriting project code, data, results or manuscript work.

## 6. Dependencies and living citations

Projects declare other projects, software, datasets, methods or publications in `.lqmb/dependencies.json`.

Where a dependency supports an immutable identifier, record one: release, version, Git commit, DOI or equivalent.

A newer upstream version does not rewrite historical provenance. It creates an update opportunity that can be evaluated by humans.

## 7. Duplicate-update avoidance

Before creating a template-update branch, check whether another contributor already has an open pull request updating the project to the same template release.

If one exists, work with the existing pull request instead of creating a duplicate.

## 8. Version-controlled evolution

A project adopts a new template release through an ordinary branch and pull request. The resulting merge is therefore part of the project's history.

This means that a project's evolution remains reproducible: the repository records when the template changed and what project files were updated.

## 9. Extension beyond LQMB

The dependency model is intentionally not limited to LQMB repositories. It can eventually describe external software, methods, data resources and research projects.

This creates the possibility of a living research dependency graph: a versioned record of what a project depends on and what it may consider updating.

## 10. Framework at a glance

```text
lqmb-template (living upstream project)
        │
        ├── release v0.2.0
        │
        ├── release v0.3.0
        │
        └── future releases
                 │
                 ▼
        LQMB living project
                 │
        .lqmb/project.json
        .lqmb/dependencies.json
        .lqmb/manifest.json
                 │
        first substantive interaction
                 │
        check upstream versions
                 │
        ┌────────┴────────┐
        │                 │
     current           update available
                          │
                     human decides
                          │
                    update branch
                          │
                 three-way comparison
                          │
                    tests + review
                          │
                        PR
                          │
                       merge
```

## What this framework is not

It is not an automatic synchronisation service and it is not permission for Claude to rewrite living projects whenever a template changes.

The purpose is to make relationships explicit, changes discoverable, updates reversible and scientific provenance durable.
