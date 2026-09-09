# 021 — `embarch-topology/decisions/crate.md` is in reserve

**State:** claimed — leg 057, 2026-09-09, `agent/topology/021-compact-topology`
**Source:** `scripts/check-doc-size.py`'s reserve floor, surfaced by `tasks/topology/020`
**Scope:** topology
**Hardware:** none
**Owner:** no
**Compacts:** embarch-topology/decisions/crate.md
**Size debt due:** 2026-10-08

## What

`crate.md` is **11,290 / 12,288 B (91.9%), 998 B left**. It crossed on
`topology/020`'s two qualification paragraphs on decisions 4 and 8 (roughly
1,280 B added), which were necessary — a caller's uniqueness claim needed
separating from what the crate itself guarantees — not padding.

**Prefer a split.** [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split
restates nothing, so it costs no argument, and a file warned this far out
still has a seam to cut. Decision 23 (storage location) is the file's longest
single entry and reads as a candidate seam — its own reasoning is
self-contained and only cited from `spec.md`, not built on by the decisions
around it — but check its inbound links first
(`scripts/check-duplication.py topology` and a grep for `decisions/crate.md#23`
or similar anchors) before moving it anywhere.

## Why now

The debt is real once a file is within one amendment of its cap, and
recording it is the whole mechanism: an unfiled file in reserve is what
`check-doc-size.py` fails on, not the reserve itself.

## Doc-size reserve in `embarch-topology`, at dispatch (leg 057, 2026-09-09)

The numbers above are stale — re-measured at dispatch, `decisions/crate.md` is **11,474 / 12,288 B,
814 B left** (93.4%), not 11,290. `decisions/enrollment.md` is **11,346 / 12,288 B, 942 B left**
(92.3%), filed under `tasks/topology/019-compact-topology.md` (open) — do not pay it here, but do
not push it further either. Nothing else in `embarch-topology` is in reserve. If this unit leaves a
file in reserve with nothing filed, file `tasks/topology/<NNN>-compact-topology.md` in the same
commit — your own scope's directory, never `tasks/doc/`.

**This leg runs in burndown, which forbids authoring a new numbered decision.** A split renumbers
nothing and is fine; writing a *new* decision is not. If the pass turns out to need one, stop and
say so.

**If you split, repoint every inbound link by hand and verify it.** `check-links.py` passes a
`decision N` link whose target file no longer defines N, and `check-decision-refs.py` resolves
numbers against the sub-project rather than the file, so a split strands links silently. That gap is
`tasks/doc/022` / `tasks/doc/027`, and `topology/017` hit it one leg ago on this same repo.

## In flux: no

The qualifications `topology/020` added to decisions 4 and 8 are complete
statements, not placeholders — they name `api/038` as closed and
`embarch-umbrella/src/token.rs` as still open, and neither will need
rewording when `umbrella/036` lands (it closes the third mirror; it does not
change what this file already says about it).

## Done when

- [ ] `crate.md` is out of reserve, or the task says why it cannot be and
      what was deleted or split instead.
- [ ] Whichever it was — split or delete — is stated, with the byte numbers
      before and after.
