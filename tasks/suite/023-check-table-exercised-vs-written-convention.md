# doc — a suite-wide convention for "has this check arm actually run"

**State:** open — **announced and parked, `ts 1789093650.796139`, posted 2026-09-10 20:27:31 MDT,
window closes 20:57:31 MDT.** Leg 073 announced it and deliberately did not run it: that leg ended
at its 4-unit cap before the window closed. **The next leg completes this window; it does not
restart it** (`../../embarch-fleet/ops.md` §4). Re-read the thread on that `ts` before acting — a
reply saying go runs it now, cancel drops it back to `open` with the reply quoted, silence past
20:57:31 means it may run. Times taken from `date` on the machine at the moment of posting, not
derived from the Slack `ts`.
**Source:** tasks/umbrella/032 (check 14's `WslHost`/`Remote` skip arms are unreachable on a
set-up machine) — the umbrella half landed in `embarch-umbrella/spec.md` (a `measured` marker
on a check-table row, cited to a decision that records a real run) and
`decisions/doctor.md` decision 31.
**Scope:** suite
**Hardware:** none
**Owner:** no

**Filed under `suite/` rather than `doc/` by leg 042.** The drop was written
`Scope: doc`, but its whole subject is `DOC-CONVENTIONS.md` — a shared
suite-level doc that `protocol.md` §3 reserves to the supervisor. `suite/` is
the mechanism that keeps a task off a worker; `doc/` is not. Running it needs
the §8 announcement-and-park window, so a leg takes it as its own unit or
leaves it.
**Hardware:** none

## What

`embarch-umbrella/spec.md`'s `doctor` check table now marks a row `measured` only once a real
run has hit that arm, and says so in prose next to the table (per-file, since `DOC-CONVENTIONS.md`
is off limits to a worker). Three instances of the same shape have now turned up across the
suite — umbrella decision 18 (check 5's Linux-only probe scan), umbrella decision 31/check 14
(this task), and embarch-topology's `TopologyClass::Local`-gated branch named in 032's own "why
this is worth recording" section (leg 022) — which suggests "exercised vs. designed-only" is a
suite-wide table-shape question, not an umbrella-only one.

## Why now

032's supervisor direction (leg 041) was explicit that the durable answer belongs in
`embarch-umbrella/spec.md` first, as a sub-project-local convention, and that generalizing it
into `DOC-CONVENTIONS.md` is a refused branch for a worker — "say so in an inbox drop and leave
the suite-wide half there." This is that drop.

## Done when

- [ ] A decision made (by the owner or a supervisor, not a worker) on whether `DOC-CONVENTIONS.md`
      should adopt a `measured`-style marker as a suite-wide convention for check/table rows that
      distinguish an exercised arm from a merely-designed one, given it has now recurred three times.
- [ ] If adopted, `DOC-CONVENTIONS.md` gets the convention and the other sub-projects with
      class/state-gated check tables (`embarch-topology`, and any other doctor-adjacent surface)
      get a pointer or a pass applying it.
- [ ] If rejected, a one-line note here or in `DOC-CONVENTIONS.md`'s own history saying why three
      instances did not clear the bar for a suite-wide rule.
