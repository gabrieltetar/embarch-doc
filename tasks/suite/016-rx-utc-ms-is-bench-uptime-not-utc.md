# 016 — `rx_utc_ms` is dev-bench uptime, not UTC, and three contracts assert a resync that does not exist

**State:** done — leg 077, 2026-09-10, supervisor-executed. Window from leg 076 at ts
`1789097474.082349` elapsed (39m) with no objection in-thread; not restarted.
**Was:** open — announced to #embarch-fleet by leg 076 at ts `1789097474.082349`; the `ops.md` §4
30-minute window opened then. Do not restart the window: if this leg dies first, the next leg reads
that `ts` with `fleet-read.py --thread` and completes the remaining time.
**Source:** suite review pass 2026-09-06, dimension 5 (cross-surface consistency). Code-confirmed.
**Scope:** suite
**Hardware:** none. The fix is a rename plus three doc corrections, or an offset application in firmware; confirming the firmware half on a board would need the bench, but the flaw was found by reading and needs no board to fix.
**Owner:** no

## What

One column name is bound to two incommensurable clocks, and they sit side by side in every
rendered stream row.

`embarch-dev-bench/app/src/ble_bridge_real.c:320-324` stamps
`.rx_utc_ms = (uint64_t)k_uptime_get()` — **milliseconds since the bench booted** — under a
comment that says so: *"no `Hello.host_utc_ms` clock-offset tracking exists on this board yet,
and Core restamps on receipt regardless."* `hello.host_utc_ms` is decoded
(`app/src/serial_protocol.c:1377`) and read by nothing but a round-trip test
(`app/tests/serial_protocol/src/main.c:40`). No offset arithmetic exists anywhere in the
firmware.

Three contracts assert the opposite:

- `embarch-study-designer/interfaces/decoders.md:27` — *"`rx_utc_ms` is stamped by dev-bench at
  capture time off its own clock, **seeded and resynced from the host on every handshake**"*
- `embarch-study-designer/decisions/versioning.md:30` — *"**That is what makes a sample's
  timestamp a real UTC one rather than uptime-relative.**"*
- `embarch-study-designer/src/protocol.rs:31-33` — *"it seeds/resyncs its own UTC offset from
  this on every `Hello` … which is what makes `Sample::rx_utc_ms` meaningful."*

`embarch-dev-bench/open.md:24` is the one honest statement in the suite: *"No timestamp this
firmware produces is UTC-corrected — arrival stamps come off device uptime, and no host-clock
offset tracking is implemented for any of them."*

Meanwhile the suffix means real UTC in every sibling field — `core_rx_utc_ms`, `host_utc_ms`,
`started_utc_ms`, `ended_utc_ms`, `confirmed_at_utc_ms` — and `embarch-ui/src/trace.rs:2602`
documents `core_rx_utc_ms` as *"Absolute UTC milliseconds."* Worse, `rx_utc_ms` in an **outpost**
trace file *is* Core's clock (`embarch-outpost/spec.md:88-89`), so one name means the bench's
uptime in one CSV and the host's epoch in another.

Core renders both in one row. `embarch-core/src/stream_store.rs:740` produces the header
`rx_utc_ms,step_name,value,unit,channel_id,core_rx_utc_ms` (asserted at
`embarch-core/src/study.rs:4298`), and `:757` the transcript equivalent.

Candidate direction: make the name carry the epoch. Either the bench applies the offset it
already receives — which also closes `embarch-dev-bench/open.md:24` — or the field the bench
stamps stops claiming UTC and the three contracts above are corrected to match. Whichever is
chosen, one name must not mean two clocks in one row.

## Why now

Anyone who plots a transcript's `rx_utc_ms` against a power capture's, or against a trace's
`rx_utc_ms`, lands in 1970 with no way to see why, because the name asserts an epoch the value
does not have. Nothing catches it: the firmware is self-consistent, the CSV parses, and the
interface doc agrees with the name — the only contradiction is in another repo's `open.md`.
This is `embarch-decision-reversals.md` shape 5, a guess indistinguishable from an answer, with
the *name* as the false witness.

## Done when

- [x] No field named `*_utc_ms` anywhere in the suite carries a value that is not milliseconds
      since the Unix epoch, **or the exception is named at the point a consumer reads it.** —
      Second arm taken. The exception is now stated in `interfaces/decoders.md` where the row shape
      is described, on `Hello.host_utc_ms` in `src/protocol.rs`, on `GattTranscriptEntry::rx_utc_ms`
      in `src/gatt.rs`, and on the outpost row renderer in `src/outpost.rs` — which is the one place
      the two clocks sharing the name are visible to the same reader.
- [x] `embarch-study-designer/interfaces/decoders.md`, `decisions/versioning.md` and
      `src/protocol.rs` say what the bench actually does. — All three corrected; decision 12's
      claim that the resync "is what makes a sample's timestamp a real UTC one" is struck by name.
- [x] `embarch-dev-bench/open.md:24`'s bullet is **still true** and left standing: *"No timestamp
      this firmware produces is UTC-corrected — arrival stamps come off device uptime, and no
      host-clock offset tracking is implemented for any of them."* Nothing here changed the
      firmware, so closing it would have been the same false claim in a new place.
- [x] Gate green; `changelog.d/` fragment; no `status.d/` fragment — nothing suite-level
      (`embarch.md`, `suite/features.md`, `suite/roadmap.md`) asserted the resync, which is part of
      why this survived: the false claim lived only in one sub-project's contracts.

## Resolution — leg 077, 2026-09-10

**Fixed the false claims; did not make the rename.** The three contracts asserted a mechanism that
does not exist, and that is a lie a reader acts on. The name being wrong is a *second* defect with a
different cost and a different blast radius — `rx_utc_ms` is a column in Core's CSV header and its
transcript, a field in `embarch-study-designer`'s `Sample` and `GattTranscriptEntry`, a wire struct
member in `embarch-dev-bench`, and a differently-meaning column in every outpost trace. Renaming it
reaches four repos and every capture file already on disk, none of which a code change touches.
Doing both in one pass would leave nobody able to attribute a broken reader to either half.

The rename, and the firmware alternative that would make the name honest instead, are
`tasks/suite/027` with the argument attached. `embarch-study-designer` decision 72 records what the
field carries, what would make decision 12's struck sentence true again, and why fixing the firmware
unattended was refused: it needs the bench, and it silently makes captures taken before it
incomparable with captures taken after.

**Least sure about:** whether leaving the name is the right call rather than a comfortable one. The
task's own words are that the *name* is the false witness, and naming the exception at four read
points is a weaker remedy than removing the falsehood — it works only for someone who opens the
doc, and the whole failure mode is someone who opens the CSV. `suite/026` exists so that is a
scheduled decision rather than a thing quietly settled by inaction.
