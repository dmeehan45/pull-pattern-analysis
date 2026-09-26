# Corpus agent rules

Read [../SYSTEM_RULES.md](../SYSTEM_RULES.md) before writing.

This directory contains the live analytical working set.

During normal corpus work:

- canonical artifacts are JSON only;
- use stable collision-resistant IDs;
- check for duplicates and same-episode evidence before creating anything;
- accepted EV artifacts are immutable;
- revisions must increment exactly once;
- preserve contradictions and counterevidence;
- propagate `needs_review` when upstream evidence changes;
- do not modify schemas, docs, scripts, system policy, or root agent instructions;
- run `make index && make qa` before completion.

If input is raw or too large, return `NEEDS_PREPROCESSING`.

If the needed concept cannot be represented, return `FRAMEWORK_CHANGE_REQUIRED`.

Do not invent a local workaround.
