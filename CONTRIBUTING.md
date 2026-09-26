# Contributing

Start with [SYSTEM_RULES.md](./SYSTEM_RULES.md) and [AGENTS.md](./AGENTS.md).

## Normal corpus changes

A normal customer-learning change should touch only:

- `corpus/evidence/`
- `corpus/anecdotes/`
- `corpus/patterns/`
- `corpus/hypotheses/`
- `corpus/falsification/`
- `corpus/archive/`
- `handoffs/explore/`
- generated `corpus/INDEX.md`

Before opening or merging a change:

```bash
make qa
```

If the index is stale:

```bash
make index
make qa
```

## Framework changes

Changes to schemas, system policy, agent instructions, validators, documentation, tests, or workflows are framework changes.

Keep them separate from evidence ingestion. Use the `framework-change` PR label and owner review.

## Branch protection

For hard repository-level enforcement, configure the default branch to:

- require pull requests;
- require the `corpus-guard / validate` status check;
- require CODEOWNERS review for protected framework paths;
- dismiss stale approvals when new commits are pushed;
- block force pushes and branch deletion.

The files in this repository provide validation and review boundaries, but GitHub branch rules are what prevent a writer with direct-push permission from bypassing them.
