# 016 — `decisions/doctor.md` and `spec.md` are in reserve

**State:** blocked
**Source:** scripts/check-doc-size.py --pressure, after `umbrella/011`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/decisions/doctor.md, embarch-umbrella/spec.md
**In flux:** yes — `tasks/umbrella/007`, `012`, `013` and `015` are open and every one of them rewrites a row of `spec.md`'s doctor table or an entry in `decisions/doctor.md`
**Must not delete:** decision 22's three unbuilt checks and the sentence saying they are unbuilt; decision 23's original claim *and* the amendment saying which half of it decision 40 replaced — a retired-or-amended entry that loses what it used to say stops being a tombstone; decision 31's note that check 14 runs under the WSL user's environment rather than the service account's, which is still open; `spec.md`'s twenty-row doctor table and which rows are designed-and-unbuilt.

## What

`decisions/doctor.md` is **11,918 / 12,288 B — 370 B left**, and `spec.md` is
**9,286 / 10,240 B**. `umbrella/011` put decision 40 into the first and rewrote
check 10's row in the second; both were already close, and the new decision
would not fit under the reserve line at any length that still said why the
route was chosen.

Run `scripts/check-duplication.py embarch-umbrella` first, as `009` says: the
last pass's biggest find was `decisions/doctor.md` re-arguing build status that
`spec.md`'s table owns, and decisions 18 and 31 both still carry build-status
prose.

**`009` is the sibling and is not this task.** It holds the *pass* over
`spec.md` and `open.md` and is blocked on the same queue; its reserve item for
`spec.md` was paid on 2026-09-05 and `spec.md` went back over the line here.
`open.md` is not in this item — `umbrella/011` took it 4,596 → 4,289 B.

## Why now

Nothing can be added to `decisions/doctor.md` at 370 B of headroom, and three
open umbrella tasks are queued against exactly that file. The next worker that
needs a decision entry there is blocked by arithmetic rather than by design.

## Why blocked

`In flux: yes`, for the reason `009` gives and the same queue. **Unparks with
`009`** — one pass over the sub-project, not two.

## Done when

- [ ] Both files out of reserve.
- [ ] Every `Must not delete:` item still findable, by search, in the compacted text.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
