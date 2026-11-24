# 187 — The instrument and signal tools carry a safe-off

**State:** claimed by agent/api/187-the-instrument-and-signal-tools-carry-a-safe-off, 2026-11-24 09:53
**Source:** HIL implementation plan (`notes/hil/14-implementation-plan.md`, attested phase): the safe-off field landed on `Instrument` and `SignalLink` in `embarch-topology` (`topology/072`, `suite/059`), and the api's tools still send it empty
**Issue:** EMB-334
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-topology` decision 49 now gives `Instrument.safe_off: Vec<String>`
(one command per line) and `SignalLink.safe_off: Option<String>`; Core's
`PUT /instruments` and `POST /signals` store them and answer `400` for a bad
line. `DeclareInstrumentParams` and `DeclareSignalParams` (`src/tools.rs`) list
their own fields and have no safe-off: `src/instrument.rs` builds the
instrument with `safe_off: Vec::new()` and `tools.rs` builds the signal link
with `safe_off: None`.

When this is done `declare_instrument` and its CLI verb take
`safe_off: Option<Vec<String>>`, `declare_signal` and its CLI verb take
`safe_off: Option<String>`, and both pass it through to Core as the topology
type holds it. The tool descriptions say what the field is for (the command
that switches the output off, which Core sends at a start and a graceful stop)
and that a declaration without one is listed, not refused.

**Carry a declared safe-off through a re-declare** (Finding comment on
EMB-334, 2026-11-24): `PUT /instruments` replaces an instrument by name, so a
re-declare that sends no safe-off silently drops one declared by another path.
Decide how the tool avoids that (for example, keep the stored value when the
caller omits the field, and drop it only on an explicit empty list), and record
the rule in the tool doc and by amending decision 97 in place.

**Not in this task:** the `et54` preset's safe-off line, which needs a command
from the instrument's programming manual that nothing on disk holds; that is
`api/188`, parked.

## Why now

The next Core start after a stop can only switch off what was declared, and
the agent's and the person's tools are where an instrument and a signal are
declared. EMB-334.

**Burndown leg: no new numbered decision.** Amend decision 97 in place. If the
change seems to need a new decision, stop and say so in this file.

**Doc-size reserve (dispatch note):** no `embarch-api` file is in reserve.
Decisions near their per-decision limit are ones this task does not touch
(lease#90, ledger#98, bench-exchange#89, failure-reporting#67).

## Done when

- [ ] A fake Core receives `safe_off` from each tool and each CLI verb.
- [ ] A declaration without it behaves by the rule you chose, with a test
      covering a re-declare over a stored safe-off.
- [ ] `interfaces/tools-instruments.md` (and the signal tool's doc) describe the
      field and the re-declare rule; decision 97 amended.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `--workspace` included.
- [ ] `changelog.d/` fragment dropped.
