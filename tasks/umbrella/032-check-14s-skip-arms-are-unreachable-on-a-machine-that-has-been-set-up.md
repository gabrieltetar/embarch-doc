# 032 — Check 14's `WslHost` and `Remote` skip arms cannot be reached on a machine that has been set up

**State:** open
**Source:** supervisor bench unit `umbrella/027`, 2026-09-06 — live `embarch doctor` on the primary
`wsl-host` bench
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What was observed

Check 14 returned **`PASS every-family-covered`** with `nRF54L15=jlink, nRF52840=probe-rs,
esp32c5=probe-rs` — real output from the installed Windows service exe, run from WSL.

`embarch-umbrella/spec.md` and `decisions/doctor.md` treat check 14's `WslHost` and `Remote` arms as
states the check distinguishes. Reading `src/doctor.rs:2896-2915`, they are not verdicts about
flashing at all: **all three class arms sit inside a single `else` reached only when no
`embarch-core` binary is locatable**, and each just phrases the same skip differently. On a
`wsl-host` machine `setup` has run, so the locator finds the service exe under `/mnt/c/…`, the real
`flash-backend` arm runs, and the `WslHost` wording is unreachable by construction.

## Why this is worth recording rather than shrugging at

It is the third instance of one shape in this suite, and the pattern is what matters:

- `embarch-umbrella` decision 18's `probe-not-permitted` arm needs Core running natively on Linux;
  the primary topology has Core on Windows, so the scan is skipped and the arm is dead here.
- `embarch-topology` decision 18's branch is gated on `TopologyClass::Local` and is unreachable on
  the only topology this suite is actually used on (leg 022).
- Check 14's `WslHost` arm needs a `wsl-host` machine with **no locatable Core** — i.e. one where
  `embarch setup` has not completed, which is the state `doctor` exists to diagnose but not the
  state anyone runs `doctor` from twice.

Each is defensible on its own. Together they say that a check's *class-aware* arms are the ones
least likely to have ever run, and `spec.md`'s table gives no way to tell an exercised arm from a
worded one.

## Done when

- [ ] Either the three skip arms collapse to one message plus the class name — they differ only in
      prose and none has been observed — or each keeps its wording with a note saying which are
      unreachable on a set-up machine, so nobody reads them as distinguished states.
- [ ] `spec.md`'s check-14 row stops implying the class arms are flashing verdicts. They are
      "could not ask Core" phrased three ways.
- [ ] The general question gets an answer somewhere durable: **how does a reader of `spec.md`'s
      check table tell an arm that has run from an arm that has only been written?** This is now
      the third example; it is a table-shape question, not a check-14 question.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
