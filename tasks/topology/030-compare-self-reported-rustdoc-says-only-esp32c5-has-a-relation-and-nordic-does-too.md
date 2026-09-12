# 030 — `compare_self_reported`'s rustdoc says only `esp32c5` has a declared relation; the Nordic arm is right below it

**State:** claimed — leg 089, 2026-09-11.

**Doc-size reserve for `topology`:** nothing in this sub-project is in reserve. If your work pushes a
file into its last 10% of cap, file `tasks/topology/<NNN>-compact-topology.md` in the same commit.

**Source:** refill sweep for scope spread, leg 089, 2026-09-11; the contradiction was re-read
directly against the source by the supervisor before filing, not taken from the sweep's report.
**Scope:** topology
**Hardware:** none. This is a documentation correction about which code arms exist — it is settled by
reading `compare_self_reported`, not by attaching silicon, and **nothing in this task authorises
claiming a measurement.** See the sharp edge below.
**Owner:** no

## What

`embarch-topology/src/hardware/hardware_id.rs:169` says, in bold, inside the rustdoc for
`compare_self_reported`:

> **`esp32c5` has a declared relation; nothing else does.**

and reinforces it fourteen lines later at `:180`:

> Every other chip returns [`SelfReportedIdentity::Undeclared`], which is **not** a pass …

The function directly beneath that comment has **two** declared arms:

```rust
let expected = match chip {
    "esp32c5" => esp32c5_expected_self_report(jtag_read),
    c if is_nordic_deviceid_chip(c) => nordic_expected_self_report(jtag_read),
    _ => return SelfReportedIdentity::Undeclared,
};
```

So every chip `is_nordic_deviceid_chip` classifies — the `Nrf54InfoDeviceId` and `NrfClassicDeviceId`
families — gets a real `Match`/`Mismatch`, not `Undeclared`.

**The docs outside the crate already have this right.** `embarch-topology/spec.md:83` says *"Two chip
families have a declared relation"*. So this is a stale *crate* comment disagreeing with the
sub-project's own spec, and the stale one is the one a maintainer reads while standing in the code.

## What to do

Correct the rustdoc so it describes both arms, and keep what makes the comment valuable: the
*standard* it sets — an arm is only writable when the transform is derivable from both
implementations' actual register reads, never guessed — is the reason this comment is long, and it
must survive. The `esp32c5` derivation paragraph is not the thing that is wrong and should not be
rewritten for its own sake.

**Say for the Nordic arm what the `esp32c5` paragraph says for that one**: what makes the relation
derivable rather than guessed. Take it from what is already written down — `embarch-topology`'s
`decisions/` and `spec.md` carry the nRF54L device-ID work — and **cite it rather than restating it
at length**.

**Then check the rest of this file's prose against its own code** for the same shape. A comment that
describes one arm of a `match` that has since grown a second is a drift signature, and
`is_nordic_deviceid_chip`, `nordic_expected_self_report` and `SelfReportedIdentity`'s own docs are
where a second instance would be. Report what a pass finds in this file even if the answer is
nothing.

## The sharp edge — read this before you write a word

`embarch-topology/open.md` says the nRF54L device-ID address is **confirmed on one board**, and that
two things stay open: the DUT's own readback has no independent corroboration, and
`nRF54L10`/`nRF54L05`/`nRF54LM20A` take the same arm **with no silicon ever attached**.

So the corrected comment must say that the Nordic arm *exists and is declared*, and must **not** say
or imply that it has been verified across that family. Those are different claims and this suite has
paid for conflating them before. Every field this suite records is either measured or stated, and
promoting the second to the first is the one error this task could introduce. If you cannot source a
claim from an existing decision or from the code itself, leave it out and say so here.

## Why now

`compare_self_reported` is the function whose entire job is saying whether a board's self-report and
its JTAG read describe the same silicon — the same-chip check. A maintainer deciding whether that
check is meaningful for the board in front of them reads this comment, and for **the only silicon
actually on this bench** it currently tells them the answer is an unverified `Undeclared`. That is
the reading most likely to make someone skip a real check.

This is also the fourth doc-versus-code count or enumeration defect in three days
(`umbrella/037`, `core/042`, `umbrella/054`, now this). Nothing in the gate can see any of them.

## Done when

- [ ] The rustdoc describes both declared arms and no longer says `esp32c5` is the only one.
- [ ] The derivability standard the comment sets is preserved, not lost in the edit.
- [ ] The Nordic arm's justification cites existing `embarch-topology` docs rather than restating
      them at length, and **claims no verification that `open.md` says has not happened**.
- [ ] A pass over the rest of `hardware_id.rs`'s prose for the same drift shape is reported here.
- [ ] No behaviour changes: no arm added or removed, no function signature touched.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
