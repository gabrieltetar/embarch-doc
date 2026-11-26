# embarch-core decisions: Reading an image back

**Status:** active, 2026-11-25.

Index: [../decisions.md](../decisions.md). States and the variable: [../interfaces/image-readback.md](../interfaces/image-readback.md). The design it serves: [HIL test](../../notes/hil/03-test.md) ("A run", item 3).

### 142 — `readback` reads a board's flashed segments back through the probe and says which state holds

Every signed record says `image_status: "unverified"` (decision 110) because Core had no way to read an image back; `POST /live/mem-read` stops at 256 words. This adds the function, `src/readback.rs`, which the smoke check calls before a bench's first test ([143](smoke-check.md)); the run record is a later unit, and `signing.rs` is unchanged. It is not a route.

**What it reads.** The segments of the board's newest `flashed-images.jsonl` entry (decision 93, `FlashedEntry.segments`), each in chunks of at most `MAX_WORDS` words, hashed with SHA-256 over exactly the segment's bytes (an unaligned start or length reads the covering words and trims). Each chunk is one `live::read_ranges` call, so the core halts only as long as one chunk takes (decision 81) and nothing is written. The probe sits behind `CoreAccess`, so every state is tested against a fake memory.

**The DUT: `holds`, `differs`, `claim`.** `holds`: every segment matches the one flashed. `differs`: names the first segment, by address and length, whose hash does not. `claim`, with the reason: a refused read (read-out protection included), no probe, no entry since this store began, or an entry with no segments (a format `image_detail` does not read). A claim is Core declining to say, never a mismatch.

**A bench board: `released`, `unreleased`, `unknown`, `unverified`.** The read-back segments give an identity (`hil_image::identity`), looked up in `bench-firmware.json`. A hit is `released`, naming app, board and version. A miss is `unreleased`, carrying the scope of the flash that put the image there (decision 93's `scope`). No entry, or an entry with no segments, is `unknown`: with no recorded ranges there is nothing to read. No probe, a refused read, or no list loaded is `unverified`, with the reason.

**Where the list comes from.** The path in `EMBARCH_BENCH_FIRMWARE_LIST`, schema checked. The name is the HIL plan's recommendation; the owner may strike it for a key in Core's config file, and nothing else depends on the spelling.

**Only the newest entry per chip.** `ImageLog` keeps one entry per chip, not per probe, so two boards of one chip share an entry. Choosing the entry by probe serial is the caller's job when a route arrives; this unit takes the entry as an argument.

**Verified:** unit tests over a fake memory only. **Not measured: whether a whole image reads back through the probe on each chip family** (flash backend decisions 36, 49, 52, 54). Debt in `tasks/core/165`. Cites signing#110 and lease#93, which are over their limits and do not grow.
