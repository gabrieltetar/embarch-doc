# 100 — The studies guide leads with the signal's own baud

**State:** done — fragment delivers corrected sections 3 and 4 step 1
**Source:** suite review audit, 2026-11-23: `suite/studies-guide.md` sends a newcomer to a registry edit for a signal's line rate
**Issue:** EMB-318
**Scope:** doc
**Hardware:** none
**Owner:** no

## What

`suite/studies-guide.md` §3 (the third knob paragraph) presents
`EMBARCH_SIGNAL_BAUD`, set in the Core service's registry Environment with a
restart, as the control for a DUT signal's line rate, and §4 step 1 lists a
signal's name and route only. The code says a signal's own `baud` wins
(`embarch-core/src/stream_store.rs`, `link.baud.unwrap_or_else(signal_baud)`),
and both `embarch-api declare-signal` (`src/cli.rs`) and the `declare_signal`
MCP tool take it.

Confirm each of those three facts in the code first, and record what you
found in this file. Then write the corrected text: §3 names declaring the
signal with its baud as the way to set a line rate, and the env var only as
the fallback for a signal that declares none; §4 step 1 shows the baud on the
declare. Assert no DUT's actual rate: which rate a given board needs is the
owner's call, not the guide's.

`suite/studies-guide.md` is a shared suite-level doc, which a `doc` worker
does not edit (`../../embarch-fleet/protocol.md` §3, §9). **Deliver the
change as a `status.d/doc-*` fragment** carrying the replacement text for each
passage, per `status.d/README.md`; the supervisor applies it at the fold.

If `embarch-core/decisions/signal-exchange.md` (cited by the audit) also
presents the env var as the control, say so in this file and do not edit it:
that path is `core`'s.

## Why now

A newcomer following the guide edits the Windows registry and restarts a
service to do what one field on the declare already does. EMB-318.

**Burndown leg: no new numbered decision.** None should be needed.

## Done when

- [x] The three code facts are confirmed, with where, in this file.
- [x] A `status.d/doc-*` fragment gives §3 and §4 step 1 text that names the
      per-signal `baud` first and the env var as the fallback.
- [x] `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Findings

Confirmed 2026-11-24:

1. `embarch-core/src/stream_store.rs:116-119`, `signal_baud_for`: `link.baud.unwrap_or_else(signal_baud)`; `signal_baud()` reads `EMBARCH_SIGNAL_BAUD` else `DEFAULT_SIGNAL_BAUD` (1_000_000).
2. `embarch-api/src/cli.rs` `declare-signal` takes `baud` (`Option<u32>`, passed to `parse_signal_link`, ~lines 277, 1699).
3. `embarch-api/src/tools.rs:916-920` the declare_signal MCP params carry `baud: Option<u32>` ("e.g. 115200 for a DUT console", `embarch-topology` decision 37).

`embarch-core/decisions/signal-exchange.md` does not exist in the main checkout (no `decisions` path under `embarch-core`), so there is nothing there to flag. Replacement text is in `status.d/doc-studies-guide-signal-own-baud.md`.
