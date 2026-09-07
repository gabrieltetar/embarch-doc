# 013 — The scan census logs the two things that cannot identify a DUT and drops the one that can

**State:** claimed — leg 035, 2026-09-07, **worker finished and pushed; the leg died before folding — see the recovery note at the bottom of this file**, branch `agent/dev-bench/013-census-manufacturer-data`.
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

- [ ] `report_scan_seen()`'s log line carries the company ID and the manufacturer payload bytes as
      hex for every advertiser that sent the element, and says **nothing** for those that did not —
      absence is a fact, not a zero.
- [ ] The cap is explicit and the line cannot be truncated silently; whatever the ceiling is,
      exceeding it is visible in the output. (This is the same property `007` wants for the
      `fail_reason` string — one answer should serve both.)
- [ ] A host-side test over a **synthetic** advertising payload proves the element is parsed at the
      right offset, including the case where the payload is shorter than the company ID.
- [ ] `embarch-dev-bench`'s decisions record why the element is logged **and** that the
      FICR-suffix correspondence is a claim read off client firmware, unconfirmed on air — with a
      pointer to whatever bench task confirms it.
- [ ] Whatever of `007` and `008` your pass covers is closed in the same commit, and your report
      says which.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/dev-bench-*` fragment.

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

## Recovery note — owner's session, 2026-09-07 12:1x

**The worker finished, pushed both halves, and the supervisor never woke to land
it.** Leg 035 dispatched this unit at 11:30, said "two workers in flight,
holding", and stopped. This worker reported complete at 11:52, both branches
pushed:

- code `agent/dev-bench/013-census-manufacturer-data` (5540469) on `embarch-dev-bench`'s origin
- doc `agent/dev-bench/013-census-manufacturer-data-doc` (fa3ef91) on `embarch-doc`'s origin

The completion notification was delivered to the **listener session's** main
loop instead of to the supervisor subagent that spawned this worker. The
listener read it, correctly concluded "worker report to the running supervisor,
not a leg completion — no listener action", and did nothing. The supervisor was
never resumed, so nothing folded, `.fleet/tick` was last touched at 11:30:42,
and the deadman pulled the pump latch at 12:09.

**So phase-0 recovery must RE-LAND this, not block it.**
[tasks/README.md](../README.md)'s rule — a worktree with commits ⇒ `blocked`
naming the branch — is written for a worker that died mid-edit. This one did
not: it ran to completion and its own report is in the leg's transcript. Leg
033 took exactly this route this morning for `api/040` and `ui/003`, and its
log entries say why: re-dispatching throws away finished green work to buy a
self-report you already have a better substitute for.

**Gate on the merge result, not the branch**, and note the branch predates four
owner commits (through `54c6882`), so the doc half needs a rebase before it will
fast-forward. **`check-doc-size.py` changed while this worker ran**: reserve is
now `max(1.2 KB, 10%)`, so re-check whether this unit's own additions put a
file into reserve that its author had no reason to file.
