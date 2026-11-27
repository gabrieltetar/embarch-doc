# embarch-api decisions: Bench instruments

**Status:** active, 2026-10-28.

Decision 97: the tools and subcommands over [embarch-core decision 104](../../embarch-core/decisions/instruments.md)'s routes, for an instrument [embarch-topology decision 49](../../embarch-topology/decisions/instruments.md) declares. Phase 2 of [embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), landed as `tasks/suite/049`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Tools: [../interfaces/tools-instruments.md](../interfaces/tools-instruments.md).

### 97 — Three instrument tools, a measured preset, and an instrument reached only by a study step

**`declare_instrument`, `list_instruments`, `remove_instrument`**, each a tool and a subcommand of the same name, and three `CoreClient` methods (`declare_instrument`, `instruments`, `remove_instrument`) reading and returning topology's own wire types, so nothing is mirrored. A body-less `404` from any of them names a Core older than decision 104, as the bootload routes do.

**A preset carries the line facts the field measured; it is not a model database.** `preset: "et54"` fills an ET54-series electronic load's: 9600 baud, LF out (the load ignores CR alone), CR LF back, 200 ms between commands, `Rexecu success` / `Rexecu err`. Every explicit field overrides it, and Core stores the explicit values, so a preset never has to be resolved again. Without one, `baud` is required and the terminators default to LF and CR LF. Terminators are named `lf`, `cr` or `crlf` on both surfaces: a JSON or shell string carrying a literal `\n` would otherwise reach an instrument as two characters. A second preset is added when a second instrument has been measured, not before.

**`safe_off` is carried by `declare_instrument` and `declare_signal`, and a re-declare keeps the stored one (amended 2026-11-24, EMB-334, `tasks/api/187`).** Topology decision 49 gave `Instrument.safe_off: Vec<String>` and `SignalLink.safe_off: Option<String>`; the tools take `safe_off` (a list of commands, one per line; a single line) and pass it through as the topology type holds it. A declaration without one is listed, not refused. Core's `PUT /instruments` and `POST /signals` replace by name, so a call that sent nothing would silently drop a line declared by another path. **The rule: omitted keeps the stored value, an explicit empty list (instrument) or empty string (signal) clears it.** The tool reads the stored row first (`GET /instruments`, `GET /signals`) and copies its `safe_off` over; a read that fails stops the declare rather than dropping the line. The subcommands take `--safe-off` (repeatable on `declare-instrument`) and `--clear-safe-off` (instrument), or `--safe-off ""` (signal). A given `safe_off` skips the read. The `et54` preset carries none: its off command is not on disk (`tasks/api/188`).

**There is no `instrument_exchange` tool, subcommand or `CoreClient` method (amended 2026-11-23, EMB-257).** The first cut had one, an error when a query got no whole line or a set was `refused` or `unacknowledged`. Core now refuses the route to every caller, `409`, naming a host study's `Instrument` step as the way in (embarch-core decision 104, `tasks/core/142`), so the tool could only fail. `run_host_study`'s description says an instrument is reached by that step; the step's own result carries the reply and ack.

### 138 — `declare_instrument` carries metrology and calibration, and a re-declare keeps what is stored

**Core takes an instrument's metrology and calibration** (`suite/063`, [embarch-topology decision 51](../../embarch-topology/decisions/instruments.md)); until now this crate sent `metrology: []` and no calibration, so nothing could declare the `U`, resolution and range a Test's limit needs. Both surfaces take them in topology's own shape, sent as given. The tool: `metrology` (a list of `{quantity, unit, resolution, U, k, basis, range: {min, max}}`, `basis` one of `datasheet`, `certificate`, `declared`), `calibration` (`{serial, certificate_ref, due, certificate?}`) and `clear_calibration`. The subcommand: `--metrology '<json>'` (repeatable), `--calibration '<json>'`, `--clear-metrology`, `--clear-calibration`; the JSON is the tool's, so the two cannot drift. `certificate` is a path: the file is read here and only its SHA-256 (lower-case hex) is sent; the file stays with the person.

**Refused before Core is called**, by topology's own `Instrument::check`, which names the field: a `due` that is not a real `yyyy-mm-dd` date, a negative or non-finite `U` or resolution, `k` not above zero, a range whose `min` is not below its `max`, an unknown `basis`, an unreadable certificate file. This crate adds no second validator.

**Omitted keeps the stored value, as `safe_off` does (decision 97):** `PUT /instruments` replaces by name, so a re-declare that sent no metrology would erase what another path declared. The declaration reads `GET /instruments` unless all three of `safe_off`, `metrology` and `calibration` are given; `metrology: []` / `--clear-metrology` and `clear_calibration` / `--clear-calibration` drop them.

**The tool's text says what each value decides:** `U` and resolution decide whether a limit can be judged at all, a calibration past its due date makes a verdict inconclusive, and on a Core that is not attested a value the agent declares reads "declared by the agent" (the text tells the agent to declare only what a datasheet or certificate gives). The client crate re-exports `Metrology`, `MetrologyBasis`, `MeasuringRange` and `Calibration`: additive.

**Not verified:** against a mock Core and in unit tests only; no Core with decision 51 has been given a declaration from here, and what Core stamps on a measurement was not read back.

**Not verified:** run only against a mock Core and in unit tests; no Core with decision 104 is deployed and no instrument has been declared.
