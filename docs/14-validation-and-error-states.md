# Validation and error states

Mechanical validation exists to make unsafe corpus changes noisy.

## Corpus validator

Run:

```bash
python scripts/validate_corpus.py --root .
```

The validator checks:

- JSON-schema conformance;
- stable ID prefixes and filename/ID agreement;
- duplicate artifact IDs;
- duplicate source fingerprints;
- broken and wrong-type references;
- working-set size boundaries;
- evidence packet size boundaries;
- unsupported file types in canonical artifact directories;
- active demand hypotheses derived from non-supported patterns;
- current downstream artifacts depending on stale/unreviewed upstreams;
- resolved falsification items without resolutions;
- supported patterns with no resolved falsification attempt;
- expired dated next-commitment windows as warnings.

## Change-set guard

On pull requests, `scripts/validate_change_set.py` compares base and head.

It prevents:

- protected framework edits without the `framework-change` label;
- new artifacts starting at a revision other than 1;
- deletion of active artifacts without archival;
- canonical artifact renames;
- stable ID changes;
- mutation of accepted evidence packets;
- edits that fail to increment revision exactly once.

## Index guard

`corpus/INDEX.md` is generated.

CI fails when canonical artifacts change without regenerating the index.

Never hand-edit the index.

## Important enforcement limit

GitHub Actions cannot stop a user or agent with direct-push permission from writing to an unprotected default branch. A failing check records the violation after the push.

To make the boundary hard, enable GitHub branch protection/rulesets requiring:
- pull requests;
- the validation status check;
- CODEOWNERS review for framework files;
- no force pushes.

This is a repository-administration boundary, not something a schema can solve.

## Recovery

When validation fails, fix the artifact that caused the error.

Do not:
- delete another artifact merely to satisfy a reference;
- loosen a schema during corpus-operation mode;
- suppress the validator;
- move data into prose to escape schema checks.

If the current system genuinely cannot represent correct evidence, return `FRAMEWORK_CHANGE_REQUIRED` and handle the model change separately.
