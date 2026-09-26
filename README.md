# Pull Pattern Analysis

An operational framework for turning raw customer evidence into **PULL anecdotes**, testing whether those anecdotes replicate into **PULL patterns**, and forming **demand hypotheses** that have survived explicit attempts at falsification.

This repository is designed to back an analysis agent used by product teams and founding teams working from interviews, sales calls, support conversations, field notes, CRM records, emails, transcripts, and other raw customer inputs.

## Core flow

```text
raw customer evidence
        ↓
PULL anecdotes
        ↓
candidate PULL patterns
        ↕  challenge / seek disconfirming evidence
supported, revised, or rejected PULL patterns
        ↓
demand hypotheses
        ↓
offer / product / sales tests
        ↓
observed commitment or falsification
        ↓
revised evidence base
```

This is deliberately **not** a pipeline that turns every collection of anecdotes into a demand hypothesis. Its purpose is to kill weak patterns early.

A useful output is often:

> We do not yet have enough evidence to claim a pattern. Here are the highest-information questions, cases, and observations that would distinguish the competing explanations.

## Intellectual lineage

The foundation is Rob Snyder's PULL framework from *The Power of PULL* (Basic Venture, 2026). Snyder's framework describes PULL using four elements:

- **Project** — the product-agnostic thing a person is trying to accomplish.
- **Unavoidable** — the situation that makes the project a priority now.
- **List** — the options available to accomplish the project.
- **Limitations** — why those options do not adequately accomplish it.

Snyder later argued that teams should start from a **PULL anecdote** — one real person exhibiting real PULL now — rather than inventing a PULL hypothesis from abstract reasoning and then searching for confirming examples.

Primary sources:
- Rob Snyder, *The Power of PULL: What You Need to Know About Customer Demand to Build a Successful Startup (and Why Most Founders Get It Wrong)*, Basic Venture, July 7, 2026: https://www.hachettebookgroup.com/titles/rob-snyder/the-power-of-pull/9781541705951/
- Rob Snyder, "The PULL framework," May 2, 2025: https://thephysicsofstartups.substack.com/p/the-pull-framework
- Rob Snyder, "The PULL Quickstart Guide": https://thephysicsofstartups.substack.com/p/the-pull-quickstart-guide
- Rob Snyder, "No more PULL hypotheses," September 4, 2026: https://thephysicsofstartups.substack.com/p/no-more-pull-hypotheses
- Rob Snyder, "Are they pulling?", June 26, 2026: https://thephysicsofstartups.substack.com/p/my-sales-call-analyzer

## What this repository adds

The following are **extensions developed in this repository**, not claims about Snyder's framework:

- **PULL pattern** — a descriptive recurring structure across multiple independent PULL anecdotes.
- **Demand hypothesis** — a falsifiable prediction that actors in a defined state will commit scarce resources when a particular project, forcing condition, option failure, and acceptance boundary are present.
- Explicit **time boundaries** and revalidation.
- Explicit **resource commitment** rather than assuming budget existence proves demand.
- Explicit **transaction path** from intent to resource allocation.
- Explicit **acceptance boundary** linking demand-side evidence to supply requirements.
- Explicit **observable next commitment**.
- A continuous **falsification loop** that searches for counterexamples, rival explanations, missing cases, and selection effects before generalizing.

The distinction is:

```text
PULL anecdote      = what happened
PULL pattern       = what appears to recur
Demand hypothesis  = what we predict will recur, under specified conditions
```

## Two jobs for the agent

### 1. Evidence synthesis

Given a potentially large set of raw customer inputs, the agent should preserve source provenance, extract independent PULL anecdotes, distinguish observed facts from interpretation, compare anecdotes without prematurely merging them, surface candidate PULL patterns, and form demand hypotheses only where evidence warrants them.

### 2. Adversarial inquiry

For every emerging pattern, the agent should ask:

- What would have to be true for this pattern to be wrong?
- What cases are missing from the evidence?
- What alternative explanation fits the same observations?
- Are we over-sampling buyers, enthusiastic users, one role, one channel, or one moment in time?
- What question or observation would most reduce uncertainty?
- What evidence should we actively seek that could kill this pattern?

The output is not merely "more research questions." It is a **falsification queue**, prioritized by information value.

## Repository guide

- [AGENTS.md](./AGENTS.md) — instructions for an agent operating this framework
- [docs/01-concepts.md](./docs/01-concepts.md) — concepts, lineage, and extensions
- [docs/02-pull-anecdote.md](./docs/02-pull-anecdote.md) — anecdote structure
- [docs/03-pull-pattern.md](./docs/03-pull-pattern.md) — pattern synthesis
- [docs/04-demand-hypothesis.md](./docs/04-demand-hypothesis.md) — demand hypothesis definition
- [docs/05-analysis-protocol.md](./docs/05-analysis-protocol.md) — end-to-end analysis process
- [docs/06-falsification-protocol.md](./docs/06-falsification-protocol.md) — challenge loop and bias controls
- [docs/07-question-generation.md](./docs/07-question-generation.md) — high-information follow-up questions and data requests
- [docs/08-evidence-model.md](./docs/08-evidence-model.md) — evidence states, provenance, and independence
- [schemas/](./schemas/) — machine-readable artifacts

## Governing principle

**Do not optimize for producing a hypothesis. Optimize for discovering what the evidence can survive.**
