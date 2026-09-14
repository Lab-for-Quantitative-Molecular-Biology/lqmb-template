# LQMB Template Update Protocol

## Purpose

`lqmb-template` is a living upstream project. Downstream LQMB projects do not
silently synchronize to it. Instead, they declare the exact template release
and commit they adopted, detect later upstream releases, and propose updates
through ordinary version-controlled project changes.

## Canonical relationship

A downstream project records:

```json
"template": {
  "repository": "https://github.com/Lab-for-Quantitative-Molecular-Biology/lqmb-template",
  "version": "0.2.0",
  "commit": "<immutable commit>",
  "sync_policy": "prompt"
}
```

The template repository itself is special and records `version: "self"` and
`commit: "self"`.

## First-interaction check

At the first substantive interaction with a project:

1. Read `.lqmb/project.json`, `.lqmb/dependencies.json`, and `.lqmb/manifest.json`.
2. Run:
   ```bash
   python3 .lqmb/bin/template-status.py --check-upstream
   ```
3. If the upstream query succeeds, compare the recorded release to the latest
   released `vX.Y.Z` tag.
4. If upstream cannot be queried, state that explicitly and do not infer that
   the project is current from local metadata alone.
5. If an update is available, inform the human user. Do not modify files automatically.

## Avoiding duplicate update work

Before creating an update branch:

1. Check GitHub for an existing open pull request that updates this project to
   the same target template release.
2. If one exists, do not create a duplicate branch. Review or contribute to
   the existing PR instead.
3. If repository access is unavailable, state that duplicate checking could
   not be performed rather than assuming no update exists.

## Preparing an update

Create:

```text
chore/lqmb-template-vX.Y.Z
```

Then obtain both the project's recorded template snapshot and the target
template snapshot.

The update is a three-way comparison:

- **Base:** the exact template commit recorded by the project.
- **Target:** the new template release.
- **Project:** the files currently present in the living project.

## Path classes

`.lqmb/manifest.json` defines four classes.

### template_managed_paths

These are maintained by the upstream template.

### project_configured_paths

These use the template's structure but contain project-specific values.

They must be preserved and updated deliberately, not overwritten wholesale.

### protected_paths

These are project-owned and must never be overwritten by template updates.

### shared_paths

These require explicit human resolution when both upstream and project have
changed.

## Three-way update rule

For every template-managed file:

- Project == Base and Target != Base → adopt Target.
- Project != Base and Target == Base → preserve Project.
- Project == Base and Target == Base → no change.
- Project != Base and Target != Base → human review is required.

Never copy the entire template repository over a living project.

## After updating

1. Update the project's recorded template version and exact target commit.
2. Run project validation.
3. Review `git diff` and `git status`.
4. Confirm no project data, results, code or protected files were overwritten.
5. Record the update in the changelog or project decisions.
6. Open a pull request.
7. Human review is required before merge.

The update is therefore itself a living, version-controlled project contribution.
