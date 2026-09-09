# Measure the 250,000-row view cap at the next number up, so raising it stops being an extrapolation

**State:** done, 2026-09-09
**Source:** `embarch-ui/open.md` — "it should be made against a measurement at the new number rather than by extrapolating this one"
**Scope:** ui
**Hardware:** none
**Owner:** no

## Supervisor's dispatch note, leg 058 (2026-09-09, burndown)

**Doc-size reserve in `embarch-ui`** — one file is inside the last 10% of its cap, and a second is
53 bytes clear of the line and will re-file itself on the next byte:

- `embarch-ui/spec.md` — 9,461/10,240 B, **779 B left**; filed against `tasks/ui/018-compact-ui-spec.md`
  (state `open`, not blocked), so you owe no new compaction task for it.
- `embarch-ui/decisions/study-designer.md` — 11,007 B against an 11,059 B reserve line: **53 B of
  clearance**, deliberately left there by leg 057 after that file was caught losing an invariant to
  a squeeze. **Do not write to it and do not shave it.** If your measurement genuinely belongs
  there, stop and say so in your report.

`embarch-ui/open.md` is not in reserve, which matters because rewriting its cap bullet is one of
this unit's Done-when items. **That is where the measured numbers go.**

**This leg runs in burndown mode: do not author a new numbered decision.** The Done-when's "the cap
is either changed or explicitly kept, with the number cited" is satisfied by recording the
measurement and the resulting cap in `open.md` and in the `changelog.d/` fragment, marked
`[measured 2026-09-09, <build>]` per `DOC-CONVENTIONS.md`. **Keeping the cap where it is, with the
measurement as the stated reason, is a complete and legitimate outcome** — the task says so
explicitly. If you conclude the outcome needs its own numbered decision in
`decisions/trace-transfer.md`, stop and say so in your report rather than writing one.

If your work pushes a file into reserve or leaves one there unfiled, file
`tasks/ui/<next free NNN>-compact-ui.md` in the same commit (`tasks/README.md` has the shape, and
the path is `tasks/ui/`, never `tasks/doc/`).

## What

`embarch-ui/open.md` says the 250,000-row cap "is now the only term left, and the reason it was set
is gone". The cap is `src/trace.rs:120`. The instrument already exists at `src/trace.rs:3748`
(`summarise_a_capture_from_disk`, `EMBARCH_VIEW_CSV`) but needs a real file on disk.

Add a synthesiser plus an `#[ignore]`d measurement test that builds captures of the committed
fixture's shape at 250k / 500k / 1M rows and prints decode time, resident view size and `/bins`
payload size at a reference grid width. Put the numbers in `open.md` (or a decision), then either
raise the cap with the measurement beside it or leave it where it is **with the measurement as the
reason**. Both outcomes close this; an unstated one does not.

## Why now

`open.md` states the decision is blocked only on a measurement at the new number, and
`decisions/trace-transfer.md` 18 already removed the transfer half of the original justification.
Nothing else about it is open.

## Done when

- [x] A synthesiser and an `#[ignore]`d measurement test exist and run from a documented one-line
      invocation, needing no file on disk. `src/trace.rs`'s `scratch_view::synth_capture` builds a
      CSV of the committed fixture's kind proportions entirely in a `String`; `scratch_view::
      measure_the_row_cap_at_scale` drives it at 250k/500k/1M rows, run with
      `cargo test --release measure_the_row_cap_at_scale -- --ignored --nocapture`.
- [x] Decode time and both payload sizes are recorded at three row counts, marked
      `[measured <date>, <build>]` per `../../DOC-CONVENTIONS.md`. In `open.md`.
- [x] The cap is either changed or explicitly kept, with the number cited. Kept at 250,000 —
      decode time and resident view JSON both grow somewhat worse than linearly with row count
      (257 ms/4.48 MB at 250k to 1.69 s/18.1 MB at 1M), which is the cost decision 18 said raising
      the cap would come down to; the `/bins` payload itself stays small at all three points, so
      the payload half of the original justification is confirmed still fixed. No new numbered
      decision was authored (this leg runs in burndown mode, dispatch note); keeping the cap with
      the measurement as the stated reason is the outcome the task names as complete.
- [x] `open.md`'s bullet is rewritten to what is now unknown: whether the decode-time cost is
      acceptable against the (currently unmeasured) `/study/{id}/streams` request-path budget.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`/`test`/`clippy
      --all-targets -- -D warnings` clean in `embarch-ui`; `check-docs.py` 10/10 green in
      `embarch-doc`; `check-client-names.py` and `check-ownership.py` (both repos) clean.
- [x] `spec.md`/`decisions.md`/`open.md` updated (only `open.md` needed a change; `spec.md`
      already states 250,000 rows and is unaffected since the cap didn't move, and it is itself in
      reserve per this leg's dispatch note, so no edit was made there), `changelog.d/` fragment
      dropped (`changelog.d/ui-row-cap-measured.decided.md`). No suite-level fact was made false,
      so no `status.d/` fragment. `open.md`'s edit pushed it into reserve (3,630 B → 4,191 B
      against a 3,920 B reserve line), filed as `tasks/ui/021-compact-ui.md` in this commit.
