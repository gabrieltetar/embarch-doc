# Atlas notes: the measured plane

**Status:** draft, 2026-11-15.

## What feeds it

**Live findings only.** A Live answer that settles something the documents left open becomes a `measured` fact, as [the HIL notes](../hil/05-live.md#writing-a-finding-back) already decided; **Studies and Tests stay in their published zips, and the atlas links them.** Chosen over all three modes writing records, and over Live and Test.

## A measured fact

- **How it was measured**: `via: live`, or `via: study` / `via: test` with the zip's hash and Core's run-log entry holding that zip's manifest hash, the atlas running `verify` on the zip when it uses the fact ([HIL notes](../hil/05-live.md#writing-a-finding-back), HIL review round 3, owner 2026-11-19); **a `via: live` fact is answered as development evidence**, so a Live result cannot be cited through the atlas ([HIL notes](../hil/05-live.md#writing-a-finding-back), owner, HIL review round 1).
- **Its receipt**: the live call, the unit (its MCU's unique ID, and through it the board revision and reworks, [02](02-hardware.md#units)), the image hash (Core's `last_images`), the time, and **Core's call-log entry, the record**, with the live-log line, its mirror, beside it ([HIL notes](../hil/05-live.md#the-live-log), HIL review round 4, owner 2026-11-20).
- **Shown beside the claim it bears on**: a datasheet's value, a design claim, a netlist connection. **A disagreement is a check finding** ([09](09-interactions.md)).
- **Measured on other hardware or another image is written, never refused**, and shown as such: the image rule is the HIL notes', the hardware rule follows from the target declaring its hardware ([02](02-hardware.md#which-hardware-an-atlas-joins-against)).
- `measured` is already a provenance class (`embarch-atlas` repo, `DESIGN.md`, "Records"); nothing writes it yet.

## Open

- **The write-back verb and MCP tool, and their fields.** Left to this rework by the HIL notes. Recommended: one verb, given Core's call-log entry, the fact or entity it bears on, and the value read; the receipt is filled in from that entry, the live-log line beside it.
- **The link to a Study or Test**: the zip's path and hash, the run, the unit and the image, attached to the facts it bears on. Its shape.
- **Where measured records live once planes are shared** ([01](01-planes.md#open)).
