# 079 — `embarch-umbrella/decisions/install.md` is in reserve

**State:** blocked — see `**In flux:**` below.
**Source:** scripts/check-doc-size.py --pressure, run by `umbrella/078`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/decisions/install.md
**In flux:** yes — the sole file on the `Compacts:` line is in flux (per-file answer, and here
there is only one file). See the "In flux" section for what is still moving.
**Unparks when:** decision 28's Windows-side verification debt closes — a real Windows machine
confirming the registry `PATH` write and a new shell picking it up — since that debt, once paid,
adds a sentence to this file the way every other closed hardware debt in it already has (decision 3,
21). Landing that is reason to re-read this field rather than to unpark on sight.

**Size debt due:** 2026-10-17

**Reserve:** `install.md` was steady at 11,009 B (89.6%, out of reserve) until `umbrella/078`
(2026-09-17) added decision 54 — weighing a user-level service against decision 3 and recording why
it stays rejected — the only correct home for that decision per `decisions.md`'s own routing
(decisions 3, 4, 5, 14, 21, 25, 28 are this file's mission, and decision 54 is directly about
decision 3). That pushed the file to **12,071 B (98.2% of the 12,288 B role cap), 217 B left.** The
entry was written at the decision-entry target size already (DOC-COMPACTION.md §5, ~1,050 B against
the 1,200 B ceiling); there was no slack to shave without weakening the reversal condition or the
platform-split reasoning, and the task that added it was explicit that squeezing a decision to fit
is the wrong move when the room genuinely is not there (this file's own `tasks/README.md` guidance).

Not filed against `009`, which already carries `decisions/bind.md` under its own, unrelated
check-17 history — mixing the two would put one compaction task in the position of naming a pass
across two unrelated reserve episodes in two different files.

## What

Bring `install.md` back under 90% (11,059 B) without deleting a live decision or its reversal
condition — read for duplication against `spec.md` first
(`scripts/check-duplication.py embarch-umbrella`), then look for wording to shorten across the older
entries (3, 7's cross-reference weight, 28's verification narrative) before considering a split.
Decisions 3, 4, 5, 14, 21, 25, 28 and 54 are one mission (setup/install/service) and a split here
would need a real seam, not a size-driven cut. Run `scripts/check-doc-size.py --pressure` before and
after and record the new percentage here.

## Why now

Not yet blocking anything — 217 B of headroom remains. Filed now per this repo's own reserve
convention (`DOC-COMPACTION.md`, `check-doc-size.py`'s "RESERVE"/"UNFILED" band) so the debt survives
past this leg rather than living only in a supervisor's report.

## In flux

**Yes.** Decision 28 (the canonical-location install and real `PATH` write) is explicitly unverified
end to end — no Windows linker in this sandbox, checked only by extracting the registry code into a
throwaway crate and type-checking it against the target. Whenever that verification runs for real, it
lands in this file, next to decision 28's own paragraph, the way decision 3's WSL2 misreport fix and
decision 21's build history already do. That is new prose in this exact file, not a different one.

## Done when

- [ ] `install.md` back under 90% of its 12,288 B cap, by shortening or moving, not by deleting a
      live decision, its reversal condition, or a rejected-alternative clause.
- [ ] `scripts/check-duplication.py embarch-umbrella` checked before any content is moved elsewhere.
- [ ] No decision's number, claim, or reversal condition disappears — retire per `DOC-CONVENTIONS.md`
      if one stops describing anything true; never delete outright.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
