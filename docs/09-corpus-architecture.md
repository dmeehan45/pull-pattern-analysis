# Corpus architecture

## Purpose

This repository is a **curated analytical sidecar**, not an organizational knowledge base and not a raw research archive.

Its job is to keep a small, high-signal working set of customer evidence and the derived PULL artifacts that a product or founding team needs during exploration.

The corpus should make it easy for a human or agent to:

- point at a compact evidence base;
- add a new preprocessed customer episode;
- extract or revise a PULL anecdote;
- compare that anecdote with existing patterns;
- detect contradictions, duplicates, or changed assumptions;
- pull current demand context into an exploration conversation;
- identify what evidence should be collected next.

It should **not** become the place where every call recording, transcript, research document, CRM record, or company note is copied.

## Canonical layers

The live analytical corpus has four layers:

```text
external/raw source
      ↓ preprocessing
evidence packet
      ↓ interpretation
PULL anecdote
      ↓ cross-case synthesis
PULL pattern
      ↓ prediction
demand hypothesis
```

A fifth artifact, the **falsification item**, can attach to any candidate pattern or hypothesis.

### Raw source

Lives outside this repository.

Examples:
- full interview transcript;
- call recording;
- CRM thread;
- support history;
- research repository;
- email chain;
- sales notes.

The corpus stores a pointer, not a copy, unless the source is already short, intentionally redacted, and appropriate to commit.

### Evidence packet

The minimum ingestion unit.

An evidence packet is a compact, provenance-rich reduction of one customer episode. It preserves the facts needed for PULL analysis while removing conversational bulk.

### PULL anecdote

An interpretation of one actor + Project + active time window.

It may reference multiple evidence packets from the same episode.

### PULL pattern

A cross-case synthesis across independent anecdotes.

### Demand hypothesis

A predictive claim formed only after a pattern has survived meaningful challenge.

## Working-set budget

Git can store far more data than this framework should.

The limiting resource is **analytical attention and agent context**, not repository capacity.

Use these as operational soft limits, not technical guarantees:

- **Evidence packet:** target <= 800 words.
- **Quoted/excerpted evidence:** target <= 12 short excerpts per packet.
- **One active partition:** target <= 100 evidence packets or roughly <= 80,000 words of curated source material, whichever comes first.
- **Active patterns:** keep the set small enough that a reviewer can understand the current map; if dozens of unrelated patterns accumulate, partition the corpus.
- **Raw transcripts:** zero by default.

When the active partition exceeds these limits, do not keep compressing indefinitely. Split by a meaningful analytical boundary such as:
- product surface;
- customer type;
- market;
- Project family;
- material time period.

Then maintain a smaller cross-partition synthesis only for patterns that genuinely span those boundaries.

## Why a working-set budget matters

A larger corpus does not automatically create better inference.

Past a certain point:
- duplicated episodes look like replication;
- stale evidence remains visible after market conditions change;
- agents spend context reconstructing history instead of testing current claims;
- broad semantic retrieval favors repeated language over discriminating evidence;
- contradictions are easier to miss.

The objective is **high-information evidence density**, not completeness.

## Recommended directory shape

A live deployment may use:

```text
corpus/
  evidence/
  anecdotes/
  patterns/
  hypotheses/
  falsification/
  archive/
  INDEX.md

handoffs/
  explore/

templates/
schemas/
docs/
```

The canonical record should live in individual artifact files.

Avoid a hand-maintained monolithic database file that every agent edits. Central indexes should be treated as generated navigation aids, not the source of truth, because they create unnecessary merge conflicts.

## Active vs archived

Archive an artifact when:
- the time window has expired;
- the market condition that created it has materially changed;
- the Project is no longer relevant to the active exploration area;
- a pattern was rejected but should remain historically traceable;
- a hypothesis was superseded.

Archiving is not deletion.

Historical artifacts are valuable for:
- detecting repeated mistakes;
- understanding why a hypothesis changed;
- identifying old patterns that reappear.

## Public-repository warning

This framework repository is public.

A real customer corpus should therefore be either:
- stored in a private deployment/fork; or
- aggressively redacted and pseudonymized before commit.

Do not commit customer PII, secrets, private transcripts, confidential account details, regulated data, or proprietary internal documents to a public repository.

Use stable pseudonymous actor and organization IDs when identity is not analytically necessary.
