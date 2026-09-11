# 025 — Route the probe-vendor-ID fact to `embarch-core`, or record why umbrella keeps its own copy

**State:** claimed by leg 081 (supervisor-executed) — `ops.md` §4 window opened 01:23:21 MDT at
`ts 1789111401.646499` and **closed 01:53:21 MDT with no objection in the thread and none in the
channel**. Silence is consent, so this runs.
**Source:** worker leg 060, task `tasks/umbrella/035` (2026-09-09); drained from `inbox/` and
numbered by the supervisor, leg 060
**Scope:** suite
**Hardware:** none
**Owner:** no

**Not dispatchable while the fleet is in burndown**, and not dispatchable to a worker at all: it
spans `embarch-umbrella` and `embarch-core`/`embarch-topology` (a worker gets one repo,
`../../embarch-fleet/protocol.md` §5) and its only dispositions both author a numbered decision,
which [burndown.md](../../../embarch-fleet/burndown.md) forbids. It is a supervisor unit for a
normal-mode or attended leg, and it needs `ops.md` §4's announcement window like every `suite` task.
Filed `open` rather than `blocked` because nothing needs unblocking — only the mode has to be off.

## What

`embarch-umbrella`'s `doctor` check 5 (`src/doctor.rs:687-779`) walks
`/sys/bus/usb/devices` in umbrella's own process and judges each device against
its own nine-entry `DEBUG_PROBE_VENDOR_IDS` table, to see a debug probe an
unprivileged enumeration can't (decision 18). `035` corrected
`embarch-umbrella/spec.md` and `Cargo.toml` to state this as the one named
exception to "umbrella holds no hardware knowledge" rather than leave the
stated boundary contradicted — that correction is done and out of scope for
this drop.

Left open, and explicitly out of scope for `035` (burndown: no new numbered
decision, no reach into `embarch-core`): **should this enumeration move into
`embarch-core`, which already holds a second, measured probe-vendor-ID table**
(`embarch-topology/src/hardware/port.rs:41,52,60`, three link VIDs, each with a
doc comment) **— or does umbrella keep its own for a stated reason** (e.g. it
needs to answer this before Core is known to be reachable)? Either answer
needs a numbered `embarch-umbrella` decision; right now none exists and
`open.md` only carries the unmeasured-vendor-IDs caveat, not the routing
question.

## Why now

Two sub-projects each hold an independent probe-vendor-ID list with no stated
relationship between them. An engineer whose probe is misidentified has to
guess which of two repos to fix, and whichever repo does not get fixed will
silently drift back out of sync.

## Done when

- [ ] A numbered `embarch-umbrella` decision (and/or an `embarch-core`/
      `embarch-topology` one) states whether check 5's list moves into Core or
      stays in umbrella, and why.
- [ ] If it moves, `embarch-umbrella/src/doctor.rs`'s table is deleted and
      check 5 becomes a Core call; if it stays, `spec.md`'s exception clause
      (added by `035`) names the reason it stays rather than just the fact
      that it does.
