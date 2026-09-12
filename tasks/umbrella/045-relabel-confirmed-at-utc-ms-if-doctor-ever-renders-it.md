# 045 — Relabel `confirmed_at_utc_ms` if `doctor` ever renders it, so it doesn't read as freshness

**State:** done — leg 069, `agent/umbrella/045-confirmed-at-label`. Confirmed
`doctor` renders neither `confirmed_at_utc_ms` nor `validated_at_utc_ms`
today; no display to relabel. Folded the constraint into `doctor.rs`'s
module doc comment (`embarch-umbrella/src/doctor.rs`) so the first check
that adds such a display cites decision 57 and uses "Enrolled". No
`open.md` bullet added — that file is treated as full per this task's own
pre-dispatch note.

**Supervisor's pre-dispatch note (leg 069, 2026-09-10).** Read the task's own warning before you
plan: `doctor` renders nothing here today, so **"write the constraint down where the next person to
add such a line will see it" is a legitimate and possibly complete outcome.** Do not manufacture a
rendering in order to have something to relabel. If the honest answer is that the only change is a
recorded constraint plus closing the task, make that change and say so plainly.

**Doc-size reserve in this sub-project is tight:** `embarch-umbrella/open.md` is 4996/5120 B —
**124 bytes left**, filed as `tasks/umbrella/038-compact-umbrella.md` (`blocked`), and it is the
soonest-due entry in the whole size ledger (2026-09-12). Treat it as full: do not add an `open.md`
bullet for this. `embarch-umbrella/decisions/doctor.md` is 11082/12288 (1206 B left, filed as
`tasks/umbrella/048`) and `decisions/bind.md` is 11447/12288 (841 B left, filed as
`tasks/umbrella/009`). If your work pushes any other `embarch-umbrella` doc into the last 10% of
its cap unfiled, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.
**Filed from `inbox/` by leg 066, 2026-09-10**, in the same fold as `umbrella/036`. It parses, its
`Hardware: none` is correct, and its scope is right. Filed immediately rather than left for the
next leg's drain because `core/027`'s entry in `supervisor-log.md` names these two drops as the
**only** thing carrying the user-visible half of decision 57 — a decision whose whole content is
that two screens should say "Enrolled" instead of "Validated", on two screens neither of which has
been changed. A drop in `inbox/` is not in the queue and nothing dispatches from it.

**Read its `## What` honestly before claiming it: `doctor` renders nothing here today**, so this
task may be a no-op that closes by writing the constraint down where the next person to add such a
line will see it. That is a legitimate outcome and is what the "if ever" in the title means.
**Source:** `tasks/core/027`, `embarch-core` decision 57 (`decisions/enrollment.md`)
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`doctor` today contains no occurrence of `confirmed_at_utc_ms` and calls no
`POST /validate` — verified against the code as it stands (`src/doctor.rs`),
and correctly so: `doctor` takes no `hw_lock` and waits on no board, which is
exactly what `/validate` does, so it cannot show a live-check instant either.

That leaves nothing to fix today. But if `doctor` (or any future umbrella
surface) ever renders `confirmed_at_utc_ms` from `/probes/enrolled` or
`/probes/enroll`, it must not label it in any way that implies a live check —
"Validated", "Last validated", "Verified", or similar. `embarch-core` decision
54 records why: that field is enrolment time only, unmoving until someone
re-enrolls, and Core deliberately does not persist a real last-validation
instant beside it (the store that would need to live in is
`embarch-topology`'s, not Core's, and every board enrolled before such a field
existed would have no honest value to show for it).

The honest word both `doctor` and `embarch-ui`'s Topology tab can use for this
same field is **"Enrolled"** (or "Enrolled at"). If a surface wants to say
something about freshness, it has to call `POST /validate` and show that
response's own `validated_at_utc_ms`, not treat `confirmed_at_utc_ms` as a
proxy for it.

## Why now

Residue of a four-task chain (`embarch-topology/tasks/topology/009` →
`embarch-core` decision 50 → `tasks/umbrella/041`, `tasks/ui/020`, both closed
unsatisfiable because `doctor` and the Topology tab don't read the response
`validated_at_utc_ms` actually lives on). `tasks/core/027` closed the design
question by choosing "label, don't add" rather than persisting a second
timestamp, and its decision requires this follow-up be filed rather than
assumed.

## Done when

- [x] No code change is required today — `doctor` shows neither timestamp.
      This task exists so that the first PR that *does* add a
      `confirmed_at_utc_ms`-derived display to `doctor` cites this file and
      decision 57, and labels it "Enrolled", not "Validated".
- [x] If `doctor` grows such a display in this task's own scope, it uses that
      wording and the task closes `done`; otherwise it can close `done` once
      this reasoning is folded into `doctor`'s own doc comments or spec, so a
      future editor doesn't have to rediscover it. Done via a module doc
      comment in `embarch-umbrella/src/doctor.rs`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
