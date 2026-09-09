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

- [x] `crate.md` is out of reserve, or the task says why it cannot be and
      what was deleted or split instead.
- [x] Whichever it was — split or delete — is stated, with the byte numbers
      before and after.

## Resolution (leg 057, 2026-09-09)

**Split, not deletion.** Decision 23 (storage location) moved verbatim, byte for
byte, out of `decisions/crate.md` into a new file `decisions/storage.md`. No
decision was renumbered, retired, or authored — this leg runs in burndown,
which forbids a new numbered decision, and none was needed: a split was
sufficient.

**Byte counts:** `decisions/crate.md` **11,474 -> 7,782 B** (63.3% of the 12,288
cap; `check-doc-size.py --pressure` now reports it `PAID`). New file
`decisions/storage.md`: **4,041 B**, well inside the same 12,288 B cap.

**Inbound links checked and repointed:**
- `scripts/check-duplication.py topology` — clean, no 12+-word overlap.
- Grepped the whole tree for `crate.md#23`, `[decision 23]`, `[decisions/crate.md]`,
  and every `decision 23` occurrence. The only *link* to the file was
  `embarch-topology/decisions.md`'s routing table row; every other hit was a
  bare `decision 23` citation (DOC-CONVENTIONS.md: a decision number addresses
  the sub-project, not a file, so those needed no repointing) or another
  sub-project's own, unrelated decision 23 (`embarch-umbrella/decisions/mcp.md`,
  `embarch-ui`, `embarch-core`, `embarch-dev-bench`, `embarch-study-designer`
  each number their own decisions independently).
- `embarch-topology/decisions.md` updated: the `decisions/crate.md` row's
  decision list dropped `23` (now `1, 2, 3, 4, 6, 8, 13`), and a new row for
  `decisions/storage.md` (`23`) was added.
- `embarch-topology/spec.md`'s citation of "(decision 23)" is a bare number,
  not a file link, so it needed no change and still resolves correctly.

**Deletions, enumerated (nothing summarised):**
- The entire decision 23 entry — heading through its closing paragraph — was
  cut from `decisions/crate.md` (5 paragraphs: the storage-path claim, the
  "why the same directory" paragraph, the "settled from both crates' source"
  paragraph, the "not a new fact for detection to derive" paragraph, and the
  closing "embarch-core's own docs already state its half" paragraph).
- Nothing else in `crate.md` was touched or reworded. No sentence was deleted
  from decisions 1, 2, 3, 4, 6, 8, or 13.
- The full decision-23 text was preserved verbatim in the new
  `decisions/storage.md` — this is a move, not a compaction-by-content cut.

**Human question (`DOC-COMPACTION-PASS.md`), answered honestly:** yes.
`spec.md` already states the one-line declared fact ("Storage is one file
under a machine-wide directory this crate owns... (decision 23)") and points
at the decision for the reasoning; nothing in `spec.md` depended on decision 23
sitting in `crate.md` specifically rather than its own file — the decisions
layer's job is "why", reached by number, not by which of the topic files holds
it. Anyone working on the crate today can still load `spec.md` for the current
shape, and follow the decision number to `decisions/storage.md` (or any other
topic file) for the reasoning behind a specific choice, exactly as before the
split.

**Gate:** `scripts/check-docs.py` — all 10 checks green. `check-ownership.py`
— all changed paths owned by `topology` (3 in `embarch-doc`, 0 in the code
repo — this is a pure doc split, no code change). `check-client-names.py` —
clean against the denylist.

No new decision was authored. No hardware change. No code-repo change: the
`embarch-topology` code worktree has nothing to commit.
