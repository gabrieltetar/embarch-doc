# Observe `hw_lock` contention live — a second request must `409` naming the holder

**State:** open
**Source:** owner's bench session 2026-09-06 — `embarch-core/spec.md` §2 states the contention rule and nothing has ever observed it against real hardware
**Scope:** core
**Hardware:** bench
**Owner:** no

## Roles this needs

`dut` and `dev-bench` — two probes, which is what lets a real operation be held long enough
to collide with. Validate both first; if either is unattached, leave this `open`.

## Bench facts — owner-supplied, do not infer

- `dut` = probe `000852006107`; `dev-bench` = probe `001057729826`. Both nRF54L15.
- `GET /serial-log` takes `hw_lock` for its whole `duration_ms` and is the cheapest way to
  hold the lock deliberately. **There is a companion host-side task** to bound that parameter
  — do not conflate the two; this one only observes the current behaviour.
- DUT console: **uart20, TX P1.05 / RX P1.04**.
- **`409` is a refusal, not a fault.** `../../embarch-fleet/protocol.md` §7 says an agent
  misreads it as a bug in its own change; here it is the expected result and the whole point.
- **Read-only.** No flash, no study.

## What

`spec.md` §2's rule — a second hardware request while `hw_lock` is held is rejected with
`409` **naming the holder** — is observed rather than asserted. Hold the lock with one
request, issue a second, and record the exact status and body the caller receives. Confirm
the message actually identifies the holder in a form an operator can act on, and that the
lock is released when the first request completes rather than on a timeout.

If the message does **not** name the holder usefully, that is the finding, and it belongs in
`inbox/` with the observed body — do not fix Core's error text in this unit.

## Why now

This is the refusal every agent in the fleet will now meet the moment two hardware paths
overlap, and its wording is what stops a supervisor treating it as a bug. It has never been
observed against real hardware, and it is read-only to check.

## Done when

- [ ] The `409` body and status are recorded verbatim from a real collision.
- [ ] Whether it names the holder in an actionable way is stated plainly, either way.
- [ ] Release-on-completion is confirmed (a second request succeeds once the first returns),
      distinguished from release-on-timeout.
- [ ] `embarch-core/spec.md` §2's rule is marked observed, with provenance per
      `../../DOC-CONVENTIONS.md`, or corrected if the behaviour differs.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
