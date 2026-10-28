# embarch-core decisions: Bench instruments

**Status:** active, 2026-10-28.

Decision 104: Core talks to a declared bench instrument ([embarch-topology decision 49](../../embarch-topology/decisions/instruments.md)), one command at a time, from a route and from a host study's `Instrument` step. Phase 2 of [embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), landed as `tasks/suite/049`; [embarch-api decision 97](../../embarch-api/decisions/instruments.md) is the tools.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Routes: [../interfaces/instruments.md](../interfaces/instruments.md).

### 104 — An instrument command is a flush line, the instrument's pacing, the command and one reply line; an unacknowledged set fails

**Routes.** `PUT /instruments` declares (or replaces by name), `GET /instruments` lists, `DELETE /instruments/{name}` retracts, `POST /instruments/{name}/exchange` sends one command. The writers and the exchange take `hw_lock`, like `PUT /bootload/ports` and a signal exchange; the three are lease-gated, `GET` is not. A host study's `Instrument` step runs through the route's own body (`run_instrument_exchange`), decision 95's rule for `Exchange`, so a step and the route cannot disagree about an instrument.

**One exchange: open at the declared baud, drop pending input, a flush line, pace, the command, one reply line, close.** The flush line is the write terminator alone. The first instrument's parser holds a partial line from an earlier session and answers the next command `Rcmd err`; an empty line clears it. Its answer is waited for up to 300 ms and **returned apart as `flush_reply`, not dropped**, so a poisoned parser shows in the answer instead of hiding. That costs up to 300 ms per exchange; a session that kept the port open would avoid it, and was rejected for the reason decision 79 opens and closes a signal's port per exchange: nothing else on the bench waits on an idle instrument.

**Pacing is the instrument's `min_interval_ms`, held process-wide** across the route and every host study, measured from the end of one command's read to the next write — the flush line counts. So an exchange on an instrument declaring 200 ms costs at least 200 ms more, which is what that instrument asked for.

**What is read.** A query reads until the read terminator, at most `timeout_ms`. A set is read the same way only when the instrument declares `ack_ok`; otherwise it is written and not read, because waiting out a timeout for an answer nothing expects is a second per command. The reply is the line before the terminator, raw.

**An unacknowledged set fails.** With `ack_ok` declared, a set's answer is `ok` (holds `ack_ok`), `refused` (holds `ack_err`), or `unacknowledged` (anything else, or nothing). A step passes only on `ok`: `Rcmd err` or silence means the action was not carried out as far as anyone can tell, and a study that carried on would measure a load that never switched. A query passes on a whole reply line; empty is `empty_reply`, a partial line `TimedOut`. The step's `detail` adds `replied`, `acknowledged`, `unacknowledged` and `written`.

**`409` while a study holds `study_lock`** (a host study, or the dev-bench handshake): a manual command would land between a study's own steps on an instrument the study is driving. Also `409` when the port is not enumerated after `port_wait_ms`, or the identity matches several ports; `404` for an undeclared name; `400` for an empty line, a CR or LF inside it (one command per exchange; the terminator is added), or a timeout outside 1..=10,000 ms. At submission a host study names only declared instruments, or is `400`.

**Rejected: an instrument as a declared signal.** A signal is a DUT wire (`embarch-topology` decision 37); its exchange has no pacing, no acknowledgement and an echo rule an instrument does not have, and a load on the signal table would show in every place that lists the DUT's wires.

**Not verified:** nothing here has met an instrument. Tests run over a scripted port: the flush line and its kept answer, the three acknowledgements, a set with no `ack_ok` written and not read, a silent query, and pacing across two commands. Owed on a bench: `*IDN?`, `MEAS1:ALL?`, `CH1:SW ON`/`OFF` read back and `LOAD1:ABNO?` on the first instrument, with the time per command recorded here.
