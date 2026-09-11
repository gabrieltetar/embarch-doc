# 016 — the two census gates `008` fixed have no test that can reach them

**State:** open
**Source:** `tasks/dev-bench/008`, closed by the supervisor itself, leg 070, 2026-09-10. Its third
`Done when` box could not be ticked and this task carries it.
**Scope:** dev-bench
**Hardware:** toolchain — no board is needed for the extraction half; the `native_sim` suites need
the main checkout's Zephyr workspace, which a worker's worktree does not have. See `008`'s
`Hardware:` field for the measured commands.
**Owner:** no

## What

`008` landed two changes in `app/src/ble_bridge_real.c` (decision 46) and **neither is covered by a
test, because nothing can compile that file off a board.** `app/CMakeLists.txt` picks
`ble_bridge_stub.c` under `native_sim` (decision 16), so the `scan_seen_names` ztest suite reaches
`scan_seen_names_append()` and stops there. The two uncovered gates:

1. **`scan_seen_names_summary()`** — skips nameless entries, and now returns an empty string rather
   than one of two phrases when nothing was named.
2. **the connect-timeout arm in `connect_as_central()`** — builds the `fail_reason` from
   `SCAN_SEEN_PREFIX`'s two counts, reserves `(census full)` only when `scan_seen_overflowed` is
   set, and calls `report_scan_seen()` on both filter paths.

`008`'s own "Watch for" note claimed a test could pin both from the existing fixture harness. **That
was wrong and is worth not repeating**: the harness reaches the *appender*, which was extracted for
exactly this reason, not the summary or the timeout arm.

## What would close it

Two shapes, and the first is the one `scan_seen_names.c` already proves works:

- **Extract.** Move the summary, and the `fail_reason` composition, into a file linkable without the
  BT host — the way `scan_seen_names.c` was — leaving `ble_bridge_real.c` holding only the calls
  into the Zephyr BT API. Then a ztest can build a mixed named/nameless `scan_seen[]` and assert the
  counts, the separator omission, the marker budget in both the overflowing and non-overflowing
  cases, and the both-markers case decision 45 cares about.
- **Or verify on a bench**, which closes the *behaviour* question and none of the regression one. A
  bench run is worth having either way (see `008`'s hardware debt), but it is not a substitute.

**A judgement is owed here rather than assumed:** whether a second extraction is worth it, or
whether this file is simply accepted as untested and the bench is the check. Say which, and record
it as a numbered decision — decision 16 is the standing statement that this file is untestable
under `native_sim`, and either answer is an amendment to how that is lived with.

## Why now

Two consecutive units (`015`, then `008`) have now changed byte-budget arithmetic in a file where a
`BUILD_ASSERT` is the only automated check that anything holds. The arithmetic has been right both
times; the third time is the one nobody checks.

## Done when

- [ ] Either the two gates have ztest coverage over a mixed named/nameless set on both filter
      paths, or a decision records that they will not and says what checks them instead.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/dev-bench-*` fragment if
      anything reader-facing changed.
