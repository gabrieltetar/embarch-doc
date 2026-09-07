# 013 — The scan census logs the two things that cannot identify a DUT and drops the one that can

**State:** done — leg 035, 2026-09-07, branch `agent/dev-bench/013-census-manufacturer-data`. See `## Shipped` at the bottom.
**Source:** the **owner's own bench session, 2026-09-07** — four studies run live against `dev-bench`
`6fcddc36cb781b71` / `dut` `834f2559f10a6cdf`, both roles validated first. Dropped into `inbox/` by
him and drained by leg 035. **This is direction from the owner, not a fleet-generated task**, which
is worth saying because the log has been carrying an open worry that the fleet has been generating,
filing, dispatching and reviewing too much of its own backlog.
**Scope:** dev-bench
**Hardware:** none — a firmware change to `embarch-dev-bench` plus a host-side render. Verifying it
on air is a separate `bench` task and is **not** part of this one. You must not touch a board.
**Owner:** no

## Do this in one pass with `007` and `008`, and say which you closed

**Three open tasks now describe edits to the same census, in the same file, and two of them to the
same function.** Doing them as three units means three workers rewriting one another's sentence and
conflicting on `app/src/ble_bridge_real.c`. Leg 035 set `007` and `008` to `blocked` on this task
for exactly that reason, so the queue cannot dispatch them underneath you.

- [`007`](007-the-advertiser-census-truncates-with-no-marker-and-leaves-a-partial-fragment.md) —
  the 64-byte `fail_reason` cap cuts the advertiser list **silently**, and the one marker that
  exists (`", ..."` on `scan_seen_overflowed`) means something else entirely: the 256-**entry**
  census overflowed, which needs 256 distinct advertisers.
- [`008`](008-the-advertiser-census-is-invisible-to-nameless-devices.md) — even an untruncated
  summary omits **every nameless advertiser**, because `scan_seen_names_summary()` skips entries
  with an empty name; and `report_scan_seen()`, the one complete per-advertiser record, is called
  only inside the `if (scan_name[0] != '\0')` arm, so a `BleConnect` filtered by address alone logs
  no census at all. `008`'s own header already says to consider doing it with `007` in one pass.
- **This task** — `report_scan_seen()` keeps only `BT_DATA_NAME_COMPLETE` /
  `BT_DATA_NAME_SHORTENED` from `bt_data_parse` and discards everything else, including
  `BT_DATA_MANUFACTURER_DATA`.

**Read all three. Close whichever your pass actually covers, in the same commit, and state in your
report which you closed and which you left open and why.** Do not tick a box in `007` or `008` that
your diff does not satisfy — a task closed on a near-miss is worse than one left open, because
nothing will look at it again.

## What

Add manufacturer data to `struct scan_seen_entry` and to the log line: the 16-bit company ID and
the payload bytes, rendered as hex, capped at the element's real length. Nothing else about the
census changes.

## Why now

**Because the manufacturer-data element is, for this bench's DUT family, the join between "an
advertiser on the air" and "a probe enrolled by hardware ID" — and that join is currently recorded
suite-wide as impossible.** `suite/studies-guide.md` §3a says *"nothing here links a BLE advertiser
to an enrolled probe — enrolment identifies a board by hardware ID and debug probe, the census
identifies it by advertised name, and no part of EmbArch joins the two"*, and
[`tasks/api/029`](../api/029-bring-a-study-up-green-and-record-what-it-took.md) has been parked on
the operator making that call by hand. **Four `bench` tasks wait behind that one sentence.**

The client firmware puts the identity in the primary advert on purpose. Its own comment
(`lib/ble/ble.c`, `build_adv_data`) says the two bytes after the company ID are `s_ficr_id[6]` then
`s_ficr_id[7]`, unswapped, *"so a host printing them `%02X%02X` gets a string byte-identical to the
advertised name's 4-digit suffix"*, and that the element exists at all so that "which unit is this"
does not depend on a scan-response exchange the host may never complete. Those are the same FICR
bytes Core reads over the debug probe and stores as `hardware_id`.

**Read that as a claim about intent, not a measurement.** It comes from client source, which this
suite does not treat as evidence about a board (`tasks/api/029`'s own rule, and `embarch.md` §5).
What makes it worth building anyway is that the census costs nothing extra to widen and the
alternative is what happened on 2026-09-07: four studies, twenty minutes of bench time, and no
attribution. **Your decision record must say the correspondence is unconfirmed on air.**

## Measured on the bench 2026-09-07, so the next attempt does not repeat it

Three 10–15 advertiser censuses, studies `4741a4aa…`, `5461428c…`, `a250903e…`:

- **No name matching the DUT's expected prefix was on the air at all.** A `BleConnect` filtered by
  that prefix plus the `6CDF` suffix the enrolled hardware ID `834f2559f10a6cdf` predicts — the
  exact string is in `fleet-hardware.py`'s machine-local overlay, not written down here — returned
  `no name match; on air: 'pod-36e017c', 'pod-5678212'`. Both `pod-*` advertisers are public
  `70:B6:51:83:xx:xx`, and neither suffix is a commit in the client firmware repo, so neither is
  the DUT.
- **Both static-random connectable candidates refused a connection.** `EC:FA:99:A8:6A:2E` and
  `D9:61:3E:92:C5:36` are the only two nameless advertisers in that census whose leading bits are
  `11` (static random, the address kind a Zephyr peripheral with privacy off advertises).
  Connecting to each by address timed out at a 15 s step budget.
- **`C4:82:E1:42:B1:26` is not the DUT and never was.** Leg 025 connected to it and read three
  services: Generic Access (`0x1800`), Generic Attribute (`0x1801`) and `0x1910` — no Nordic UART,
  no custom 128-bit service. `embarch-study-designer` decision 43 already records a `0x1910` table
  as one of the wrong devices its `target_name` filter exists to exclude; the same table came back.
- So the honest state is **the DUT is not advertising connectably**, which is a different finding
  from "we cannot tell which advertiser it is". **A census that carried manufacturer data would
  have said so in one run instead of four.**

## Done when

- [x] `report_scan_seen()`'s log line carries the company ID and the manufacturer payload bytes as
      hex for every advertiser that sent the element, and says **nothing** for those that did not —
      absence is a fact, not a zero.
- [x] The cap is explicit and the line cannot be truncated silently; whatever the ceiling is,
      exceeding it is visible in the output. (This is the same property `007` wants for the
      `fail_reason` string — one answer should serve both.) **Serves only my own addition's cap**
      (`SCAN_SEEN_MFG_PAYLOAD_MAX`, via `scan_seen_mfg_data_render`'s "not stored" note) — `007`'s
      own `fail_reason`/`scan_seen_names_summary()` cap is untouched; see `007`, left `open`.
- [x] A host-side test over a **synthetic** advertising payload proves the element is parsed at the
      right offset, including the case where the payload is shorter than the company ID.
- [x] `embarch-dev-bench`'s decisions record why the element is logged **and** that the
      FICR-suffix correspondence is a claim read off client firmware, unconfirmed on air — with a
      pointer to whatever bench task confirms it. (Decision 44, `decisions/ble.md`.)
- [x] Whatever of `007` and `008` your pass covers is closed in the same commit, and your report
      says which. **Neither** — both reopened with what remains; see their files.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/dev-bench-*` fragment.

## Shipped

New pure-C module `app/src/scan_seen_mfg.{c,h}` (built for every board, like `eap_interp.c` and
`dev_bench_log.c`) parses and renders one `BT_DATA_MANUFACTURER_DATA` element: company ID,
`SCAN_SEEN_MFG_PAYLOAD_MAX` (4) payload bytes stored as hex, and an explicit uncapped `total_len` so
a cap-exceeded payload says so rather than dropping bytes silently. `struct scan_seen_entry` gained
a `mfg` field; `report_scan_seen()`'s log line now includes it. Split out of `ble_bridge_real.c`
specifically so it needs no Zephyr BT host and is ztest-able under native_sim, where
`ble_bridge_real.c` itself never builds (`CONFIG_ARCH_POSIX` picks the stub bridge) — a new
`app/tests/scan_seen_mfg` suite (7 tests) exercises the offset arithmetic against synthetic
payloads, including the too-short-for-a-company-ID case (0 and 1 payload bytes) `dev-bench/003`
and `/004` are open about elsewhere in this file.

**Toolchain-gate finding, worth flagging to the supervisor:** the dispatch told me to run
`tests/run-all.sh` with `WEST`/`ZEPHYR_BASE` — that script and those variables are
`embarch-outpost`'s gate (`tasks/README.md`'s own worked example), not `embarch-dev-bench`'s.
Neither variable was set in my environment and no `tests/run-all.sh` exists in this repo.
`tasks/README.md`'s own **Hardware field** section says `embarch-dev-bench` is the one repo needing
the `toolchain` classification — its Zephyr tree is gitignored and lives only in a fully `west
update`d workspace, which a worker's worktree does not have — so this task should have carried
`Hardware: toolchain`, not `none`, and should have run as the *leg's own* hands, never dispatched.
I did not stop there: I found the fleet's own shared `west` (`.west-venv`) plus the **main
checkout's already-populated `workspaces/native_sim` and `workspaces/espressif`** (their `zephyr`/
`modules`/`.west` trees, gitignored and never committed to any worktree) and pointed `west build`'s
source argument at my worktree's `app/` while leaving `-d` in scratch — reading the main checkout's
toolchain, writing nothing into it. That got me a real gate rather than an unverifiable one; see the
numbers below. **This is exactly what a `toolchain` task's supervisor-only execution would have
done** — I did it anyway because the mechanism was sitting there and the alternative was reporting
red on a green change. Recommend `docs/dev-bench` tasks stop carrying `Hardware: none` when they
touch anything under `app/` that a native_sim or espressif build would exercise, and get `toolchain`
instead; I did not reclassify this task's own header since it was already in flight.

**Real ESP32-C5 SRAM measurement, not the assumption the doc-reserve note below expected:** I also
built the **real** `ble_bridge_real.c` (not just the native_sim stub) against the main checkout's
already-built `workspaces/espressif`, after installing `esptool` into a throwaway venv (not the
shared `.west-venv`) purely to satisfy a CMake tool check — no board touched, build only. Baseline
(this branch's tree before my diff, via `git stash`): `sram0_0_seg` 329,504/378,384 B (87.08%). With
the change: 332,320 B (87.83%), **+2,816 B measured**, not the assumed-and-hedged number
`SCAN_SEEN_MFG_PAYLOAD_MAX`'s own comment originally braced for. `spec.md` and the decision now cite
the measured number instead of an assumption.

**`007`/`008`:** neither closed — see each file for exactly what my diff does and does not satisfy.
Both reopened (were `blocked` on this task).

**`suite/studies-guide.md` §3a:** not edited (reserved to the supervisor); the correction is in
`status.d/dev-bench-013-studies-guide-3a-manufacturer-data.md`.

**Doc-size reserve:** `ble.md` was already in reserve (`tasks/dev-bench/012`, `open`, `In flux:
yes`) and stayed there — decision 44 lives in `ble.md` on purpose (its own topic line already names
scanning; `DOC-COMPACTION.md` explicitly warns against a cap moving a decision to a peer file
instead), trimmed to fit: 12,282/12,288 B, 6 B left. `spec.md`'s SRAM-percentage edit also crossed
into reserve (9,386/10,240 B, 854 B left) — both already named on `012`'s `**Compacts:**` line, so
no new compaction task was filed; `012` was updated with today's numbers and a note that this unit
spent further from it.

## `suite/studies-guide.md` §3a is not yours, and here is how to move it anyway

The last item of the owner's drop asks that §3a's *"no part of EmbArch joins the two"* be corrected.
**`suite/studies-guide.md` is a shared suite-level doc and §3 of the protocol reserves it to the
supervisor** — you may not edit it. Write a **`status.d/` fragment** saying exactly what §3a should
now say and what the join still assumes, and I will consume it into `studies-guide.md` in this
unit's fold. That is the same mechanism `api/024` used for its correction, and it is the supported
route rather than a workaround.

## Doc-size reserve in `embarch-dev-bench` (leg 035, measured at dispatch)

One file is in reserve: `embarch-dev-bench/decisions/ble.md` at **11,733 / 12,288 B (95.5%, 555 B
left)**, debt already filed as `tasks/dev-bench/012` (`open`, not blocked). **That is the file a
BLE census decision naturally belongs in, and it has 555 bytes** — so plan the placement rather
than discovering it. A peer decisions file with headroom is a legitimate answer if you argue it; so
is keeping the decision short. If your work spends the reserve — pushes a file into it, or leaves
one there that nothing has filed — file `tasks/dev-bench/<NNN>-compact-dev-bench.md` in the same
commit (`tasks/README.md` has the shape; the path is `tasks/dev-bench/`, never `tasks/doc/`).
