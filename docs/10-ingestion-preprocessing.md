# Ingestion and preprocessing

## The preprocessing boundary

The analysis agent in this repository is **not responsible for converting arbitrary raw research into usable evidence**.

Before source material enters the corpus, another human or agent should reduce it into an **evidence packet**.

This is an intentional boundary.

Do not drop ten hours of unlabeled transcript data into the repository and ask the analysis layer to discover the market from scratch.

That creates three problems:
1. the corpus becomes a data lake rather than an analytical sidecar;
2. repeated conversational language overwhelms high-value behavior;
3. the same agent both selects evidence and interprets it, increasing confirmation and summarization bias.

## Minimum preprocessing standard

Every evidence packet must contain enough information for another agent to evaluate the episode without reopening the full source.

### 1. Provenance

Include:
- evidence packet ID;
- external source reference;
- source date;
- source type/channel;
- actor ID;
- organization ID where relevant;
- episode ID;
- who/what performed preprocessing;
- collection context;
- whether the source was selected because it appeared promising.

### 2. Factual episode summary

In <= 200 words, describe:
- what was happening;
- what the actor was trying to accomplish;
- what changed;
- what action occurred.

Do not turn this into a market interpretation.

### 3. High-signal evidence excerpts

Select only the excerpts necessary to preserve:
- the actor's stated Project;
- forcing condition or timing;
- actual actions already taken;
- current options;
- option limitations;
- buying/approval mechanics;
- counterevidence.

Prefer a small number of context-preserving excerpts over a long transcript dump.

### 4. Observed actions

List concrete behavior separately from statements.

Examples:
- evaluated three vendors;
- assigned two engineers;
- requested security review;
- delayed the project;
- renewed the incumbent;
- introduced procurement;
- stopped responding.

### 5. Time information

Capture:
- observation date;
- deadline or event;
- when the Project became active;
- what happens if the deadline passes;
- whether the forcing condition has already expired.

### 6. Resource movement

Capture any evidence of:
- money;
- staff time;
- contractor effort;
- leadership attention;
- implementation work;
- procurement effort;
- political capital;
- switching cost.

Record "none observed" rather than leaving the field blank when that is meaningful.

### 7. Option set

Capture options actually:
- used;
- evaluated;
- rejected;
- delayed;
- substituted.

Include doing nothing where it is a real option.

### 8. Transaction evidence

Capture:
- budget or resource source if known;
- approver/economic buyer;
- procurement/security steps;
- purchase vehicle;
- implementation requirements;
- reasons a transaction stalled.

Do not infer these fields merely because a buyer seems senior.

### 9. Counterevidence and ambiguity

The preprocessor must preserve evidence that makes the episode less convenient.

Examples:
- actor says the problem is important but takes no action;
- stated deadline moves repeatedly;
- incumbent is "good enough";
- budget exists but is reserved for another use;
- user loves the idea but buyer does not care;
- the actor bought, but for a different reason.

### 10. Unknowns

Explicitly list missing information.

Unknowns are inputs to the falsification queue.

## What preprocessing should not do

The preprocessing step should **not**:
- decide that a PULL pattern exists;
- assign an anecdote to an existing pattern because the language sounds similar;
- fill unknown transaction mechanics with assumptions;
- delete negative evidence because it seems irrelevant;
- rewrite the customer's Project in terms of the proposed solution;
- turn ten weak quotes into one strong claim;
- produce a demand hypothesis.

Its job is reduction and normalization, not synthesis.

## Splitting long sources

A long interview or transcript may produce more than one evidence packet only when it contains genuinely different analytical episodes.

Split when there is a different:
- actor;
- Project;
- forcing window;
- organizational buying event.

Do not split merely to increase the number of cases.

All packets derived from one source should preserve the same source and episode relationships so downstream agents do not count them as independent evidence.

## Evidence packet acceptance gate

Reject or return an evidence packet for preprocessing when:
- source provenance is missing;
- actor/episode identity is too ambiguous to reason about;
- it is mostly raw transcript;
- it contains large amounts of irrelevant context;
- observed behavior and reported statements are not distinguishable;
- the packet omits obvious counterevidence present in the source;
- confidential information is included without an appropriate storage context.

A rejected packet is not lost research. It simply is not ready for this analytical corpus.
