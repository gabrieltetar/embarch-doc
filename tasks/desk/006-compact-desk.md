# 006 — four `embarch-desk` docs are in reserve after decisions 76 and 77

**State:** done — all four files clear, by verbatim splits only
**Source:** decision 76 (the hand shows this week's tiles) crossed the reserve line on `cockpit.md`; decision 77 (each session works on its own desk, EMB-94) crossed it on `decisions/desks.md`, `interfaces.md` and `spec.md`; `DOC-COMPACTION.md` §2
**Scope:** desk
**Hardware:** none
**Owner:** no

**Compacts:** embarch-desk/decisions/cockpit.md, embarch-desk/decisions/desks.md, embarch-desk/interfaces.md, embarch-desk/spec.md
**Size debt due:** 2026-11-23
**In flux:** per file — embarch-desk/decisions/desks.md, embarch-desk/interfaces.md and embarch-desk/spec.md: yes, rewritten for decision 77 on 2026-11-09 and not landed yet, so leave them until they land. embarch-desk/decisions/cockpit.md: no — 1–13, 57, 58, 60, 61 and 65 have held since October; 76 is new and stays whole.
**Must not delete:** decisions 76 and 77 in full, rejected alternatives included; 57's owner quote and its rejected fanned hand and drag piles; 61's three writers of `hours_override` and the stuck-tile failure it fixed; 37's one-bench reason; the `x-embarch-session` / `x-embarch-cwd` headers and `desks.json` in `interfaces.md`.

## What

`cockpit.md` 12,061/12,288 B (98.2%), `decisions/desks.md` 12,169/12,288 B (99.0%), `interfaces.md` 14,426/15,360 B (93.9%), `spec.md` 9,219/10,240 B (90.0%).

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it; this is that filing.

## 2026-11-09 dispatch note

Decision 77 has landed since this was filed: `embarch-desk` `0c44f9d` and `embarch-doc` `5b8d8362` are both on `origin/main`. The `In flux:` field is left as written, and it does not stop this unit, because `DOC-BUDGET.md` makes a split the default remedy and a verbatim split restates nothing. So:

- **`decisions/desks.md`, `interfaces.md`, `spec.md`: split only.** Move whole decisions or sections verbatim to a topic file (`decisions/<topic>.md`, `spec/<topic>.md`, or an `interfaces/` file if the repo already uses one) and leave a pointer. Reword nothing in them; decision 77 is hours old.
- **`decisions/cockpit.md`: split first; squeeze only where there is no seam**, and then per `DOC-COMPACTION-PASS.md` (every deleted hunk quoted in the commit message).
- Check a seam's inbound links before cutting, and run `scripts/check-duplication.py desk` first.
- Fourteen `embarch-desk` issues are waiting in Fleet Ready. Leave each file with room, not just under its line.

## Done when

- [x] All four files are clear of their reserve line.
- [x] Every `Must not delete:` item is still readable.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
