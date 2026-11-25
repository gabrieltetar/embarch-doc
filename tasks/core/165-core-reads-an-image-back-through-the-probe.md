# 165 — Core reads an image back through the probe and says which state holds

**State:** claimed by agent/core/165-core-reads-an-image-back-through-the-probe, 2026-11-25 15:44
**Source:** EMB-362 — Core cannot read an image back through the probe
**Issue:** EMB-362
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

No readback path exists. `POST /live/mem-read` reads at most `MAX_WORDS` (256)
words under a halt (`src/live.rs`), and every signed record says
`image_status: "unverified"` (`src/signing.rs`). The HIL design reads the DUT's
image back through the probe and compares its segments with what Core flashed,
and compares every bench board's image with the released bench-firmware list
(`embarch-doc/notes/hil/03-test.md`, "A run", item 3). The smoke check, the
run record and every report's "Observed by Core" line wait on this. When this
is done:

- **`readback(board) -> ImageStatus`**, behind the `CoreAccess`-style trait
  `live.rs` already uses, so it is tested without a board. It reads each
  segment of the newest `flashed-images.jsonl` entry for the board (decision
  93, `FlashedEntry.segments`) in chunks and hashes it. A readback halts the
  core only as long as a chunk takes, as `mem-read` does, and writes nothing.
- **The DUT**: `holds` (every segment matches), `differs` (naming the first
  range that does not), or `claim` with the reason (read-out protection, no
  probe, no entry since this store began, an entry with no segments).
- **A bench board**: its identity (`hil_image::identity` over the read-back
  segments) against `bench-firmware.json`, which Core reads from the path in
  `EMBARCH_BENCH_FIRMWARE_LIST`. A hit is `released`; a miss is `unreleased`
  with the scope of the flash that put it there, or `unknown` with no entry;
  a board with no probe is `unverified`. The variable's name is the plan's
  recommendation, and the decision says the owner may strike it for a key in
  Core's config file.
- Nothing calls `readback` from a route or a run yet; the smoke check and the
  run record are later units. Do not change what `signing.rs` writes.

## Where to look

- `src/live.rs` — `CoreAccess`, `read_ranges`, `MAX_WORDS`
- `src/lease.rs` — `FlashedEntry`, `ImageDetail`, `image_detail`
- `embarch-study-designer/src/hil_image.rs` — `Segment`, `identity`; read only
- `embarch-doc/embarch-core/decisions/lease.md` (93) and `live-read.md`
- `embarch-doc/notes/hil/03-test.md`, "A run", item 3;
  `notes/hil/06-report-and-publish.md`, "The audit appendix"

## Where the doc goes

A new decision in a new topic file (an `image-readback.md` or similar) and an
`interfaces/` entry for the states and the variable. `check-doc-size.py
--pressure` lists signing#110 and lease#93 over their limits, and run-log#111
and instruments#104 near theirs: do not grow those, cite them. No `embarch-core`
file is in reserve at filing; if your work pushes one in, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

## Hardware verification

**Not measured**: whether a whole image reads back through the probe on each
chip family the suite targets, in particular on a family Core flashes with its
vendor tool rather than through the probe library (flash backend decisions 36,
49, 52 and 54). A read writes nothing, but its behaviour there is unknown.
Leave a hardware-verification debt naming each chip family to read back, for
the first Test run on the bench.

## Done when

- [ ] Against a fake `CoreAccess`: every segment matching gives `holds`; one
      changed word gives `differs` naming its range; a refused read gives
      `claim` with the reason.
- [ ] A bench board whose identity is in a fixture list gives `released`; one
      that is not gives `unreleased` with the recorded scope, or `unknown`
      with no entry.
- [ ] A hardware-verification debt names each chip family to read back.
- [ ] A decision and an interface doc give the states and the variable.
- [ ] Gate green. The native Windows build is a debt the owner runs.
