# 167 — A bench is smoke-checked before its first test

**State:** open
**Source:** EMB-368 — no smoke check runs before a bench's first test
**Issue:** EMB-368
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A Test may judge a DUT only on a bench that is set up, identified and running
the firmware it claims. The design (`embarch-doc/notes/hil/03-test.md`,
"Benches" and "A run", item 3): before a bench's first test, the topology the
bench needs is live, the DUT's and every board's identity validates, each
companion board answers a hello, each instrument answers an identity query
(its `*IDN?` reply goes in the report), and the DUT's image is read back, as is
every bench board's; a failing check names the piece, runs no test on that
bench, and is an error for each of them. The same DUT unit moves from bench to
bench, and the runner refuses a different unit on a later bench.

Today the executor (`src/test_executor.rs`, `drive`) raises the setup prompt
before each bench after the first and checks nothing: its comment says the
smoke check is this issue, and its test asserts "no smoke check exists yet".
The pieces exist separately: `validate` (`src/api.rs`), the instrument query
(`src/instrument.rs`), a board's hello line in `run.json`, and the image
readback `core/165` landed (`src/readback.rs`, decision 142, not yet called).

When this is done, before a bench's first test (the first bench included):

- **Declared**: the bench's signals, roles and instruments are declared.
- **Identity**: `validate` passes for the DUT and each bench board.
- **Hello**: each bench board answers the hello line its bench entry carries.
- **Instruments**: each answers `*IDN?`, and the reply is kept.
- **Images**: `readback` runs for the DUT and each bench board; a DUT image
  that `differs` fails the check. What a bench board's `unreleased` or
  `unknown` means for the check is yours to decide and state.
- **Unit key**: the DUT's hardware ID from `validate`. On a later bench a
  different ID is a failed check that refuses that bench. Where the ID cannot
  be read, the run carries `unit_identity_not_read`; if no declared-serial
  field exists yet to key on instead, say so in the decision rather than
  inventing one.
- **Calibration**: a calibration whose serial differs from the `*IDN?` reply is
  not applied, and the measurement says so (`src/host_parse.rs` marks this
  unchecked today, citing EMB-368).
- **A failure** skips that bench's tests as `error` with reason
  `smoke_check`, naming the piece, and the run goes on to the next bench
  (the existing failure policy, decision 136).
- The findings are kept on the run's progress/outcome so the run record
  (a later issue) can carry them; they need no route of their own here.

## Where to look

- `src/test_executor.rs` (`drive`, the `Env` trait, `CoreEnv`, the setup
  window and its tests, which run over fakes)
- `src/api.rs` (the validate path), `src/instrument.rs` (`talk`, `ask`),
  `src/readback.rs`, `src/host_parse.rs` (the calibration line)
- `embarch-doc/embarch-core/decisions/test-run-executor.md` (136, 137) and
  `test-run-setup.md` (139)
- `embarch-doc/notes/hil/03-test.md` and `06-report-and-publish.md` ("The
  audit appendix") — read only; `notes/` is not yours to edit

## Where the doc goes

A new core decision, in a new topic file or `test-run-executor.md` (5.6 KB).
`check-doc-size.py --pressure` lists these core decisions at or over their
limit: `signing#110`, `analog-capture#127`, `host-study#95`,
`definitions#133`, `lease#93`, `stopping-a-study#128` (over), and
`test-run-go#135` (95 B left), `run-log#111` (120 B), `instruments#104`
(144 B). Do not grow any of them; point at them from the new decision instead.
Decision 142's "nothing calls it yet" becomes false: amend that sentence in
place. `main.rs`'s `#[allow(dead_code)]` on the readback module goes if
nothing in it is left unused.

## Done when

- [ ] Over fakes: a missing signal, a failed validate, a silent hello, a
      silent `*IDN?` and a differing DUT image each skip the bench's tests as
      `error`, `smoke_check`, naming the piece.
- [ ] A different DUT hardware ID on bench B refuses bench B, and bench A's
      results stand.
- [ ] A passing check records every identity, every `*IDN?` reply and every
      image status.
- [ ] A calibration whose serial differs from the `*IDN?` reply is not applied,
      and the measurement says so.
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
- [ ] **Hardware debt** recorded here: the check run once against a real bench
      (DUT, one bench board, one instrument).
