# Multi-agent corpus maintenance

## Assumption

Multiple humans and agents may read and update the corpus concurrently.

No single agent should be assumed to have complete historical context.

The repository therefore needs rules that make local edits safe and make changed assumptions discoverable.

## Core principle

**Source evidence is durable; interpretations are revisable.**

That leads to different mutation rules for different artifacts.

## Artifact mutability

### Evidence packets

Accepted evidence packets are effectively immutable.

If a factual correction is required:
- create a new revision;
- reference the prior packet with `supersedes`;
- explain the correction.

Do not silently rewrite historical evidence.

### PULL anecdotes

Anecdotes may be revised as new evidence from the same episode arrives.

Every revision must:
- preserve the anecdote ID;
- increment revision metadata;
- list newly added evidence packet IDs;
- record what interpretation changed and why.

If the new evidence actually represents a different Project or time window, create a new anecdote rather than stretching the old one.

### PULL patterns

Patterns are mutable synthesis objects.

New evidence may:
- support;
- challenge;
- split;
- narrow;
- reject;
- stale;
- supersede

a pattern.

Never delete the old reasoning. Use status and revision history.

### Demand hypotheses

Demand hypotheses are versioned predictions.

A materially changed actor state, forcing condition, acceptance boundary, transaction path, or predicted commitment should create a new revision or superseding hypothesis rather than being silently edited into a different claim.

## Stable IDs

Use stable IDs that do not expose customer names.

Recommended prefixes:
- `EV-` evidence packet;
- `PA-` PULL anecdote;
- `PP-` PULL pattern;
- `DH-` demand hypothesis;
- `FQ-` falsification item.

IDs should remain stable across revisions.

Human-readable titles can change.

## Required relations

Artifacts should be able to reference typed relations such as:

- `derived_from`
- `supports`
- `contradicts`
- `qualifies`
- `duplicates`
- `same_episode`
- `supersedes`
- `split_from`
- `tests`

Do not force contradictory evidence into a single reconciled statement before the conflict is understood.

## Before-write reconciliation pass

Before creating or changing an artifact, an agent must check for:

### Duplicate source
Does the same external source reference or source fingerprint already exist?

### Duplicate episode
Does another packet describe the same actor, Project, and buying event?

### Existing anecdote
Would the new evidence update an existing actor + Project + time-window anecdote rather than create another one?

### Pattern impact
Does the evidence support, contradict, qualify, or split an existing pattern?

### Hypothesis impact
Does the evidence change:
- the actor state;
- forcing condition;
- transaction path;
- acceptance boundary;
- predicted next commitment;
- falsification status

of an active demand hypothesis?

### Temporal conflict
Is the apparent contradiction actually evidence from different market conditions or time windows?

## Impact propagation

When new evidence changes an upstream object, downstream artifacts must not remain silently "current."

Use an impact state:

- **current** — reviewed against all linked accepted evidence;
- **needs_review** — linked evidence changed or conflicting evidence arrived;
- **stale** — known to depend on conditions that may no longer hold.

Example:

```text
new EV contradicts PA-12
        ↓
PA-12 revised
        ↓
PP-03 marked needs_review
        ↓
DH-02 marked needs_review
```

An agent does not have to resolve the entire chain in one edit.

It does have to mark the affected downstream objects.

## Write protocol for concurrent agents

For multi-agent/team use, prefer:

1. pull/read the latest main branch;
2. perform the reconciliation pass;
3. make one coherent change set;
4. validate schemas and references;
5. commit on a branch;
6. merge through a pull request or equivalent review boundary.

A direct-to-main workflow is reasonable for a single operator, but becomes fragile when multiple agents write concurrently.

Keep change sets narrow:
- ingest one batch;
- revise one pattern family;
- resolve one falsification queue;
- produce one exploration handoff.

This makes Git history usable as the audit trail.

## Avoid a central write bottleneck

Do not require every agent to update one giant hand-maintained index file.

Canonical state lives in individual artifacts.

Navigation indexes should be generated or cheaply rebuilt from artifact metadata.

That reduces merge conflicts and prevents an outdated index from becoming false authority.

## Reconciliation after merge conflicts

A Git merge conflict is only the mechanical layer.

After resolving it, the agent must ask whether the concurrent changes introduced an **analytical conflict**.

Examples:
- two agents created separate anecdotes from the same episode;
- one pattern was promoted while another agent added a counterexample;
- two hypotheses use different definitions of the same actor segment;
- a new source invalidates an acceptance boundary.

Resolve the analytical conflict explicitly even if Git can merge the files automatically.

## Periodic hygiene pass

At reasonable intervals, run a corpus hygiene pass that checks:
- duplicate evidence packets;
- duplicated anecdotes;
- orphan references;
- stale patterns;
- unresolved contradictions;
- hypotheses whose deadlines expired;
- patterns supported only by dependent cases;
- falsification items that were answered but never reconciled;
- artifacts no longer relevant to the active exploration area.

Hygiene should make the active corpus smaller and clearer, not merely produce another report.
