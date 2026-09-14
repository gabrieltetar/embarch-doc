# 050 — Compact `embarch-ui/open.md`

**State:** claimed — leg 111, 2026-09-13, branch `agent/ui/050-compact-ui-open-md`.
**Source:** `scripts/check-doc-size.py`, run as part of `tasks/suite/018`'s gate. That unit added
one bullet to `embarch-ui/open.md` pointing at [suite decision 4](../../suite/decisions.md), and
the file crossed into reserve: **4,341/5,120 B, 779 B left, 84.8%.** Filed in the same commit per
`../../embarch-fleet/protocol.md` §5 and `tasks/README.md`.
**Scope:** ui
**Hardware:** none — reading and rewriting one doc file.
**Owner:** no

**Compacts:** embarch-ui/open.md
**Size debt due:** 2026-09-27
**In flux:** no. Every bullet in this file names either a settled decision with a stated trigger,
or a measurement that has already been taken. Nothing in it is mid-change: the newest bullet
*closes* a question rather than opening one, and the two oldest have explicit triggers naming an
event outside this repo.
**Must not delete:**

- **The archive bullet's two-part shape** — that `assemble-suite.yml` ships three binaries and not
  this one, that the documentation half is closed, and that admitting `embarch-ui` is
  `embarch-umbrella` decision 14's call and the suite's, not this repo's. **Suite decision 4 now
  leans on this bullet** as half of its argument, so shortening it into "the UI is not shipped"
  removes the premise of a decision in another file.
- **The 250,000-row cap's measurement table and the sentence naming what is still unmeasured** —
  the three awaited Core calls `decode_trace` makes before `parse` runs. The numbers are the reason
  the cap is where it is, and the unmeasured half is the reason 1.32 s is not the whole cost.
- **The stale-prefix bullet's hardware debt**: 18 records from a real capture, buffered in the
  bridge past Core's open-time purge, never replayed; `STALE_PREFIX_MAX_ROWS` (512) is an
  assumption about a FIFO nobody has measured. That is a debt against a board and it must survive.

## What

`embarch-ui/open.md` is in reserve — note the reserve here is the **`RESERVE_FLOOR` of 1,200 B**,
not 10% of the cap, because 10% of 5,120 is only 512. That is why an 84.8% file is flagged and why
this one went from clear to in-reserve on a single 468 B bullet: it was 47 B below the line before
`suite/018` touched it.

Run a compaction pass per `DOC-COMPACTION-PASS.md`. The cold half here is mostly **prose length,
not content** — this file has no superseded reasoning to cut, so a split is the wrong remedy and
squeezing is the right one. Every bullet is a live question or a live debt.

## Why now

Reserve at 779 B left means the next unit that records anything in this file meets the wall
mid-flight — and `embarch-ui` has an open question queue that lands in exactly this file. The
`DOC-BUDGET.md` split-first rule does not apply: there is no seam, because there is only one kind
of thing in here.

## Done when

- [ ] A compaction pass run per `DOC-COMPACTION-PASS.md`, keeping every question, every trigger and
      every measurement, and cutting length.
- [ ] The three Must-not-delete items above survive verbatim in substance.
- [ ] `check-doc-size.py` green for `embarch-ui/open.md` with room to spare, not just under the
      reserve floor.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Dispatch note — leg 111, 2026-09-13

**This is a compaction unit, and it is judged on a question no script answers.** When you are
done, answer `DOC-COMPACTION-PASS.md`'s human question **in your own words, in your closing
section**: *can `spec.md` alone answer what someone needs to work on this component today?* The
supervisor copies that answer into the log entry, and a pass that merely got the byte count down
without answering it has not finished.

**`In flux:` is `no` for `embarch-ui/open.md`, per-file, and that is why this is dispatchable at
all.** Confirmed today, unchanged. Sizes re-measured: **`embarch-ui/open.md` 4,341 / 5,120 B, 779 B
left (84.8%)**, and the reserve floor here is the flat `RESERVE_FLOOR` of 1,200 B rather than 10%
of the cap — which is why an 84.8% file is flagged. **"Room to spare" means clear of 3,920 B**, not
clear of 5,120.

**The task is explicit that a split is the wrong remedy here and squeezing is the right one.**
Take that seriously: there is one kind of thing in this file, so there is no seam, and
`DOC-BUDGET.md`'s split-first rule does not apply. Cut *length*, not questions, triggers or
measurements. The three `Must not delete:` items above survive in substance — in particular the
archive bullet, because **suite decision 4 now leans on it** and shortening it to "the UI is not
shipped" would delete the premise of a decision that lives in another file.

Nothing else in `embarch-ui` is in reserve. **If your pass somehow pushes another `embarch-ui` doc
into its reserve band**, file `tasks/ui/052-compact-ui.md` in the same commit — **`tasks/ui/`, your
own scope**, never `tasks/doc/`, which `check-ownership.py` refuses to every worker.

**One repo, one branch, one task.** This is a doc-only unit, so most of the work is in
`embarch-doc`; both worktrees are on `agent/ui/050-compact-ui-open-md`. `embarch-ui`'s worktree has
`embarch-study-designer`, `embarch-api` **and `embarch-topology`** symlinked beside it — the last
one is the trap, since it is reached through `embarch-api/crates/embarch-core-client` and not
through `embarch-ui`'s own manifest — so `cargo build` resolves if you need it.
