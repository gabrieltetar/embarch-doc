# 074 — `embarch-api/decisions/studies.md` is in reserve after `suite/015`'s retirement tombstone

**State:** claimed — leg 093
**Source:** `suite/015` (leg 093, 2026-09-11) retired the three fixed-channel study-data aliases and
recorded the retirement inside decision 39, where the "kept for one release" grant was written.
That tombstone put the file at 11,784/12,288 B — 95.9%, 504 B left. `DOC-COMPACTION.md` §2.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/studies.md
**Size debt due:** 2026-10-11
**In flux:** no. The thing that made this file churn was the study-read surface settling, and
`suite/015` is the last move in that sequence: the three aliases are gone, `study_stream_data` and
`list_study_streams` are the whole read path, and there is no deferred follow-on pointing back here.
Decision 40's reflash rules and decision 39's manifest half have been stable since they landed.
**Must not delete:**

- **Decision 39's manifest-rides-the-build argument**, including *why* it is derived from the
  firmware path rather than passed as a parameter (a dozen flash call sites, each a place to
  forget), and the sentence naming the inherited artifact-transfer gap. That gap is tracked in
  `embarch-api/open.md` and the cross-reference is the only thing connecting the two.
- **The `truncated` bullet.** It is the reason `list_study_streams` exists at all and the reason
  the aliases were retired; a compaction that shortens it removes the justification for the
  retirement recorded three paragraphs above it.
- **The retirement tombstone itself**, and specifically the sentence saying the "one release" grant
  had no closing edge because `v0.1.0` is still the only release. That is the fact that explains
  why a dated expiry sat unexpired for a month, and it is the generalizable lesson.
- **Decision 40's "this crate will not move an engineer's tree" rule**, both the argv-inspection
  mechanism and its deliberate over-rejection rationale. `embarch-api/spec.md` §2 restates the
  first sentence on purpose; the argument lives only here.
- **The verification asymmetry in decision 40** — bench flashed-then-read-back, DUT
  verified-then-flashed — which is control flow derived from what is physically observable, and
  is re-derived wrongly if the reasoning is cut.

## Candidate shape

The file's natural seam is **decision 39 (what a study reads back) vs decision 40 (what a study
flashes first)**. A verbatim split into `decisions/study-reads.md` and `decisions/study-reflash.md`
restates nothing and would take both halves well clear of the cap — prefer that to a shortening
pass, per `DOC-BUDGET.md`'s split-first rule.

## Doc-size reserve in your sub-project, at dispatch

`embarch-api` has **four** files in reserve. Only the first is yours to spend against here; the other
three are parked behind their own blocked tasks and **you must not push any of them deeper**:

- `embarch-api/decisions/studies.md` — 11,784/12,288 B, **504 B left** (this task's target)
- `embarch-api/decisions/client-crate.md` — 11,639/12,288 B, 649 B left (`tasks/api/073`, blocked)
- `embarch-api/decisions/surface.md` — 11,258/12,288 B, 1,030 B left (`tasks/api/069`, blocked)
- `embarch-api/interfaces/config.md` — 11,193/12,288 B, 1,095 B left (`tasks/api/071`, blocked)

**This is a docs-only unit. Do not move text into another file in that list** — a compaction that
clears one file's reserve by pushing another into its own is not a compaction, and two legs this week
caught themselves doing exactly that. The split named above lands both halves in *new* files, which
is why it is the recommended shape. If your work spends reserve anywhere else in `embarch-api`, file
`tasks/api/<next NNN>-compact-api.md` in the same commit.

## Done when

- [ ] `embarch-api/decisions/studies.md` is out of its reserve band.
- [ ] Every "Must not delete" item above is still findable, by a reader who does not know it moved.
- [ ] Decision numbers are unchanged; `check-decision-refs.py` and the full doc gate are green.
