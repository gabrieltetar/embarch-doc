# embarch-topology decisions: Bench instruments

**Status:** active, 2026-10-28.

Decision 49 is the `instruments` table: a bench instrument Core drives over a USB serial line, declared with the line facts it needs. Phase 2 of [embarch-host-study-proposal.md](../../embarch-host-study-proposal.md), landed as `tasks/suite/049`; [embarch-core decision 104](../../embarch-core/decisions/instruments.md) is the route that talks to one, [embarch-api decision 97](../../embarch-api/decisions/instruments.md) the tools.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 49 — A bench instrument is declared with its port identity and its line facts, in its own table

**`Instrument { name, protocol: scpi, port: UsbPortId, baud, write_terminator, read_terminator, min_interval_ms, ack_ok?, ack_err? }`**, an `instruments` table in `enrollment.toml` beside `bootload_ports` (decision 36), skipped when empty so a store that never declared one is rewritten unchanged. It is found by `UsbPortId` exactly as a bootload port is, and an identity matching more than one live port is an error naming every one, never a pick.

**Declared, never detected**, for decision 36's reason made sharper: the first instrument sits behind a CH340 bridge, whose VID:PID every CH340 shares and which carries no USB serial number. **Two instruments one live port could match both of are refused at declaration**, as a bootload pair is; the remedy is a serial number or an interface that differs, and saying so at declaration puts it in front of the person who can act on it.

**The line facts are the instrument's, so they are declared once here and every caller reads them.** The first instrument taught them the hard way: it ignores a command ended by CR alone, ends replies with CR LF, wants 200 ms between commands, answers a set `Rexecu success` or `Rexecu err` and an unknown command `Rcmd err`, and a partial line poisons its parser for the next command. Carried in each caller, a study step and a one-off exchange would disagree about them on the first edit. So: terminators default to LF out and CR LF back; `min_interval_ms` defaults to 0; **`ack_ok` is what makes a set checkable**, and `ack_err` without `ack_ok` is refused because a set is judged by `ack_ok` alone (decision 104 has why an answer holding neither is a failure).

**The wire types live here too**: `InstrumentExchange` (one command: `line`, `query`, `timeout_ms`, `port_wait_ms`), `InstrumentReply` (the raw reply line, `terminated`, `ack`, the flush line's answer, pacing and timing), and `Ack` (`ok`, `refused`, `unacknowledged`), so Core and `embarch-core-client` cannot drift (decision 31's posture). `judge_ack` and `InstrumentReply::succeeded` say what an answer means in one place. **Nothing parses a value**: a reply is text, an instrument's own prefix kept.

**A name is a URL path segment**: ASCII letters, digits, `-`, `_`, `.`, at most 64 bytes. Only `scpi` exists; `protocol` is an enum so a second one is a new variant, not a reinterpretation.

**Not verified:** no instrument has been declared on a real bench. The line facts above are the field's (seen on the unit or in its manual, recorded in `tasks/suite/049`), not a run of this code. One of them matters to a reader of an error: the CH340 enumerates with the load switched off, so a query with no reply is not a missing port.
