# 008 — The advertiser census only ever lists devices that advertise a name, and the one complete record is gated on a name filter

**State:** claimed by the supervisor itself, leg 070, 2026-09-10 19:05 — **as a `toolchain` unit, not
a worker dispatch.** The `Hardware:` field below is corrected in the same commit, with the
measurement that corrects it. **Standing note from the previous pass:** unparked by `013` landing. **`013`'s pass did not cover this.** It added Manufacturer Specific Data to `report_scan_seen()`'s per-advertiser record for every entry already in `scan_seen[]`, named or not — so a nameless advertiser that *is* recorded now shows more about itself than before. But `013` left both of this task's actual gates untouched: `scan_seen_names_summary()` still `continue`s past every entry with an empty name, and `report_scan_seen()` is still called only inside `connect_as_central()`'s `if (scan_name[0] != '\0')` arm, so an address-filtered `BleConnect` that times out still logs no census at all. Both fixes belong to the gating logic in `connect_as_central()`, not to the per-entry struct `013` widened, and were left for their own pass rather than folded in.
**Source:** supervisor bench unit, leg 025, 2026-09-06 — measured against the real bench, then confirmed in source
**Scope:** dev-bench
**Hardware:** toolchain — **corrected from `none` by the supervisor, leg 070, 2026-09-10, and
measured rather than assumed.** No board is needed, which is what `none` was reaching for and is
still true. But the change is C in `app/src/ble_bridge_real.c`, and a worker's worktree contains
`app/` and a `west.yml` and no Zephyr at all — the workspaces are gitignored and live only in the
main checkout (`tasks/README.md`'s `toolchain` paragraph). Filed `none`, this task sent a worker at
code it could not compile.

**What was measured, so nobody re-derives it or records a false debt again** [2026-09-10]:

    cd /home/gabriel/Github/embarch/embarch-dev-bench
    ZEPHYR_BASE=/home/gabriel/Github/embarch/embarch-dev-bench/workspaces/native_sim/zephyr \
      /home/gabriel/Github/embarch/.west-venv/bin/west build -p -b native_sim \
      -d <builddir> app/tests/serial_protocol
    <builddir>/zephyr/zephyr.exe

Built clean and the suite ran **PROJECT EXECUTION SUCCESSFUL** from the main checkout. **The fleet's
`west` and the Zephyr workspaces both exist and both work.** Three supervisor log entries before
this one recorded "this environment has no `west` and no `ZEPHYR_BASE`" as a hardware debt; that was
true of the *worktree* the worker was standing in and false of the machine, and it had begun to
propagate as a standing fact about the suite. The `toolchain` classification is exactly the
distinction — undispatchable, not unrunnable.
**Owner:** no

**`007` has landed, so the one-pass advice below is spent — read what it left instead.** `007` was
the *truncation* half (the 64-byte cap cutting the list silently, with the only marker meaning
something else); it landed on 2026-09-10 as `embarch-dev-bench` **decision 45** in
`decisions/scanning.md`, which introduced `scan_seen_names_append()` in `app/src/scan_seen_names.c`
and a `(census full)` marker distinct from `(truncated)`. Its task file is gone from the queue with
it. Its own follow-up, `tasks/dev-bench/015`, is still open. This task is the different and larger
hole in the same string: **even an untruncated `fail_reason` omits every nameless advertiser.** It
still lands in `scan_seen_names_summary()`, which `007` did not change, and it is independent of
`015`.

*(Link repointed by leg 068: this file referenced `007`'s task file by relative path, and `007`'s
fold removed that file from the queue, leaving `check-links.py` red on `main`. See the leg 068 log
entry — the fold that removed it reported the gate green.)*

## What

Two separate gates in `app/src/ble_bridge_real.c` make a nameless advertiser invisible, and
together they are why "the census" has been read as more complete than it is.

1. **`scan_seen_names_summary()` skips every entry with an empty name** —
   `if (scan_seen[i].name[0] == '\0') { continue; }`. That summary is what fills the step's
   64-byte `fail_reason`. So `no name match; on air: …` is a list of *named* advertisers, and a
   device advertising no local name never appears in it whether or not the 64 bytes ran out.
2. **`report_scan_seen()` — the one complete per-advertiser record, address and connectability
   included — is called only inside the `if (scan_name[0] != '\0')` arm** of the connect timeout
   in `connect_as_central()`. A `BleConnect` filtered by **address alone** that finds nothing
   logs no census at all and returns a bare `outcome_timed_out()`.

When this is done, a reader can tell from the study's own output how many advertisers were seen
and how many of them were nameless, and asking for a census does not depend on filtering by a
name you had to invent.

## The measurement

Two 20 s censuses five minutes apart, 2026-09-06, `dev-bench` `6fcddc36cb781b71` on probe
`001057729826`, both roles validated live first. Studies `458c7df0dd599bce574d1d4264bee485` and
`6d15c4896b733f7480ea579b64e7210d`.

- **10 advertisers on the air both times. 2 named** (`GABRIEL`, `pod-36e017c`).
- `fail_reason` both times: `no name match; on air: 'GABRIEL', 'pod-36e017c'` — **47 bytes of the
  64**, so nothing was truncated and **eight advertisers were missing anyway**, four of them
  connectable.
- The log sink had all ten, with addresses and connectability, on both runs.
- One of the nameless connectable ones, `C4:82:E1:42:B1:26 (public)`, was reached by
  `target_address` and its `GattDiscover` returned three services (study
  `bd39085d9aa34162a1a555494642ae43`, both steps `Pass`). **Nameless does not mean unreachable;
  it means unfindable by the census as it stands.**

## Why now

`suite/studies-guide.md` §3a teaches the nonsense-`target_name` trick as *the* scan, and
`embarch-study-designer` decision 43 records the same reasoning. On the strength of that census,
`tasks/api/029` concluded on 2026-09-06 that **not one advertiser was attributable to the DUT** —
and three bench tasks (`ui/007`, `outpost/002`, `study-designer/007`) sit behind that conclusion.
It is now clear that a census with no plausible DUT in it is **equally consistent with a nameless
DUT**, which is a materially weaker statement than the one that was written down. §3a has been
corrected to say so; the mechanism is still what it was.

## Watch for

- **The 64-byte `fail_reason` is the constraint, and it is why this is not simply "list them
  all".** A count is cheap and unambiguous: something like `no name match; 2 named of 10 on air:
  'GABRIEL', 'pod-36e017c'` tells a reader both that the list is partial and by how much, in a
  handful of bytes. Weigh that against widening `OUTCOME_MAX_FAIL_REASON_LEN`, which is a wire
  size.
- **`scan_seen_overflowed`'s `, ...` marker already means something else** — the 256-entry census
  overflowed — and `studies-guide.md` §3a warns readers not to confuse it with truncation. Do not
  overload it with a third meaning.
- **Ungating `report_scan_seen()` from the name filter is the cheaper half** and probably the more
  valuable one: it costs one log line per advertiser on a path that has already failed, and it is
  what makes an address-filtered connect diagnosable at all.
- A test can pin both without hardware from the existing fixture harness: a scan set containing
  named and nameless entries, asserting the summary reports the count and the log sink gets every
  entry on both filter paths.

## Done when

- [ ] A `fail_reason` census says how many advertisers were seen, not only which ones were named.
- [ ] The complete per-advertiser log record is emitted on an address-filtered connect too, not
      only a name-filtered one.
- [ ] Tests cover a mixed named/nameless scan set on both filter paths.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, and a
      `status.d/` fragment for `suite/studies-guide.md` §3a — its "the bench's log sink is the
      census" paragraph is a workaround and should shrink when this lands.
