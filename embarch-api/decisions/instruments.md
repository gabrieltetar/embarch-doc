# embarch-api decisions: Bench instruments

**Status:** active, 2026-10-28.

Decision 97: the tools and subcommands over [embarch-core decision 104](../../embarch-core/decisions/instruments.md)'s routes, for an instrument [embarch-topology decision 49](../../embarch-topology/decisions/instruments.md) declares. Phase 2 of [embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), landed as `tasks/suite/049`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Tools: [../interfaces/tools-instruments.md](../interfaces/tools-instruments.md).

### 97 — Three instrument tools, a measured preset, and an instrument reached only by a study step

**`declare_instrument`, `list_instruments`, `remove_instrument`**, each a tool and a subcommand of the same name, and three `CoreClient` methods (`declare_instrument`, `instruments`, `remove_instrument`) reading and returning topology's own wire types, so nothing is mirrored. A body-less `404` from any of them names a Core older than decision 104, as the bootload routes do.

**A preset carries the line facts the field measured; it is not a model database.** `preset: "et54"` fills an ET54-series electronic load's: 9600 baud, LF out (the load ignores CR alone), CR LF back, 200 ms between commands, `Rexecu success` / `Rexecu err`. Every explicit field overrides it, and Core stores the explicit values, so a preset never has to be resolved again. Without one, `baud` is required and the terminators default to LF and CR LF. Terminators are named `lf`, `cr` or `crlf` on both surfaces: a JSON or shell string carrying a literal `\n` would otherwise reach an instrument as two characters. A second preset is added when a second instrument has been measured, not before.

**There is no `instrument_exchange` tool, subcommand or `CoreClient` method (amended 2026-11-23, EMB-257).** The first cut had one, an error when a query got no whole line or a set was `refused` or `unacknowledged`. Core now refuses the route to every caller, `409`, naming a host study's `Instrument` step as the way in (embarch-core decision 104, `tasks/core/142`), so the tool could only fail. `run_host_study`'s description says an instrument is reached by that step; the step's own result carries the reply and ack.

**Not verified:** run only against a mock Core and in unit tests; no Core with decision 104 is deployed and no instrument has been declared.
