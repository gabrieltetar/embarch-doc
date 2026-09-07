# Serve the two caps `app.js` restates instead of hardcoding 250,000 and 32

**State:** done
**Source:** owner's repo survey, 2026-09-06 — `embarch-ui/spec.md`'s Invariants forbid exactly this
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Two server-enforced limits are copied into the browser:

- `assets/app.js:3661` — `"this view caps at 250,000"` restates `MAX_ROWS` (`src/trace.rs:120`).
- `assets/app.js:2726` — `.slice(0, 32)` restates `MAX_STREAM_NAME_LEN` (`src/limits.rs`, used at
  `src/study_designer.rs:491`), and its own comment names the constant it is copying.

Both numbers should reach the browser from the server — the row cap as a field on `TraceView`
(beside `rows_dropped_by_cap`), the name limit on the actions response beside `max_monitor_targets`
— and `app.js` renders what it was served.

## Why now

`embarch-ui/spec.md`'s Invariants say outright "**A limit enforced server-side is *served*, never
restated in `app.js`**", and `decisions/gatt-capture.md` 17 already did exactly this for
`MAX_MONITOR_TARGETS` because "a browser-side copy of a limit is a number that drifts silently the
day the limit moves". These two were missed.

## Done when

- [x] `TraceView` carries the row cap; the actions response carries the stream-name limit; both come
      from the constants, not literals. `TraceView::row_cap = MAX_ROWS` (`src/trace.rs`);
      `ActionsResponse::max_stream_name_len = MAX_STREAM_NAME_LEN`
      (`embarch_study_designer::limits`, already `pub`) beside `max_monitor_targets`
      (`src/study_designer.rs`).
- [x] `grep -n "250,000\|250000\|, 32)" assets/app.js` finds no limit restatement. Verified empty
      after the change. The only other `.slice(0, 32)`-shaped hit that grep could have found before
      the edit was the same line this task names (`charLabel(...).slice(0, 32)`) — there was no
      second, unrelated `, 32)` slice anywhere else in the file to leave alone.
- [x] Rust tests assert each served field equals the constant it mirrors.
      `trace::tests::served_row_cap_is_the_enforced_constant` and
      `study_designer::tests::served_stream_name_limit_matches_the_constant`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`/`test`/`clippy --all-targets
      -D warnings` clean in `embarch-ui`; `check-docs.py`, `check-ownership.py --scope ui` (both
      repos) and `check-client-names.py` all clean.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. `spec.md`'s "Two view caps" line now names
      both served fields; `decisions.md` gained decision 21 (`decisions/trace-view.md`) and 22
      (`decisions/study-designer.md`); `open.md` needed no change (item 11's cap-raising question is
      untouched by serving the current value). No `status.d/` fragment: nothing suite-level changed
      — this is an internal wire addition to one sub-project's own responses.

## What shipped

- `src/trace.rs`: `TraceView::row_cap: usize`, set to `MAX_ROWS` at construction; a test pinning it.
- `src/study_designer.rs`: `ActionsResponse::max_stream_name_len: usize`, set to the already-`pub`
  `embarch_study_designer::limits::MAX_STREAM_NAME_LEN` (no reach into that crate needed — point 1
  of this task's brief turned out to already be satisfied); a test pinning both served limit fields
  by serializing an `ActionsResponse` and reading back the JSON.
- `assets/app.js`: the row-cap banner reads `view.row_cap` (falls back to a capped-but-unstated
  message, never a guessed number, if the field is ever missing); the GATT-tap default name slices
  to `sdMaxStreamNameLen` (`null` until the actions response has been fetched, and **no slicing at
  all** while it is `null` — a wrong guessed cap would let an over-long name through with false
  confidence, where no slicing just falls back to `build_study`'s own submit-time refusal, the same
  behaviour this UI already had before the `.slice(0, 32)` existed).
- `embarch-ui/decisions/trace-view.md`: compacted the settled repartition/three-tier-axis prose
  (11,080 B → 10,485 B, preserving every `Must not delete:` fact from `tasks/ui/009` — verified by
  grep) to make room for new decision 21, landing at 10,989 B — clear of the 11,059 B reserve line
  and slightly under the file's size before this unit touched it. Decision 19 was not read for
  meaning or touched in any way. `tasks/ui/009` closed as a ride-along (`DOC-COMPACTION.md` §2);
  `tasks/ui/007`, which decision 19 is actually blocked on, is unaffected and still open.
- `embarch-ui/decisions/study-designer.md`: added decision 22 (short, ~460 B) per this task's own
  judgement call that the stream-name-limit half belongs here rather than in `trace-view.md`. This
  file was already past its own reserve line before this edit and `tasks/ui/011` already exists,
  open and unblocked, to compact it — so no compaction ride-along here, per this task's own
  instructions ("that is a judgement, not an instruction"). `tasks/ui/011` updated with the new byte
  count so its own job description stays honest about what it now has to clear.
- `tasks/ui/009-compact-ui.md`: closed (see above).
- `tasks/ui/011-compact-ui-study-designer-decisions.md`: left open, noted the new byte count.
- `changelog.d/` fragment dropped.

## Reserve — read before you write a doc (supervisor, leg 030)

Two `embarch-ui` docs are in reserve, and **the one your decision most naturally belongs in is the
parked one**:

- **`embarch-ui/decisions/trace-view.md`, 11,080 / 12,288 B, 1,208 B left** — filed against
  `tasks/ui/009`, which is **`blocked` on `In flux: yes`**. Read `tasks/ui/009` before you write:
  the flux is **only** decision 19 (which `tasks/ui/007` exists to settle) and the paragraph above
  it. The rest of that file — the three-tier axis table, the 46× error, decision 10's repartition
  material — it declares finished. So if this unit's decision belongs in `trace-view.md`, write it
  there, keep it short, and **if you leave that file deeper in reserve, compact the settled parts in
  the same commit**, carrying `tasks/ui/009`'s `Must not delete:` list verbatim and closing only
  that file's item (`DOC-COMPACTION.md` §2's ride-along). Do not touch decision 19.
- **`embarch-ui/decisions/study-designer.md`, 11,164 / 12,288 B** — filed against `tasks/ui/011`,
  which is `open` and not parked. The stream-name-limit half of this task is closer to this file's
  mission than to `trace-view.md`'s; that is a judgement, not an instruction.

If your work pushes any other file into its last 10%, file `tasks/ui/<NNN>-compact-ui.md` in the
same commit.
