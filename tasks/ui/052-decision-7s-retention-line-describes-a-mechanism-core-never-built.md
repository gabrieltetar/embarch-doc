# 052 — `embarch-ui` decision 7's retention line describes a mechanism Core never built

**State:** claimed by agent/ui/052-decision-7-retention-line, 2026-09-13 23:45
**Source:** an `inbox/` drop written by `core/058`'s worker mid-sweep, 2026-09-13, filed here by leg
112. It found this while checking `embarch-core/src/main.rs`'s citation of `embarch-ui` decision 7
and **could not fix it — `embarch-ui` is not that worker's scope.** The drop is reproduced in full
below; it is the worker's own text, not a restatement.
**Scope:** ui
**Hardware:** none — doc text only. No board, no probe, no live Core, no deploy.
**Owner:** no

## What

`embarch-ui/decisions/debug-tab.md` decision 7 still reads:

> Retention is a size-capped rotating logfile rather than a time-based policy — bounded disk, no
> cleanup pass.

That describes **Core's** logfile, which the Debug tab reads via `/logs/recent` — decision 7's own
text says *"`embarch-ui` never reads Core's logfile directly… The UI is handed the data, never the
file."* But `embarch-core/decisions/logging.md` decision 16, and `embarch-core/src/main.rs`'s
`build_log_file_writer`, say Core's log is a **daily-rolling** file with `max_log_files(7)` —
**date-based, not size-capped.**

**No later paragraph, blockquote or "(corrected …)" note anywhere in `debug-tab.md` walks it back.**
The reporting worker grepped the whole file for `corrected`, `size-capped`, `daily-rolling` and
`rotating logfile`; the size-capped sentence is the only hit and it stands unqualified.

## Why it is filed rather than already fixed

**Two `embarch-core` source comments assumed the correction had happened** — `src/main.rs`'s
`build_log_file_writer` and `src/logs.rs`'s module doc, the latter stating outright *"That decision
is corrected in place."* **It is not, and was not.** `core/058` fixed both `embarch-core` sides to
stop asserting a correction that does not exist, which is the half it owned. This task is the other
half.

That is the shape worth noticing: **a decision the world moved past, still asserted as current by a
citation in another repo — and the citation was not wrong about the number, it was wrong about
whether the decision had been amended.** The sweep series (`core/054`, `core/056`, `umbrella/065`,
`umbrella/066`, `study-designer/044`–`047`, `ui/049`, `core/058`) keeps producing this class, and
nothing gates it: `check-decision-refs.py` resolves numbers only inside `*.md`, and a citation to a
real decision whose *body* has gone stale resolves perfectly.

## What the fix is not

**Do not silently rewrite decision 7 to say "daily-rolling" as though it always had.** A decision is
a record of what was decided, and this one recorded a retention policy that shipped differently. The
suite's own pattern for a superseded claim is a dated parenthetical or a blockquote
(`DOC-CONVENTIONS.md`), and `embarch-decision-reversals.md` is where a genuine reversal goes. Which
of those applies is the judgement this task exists to make — decide it explicitly and say why in the
commit message.

## Done when

- [ ] `embarch-ui/decisions/debug-tab.md` decision 7 either describes the actual daily-rolling
      mechanism Core built, or is explicitly marked as describing an earlier design that shipped
      differently — one or the other, chosen deliberately and justified in the commit message.
- [ ] Checked whether any other `embarch-ui` file (`spec.md`, source comments, shipped strings)
      repeats the "size-capped" claim and needs the same fix.
- [ ] `embarch-core`'s two comments re-read to confirm they now agree with whatever this task lands —
      `core/058` corrected them to stop claiming a correction exists; if this task *makes* one exist,
      they may want updating again. **That is a finding for `inbox/`, not an edit**: `embarch-core`
      is not this task's scope.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
