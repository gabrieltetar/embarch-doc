# 034 — Name the new `BleConnect` worked-example fixture in `suite/studies-guide.md` §3b

**State:** open — **announced and parked awaiting its window, leg 097, 2026-09-12.**
Announced to `#embarch-fleet` at `ts 1789201472.118549`; the 30-minute silence-as-consent window
(`embarch-fleet/ops.md` §4) closes at **02:54 local**. Execute it as a supervisor unit, not a
worker's, only if no objection has arrived by then. **If a leg ends before the window closes, leave
this line intact and complete the window rather than restarting it** — the `ts` above is the clock.
**Source:** `inbox/suite-studies-guide-name-ble-connect-fixture.md`, split out of `tasks/api/076` by
its own worker: that task's `Done when` asked for `suite/studies-guide.md` §3b to name the new
fixture, but `suite/` is outside the `api` ownership row
(`check-ownership.py --scope api` refuses any write there), so the sentence could not be added from
inside that task. Drained into the queue by leg 097, 2026-09-12.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-api/tests/fixtures/ble_connect_worked_example.json` now exists (landed as `api/076`, code
`f402163`): a `BleConnect` step with an explicit `target_address`, round-tripped into `Study` by
`embarch-api/tests/ble_connect_fixture.rs`, never submitted to Core. It is the worked form of
`studies-guide.md` §3b's advice — "a real study sets `target_address` or `target_name`" — which
until now had no authored example anywhere in the tree.

## Why now

One sentence closes a documented gap; leaving it undone means the advice keeps citing nothing.

## Size note

`suite/studies-guide.md` is **in reserve** — 24,114 of a 25,600 B cap, 1,486 B left — and its
compaction task `tasks/suite/004-compact-suite.md` is `blocked`. One clause fits comfortably;
do not expand this into a worked-example section.

## Done when

- [ ] `suite/studies-guide.md` §3b (the sentence "So a real study sets `target_address` or
      `target_name`.") gets one added clause or sentence naming
      `embarch-api/tests/fixtures/ble_connect_worked_example.json` and
      `embarch-api/tests/ble_connect_fixture.rs`.
- [ ] `scripts/check-docs.py` still green.
