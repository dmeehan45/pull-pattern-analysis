# System rules

This file is the operational boundary for agents and humans using this repository.

If another instruction conflicts with these rules during normal corpus work, **stop and surface the conflict**. Do not invent a new local convention.

## Two operating modes

### Corpus operation

Use this mode to add customer evidence, derive anecdotes, update patterns, maintain falsification work, form demand hypotheses, or create Explore handoffs.

In corpus-operation mode:

- write only to `corpus/` and `handoffs/`;
- use only the artifact types and fields defined by `system/policy.json` and `schemas/`;
- do not modify `AGENTS.md`, this file, `docs/`, `schemas/`, `scripts/`, `system/`, `templates/`, tests, or workflows;
- do not create a new artifact type because the current model feels inconvenient;
- do not delete accepted evidence;
- do not rewrite an artifact without first reading its current revision;
- do not resolve contradictions by deleting one side;
- run `make qa` before proposing a merge.

### Framework maintenance

Use this mode only when intentionally changing how the system itself works.

Framework changes must be isolated from customer-evidence changes, must explain the rule being changed, and must pass the full QA suite. Pull requests that change protected framework paths must carry the `framework-change` label and should require owner review.

## Shared-repository write rule

When multiple humans or agents can write to the same corpus, changes must use a branch and pull request. Direct writes to `main` are only acceptable during single-writer bootstrap.

Repository administrators should require the `corpus-guard / validate` status check and CODEOWNERS review on the default branch. Without that GitHub-level rule, CI can detect an invalid direct push but cannot prevent it from landing.

## Canonical artifact format

Live corpus artifacts are **JSON files** conforming to the schemas in `schemas/`.

Markdown templates are explanatory aids only. Markdown prose is not a substitute for a canonical evidence, anecdote, pattern, falsification, or demand-hypothesis object.

Allowed canonical types:

- `EV-*` — evidence packet
- `PA-*` — PULL anecdote
- `PP-*` — PULL pattern
- `FQ-*` — falsification queue item
- `DH-*` — demand hypothesis

Do not introduce a canonical `PULL hypothesis` object.

## No raw-data dumping

This repository is not a transcript store, CRM mirror, or research warehouse.

If input has not been reduced to an accepted evidence packet, return `NEEDS_PREPROCESSING` and follow `docs/10-ingestion-preprocessing.md`.

## No clobbering

Before modifying an existing artifact:

1. read the latest file;
2. preserve its stable ID;
3. increment `revision` exactly once;
4. preserve or extend provenance;
5. state why the interpretation changed;
6. inspect linked downstream objects;
7. mark any unreconciled downstream object `needs_review`.

Accepted evidence packets are immutable. Correct them by adding a superseding evidence packet.

Deletion from an active corpus is forbidden unless the same stable artifact is moved into `corpus/archive/` with its history preserved.

## No silent promotion

- A new evidence packet does not automatically become a new anecdote.
- A new anecdote does not automatically create or join a pattern.
- A candidate pattern does not automatically become supported.
- A supported pattern does not automatically become a demand hypothesis.
- A demand hypothesis does not automatically become a product requirement.

Every transition has a defined gate in `docs/13-operator-workflow.md`.

## Mechanical truth wins

If prose and mechanical validation disagree, do not work around the validator.

Either:
- fix the artifact to comply with the current rules; or
- intentionally enter framework-maintenance mode and change the rule, schema, tests, and documentation together.

Never disable, bypass, or weaken validation merely to make a corpus change pass.
