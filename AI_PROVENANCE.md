# LQMB AI Provenance

LQMB distinguishes human scientific authorship from AI assistance.

## Required commit provenance

For material Claude contribution, use actual Git commit trailers:

```text
AI-Assisted: Claude
AI-Role: Generated
```

or:

```text
AI-Assisted: Claude
AI-Role: Modified
```

or:

```text
AI-Assisted: Claude
AI-Role: Assisted
```

For work without material AI assistance:

```text
AI-Assisted: None
```

After a human has actually reviewed the change, add:

```text
Human-Reviewer: <name>
```

A `Human-Reviewer` trailer must never be added merely because Claude expects a human to review later.

## Pull requests

Pull requests should state:

- whether Claude materially contributed;
- what Claude contributed;
- what the human contributor reviewed;
- what tests or validation were performed.

The PR record supplements, but does not replace, commit-level provenance.

## Authorship

AI assistance is not scientific authorship. Human contributors remain responsible for the scientific content they approve.

## Conventional AI attribution

Claude Code or Git tooling may also add:

```text
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
```

This is supplementary to the LQMB provenance fields.

## Line-level attribution

LQMB does not attempt to permanently classify individual lines of source code as AI-written or human-written. The durable provenance record is maintained at the commit and pull-request level, together with human review.
