# embarch-core decisions: An instrument's metrology and calibration on its measurements

**Status:** active, 2026-11-25 (`tasks/core/163`, EMB-360; `embarch-topology` decision 51; `notes/hil/06-report-and-publish.md` "The audit appendix", Instruments). Index: [../decisions.md](../decisions.md). Surface: [../interfaces/instruments.md](../interfaces/instruments.md). Builds on [instruments.md](instruments.md) (104) and [host-parse.md](host-parse.md) (131).

### 140 — A bench instrument's value takes its declared `U`, resolution and calibration; the calibration is judged against the day the value was read

**Declaring.** `PUT /instruments` already took the `Instrument` of the shared crate, `metrology` and `calibration` included, so they are stored in the identity store and the declaration is already in `Declarations` with the token's scope (decision 131's ledger, `instrument`). Nothing new is stored.

**Stamping.** `host_parse::measurement` looks the instrument up at write time (`instrument::get`, injected as `instrument_of` so tests need no enrollment dir) for a step that addressed an `Instrument`. The metrology entry that speaks for the value is **the one whose `unit` equals the parse's unit, when exactly one does**; two entries in one unit leave no honest pick, so none applies and the value stays `undeclared`. The value then carries `resolution`, `uncertainty {U, k, basis}` (the entry's basis: `datasheet`, `certificate` or `declared`) and `u_source: "source"`. `declared_by` gains `{what: "instrument", name, scope}`, the scope from the ledger and `agent` where Core did not see it declared (an unattested Core takes the agent's declaration; the report prints it, 06). A DUT's or a board's value is untouched.

**Calibration.** `instrument.calibration` on the measurement holds the declared block (`serial`, `certificate_ref`, `due`, `certificate_sha256?`) and `serial_checked: false` until the smoke check has kept the instrument's `*IDN?` reply; then the serial is compared and a difference is not applied ([143](smoke-check.md)). An instrument with no calibration has no `calibration` key.

**Judging.** `judge_measurements` sets `calibration_expired` on an instrument value when its `due` is **before the UTC date of `at_utc_ms`** (due on the day itself is still valid; **chosen, not measured**), so the shared crate's rule reads it `inconclusive`, `calibration_expired`. `calibration_undeclared` for an instrument value is "no `calibration` key"; for every other origin it is the old "the test names no source". The date is computed from the timestamp (`utc_date`), as no date crate is a dependency.

**Not built.** A bench board's characterisation validity period; the serial check; the report's per-instrument calibration status (publish).
