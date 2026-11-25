# 165 — Core reads an image back through the probe and says which state holds

**State:** done — readback and its states built host-side over a fake CoreAccess; decision 142; hardware debt filed
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

- [x] Against a fake `CoreAccess`: every segment matching gives `holds`; one
      changed word gives `differs` naming its range; a refused read gives
      `claim` with the reason.
- [x] A bench board whose identity is in a fixture list gives `released`; one
      that is not gives `unreleased` with the recorded scope, or `unknown`
      with no entry.
- [x] A hardware-verification debt names each chip family to read back.
- [x] A decision and an interface doc give the states and the variable.
- [ ] Gate green. The native Windows build is a debt the owner runs.

## Hardware-verification debt

Not measured: whether a whole image reads back through the probe on each chip family. For the first Test run on the bench, run `readback` (a bench-side caller does not exist yet; use a scratch call through `live::read_ranges` over the flashed segments) after a flash and compare, on each:

- **nRF54L (L15, L10, L05)**: RRAM, flashed with `nrfutil`/J-Link (decisions 36, 52), read through probe-rs; does a whole segment read back, and does a read-out-protected part give a refusal that becomes a `claim`?
- **nRF54H**: refused by the flash backend (decision 49); whether probe-rs reads it at all.
- **STM32 (G0, F4)**: flashed through probe-rs; a G0 in WFI needs the halt per chunk (decision 81); confirm a 1 KiB chunk halts in the low milliseconds.
- **esp32c5**: RISC-V; `read_ranges` reads Cortex-M's `DHCSR` first, so this needs checking before anything else.
