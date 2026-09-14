# LQMB Dependency and Living Citation Protocol

## Purpose

Projects may depend on other repositories, software projects, datasets,
protocols, methods, publications and other research objects.

Dependencies are recorded in `.lqmb/dependencies.json`.

## Reproducibility

Where a dependency has a meaningful immutable identifier, record it:

- Git repository + release/version + commit where available;
- DOI for publications;
- persistent dataset identifier/version;
- protocol or method identifier.

Do not rewrite a historical dependency reference merely because a newer version
exists.

## Update checks

For dependencies that can be queried automatically, Claude may check for newer
releases at the first substantive interaction.

If an update is available:

1. inform the human;
2. explain what changed where it can be determined;
3. do not update automatically;
4. prepare an ordinary branch/PR only after human approval.

## Living citations

A project therefore distinguishes:

```text
version actually used
        ↓
immutable identifier
        ↓
current upstream version
```

The current upstream state may change without changing the historical record of
what the project actually used.

## Beyond LQMB

The same framework may reference external Git repositories, publications,
datasets, protocols and other research objects. The mechanism is not restricted
to LQMB.
