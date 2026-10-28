# embarch-api decisions: Bench instruments

**Status:** active, 2026-10-28.

Decision 97: the tools and subcommands over [embarch-core decision 104](../../embarch-core/decisions/instruments.md)'s routes, for an instrument [embarch-topology decision 49](../../embarch-topology/decisions/instruments.md) declares. Phase 2 of [embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), landed as `tasks/suite/049`.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Tools: [../interfaces/tools-instruments.md](../interfaces/tools-instruments.md).

### 97 — Four instrument tools, a measured preset, and an unacknowledged set is an error

**`declare_instrument`, `list_instruments`, `remove_instrument`, `instrument_exchange`**, each a tool and a subcommand of the same name, and four `CoreClient` methods (`declare_instrument`, `instruments`, `remove_instrument`, `instrument_exchange`) reading and returning topology's own wire types, so nothing is mirrored. A body-less `404` from any of them names a Core older than decision 104, as the bootload routes do.

**A preset carries the line facts the field measured; it is not a model database.** `preset: "et54"` fills an ET54-series electronic load's: 9600 baud, LF out (the load ignores CR alone), CR LF back, 200 ms between commands, `Rexecu success` / `Rexecu err`. Every explicit field overrides it, and Core stores the explicit values, so a preset never has to be resolved again. Without one, `baud` is required and the terminators default to LF and CR LF. Terminators are named `lf`, `cr` or `crlf` on both surfaces: a JSON or shell string carrying a literal `\n` would otherwise reach an instrument as two characters. A second preset is added when a second instrument has been measured, not before.

**`instrument_exchange` is an error when the command did not do its job**: a query without a whole reply line, or a set whose acknowledgement is `refused` or `unacknowledged`. The tool returns the full reply either way (`isError` set on the failure) and the subcommand exits 1, so a script or an agent cannot read an unconfirmed set as done. The reply is raw text, the instrument's own prefix kept.

**The exchange tool's description says a command can change the instrument's state** (switch a load's input, lock its front panel) and to send only what the person asked for, because an agent holding the tool holds the bench's power path.

**Not verified:** run only against a mock Core and in unit tests; no Core with decision 104 is deployed and no instrument has been declared.
