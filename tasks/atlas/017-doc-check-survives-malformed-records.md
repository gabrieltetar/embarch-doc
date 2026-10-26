# 017 — `doc check` reports a malformed record as a finding instead of crashing on it

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-atlas finding 2), verified by Opus against embarch-atlas@0cf93cec
**Scope:** atlas
**Hardware:** none — Checker logic over fixture records. `tests/datasheet_synth.py` and `tests/mutate_records.py` already build and mutate such records.
**Owner:** no

## What

`run_check` (`src/embarch_atlas/check.py:1192`) runs schema validation (`R.validate`, `check.py:1228`) last. Two steps before it dereference record fields and assume the schema's shapes:
- `check_registers`, at `check.py:1207`, before the per-record loop starts.
- `record_checks`, at `check.py:1227`, for the same record.

So one LLM-written record of the wrong shape raises out of the whole run:
- `"bits": [7]` fails the unpack at `check.py:745`.
- `"width": "8"` fails `[None] * w` at `check.py:742`.
- A field with no `reg` raises `KeyError` at `check.py:814`.
- A `reset` that `int(…, 0)` cannot parse raises at `check.py:756`.
- `"p": "8"` becomes `["8"]` (`records.py:193-197`) and fails `1 <= p` in `DocText.has` (`check.py:237`).

The session gets a Python traceback that names no record, no checks.json is written, and nothing is rendered. The schema states each of these shapes (`schemas/record.schema.json`: `bits` is two integers, `p` an integer or a list of integers). `doc check` exists to turn exactly this kind of LLM mistake into a `V:` line on the record.

One possible direction: validate every record first. A record with schema errors gets its `V:` issues and stays `llm-unverified`, as principle 4 keeps a failing fact. It is also kept out of the structural and anchoring checks that assume its shape. Every other record is checked as today.

## Why now

DESIGN.md principle 4: "Nothing is deleted for failing a check. A failing fact is kept and marked `llm-unverified`." The checker's own error-injection harness covers wrong values, not wrong types. The crash therefore shows up in a translation session, mid-document, at the point where the session most needs to know which record to fix.

`tasks/atlas/011` (new record kinds and their `doc check` rules) and `016` (check W) also edit `check.py`. This change is small and should land before them, so their new checks inherit the shape guard.

## Done when

- [ ] `doc check` on a fixture document holding one record of each malformed shape above exits through its normal report and writes checks.json. Each malformed record carries a `V:` issue naming its id and field. Every well-formed record's results are identical to a run without the malformed ones.
- [ ] A test generates, for each schema-typed field that a check dereferences, a record with that field of the wrong type or length, and asserts that `run_check` does not raise.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `DESIGN.md` (the `doc check` row, or the checks section of the translate-docs procedure it points to) says that a schema-invalid record is reported and not run through the other checks. `changelog.d/` fragment dropped.
