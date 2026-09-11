# 024 — Compact embarch-topology/spec.md

**State:** done — leg 081, 2026-09-11
**Size debt due:** 2026-09-24
**Source:** `scripts/check-doc-size.py` — 89.4% of cap after `tasks/topology/011`'s edit
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/spec.md` was at 9151/10240 B when this task was filed.
`tasks/topology/025` added a new section (caller granularity contract,
decision 29) and paid its own compaction debt in the same commit per
`DOC-COMPACTION.md` §2 — the file is now 9195/10240 B (89.8%, just under the
90% floor) — but it is still inside reserve and this task stays open: any
further growth from `004`/`020` lands back over the floor with no slack
left. Compact it per `DOC-COMPACTION.md` §3/§7 — a pass over its own prose,
not a new section — down to comfortably below the 90% floor.

**Compacts:** `embarch-topology/spec.md`

**In flux:** no, as of 2026-09-11 — one file (`embarch-topology/spec.md`), and the flux is
spent. This field read `yes` on the grounds that `tasks/topology/011` had just added the
decision-28 sentence and that `tasks/topology/004` and `tasks/topology/020` were "open against
the same file's surface". **All four of those are now `done`** — `011`, `004` and `025` landed
2026-09-08 through 2026-09-10, `020` at leg 050 — and `topology/024` is the only task left in
this scope, so nothing is moving in `spec.md` for a compaction pass to race. Unparked by leg 080
after `topology/027`'s reviewer found this `State:` line still asserting `020` as live work three
days after it closed; the park's reason was stale, not wrong when written. The **Must not
delete** list below is unchanged and still binds — it is what a settled file still owes a
compactor.

**Must not delete:**
- The decision-28 sentence added to the "two things built from it" list
  (CLI mutation refusal / local-bootstrap).
- The process/call-site code block (`Core, mid-flash/reset/run_study: ...`).
- The "What a caller may assume across calls" section and its decision-29
  pointer (added by `tasks/topology/025`).
- Anything `open.md` currently points at by section name.

## Why now

`check-doc-size.py` names a file in reserve with no debt filed as a gate
failure (`protocol.md` §5 step 5); this records the debt rather than leaving
it unfiled.

## Done when

- [x] `embarch-topology/spec.md` is below 90% of its cap. 9195 B -> 8726 B
      (85.2%, 1,514 B of headroom) — a prose-only pass, no section added or
      removed, per `DOC-COMPACTION-PASS.md`.
- [x] Nothing on the **Must not delete** list is gone or now reads as false.
      The decision-28 sentence, the `Core, mid-flash/reset/run_study: ...`
      call-site block, and the whole "What a caller may assume across calls"
      section (with its decision-29 pointer) sit inside two fenced/protected
      spans that were not touched — verified by re-reading the diff. The one
      section-name reference from outside the file
      (`decisions/scope.md:37` → `spec.md, "What a caller may assume across
      calls"`) still resolves; that header text is unchanged.
- [x] Gate green — `check-docs.py` (11/11), `check-ownership.py --scope
      topology` and `--code-repo`, `check-client-names.py --repo` (both
      worktrees), and in `embarch-topology`: `cargo build`/`test`/`clippy
      --all-targets -- -D warnings`, all clean; the code worktree carries no
      diff.

## Still in reserve

Compacting this pass did not clear the cap's reserve band by much margin —
8726/10240 B is 85.2%, comfortably under the 90% floor with ~1.5 KB of
headroom, but this is the file's *first* compaction pass and it stayed a
straight prose tightening (no hot/cold split, no content moved out) per the
task's own scope. Any future growth of comparable size to `topology/011`'s
or `topology/025`'s additions will use a meaningful fraction of that headroom
again. Not filing a further debt task now — `check-doc-size.py` passes and
nothing is in reserve — but a reviewer of the next `spec.md`-touching task
should re-check the percentage before assuming slack.
