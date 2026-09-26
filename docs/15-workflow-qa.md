# Workflow QA

Reviewed: 2026-09-26

This review treats the repository as one bounded workflow from customer evidence to a demand hypothesis and then to a product Explore handoff.

## Input and preprocessing

Raw transcripts and research archives are outside the live corpus. The accepted input is a preprocessed EV artifact with provenance, collection context, timing, observed behavior, resource movement, options, transaction evidence, counterevidence, unknowns, and privacy state.

A packet that is too raw returns `NEEDS_PREPROCESSING`.

A valid evidence packet does not have to become an anecdote. If there is not enough evidence for an actor + product-neutral Project + active time window, return `ANECDOTE_NOT_READY`.

## Duplicate, conflict, and concurrency behavior

Stable IDs, actor/episode identity, source fingerprints, typed relations, and dependent-case groups reduce accidental double counting.

Accepted evidence packets are immutable. Mutable analytical artifacts retain a stable ID and must increment revision with a new revision note. Active artifacts cannot simply be deleted; archival preserves history.

When upstream evidence changes, downstream interpretations use `current`, `needs_review`, or `stale`. Validation rejects downstream objects that claim to be current while relying on unreconciled upstream objects.

For a shared repository, use branches and pull requests. The change-set guard checks the base and head revisions rather than assuming one writer has complete state.

## Promotion boundaries

A PULL pattern begins as `candidate`.

A pattern cannot validate as `supported` without linked falsification work and at least one resolved falsification item.

A candidate or active demand hypothesis can derive only from a supported PULL pattern. Transaction path, acceptance boundary, observable next commitment, falsification conditions, and a canonical statement are required.

This prevents the repository from behaving like an automatic evidence-to-hypothesis generator.

## Explore boundary

Explore handoffs are compact Markdown outputs, not another research store. They are limited to 2,500 words and must reference an existing usable demand hypothesis. Stale, superseded, or rejected demand hypotheses cannot be handed downstream as current Explore context.

The handoff carries demand evidence and uncertainty. Product requirements, architecture, and implementation stay downstream.

## Working-set boundary

The active sidecar is limited to 100 evidence packets and roughly 80,000 words of curated evidence. Individual EV packets are limited to roughly 800 words and 12 excerpts.

When the boundary is exceeded, partition or archive. Do not expand the sidecar into an organizational knowledge base.

## Defined stop states

The operator workflow defines these bounded outputs:

- `NEEDS_PREPROCESSING`
- `DUPLICATE_SOURCE`
- `AMBIGUOUS_EPISODE`
- `ANECDOTE_NOT_READY`
- `CONFLICT_REQUIRES_REVIEW`
- `PATTERN_NOT_READY`
- `HYPOTHESIS_NOT_READY`
- `FRAMEWORK_CHANGE_REQUIRED`

An agent should return the relevant state rather than invent information to continue.

## Mechanical QA coverage

CI currently exercises:

- Python compilation of enforcement scripts;
- every canonical JSON template against its schema;
- a complete synthetic EV → PA → PP → FQ → DH flow;
- a negative test preventing a DH from preceding a supported pattern;
- accepted-evidence immutability;
- framework-change protection;
- whole-corpus validation;
- generated-index freshness.

## External repository setting still required

Repository files cannot make a GitHub status check mandatory by themselves.

For shared use, the default branch should be configured to require pull requests, the `corpus-guard / validate` check, and CODEOWNERS review for protected framework paths, while disallowing history-rewriting updates to the protected branch.

Without that repository-level rule, CI can report an invalid direct push after it occurs but cannot stop a writer with direct-push permission from landing it.

## Deliberate non-mechanical judgments

The system does not claim to prove whether customer statements are true, whether two actors are genuinely comparable, whether selection bias is eliminated, or whether a market is sufficiently large.

Those remain analytical judgments. The system's job is to preserve provenance, expose uncertainty, and prevent unsupported transitions from silently becoming facts.
