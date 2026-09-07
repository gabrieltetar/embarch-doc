# 034 — Read check 11's `compatible` verdict and check 13's comparison on a live bench

**State:** claimed by the supervisor's own hands (leg 030, bench unit), 2026-09-07 01:46
**Source:** `umbrella/030`'s hardware-verification debt, leg 026, 2026-09-06 — the host-side half
landed (`embarch-umbrella` `d329842`, doc `8037467`) and left exactly one box unticked
**Scope:** umbrella
**Hardware:** bench
**Owner:** no

## Why this one matters more than its size

**It is, as of leg 026, the only bench task in the queue that is not waiting on a sentence from the
owner.** `api/029`, `ui/007`, `outpost/002` and `study-designer/007` all need the DUT's advertised
name or address before they can reach the DUT at all. This one needs neither: it runs `doctor`
against a Core that is up, with the bench attached, and reads two fields.

It also closes something that has been open for weeks under a wrong reason. `embarch-umbrella/open.md`
carried check 11's `compatible` verdict as *"the last live unknown, needing a bench"* — **and a bench
was never what it needed.** Two boards were attached, enrolled, validated and handshaking three times
out of three, and the check still could not read the field, because `doctor` gave a call that opens a
serial link the same 500 ms it gives a device scan. That is fixed and **unverified**.

## Roles this needs

`dev-bench`, attached and enrolled, with **Core up**. Validate before starting; if it is unattached,
leave this `open` and say so once — do not mark it blocked.

The three runs this task follows up had **both** boards attached (`dut` `834f2559f10a6cdf` on probe
`000852006107`, `dev-bench` `6fcddc36cb781b71` on `001057729826`, both re-validated 2026-09-06
20:33). Reproduce that arrangement rather than a narrower one, so a difference in the result is
attributable to the fix and not to the setup.

## Bench facts — supplied, do not infer

- Dev bench: **nRF54L15DK**, link **COM17 / VCOM1, interface 2** — the *higher* interface, not the
  lowest. Enrolled with `link_port_interface=2`.
- **Nothing is flashed and nothing is built by this task.** It is `doctor`, which is read-only, plus
  one authenticated HTTP GET. If a step seems to want a flash, stop.
- The three prior runs are in `C:\ProgramData\embarch\logs\dev-bench.log.2026-09-07` at
  `00:23:55.53`, `00:24:17.16` and `00:24:33.90` UTC, each `--- link opened on COM17 (firmware
  49958d34, wire schema v15) ---`. That is the evidence Core did the work while `doctor` gave up.

## What to run

1. `embarch doctor`
2. `embarch doctor --json`
3. **A timed authenticated GET of `/dev-bench/hello`** — this is the part that turns an assumption
   into a measurement, and it is the reason this task is worth a sitting rather than a glance.

## Why step 3 is not optional

`LINK_HANDSHAKE_GET_TIMEOUT` is **10 s and it is assumed, not measured** — `embarch-umbrella`
decision 44 says so in those words. **No run on this bench or any other has ever produced a handshake
duration**, so nothing yet establishes what the budget has to exceed; it was sized like
`MCP_HANDSHAKE_TIMEOUT` and kept under `embarch-api`'s 15 s `serial_timeout_secs`. One timing turns
that into a number.

Check 12's verdict in the same run is the missing evidence for the *other* budget: `/dev-bench/port`
sits on `DEVICE_SCAN_GET_TIMEOUT` (500 ms) **by argument rather than by measurement** — Core does the
same *kind* of work for it as for `/status` — and its own enumeration has never been timed either.

## Done when

- [ ] `dev-bench` validated live and matching before anything ran.
- [ ] Check 11's **`compatible` verdict** recorded — the value, not "it worked".
- [ ] Check 13's **real comparison** recorded, likewise.
- [ ] `/dev-bench/hello`'s handshake **duration** recorded, and `decisions/budgets.md` decision 44's
      "assumed, not measured" clause amended to say what was measured — or left alone with a note
      saying why, if the timing could not be taken.
- [ ] Check 12's verdict recorded, as the `DEVICE_SCAN_GET_TIMEOUT` evidence.
- [ ] **If it still fails, that is a complete answer and a more interesting one.** The failure now
      names its own verb — `timed out after 10000 ms` versus `could not connect` — and that
      distinction has never been seen in the wild. Record the exact string. A `timed out after
      10000 ms` means the budget is still short and the handshake is slower than anyone has assumed;
      a `could not connect` means the diagnosis in decision 44 was wrong about which failure it was,
      which is a thing decision 44 already says it could not prove.
- [ ] `embarch-umbrella/open.md`'s hardware-debt bullet closed or narrowed to what is still unrun.
- [ ] `features.d/umbrella-070` and `-080`'s "never been read" / "never completed on a bench"
      Status cells updated. **Read the note below before touching them.**
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Before you write a `features.d/` row for this

**`suite/features.md` has 14 bytes of headroom**, measured at leg 026's `umbrella/030` fold — see
`tasks/suite/004`'s "The prediction below fired" section. Any row you lengthen has to be paid for by
a row you shorten, in the same commit, and the failure shows up in the *supervisor's* fold rather
than in your own gate. The good news for this task specifically: recording a verdict is **shorter**
than recording that it has never been read, so this one should give bytes back.
