# 105 — A live finding is written back to the atlas as a measured fact

**State:** open
**Source:** Fleet Ready issue (owner): `measured` is a provenance level in the atlas's records, and nothing writes it
**Issue:** EMB-267
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

`measured` is a provenance level in `src/embarch_atlas/records.py` and
`schemas/record.schema.json`, and nothing writes it. The design
(`notes/hil/05-live.md`, "Writing a finding back"): a live answer that settles
something the datasheet or schematic left open becomes a `measured` fact, with
its receipt. `notes/atlas/08-measured.md`, "Open", left the verb's name and
fields to the atlas and recommended one verb. It is step 2 of
`embarch-atlas-planes-proposal.md`, "Order". The owner put it in the Live
phase on 2026-11-23.

When this is done, there is one CLI verb and one MCP tool (their names are this
unit's call) that write a measured fact:

- **Inputs:** Core's call-log entries, the fact or entity the finding bears on,
  and the value read.
- **The receipt comes from Core's entry**, read through `embarch-api
  call-log`, never from the caller: the live call, the board, the time, and
  Core's entry, with the live-log line beside it. Where the caller and Core's
  entry disagree, Core's entry wins. An entry Core does not hold is refused.
- **The image:** "read back" when `image_check` matched the pinned build, else
  "as last flashed by Core" from `last_images`, else "unknown". Reuse the
  `last_images` lookup `atlas/104` adds. A finding measured on another image is
  written, never refused, and marked "measured on a different build".
- **`via: live` only.** `via: study` and `via: test` wait for the attested
  phase, whose fingerprint file their check needs.
- **Append-only**, as the measured plane is.

Read the `notes/` files and the proposal; do not edit them.

## Why now

The next session answering a hardware question from the atlas needs the
finding, and the following unit compares a measured value with the datasheet
(EMB-268, waiting on this).

**Was parked behind `atlas/104`**, which landed on 2026-11-23: both change the
live-log line, and this unit's image lookup and receipt build on 104's. 104 put
the `last_images` lookup in `src/embarch_atlas/livelog.py` (`image_sha256`) and
made a decoded line follow only a call that cited Core entries.

**Burndown leg: no new numbered decision.** `embarch-atlas/design.md` and the
repo's `DESIGN.md` "Records" and "Live" are amended in place. If the work needs
a new decision, stop and say so in this file and in your report.

## Done when

- [ ] A fixture write-back writes a schema-valid `measured` record with `via: live` and a receipt whose call, board and time come from Core's entry.
- [ ] A write-back citing an entry Core does not hold is refused.
- [ ] One measured on another image is written, marked "measured on a different build", its image named "read back" or "as last flashed by Core".
- [ ] `DESIGN.md` and `embarch-atlas/design.md` document the verb, the tool and the record.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet), in the worktree's own venv, with `test_public_guard` running.
- [ ] `changelog.d/` fragment dropped.
