# embarch-study-designer: an image's load segments and identity

**Status:** active, 2026-11-24 (EMB-357, `tasks/study-designer/090`). Code: `src/hil_image.rs`, feature `hil-image` (needs `alloc` and `sha2`, host-only; nothing turns it on yet); fixtures `tests/fixtures/hil-image/`, tests `tests/hil_image.rs`. No new decision: the design is the one `notes/hil/14-implementation-plan.md` recommends, and the owner kept it. Consumers: Core's record of what it flashed and its readback, the script writing the bench-firmware list, a bench board's characterisation ([hil-characterisation.md](hil-characterisation.md)), and `verify`.

A chip holds load segments, not a hex or ELF file, so a readback cannot compare with the SHA-256 of the file Core was given. This file is the one definition of what an image is.

## The segment rule

`image_segments(bytes, format, base) -> Result<Vec<Segment>, ImageError>`, `format` `Hex`, `Elf` or `Bin`. The result is the **maximal contiguous address ranges the image writes**, sorted by address, each `{address, length, sha256}` (`sha256` the lowercase hex SHA-256 of that range's bytes). Records or segments that touch (one ends where the next begins) are one range; a gap, however small, makes two; two that overlap are an error (`Overlap`), not a merge.

- **Hex** (Intel HEX): data records (type 00) at the offset plus the extended segment (02) or linear (04) base; end-of-file (01) ends it; start-address records (03, 05) are ignored. A bad checksum, byte count or digit is an error naming the line.
- **ELF** (32 or 64 bit, either byte order): the `p_filesz` bytes of each `PT_LOAD` segment at its **physical address** (`p_paddr`). Bytes past `p_filesz` (zero-filled `.bss`) are not written to the chip and are not in the list. So a hex and an ELF of one build give the same list. Every offset sum and product read from the headers is checked (`checked_add`, `checked_mul`): a program-header table position, or a segment's offset plus size, that overflows `u64` or `usize` is `ImageError::Elf("truncated")` or `"segment outside the file"`, never a debug-build panic (EMB-397, `tasks/study-designer/091`). Addresses are checked as well as offsets: a range (ELF segment, hex record or bin at its base) whose start plus length passes `u64::MAX` is `ImageError::Overlap(address)`, not a panic (EMB-399, `tasks/study-designer/092`).
- **Bin**: one range at `base`, which a bin requires (`NoBase` otherwise); an empty bin gives no range.

## The identity

**The SHA-256 of the canonical JSON of the segment list**, lowercase hex: `identity(&segments)`. Canonical JSON is the array of `{"address":N,"length":N,"sha256":"…"}` with the keys in that order, numbers in decimal, and no whitespace (`canonical_json`). Two images have one identity if and only if they write the same bytes at the same addresses.

## `bench-firmware.json`

`BenchFirmwareList`, which the release ships and the bench-firmware script writes:

```json
{ "schema": 1, "release": "…",
  "images": [ { "app": "…", "board": "…", "version": "…", "commit": "…",
                "identity": "…", "segments": [ { "address": 0, "length": 0, "sha256": "…" } ] } ] }
```

`identity` is the identity of that entry's `segments` (`BenchImage::identity_consistent()` checks it). A bench board's image is compared with the entry for its `board` by identity, and by segments when the identity differs, to say which range did. **`Segment`, `BenchImage` and `BenchFirmwareList` refuse an unknown key** on deserialisation (`deny_unknown_fields`), as `interfaces/hil-shapes.md` asks of every HIL JSON file.

## The example

`cargo run --features hil-image --example image_segments -- <file> [base]` prints `{"identity":"…","segments":[…]}` for a `.hex`, `.elf` or (anything else, with `base`) bin file: what the list's script calls.

## Fixtures

`fixture.elf` is `a.S` linked by `l.ld` (two `PT_LOAD`, at 0x20000 and 0x20400, so a gap); `fixture.hex` is `objcopy -O ihex` of it and `fixture_a.bin` is `objcopy -O binary --only-section=.a`. 536, 301 and 60 bytes, committed deliberately (an x86-64 ELF stands in for firmware: the rule reads only program headers).
