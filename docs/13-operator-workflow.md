# Operator workflow

This is the shortest safe path through the system.

The workflow is deliberately bounded. An agent should never need to invent a new state transition in order to complete ordinary customer-learning work.

## 0. Determine operating mode

If the task is about customer evidence, anecdotes, patterns, falsification, demand hypotheses, or an Explore handoff, use **corpus-operation mode**.

If the task changes schemas, definitions, validators, system policy, artifact types, or agent rules, use **framework-maintenance mode**.

Do not mix the two in one change set.

## 1. Evidence enters

### Input accepted

A preprocessed evidence packet that meets `docs/10-ingestion-preprocessing.md`.

### If input is raw

Return:

`NEEDS_PREPROCESSING`

Do not store the raw material in the live corpus.

### Write

Create:

`corpus/evidence/EV-<date>-<suffix>.json`

using the evidence schema.

### Reconcile before writing

Check:
- same source fingerprint;
- same actor;
- same episode;
- possible correction/supersession;
- privacy/storage appropriateness.

### Output

One accepted EV artifact, or a duplicate/supersession/preprocessing decision.

## 2. Evidence becomes or updates a PULL anecdote

Ask whether the evidence belongs to an existing:

**actor + Project + active time window**

If yes, revise that PA rather than creating another one.

If no, create:

`corpus/anecdotes/PA-<date>-<suffix>.json`

A new PA begins at revision 1.

### Conflict handling

New evidence may support, contradict, or qualify the anecdote.

Do not remove the prior evidence reference.

If the interpretation changes:
- increment revision;
- add the new evidence;
- update counterevidence/unknowns;
- mark impacted downstream patterns `needs_review`.

## 3. Anecdotes become candidate PULL patterns

Do not pattern-match on language alone.

Compare independent episodes and negative cases.

Create a PP only when there is a concrete recurring structure worth testing.

New pattern state:

`candidate`

Immediately create one or more FQ items for the highest-risk uncertainty or rival explanation.

A pattern cannot become `supported` mechanically unless it has at least one resolved falsification item.

## 4. Challenge the pattern

Collect the evidence requested by the falsification queue.

Possible outcomes:

- remains `candidate`;
- becomes `challenged`;
- narrows;
- `split` into multiple patterns;
- becomes `supported`;
- becomes `rejected`;
- becomes `stale`.

A falsification result is itself new evidence when it comes from a customer or market episode. Ingest it through the same EV path before revising the pattern.

## 5. Pattern becomes a demand hypothesis

A demand hypothesis may be created when:

- its source PP is `supported`;
- transaction path is explicit enough to test;
- acceptance boundary is stated;
- predicted next commitment is observable;
- falsification conditions are stated;
- evidence gaps are visible rather than hidden.

Create:

`corpus/hypotheses/DH-<date>-<suffix>.json`

Start as `candidate` unless the team is actively testing the prediction.

Use `active` only when the hypothesis is the current prediction under test.

## 6. Reconcile test results

A sale, stall, refusal, procurement step, pilot, implementation event, or failed next commitment becomes new evidence.

Ingest the event as EV, update the relevant PA, and propagate review state upward.

Do not update only the hypothesis. The evidence chain should explain why it changed.

## 7. Hand off to product Explore

When the team is ready to explore supply against a demand hypothesis, create:

`handoffs/explore/<date>-<slug>.md`

using the Explore handoff template.

The handoff should point to the DH, PP, strongest evidence, strongest counterexample, transaction path, acceptance boundary, and unresolved uncertainties.

Do not create product requirements in this corpus.

## 8. Validate

After any corpus operation:

```bash
make index
make qa
```

No corpus change is complete while validation fails or the generated index is stale.

## Standard stop states

An agent should stop instead of improvising when it reaches:

- `NEEDS_PREPROCESSING` — input is too raw.
- `DUPLICATE_SOURCE` — evidence appears already represented.
- `AMBIGUOUS_EPISODE` — cannot determine whether evidence belongs to an existing episode.
- `CONFLICT_REQUIRES_REVIEW` — evidence materially contradicts an active interpretation and cannot be reconciled safely.
- `PATTERN_NOT_READY` — recurrence is plausible but has not survived challenge.
- `HYPOTHESIS_NOT_READY` — pattern or transaction evidence is insufficient.
- `FRAMEWORK_CHANGE_REQUIRED` — ordinary corpus work cannot express the needed concept without changing system rules.

These are successful bounded outputs, not agent failures.
