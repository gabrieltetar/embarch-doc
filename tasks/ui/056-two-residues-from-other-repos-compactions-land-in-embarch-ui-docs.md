# 056 — two compaction residues from other sub-projects land in `embarch-ui`'s docs

**State:** done — agent/ui/056-two-compaction-residues, 2026-09-16.
**Source:** two `inbox/` drops, folded into one task by leg 120 because they are the same scope and
would otherwise be one dispatchable slot apiece: `ui-decision-25-history-citation-dangles.md` (the
`embarch-reviewer` on `ui/055`) and `ui-debug-tab-diff-new-lines-fallback.md` (from
`embarch-core` task `065`, itself resolving an `embarch-reviewer` finding on `core/064`).
**Scope:** ui
**Hardware:** none — doc prose only. No board, no probe, no live Core, no UI launched.
**Owner:** no

They are folded, not merged: they are two independent defects in two files and each has its own
"done when". Fix both in one branch; do not let one justify skipping the other.

## Part A — `history/ui.md:38` cites a number `decision 25` no longer states

`ui/055` squeezed `embarch-ui/decisions/shell.md`#25 from 4,307 B to 3,758 B (merge `eb3e0e5`) and
cut four hunks justified as *"cold ... and cited nowhere else in the repo"*. One of the four:

> : 22 vertices plus a 4-vertex counter for the E, 15 plus a 4-vertex counter for the A, 657 B inline

But `history/ui.md:38`, untouched by that unit, reads:

> Decision 25's E vertex count was 16 (a non-union trace); corrected to 22, and a dead
> `.sd-param-value` opt-out removed.

That line's entire content is a pointer to the number the unit deleted. After `eb3e0e5`,
`decisions/shell.md` states no vertex count for the E at all. So the unit's own stated safety test
was false for that hunk — this is a residue, not a judgement call within the test.

**Severity is low and that matters for the fix.** `history/ui.md` is a historical changelog entry
describing a past correction; it asserts no live invariant and nothing downstream depends on decision
25 continuing to state "22". Do **not** revert `eb3e0e5`. Two acceptable shapes, pick one and say
why: make the history entry self-contained (carry the number in it, stop pointing at
`decisions/shell.md` for a figure it no longer has), or return the count somewhere citable.

**The cheaper one is probably the history entry.** Decision 25 is at 3,758 B with 338 B of margin and
was just paid down; spending that margin to satisfy a changelog line is the wrong direction.

## Part B — `debug-tab.md`#13 omits `diff_new_lines`'s trailing-partial-line fallback

`embarch-core/decisions/logging.md` decision 44 (retired, but this sentence was true of live code and
was cut with it) used to say:

> `read_recent`/`tail_lines` are unchanged and still return a trailing partial as a line — correct for
> "show me the tail as it stands now," and `embarch-ui`'s `diff_new_lines` already has a documented
> fallback for a window whose last entry changes under it.

`embarch-core/interfaces/logs.md`'s `/logs/recent` row now restates the **Core-side** half. The
`embarch-ui` half — that `diff_new_lines` tolerates a window whose last entry mutates, and how — is
stated nowhere in the doc repo. `embarch-ui/decisions/debug-tab.md`#13 documents the poll/diff
consumer of `/logs/recent` in detail, including an anchor defect, and never mentions this.

**Verify against the code, not against the quote.** The decision 44 text above is provenance for what
used to be true. Read `diff_new_lines` as it exists today in `embarch-ui` and document what it
actually does; if it turns out *not* to have such a fallback, that is the finding — say so, do not
write the doc to match the retired sentence.

## Watch for

- **Sweep inbound citations case-insensitively** (`grep -rni`). Part A exists because a
  case-sensitive `grep 'decision 25'` missed a sentence-initial `Decision 25` one line above a line
  it did match. See `tasks/doc/065`.
- **Reserve for `ui`:** nothing in `embarch-ui` is in the doc-size reserve as of this leg. If your
  work pushes a file into the last 10% of its cap, file
  `tasks/ui/<NNN>-compact-ui.md` in the same commit.
- Part B may want a decision-adjacent note rather than a new numbered decision. **Do not open a new
  decision number** for it; `debug-tab.md`#13 already owns this consumer.

## Done when

- [x] `history/ui.md:38` and `embarch-ui/decisions/shell.md`#25 are consistent, by whichever of the
      two shapes above you chose, with the reason stated. **Chose "return the count somewhere
      citable," not the history-entry rewrite the task suggested as cheaper**: `check-ownership.py
      --scope ui` refuses `history/ui.md` for a `ui`-scoped worker (it is `build_changelog.py`
      output, per `changelog.d/README.md`'s "nothing edits a shared history file directly" —
      confirmed by first editing it, then getting a real ownership-check red). Restored the E/A
      vertex counts to `embarch-ui/decisions/shell.md`#25 (the `layers`-mode SVG paragraph) instead,
      so `history/ui.md:38`'s existing, untouched text is correct again.
- [x] `embarch-ui/decisions/debug-tab.md`#13 (or wherever `diff_new_lines` is actually documented)
      states the trailing-partial-line behaviour and why it is correct rather than a bug — **verified
      against the current implementation**, with the function and file named. `diff_new_lines` at
      `src/logs.rs:126` does have this fallback, though the code's own doc comment (`src/logs.rs:107`)
      names a different trigger (volume aging the window out) for the same no-overlap branch — a
      mutating trailing line never produces an exact-match overlap either, so it lands in the same
      "replay the whole window" fallback. Documented in decision 13.
- [x] Decision 25 still at or under 4,096 B if touched, with bytes reported. **3,906 B** (was 3,758 B;
      +148 B for the restored vertex-count sentence), 190 B under cap.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`/`test`/`clippy --all-targets -D
      warnings` clean in `embarch-ui` (no code changes needed — Part B is doc-only). All 11
      `check-docs.py` checks green; `check-client-names.py` and `check-ownership.py --scope ui`
      (doc repo) and `--code-repo` (code repo) all clean.
