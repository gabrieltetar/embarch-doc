# 100 — The studies guide leads with the signal's own baud

**State:** claimed by agent/doc/100-studies-guide-leads-with-the-signals-own-baud, 2026-11-24 03:19
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

- [ ] The three code facts are confirmed, with where, in this file.
- [ ] A `status.d/doc-*` fragment gives §3 and §4 step 1 text that names the
      per-signal `baud` first and the env var as the fallback.
- [ ] `changelog.d/` fragment dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
