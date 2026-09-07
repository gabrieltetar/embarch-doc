# 012 — There is no worked study JSON anywhere in 3 MB of docs, `run_study` advertises an untyped object, and the one example in the tree teaches a field removed at schema v11

**State:** open
**Source:** suite review pass 2026-09-06, dimension 7 (the newcomer). Code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Studies are the hardest input in the suite and the only one submitted as a hand-authored file, and
there is no example of one.

- `grep -rn '```json' --include=*.md` over the whole doc corpus returns **zero matches.**
- `suite/studies-guide.md:14` gives `embarch-api run-study --study-file my-study.json` with no
  schema, no example and no pointer to one.
- `embarch-study-designer/interfaces/types.md` is an excellent *Rust type* reference and states
  its own aim as *"concrete enough that a `serde`-derived translation is mechanical"* — but never
  states the one thing that is **not** mechanical: `Action` is externally tagged, so a step reads
  `{"BleAdvertise": {…}}`. Zero JSON in any of the six `interfaces/*.md`.
- `run_study`'s `study` parameter is a bare `serde_json::Value` whose advertised schema is only
  `"type": "object"` (`embarch-api/src/tools.rs:221-245`), so an agent must reconstruct
  `requires`, `steps`, externally-tagged actions and three seals from a tool description.
- `suite/studies-guide.md:66` describes *"the two-step `BleAdvertise` self-test"* that ran green
  against the real bench — which **is** `embarch-api/tests/fixtures/self_test_study.json` — and
  never names the file. `grep -rn "self_test_study\|tests/fixtures"` over the corpus returns
  nothing.
- **That fixture teaches a retired field.** It carries `"validations": []`, and `Study` has no
  such field and no `deny_unknown_fields` (`embarch-study-designer/src/study.rs:90-140`), so it is
  silently accepted and dropped. The field was removed outright at schema v11 —
  `embarch-study-designer/decisions/removed.md:13-15`, decision 48, retired 2026-08-25.

Candidate direction: point the studies guide at one worked example and keep exactly one canonical
copy — most cheaply by naming the existing fixture and fixing it (drop `validations`, add a
`BleConnect` with `target_address` so §3b's advice has a form), so the file is both the doc's
example and the test's input and cannot drift. Whether the JSON belongs inline in the guide or
beside the fixture is a judgement for whoever takes it.

## Why now

The reader is asked to derive the suite's hardest input from prose, and the one artifact in the
tree that would help teaches a field deleted twelve days before this pass. That is
`embarch-decision-reversals.md` shape 3 — *an input accepted, silently discarded, and reported as
success* — landing in the example. No other dimension can see it: it is an absence, uniform across
every doc, with nothing to compare against.

## Done when

- [ ] A reader of `suite/studies-guide.md` can see a complete, currently-valid study file without
      reading a Rust type table.
- [ ] Exactly one canonical worked example exists, and a test consumes it so it cannot go stale.
- [ ] `self_test_study.json` no longer declares a field the type does not have.
- [ ] The externally-tagged shape of `Action` is stated where a hand-author or an agent meets it.
- [ ] Gate green.

**Adjacent, not the same:** `tasks/study-designer/008` withdraws `Study.gatt`/`DeclaredGatt` from
the docs — the same "the reference teaches an unbuilt field" shape in `types.md`, a different
field.
