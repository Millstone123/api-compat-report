# api-compat-report

`api-compat-report` compares two JSON Schema documents and writes a concise migration report.

## Commands

```text
python3 -m api_compatibility compare --from fixtures/user_v1.json --to fixtures/user_v2.json
python3 -m api_compatibility validate fixtures/sample_valid.json --schema fixtures/user_v2.json
python3 -m api_compatibility report fixtures/user_v1.json fixtures/user_v2.json --output migration_report.md
python3 -m api_compatibility review fixtures/user_v1.json
python3 -m api_compatibility diagnose --from fixtures/user_v1.json --to fixtures/user_v2.json
```

The supported schema subset is `type`, `properties`, `required`, and `enum`.
`validate` exits `0` for a conforming sample and `1` when violations are found.
`report` writes deterministic Markdown with stable field ordering and no timestamp.
`review` is an inspection-only view and does not resolve migration conflicts.

## Local verification

```text
python3 -m compileall -q api_compatibility
python3 -m unittest discover -s tests -v
python3 -m pytest -q
```

An isolated install is optional:

```text
python3 -m venv .venv
.venv/bin/python -m pip install --no-build-isolation .
.venv/bin/python -m api_compatibility compare --from fixtures/user_v1.json --to fixtures/user_v2.json
```
