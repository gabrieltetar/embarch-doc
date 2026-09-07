# Serve the two caps `app.js` restates instead of hardcoding 250,000 and 32

**State:** claimed by agent/ui/003-serve-the-two-caps-app-js-restates, 2026-09-07 02:05
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

- [ ] `TraceView` carries the row cap; the actions response carries the stream-name limit; both come
      from the constants, not literals.
- [ ] `grep -n "250,000\|250000\|, 32)" assets/app.js` finds no limit restatement.
- [ ] Rust tests assert each served field equals the constant it mirrors.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

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
