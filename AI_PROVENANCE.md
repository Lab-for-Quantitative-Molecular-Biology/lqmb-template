# AI provenance and authorship

LQMB projects distinguish **AI assistance** from **human authorship and scientific responsibility**.

Claude and other AI systems may assist with code, analysis, tests, documentation, literature organisation, or other project work. Human contributors remain responsible for understanding, reviewing, testing, and approving material incorporated into the repository.

## Commit provenance

When an AI system materially contributes to a commit, record this using Git trailers at the end of the commit message.

For Claude-generated code:

```text
AI-Assisted: Claude
AI-Role: Generated
Human-Reviewer: <name>
```

For Claude modifying human-written code:

```text
AI-Assisted: Claude
AI-Role: Modified
Human-Reviewer: <name>
```

For Claude providing substantial assistance without generating the final implementation:

```text
AI-Assisted: Claude
AI-Role: Assisted
Human-Reviewer: <name>
```

For work without material AI assistance:

```text
AI-Assisted: None
```

The `Human-Reviewer` identifies the person who reviewed and accepted the material for incorporation. The reviewer may be the contributor when appropriate.

## Pull requests

Pull requests should disclose whether AI materially contributed and briefly describe the contribution. Use the repository pull-request template.

## What this does not mean

AI provenance is not authorship. It does not make an AI system a scientific author or contributor of record unless a publisher, funder, institution, or other governing body explicitly requires a different disclosure.

Scientific authorship and contributorship are determined by human contribution and the applicable project, institutional, journal, and funder policies.

## Line-level attribution

LQMB does not attempt to label individual source-code lines as human-written or AI-written. Final code is often jointly developed, edited, refactored, and reviewed, making durable line-level attribution unreliable.

The authoritative provenance record is therefore the combination of:

1. Git commit metadata and trailers;
2. pull-request disclosure and review;
3. the project's contributor record; and
4. applicable publication or release disclosures.
