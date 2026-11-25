# 163 — An instrument's metrology and calibration reach its measurements

**State:** open
**Source:** EMB-360 — an instrument's uncertainty and calibration never reach its measurements
**Issue:** EMB-360
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`PUT /instruments` takes line facts only, and a bench value's `U` reads
"undeclared" (`src/measurements.rs`). The design: an instrument's resolution,
`U` and calibration date are declared, stamped in Core's signed record with the
token's scope, "checked against the date of each measurement it made", a verdict
on a value past the due date `inconclusive`, `calibration_expired`; "a
declaration whose serial differs from the `*IDN?` reply is not applied"
(`notes/hil/06-report-and-publish.md`, "The audit appendix", Instruments;
`notes/hil/12-prevention.md`). The declaration's shape is the shared crate's:
`embarch-topology/src/hardware/instrument.rs` and
`embarch-topology/decisions/instruments.md` (landed by `suite/063`); the
judgement that reads it is `embarch-study-designer/decisions/hil-tests.md`'s.

- `PUT /instruments` takes the `metrology` and `calibration` blocks and stores
  them in the identity store; the declaration is recorded in `Declarations` with
  its scope, as signals and roles are.
- A step-time value from an instrument gets `resolution`, `uncertainty {U, k,
  basis}` and `u_source: source` from the block, `instrument.calibration` from
  the calibration, and `declared_by` naming the scope.
- The serial check against `*IDN?` waits for the smoke check's reply (EMB-368,
  not built); until then the calibration is applied with its serial unchecked,
  and the measurement says so.
- On an unattested Core the agent's declaration is taken and the report prints
  "declared by the agent" (06); nothing refuses it here. On a `--service` Core,
  decision 132 already makes instrument declarations person-only.

## Where to look

- `embarch-core/src/instrument.rs`, `src/api.rs` (`PUT /instruments`),
  `src/signing.rs` (`Declarations`), `src/measurements.rs`
- `embarch-core/interfaces/instruments.md`; `decisions/instruments.md` (104)
- `embarch-topology`'s instrument declaration, read only (a change there is
  another repo: stop and report it)

## Where the doc goes

`interfaces/instruments.md` amended. **Decision 104 has 144 B left of its entry
limit and decision 110 (signing) is 2,486 B over** (`check-doc-size.py
--pressure`): put this unit's design in a new decision rather than growing
either. No `embarch-core` file is in reserve at filing. If your work pushes one
in, file `tasks/core/<NNN>-compact-core.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] An instrument declared with metrology gives its values the declared `U`
      and resolution, and `declared_by` names the scope.
- [ ] A calibration due before the measurement's time marks the value so the
      shared crate's judgement reads it `calibration_expired`.
- [ ] An instrument with no calibration gives values marked "calibration
      undeclared".
- [ ] `interfaces/instruments.md` amended.
- [ ] Gate green. The native Windows build is a debt the owner runs.
