# 178 — An interrupted Test run keeps its finished verdicts, and resumes as a new run of the rest

**State:** claimed by agent/core/178-an-interrupted-test-run-keeps-its-verdicts-and-resumes-as-a-new-run, 2026-11-26 21:22
**Source:** EMB-370 — a Core restart loses a Test run in flight
**Issue:** EMB-370
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Today a Test run that Core's restart left in flight is sealed at the next start
as `interrupted` with **every test null**, because Core keeps no per-test
checkpoint (core decision 144's "Interrupted" paragraph, `open.md`'s Test run
item). `notes/hil/03-test.md`, "A run", item 9 wants more: the run survives a
restart as far as it got, and a resume is a new run of the pending remainder,
linked to the first. When this is done:

- **At start, a Test run left in flight is closed `interrupted` with its
  finished tests' verdicts kept.** Each test the executor finished before the
  restart keeps the verdict, reason and qualifiers it signed; the test in
  flight and every later one is `interrupted` with no verdict. The run's record
  is signed then, saying so. This needs the executor to persist each finished
  test as it ends (a checkpoint beside `<run_id>.started.json`, or whatever the
  record code already writes); choose the shape and record it.
- **`POST /test-runs/{id}/resume`** prepares a new run of the pending tests,
  with `resumes` naming the first (the field already exists in the record and in
  `report-data.json`). It goes through the card and the go like any run, needs
  its own go, and its smoke check reads the images back again. Refused (state
  the code) for a run that is not `interrupted`, or one already resumed.
- **The lease is not restored by the restart**; the resume's go takes the
  session's lease as any go does.

**Not in this task:** publishing a resumed pair as one zip (decision 149 says
it is not done; leave it so), and anything in `embarch-api`. If the resume
route needs a client method, say so in your report so the supervisor files it.

## Where to look

- `src/test_executor.rs`, `src/test_run*.rs`, `src/study.rs` (the `interrupted`
  status), `src/host_study.rs` (a host study's `.partial` events file)
- `embarch-doc/embarch-core/decisions/test-run-record.md` (144 to 146; 144's
  "Interrupted" paragraph is what changes), `test-run-executor.md`,
  `test-run-go.md` (135), `interfaces/test-runs.md` or wherever the Test run
  routes are listed, `interfaces/signing.md` (`resumes`)
- `embarch-doc/notes/hil/03-test.md`, "A run", items 9 and 10

## Where the doc goes

Amend 144's "Interrupted" paragraph if it stays under its limit, else a new
decision it points to. The route goes in the interface doc with the other Test
run routes, and `DOCUMENTED_ROUTE_COUNT` moves with it. **Over or near their
limit, do not grow:** `test-run-go#135` (95 B left), `run-log#111` (120 B),
`signing#110`, `host-study#95`, `lease#93` (all over).

**`open.md` is in reserve** (4,227 of 5,120 B; out of reserve at 3,919 B). Its
compaction task `tasks/core/171` is `blocked` on `In flux: yes`, and its
`Unparks when:` is this unit: "the interruption and resume land". You are the
actor settling that flux, so **if you edit `open.md` — and its Test run item's
last sentence becomes false the moment this lands — compact it out of reserve
in the same commit**, keeping `core/171`'s `Must not delete:` list (the Test
run captures-held item, the Espressif dev-bench port item, the macOS
reasoned-only item), and answer `DOC-COMPACTION-PASS.md`'s human question in
your commit message. Leave `tasks/core/171` itself to the supervisor.

**Decision numbers:** the next core decision is the next free number in
`decisions.md`'s index at the time you write it. Twice in a row a worker's code
comment cited a neighbouring decision's number; cite the one you wrote.

## Done when

- [ ] A fixture run stopped mid-bench, then a new `AppState` over the same
      folder, gives an `interrupted` run whose signed record keeps its finished
      verdicts and marks the rest `interrupted`.
- [ ] Its resume prepares only the pending tests, names the first run in
      `resumes`, and needs its own go.
- [ ] The resumed run's smoke check reads the images back again.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [ ] Decisions and interfaces updated; `changelog.d/` fragment; a
      `features.d/` row change if the Test run feature row's caveats move.
