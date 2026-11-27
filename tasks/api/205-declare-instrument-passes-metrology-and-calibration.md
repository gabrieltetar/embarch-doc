# 205 — declare_instrument passes an instrument's metrology and calibration

**State:** claimed by agent/api/205-declare-instrument-passes-metrology-and-calibration, 2026-11-26 17:43
**Source:** EMB-375 — declare_instrument cannot pass an instrument's metrology or calibration
**Issue:** EMB-375
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Core takes an instrument's metrology and calibration since `suite/063`
(`embarch-topology` decision 51; Core keeps them in its own store). The
`declare_instrument` tool and its subcommand still send line facts only:
`src/instrument.rs` fills `metrology: Vec::new()` and `calibration: None`. So
nothing in `embarch-api` can declare the `U`, resolution or range a Test's
limit needs before it can be judged (`embarch-doc/notes/hil/03-test.md`, "The
verdict"). When this is done:

- **Optional `metrology` and `calibration` arguments** on the tool and the
  subcommand, in the shape `embarch-topology`'s `Instrument` carries them, sent
  to Core as given. A `certificate` file argument is sent as its SHA-256; the
  file itself stays with the person.
- **Refused before Core is called**: a malformed date, a negative `U` or
  resolution, a range whose low end is above its high end.
- **The tool's text says what each value decides**: `U` and resolution decide
  whether a limit can be judged; a calibration past its due date makes a
  verdict inconclusive; on an unattested Core a value the agent declares reads
  "declared by the agent".
- CLI and tool stay in parity, as decision 97 requires of the instrument tools.

## Where to look

- `src/tools.rs`, `src/instrument.rs`, `src/cli.rs`
- `embarch-topology/src/` — the `Instrument` type and its metrology and
  calibration fields — read only
- `embarch-core/src/instrument.rs` — what Core accepts — read only
- `embarch-doc/embarch-api/decisions/instruments.md` (97),
  `interfaces/tools-instruments.md`

## Where the doc goes

A new api decision, in `decisions/instruments.md` or a new topic file, and
`interfaces/tools-instruments.md` amended with the new arguments.
**`embarch-api/spec.md` is in reserve** (1,110 B left; its compaction,
`tasks/api/201`, is blocked): do not grow it — if spec must say something, say
it in fewer bytes than you remove. `check-doc-size.py --pressure` lists
`lease#90`, `test-plans#134` (over), `ledger#98`, `bench-exchange#89` and
`failure-reporting#67` near or over their limit: do not grow those.

## Done when

- [ ] Against a fake Core, the tool and the subcommand send the blocks as given.
- [ ] A malformed date, a negative `U` and an inverted range are refused, and
      Core is not called.
- [ ] The interface doc lists the new arguments and the decision records them.
- [ ] Gate green (`cargo build --workspace`, `test`, `clippy --all-targets -- -D warnings`).
