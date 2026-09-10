# 007 — The advertiser census truncates with no marker, and the truncation path leaves a partial fragment behind

**State:** done — worker unit `007-census-truncation-marker`. Both defects fixed: `scan_seen_names_append()` (new `app/src/scan_seen_names.c`/`.h`, no BT host, ztest-pinned under native_sim) formats each name-list entry into scratch first and copies it into the buffer only whole, so a rejected entry leaves no partial fragment; `connect_as_central()` now appends one of two distinct markers -- `(truncated)` for the 64-byte name-list cap, `(census full)` for the unrelated 256-entry `SCAN_SEEN_MAX` overflow -- budgeted before the name list is formatted so the final `outcome_fail` write can't truncate the marker away either. `embarch-dev-bench/decisions/scanning.md` decision 45.

**Left for the supervisor / an attended session:**
- The one 20-second on-bench re-observation this task's `Hardware:` line calls for -- no hardware was touched from this worker.
- `suite/studies-guide.md` §3a's paragraph on reading a truncated `fail_reason` -- explicitly not this worker's file to edit; needs updating to describe the new two-marker behaviour once landed.

**Verified without hardware:** `west build -b native_sim` for the new `app/tests/scan_seen_names` ztest suite (5/5 pass, including the no-partial-fragment case) and for the existing `scan_seen_mfg`/`serial_protocol`/`dev_bench_log` suites and the full `app` native_sim target; `west build -b nrf54l15dk/nrf54l15/cpuapp app` (the real board target that actually compiles `ble_bridge_real.c`, native_sim links the stub instead) -- clean, 59.64% RAM. `west`/`ZEPHYR_BASE` were available in this environment (main checkout's `workspaces/{native_sim,nordic}`, `EMBARCH_STUDY_DESIGNER_PATH` set to the sibling repo for the study-designer staticlib path dependency); no new toolchain-gap debt to report.
**Source:** observed live by the supervisor running `tasks/api/029` on the bench, 2026-09-06;
narrowed from a withdrawn `study-designer` task after a reviewer showed the capability exists
**Scope:** dev-bench
**Hardware:** none to fix; **one 20-second study to re-observe**
**Owner:** no

## What was observed

A `BleConnect` step with a deliberately unmatchable `target_name` — the documented
way to ask what is advertising near the bench (study-designer decision 43) —
returned this `fail_reason`, verbatim except for the names:

```
no name match; on air: '<name>', '<name>', '<name>',
```

**That string is exactly 64 bytes and it ends on a separator**, mid-list. It was
cut by `MAX_FAIL_REASON_LEN` and **says nothing about having been cut.**

## Two defects, and the second is the one that surprised me

**1. The truncation has no marker, and the marker that exists is for something
else.** `report_scan_seen`'s caller appends `", ..."` when
`scan_seen_overflowed` is set — but that flag means the **256-entry census**
overflowed, which needs 256 distinct advertisers. The 64-byte *string* cap is
reached at three or four names and is the case that actually happens. So the
common truncation is silent and the marked one is nearly unreachable. **A reader
cannot distinguish "these three were on air" from "these three fitted".** Where
the cut lands on a name boundary there is not even a trailing comma to notice.

**2. The truncation path leaves a partial write in the buffer.** In
`scan_seen_names_summary()` (`embarch-dev-bench/app/src/ble_bridge_real.c`
~1040–1065) the loop does:

```c
int written = snprintk(summary + used, sizeof(summary) - used, "%s'%s'", sep, name);
if (written < 0 || (size_t)written >= sizeof(summary) - used) {
        break; /* truncated -- the names that fit are still the useful part */
}
```

The comment describes the intent and **`snprintk` has already written the bytes
that fit before returning the would-be length.** `used` is not advanced, so
nothing further is appended — but what `snprintk` already deposited stays. That
is where the observed trailing `", "` came from: the separator and the start of a
name that did not fit. **The check is a post-hoc test of a write that already
happened, not a guard before one.**

Neither is a data-loss bug — the full per-advertiser record still goes to the log
sink. Both are **honesty-of-report** bugs, in the one field a study's caller
actually receives, in a suite whose stated rule is that a short capture must
never read as a complete one (`suite/studies-guide.md` §1 on `truncated`).

## Done when

- [x] A cut census is distinguishable from a complete one **from the
      `fail_reason` alone** — an unambiguous marker that fires on the string cap,
      not only on the 256-entry overflow.
- [x] The truncating write leaves no partial fragment: bound the write before it
      happens, or truncate back to the last complete name.
- [x] The two overflow conditions are distinguishable from each other, or the
      decision to conflate them is written down with its reason.
- [ ] Re-observed on the bench with the same one-step study, and the observed
      string recorded — this is cheap and it is how it was found. **Left as a
      hardware debt: no board from this worker.**
- [ ] `suite/studies-guide.md` §3a's paragraph on reading a truncated
      `fail_reason` is updated to match whatever ships. **Not the worker's file:
      hand it back to the supervisor.**
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What this is *not*

An earlier draft of this defect claimed the study vocabulary had no way to scan
at all and proposed a `BleScan` wire action. **That was wrong** — decision 43
already specifies the failed-match census and `ble_bridge_real.c` implements it,
with `embarch-dev-bench/spec.md`'s `SCAN_SEEN_MAX` row recording a real 12-entry
census. Do not re-propose a new action here; the capability ships, and only its
report is lossy.
