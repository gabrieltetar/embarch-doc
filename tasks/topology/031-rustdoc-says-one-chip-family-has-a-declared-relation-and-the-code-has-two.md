# 031 — The rustdoc says one chip family has a declared relation; the code has two

**State:** done
**Source:** refill sweep for scope spread, leg 091, 2026-09-11. **Line numbers are as the sweep
reported them — re-check each against the source before you act on it.** The sweep verified every
checkable claim in this sub-project's `spec.md`, `decisions.md`, `open.md` and `decisions/*.md`
against the code and found **no drift there** — both findings below are on the crate's *other* doc
surface, the rustdoc that consumers read.
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

**1.** `src/hardware/hardware_id.rs:169` says **"`esp32c5` has a declared relation; nothing else
does."**, and :181 says "Every other chip returns `Undeclared`". The match at :194-195 has an
`"esp32c5"` arm **and** `c if is_nordic_deviceid_chip(c) => nordic_expected_self_report(jtag_read)`.
This is pre-decision-21 text left in place when the Nordic arm landed; `spec.md:83` ("Two chip
families have a declared relation") and `decisions/validation.md:145` both describe the code
correctly.

**2.** `src/hardware/port.rs:79-81` documents `detected_by` as returning `"segger-vid-match"`,
`"espressif-vid-match"` or `"silabs-vid-match"` when `select` ran with its VID gate on, and :163
says a `NoRecognizedVid` exclusion means no port reported one of the **three** recognized link VIDs.
The gate at `port.rs:404` is `filter.no_vid_gate || matches!(c.vendor_id, Some(SEGGER_VID) |
Some(SILABS_VID))` — Espressif is deliberately excluded, and the `NotFound` message at `port.rs:234`
says why ("Espressif's native USB-Serial/JTAG is JTAG-only"). With the gate *off*, `detected_by` is
overwritten to `DECLARED_SERIAL` at :413, so `"espressif-vid-match"` is unreachable in every regime.

## Why it costs something

Finding 1's function is the one whose doc states the standard for adding an arm, so a reader
auditing gate coverage from the rustdoc concludes the Nordic bench runs undeclared — when that arm
is exactly what guards two same-family boards on one bench. Finding 2 invites a consumer to write a
dead Espressif branch, and sends someone debugging a missing ESP32 port hunting a gate bug three
lines above the intentional two-VID rule.

## What to do

Correct both doc comments against the code, reading the code first. **Change no behaviour**: do not
add Espressif to the VID gate — `port.rs:234` records why it is out, and adding it would be a
numbered decision, which this task does not authorise. Keep the "three recognized VIDs" sentence
honest about which two the gate admits and what the third is for.

## Done when

- [x] `hardware_id.rs`'s doc names both declared families and still states the standard for adding
      an arm. Already correct as of `cc8bab9` (topology/030) by the time this task ran — re-checked
      against the current source, and finding 1's quoted text ("`esp32c5` has a declared relation;
      nothing else does.") is no longer present. No edit made here.
- [x] `port.rs`'s `detected_by` list and its `NoRecognizedVid` sentence describe values that are
      actually reachable, with the Espressif exclusion explained rather than silently dropped.
- [x] No behaviour change, no new numbered decision.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
