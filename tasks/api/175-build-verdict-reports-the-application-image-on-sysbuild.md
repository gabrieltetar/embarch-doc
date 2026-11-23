# 175 — The build verdict reports the application image on a sysbuild build

**State:** claimed by agent/api/175-build-verdict-reports-the-application-image-on-sysbuild, 2026-11-23 13:36
**Source:** Fleet Ready issue, a session building a sysbuild firmware commit through `build --each`
**Issue:** EMB-232
**Scope:** api
**Hardware:** none
**Owner:** no

## What

On a sysbuild build the verdict's FLASH and RAM, its headroom and its change
against the previous commit track the application image, not MCUboot's. Today
`crates/embarch-firmware-build/src/verdict.rs` (`is_memory_header` /
`memory_table`) parses every `Memory region` table in the log and keeps the
last. A sysbuild log holds the application's table first
(`FLASH: 522368 B 712560 B 73.31%`) and MCUboot's after it
(`FLASH: 43596 B 62 KB 68.67%`), so a 522 KB application read as 43 KB with
19 KB of headroom. The verdict reports the application image's table (the
sysbuild default image, the one `artifact_path` flashes), or one row per image
with its name; which, and how a table is tied to its image, is the worker's
decision to record.

## Why now

A verdict that reads MCUboot's numbers hides an application approaching its
flash limit.

## Where

- `crates/embarch-firmware-build/src/verdict.rs` `is_memory_header` /
  `memory_table`.
- The image a table belongs to shows in the log line before it
  (`Linking C executable zephyr/zephyr.elf` under each image's build
  directory) and in the build's `domains.yaml` (`default:` names the
  application domain).

## Dispatch note

No `embarch-api` file is in size reserve. Per-decision caps close to their
limit in this scope: `ledger` #98 (15 B), `bench-exchange` #89 (122 B),
`failure-reporting` #67 (192 B); if the verdict's decision is one of those,
say so and file a new decision rather than growing it.

## Done when

- [ ] A sysbuild log with an application table then an MCUboot table gives the
      application's FLASH and RAM in the verdict.
- [ ] A test covers the two-table log; a single-image log reads as before.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
- [ ] `spec.md`/`decisions.md`/`open.md` updated where they describe the
      verdict's memory figures, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
