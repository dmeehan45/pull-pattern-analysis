# Templates

These files demonstrate canonical artifact shapes. They are examples, not live corpus records.

The example IDs are reserved by `system/policy.json`; validation rejects them inside `corpus/`.

For a real artifact: generate a new collision-resistant ID, replace example content, preserve `schema_version`, start at `revision: 1`, place the JSON file in its matching corpus directory, then run `make index && make qa`.

The Markdown evidence worksheet is only a preprocessing aid. Canonical corpus state is JSON.
