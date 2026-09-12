# 027 — `rx_utc_ms` names two different clocks in two different files, and one of them is not UTC

**State:** open — announced 2026-09-11 23:26 by leg 093, `ts` `1789190763.632399`, 30-minute window per
`embarch-fleet/ops.md` §4 (closes 23:56:03 local). **The announcement takes the doc-and-naming arm
only and explicitly disclaims the firmware arm**, which needs the board and breaks capture
comparability — that half stays the owner's. If this leg ends before the window closes, **read the
thread and complete the window rather than restarting it.**
**Source:** split out of `tasks/suite/016` by leg 077, 2026-09-10, which fixed the *false claims*
and deliberately did not make the *rename*. `embarch-study-designer` decision 72 carries the
argument for the split.
**Scope:** suite
**Hardware:** none to decide and write it. The firmware arm, if chosen, needs the dev-bench board to
confirm — and would invalidate the comparability of every capture taken before it against every one
taken after, which is a fact for the owner and not a supervisor's call to make unattended.
**Owner:** no

## What

`suite/016` established what `rx_utc_ms` actually carries and said so at every point a consumer
reads it. It left the name alone. **The name is still wrong in one of its two homes**:

- in a **study** CSV / transcript / `Sample`, `rx_utc_ms` is **dev-bench uptime** — milliseconds
  since that board booted, no epoch, no offset applied (decision 72);
- in an **outpost trace** CSV, `rx_utc_ms` is **Core's real UTC clock**
  (`embarch-outpost/spec.md:88-89`, `embarch-study-designer/src/outpost.rs`).

One name, two clocks, two files an analyst routinely opens side by side. Every sibling field in the
suite — `core_rx_utc_ms`, `host_utc_ms`, `started_utc_ms`, `ended_utc_ms`, `confirmed_at_utc_ms` —
means real UTC, so the suffix reads as a promise everywhere but here.

## Two arms, and they are not exclusive

- **Rename the study-side column** to something that does not claim an epoch (`rx_uptime_ms` is the
  obvious candidate; naming is part of the task). This is a coordinated change across
  `embarch-dev-bench` (the wire struct), `embarch-study-designer` (`Sample`, `GattTranscriptEntry`,
  the CSV headers), `embarch-core` (`src/stream_store.rs`'s header and `src/study.rs`'s assertion of
  it), and `embarch-ui` — **plus every capture file already written**, which no code change reaches.
  Decide what happens to those: a documented reading rule, or nothing.
- **Fix the firmware** so the field earns its name: dev-bench applies the offset it already receives
  in `Hello.host_utc_ms`, one subtraction at the stamp site in `ble_bridge_real.c`. This closes
  `embarch-dev-bench/open.md`'s standing "Clock-resync accuracy is not validated" bullet, and makes
  decision 12's corrected paragraph true again. **It also makes captures taken before and after it
  incomparable with no marker in the file saying which side of the change they are on** — which is
  the reason `suite/016` did not do it unattended.

**Say which arm, and why, before touching anything.** Doing both in one pass makes it impossible to
attribute a broken reader to either.

## Done when

- [ ] One arm is chosen and recorded as a numbered decision, naming what happens to already-written
      capture files.
- [ ] If the rename arm: no field named `*_utc_ms` in the suite carries a non-epoch value, and every
      citation of the old column name resolves.
- [ ] If the firmware arm: `embarch-dev-bench/open.md`'s clock bullet is closed, decision 72's
      "what would make decision 12's removed sentence true again" paragraph is struck, and the
      change is confirmed on the bench.
- [ ] Gate green; `changelog.d/` fragments per repo touched; `status.d/` fragment for anything
      suite-level this makes false.
