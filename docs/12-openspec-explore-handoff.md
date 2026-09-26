# OpenSpec Explore handoff

## Position in the product workflow

This repository is intended to sit **beside and slightly upstream of product exploration**, not to replace a team's product-development system.

OpenSpec currently describes `/opsx:explore` as a no-stakes exploration mode used to map a problem, inspect context, weigh options, and shape a plan before a proposal is written. Its subsequent `propose` step creates proposal/spec/design/task artifacts.

References:
- https://openspec.dev/
- https://github.com/Fission-AI/OpenSpec

This corpus fits naturally before or during that Explore phase.

Its job is to provide a sharper demand-side input:

```text
customer evidence
      ↓
this repo
PULL + demand analysis
      ↓
Explore handoff
      ↓
OpenSpec / product Explore
      ↓
proposal/specification if the team chooses to build
```

## Boundary

This repository should answer:

- What customer Project appears active?
- Under what forcing conditions?
- What evidence says actors are committing resources?
- What options are failing, and why?
- What transaction path appears viable or blocked?
- What acceptance boundary does supply need to cross?
- What remains uncertain?
- What evidence could falsify the demand claim?

It should **not** decide:
- the product architecture;
- implementation design;
- task breakdown;
- final requirements;
- whether a specific proposed solution is the right build.

Those belong downstream.

## Explore handoff artifact

When a product team wants to use the current corpus in a product exploration session, generate a compact handoff under:

`handoffs/explore/<date>-<slug>.md`

The handoff should contain:

### Demand context
- active demand hypothesis;
- linked PULL pattern(s);
- relevant customer state and time window.

### Evidence
- strongest supporting anecdotes;
- strongest counterexample;
- selection/sampling warning;
- unresolved contradiction.

### Acceptance boundary
What must become true for new supply to become viable?

### Transaction reality
What path can resources actually move through?

### Falsification state
What has survived challenge, and what has not?

### Open questions
Only the uncertainties that matter to the product exploration.

### Product-neutral warning
Restate the Project without assuming a solution.

## Do not mirror OpenSpec artifacts here

Do not create a second `openspec/` tree in this sidecar.

Do not copy proposal/spec/design/task documents into the demand corpus.

Instead, hand downstream tools one stable exploration brief and references to the supporting evidence.

This keeps:
- demand evidence separate from solution specification;
- customer learning reusable across multiple possible product proposals;
- product implementation churn from rewriting the historical demand record.

## Feedback loop

The handoff is not one-way.

A downstream exploration or product test may discover:
- the acceptance boundary was wrong;
- implementation cost changes the transaction path;
- buyers will not switch;
- another option is better than expected;
- a different user/buyer split exists.

Those findings should return to this corpus as new evidence packets and then flow through the normal reconciliation and falsification process.

Product exploration is therefore another source of evidence, not the terminal consumer of the corpus.
