# End-to-end analysis protocol

## 1. Ingest without collapsing

Treat each raw source as a source unit.

Capture:
- source ID;
- actor;
- organization;
- date;
- channel;
- collection method;
- relationship to seller/product;
- whether it was selected because it appeared positive.

Do not summarize the whole corpus first. Early summarization can erase negative cases and over-weight repeated language.

## 2. Resolve actors and episodes

Before counting anecdotes:
- deduplicate actor identity;
- link multiple source units to the same actor;
- link multiple actors to the same organizational buying episode;
- mark uncertain identity resolution.

This prevents quote volume from becoming fake sample size.

## 3. Extract PULL anecdotes independently

For each actor/project/window:
- Project;
- forcing condition;
- commitment;
- options;
- limitations;
- transaction path;
- acceptance boundary;
- next commitment;
- counterevidence;
- unknowns.

Use only the evidence available for that case.

## 4. Build the negative-case register

Explicitly collect:
- people with the same Project but no urgency;
- people with urgency but adequate options;
- interested people who do not commit resources;
- people who enter the funnel and disappear;
- lost deals;
- delayed projects;
- customers who bought for another reason.

Do not let a dataset of "interesting interviews" silently become the denominator.

## 5. Generate candidate patterns

Cluster on demand-side structure, not merely shared words or demographics.

Useful dimensions:
- actor state;
- Project;
- forcing condition;
- commitment behavior;
- options;
- limitations;
- transaction path;
- acceptance boundary.

A semantic similarity cluster is only a candidate pattern.

## 6. Generate rival explanations

For each pattern, produce at least one plausible alternative explanation.

Examples:
- apparent urgency is created by the sales process itself;
- all examples come from a single referral network;
- the pattern reflects one regulation that only affects a narrow subset;
- buyers are purchasing because of an existing relationship rather than the Project;
- enthusiasm is concentrated among users without purchase authority;
- the "limitation" disappears when switching cost is included;
- a recent market event temporarily creates the pattern.

## 7. Run the falsification protocol

Use [06-falsification-protocol.md](./06-falsification-protocol.md).

The agent should actively search the existing corpus for disconfirming evidence before requesting new data.

## 8. Produce the falsification queue

Use [07-question-generation.md](./07-question-generation.md).

Prioritize evidence requests by:
1. ability to distinguish rival explanations;
2. ability to invalidate a core link in the pattern;
3. feasibility of obtaining the evidence;
4. independence from the current selected sample.

## 9. Update pattern state

Candidate patterns may be:
- supported;
- revised;
- split;
- rejected;
- left unresolved.

Do not force resolution.

## 10. Form demand hypotheses

Only supported patterns should normally generate demand hypotheses.

The hypothesis must predict observable future behavior.

## 11. Test behavior, not sentiment

Prefer tests that expose:
- resource commitment;
- transaction friction;
- acceptance boundary;
- timing;
- switching behavior.

Avoid designing the next test primarily to elicit agreement or positive feedback.

## 12. Re-ingest results

Every test produces new evidence.

Feed:
- conversions;
- refusals;
- stalls;
- objections;
- implementation behavior;
- churn;
- unexpected buyers;
- counterexamples

back into the anecdote set.

The analysis is a loop, not a one-time report.
