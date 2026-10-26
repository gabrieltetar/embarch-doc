# 074 — `embarch-ui/open.md` is still in reserve after `ui/071`

**State:** claimed by agent/ui/074-compact-ui-open, 2026-10-26 00:38
**Source:** `scripts/check-doc-size.py --pressure`, filed the moment `tasks/ui/071` closes (`done`
tasks carry no debt forward, so its `Compacts:` line stops counting)
**Scope:** ui
**Hardware:** none
**Owner:** no
**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-10-05
**In flux:** no — for the pass this task now asks for. Unparked by the supervisor 2026-10-26 (overdue
since 2026-10-05, the ledger's oldest payable entry; `api/113` was unparked the same way). The file
is 5,117 / 5,120 B, **3 B left**: the owner's 2026-10-25 round added two bullets, so the next `ui`
unit that needs a line here cannot write it. `DOC-BUDGET.md` names a role-capped 5 KB `open.md` as
the case with no seam, so the remedy is not a split but **deleting answered questions** (a bullet
whose answer is already recorded in a decision, `spec.md` or `history/`), and moving a settled half
out to the decision that owns it before trimming the bullet to its open remainder — the `ui/071`
pattern. No live bullet is tightened. The original park is kept below as "Why it was parked".
**Reserve, for the worker:** `embarch-ui/open.md` 3 B left (this task); `embarch-ui/spec.md` 724 B
left, parked on `tasks/ui/078` — leave `spec.md` alone unless a settled fact has to land there, and
then check its size first.

## What

`open.md` is **4,867 / 5,120 B (95.1%), 253 B left** — under its cap (`tasks/ui/071` brought it
down from 6,630 B) but still inside the reserve band (floor `max(1,200, 10%)` from the top =
3,920 B). This is not a compaction request: 253 B is enough headroom for one more open item's
trigger note, not zero. It exists only so the file is not *unfiled* reserve, which is what
`check-doc-size.py` actually fails the gate on.

## Why now

`tasks/ui/071` explained why it stopped at 4,867 B rather than squeezing to 3,920 B: every
remaining bullet is a distinct open question with its own trigger or cross-repo pointer, and the
only two bullets that mixed settled evidence with a still-open remainder were already split (the
settled halves moved to `decisions/trace-rows.md` decision 21 and `decisions/time-chart.md`
decision 34). Getting further out of reserve from here means one of:

- a bullet's trigger fires (hardware session, bridge attachment) and the bullet is retired or
  shrinks to its result, same pattern as `ui/071`'s two moves;
- another bullet turns out to mix settled-with-open and can be split the same way;
- `embarch-ui`'s decisions get their own compaction pass and a bullet's cross-repo pointer becomes
  citable more tersely.

None of those is available yet, which is why this parks rather than dispatches work.

## Why it was parked (In flux: yes, superseded 2026-10-26)

`open.md` gained two entries in `ui/070` and had two more retired/condensed in `ui/071` inside two
weeks — it is one of this sub-project's most actively edited files, because every hardware
session, every bench run and every new Core endpoint either adds a trigger here or fires one that
was already waiting. A squeeze attempted today would very likely be re-opened by next week's leg.
**Blocked** until one of the three conditions above actually happens — check `open.md`'s size
against the cap the next time any bullet in it changes for an unrelated reason, and act only if
that change created real room or a new split seam, never by shortening a trigger to make space.

## Done when

- [ ] `open.md` is out of reserve (at or under 3,920 B), or a fresh reason is filed here for why
      not, dated and re-derived against the file's size at that time.
- [ ] Whatever unparked this (a fired trigger, a new split seam, a sub-project compaction pass) is
      named in the report, not just asserted.
- [ ] No open question closed by attrition to get there.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.
