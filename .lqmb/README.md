# LQMB project metadata

The `.lqmb/` directory records how a living project relates to the LQMB
template and to other declared dependencies.

## Files

- `project.json` — project identity and the exact LQMB template release/commit adopted.
- `dependencies.json` — declared software, project, dataset, protocol and publication dependencies.
- `manifest.json` — paths governed by the template, paths configured by the project,
  and paths protected from template updates.
- `bin/` — read-only local inspection tools used by the LQMB workflow.

## Template projects

The `lqmb-template` repository itself is the canonical upstream template. Because it
cannot meaningfully pin itself to its own future release, its `project.json` uses:

```json
"version": "self",
"commit": "self",
"sync_policy": "self"
```

Downstream projects record an immutable release version and commit.

See:

- `docs/lqmb/LQMB_LIVING_PROJECT_FRAMEWORK.md`
- `docs/lqmb/TEMPLATE_UPDATE_PROTOCOL.md`
- `docs/lqmb/DEPENDENCY_UPDATE_PROTOCOL.md`
