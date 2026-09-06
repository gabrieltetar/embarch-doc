# embarch-study-designer: open questions

**Status:** active, 2026-09-02.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Deferred with power profiling, at the repo owner's call

Power profiling as a whole moved out of the near sequence, and no front-end hardware gets ordered. These are **deferrals with a named trigger — power profiling resuming — rather than questions waiting on someone to answer them.**

- **The physical bench design** — what BLE radio, what power-sampling hardware, connector and form factor. Decision 24's front-end pick is provisional and unordered.
- **Whether one `Sample` per capture instant is the right grain**, or a genuinely multi-lead sensor needs several. The CSV row *shape* is locked and unaffected; the open half was always downstream of what the hardware turns out to be. **Answering it speculatively would be designing against imagined data.**

## Unvalidated against real hardware

- **The bench's UTC clock-resync accuracy.** Resync happens only on a handshake, so drift between resyncs — and whether it is acceptable for post-hoc analysis — is unmeasured. Core's own arrival stamp gives analysis the raw material to *detect* drift after the fact, but does not correct it or say how much is acceptable. **That judgment needs real hardware.**

## Parsed and pinned, with no consumer

- **`repeat`, `bitpack`, `crc32` and `fixed`.** They lower into a frame rendering that today only produces a layout for the flat cases; the bit-unpacker, the counted walker and the CRC check are **the render half, and are not written.** Deliberately so — **a rendering written before any real capture exists would be tested against synthetic bytes, which is exactly what decision 48 removed post-hoc validation for.** The tests pin that each primitive *parses into the right shape*, so the gap is a missing consumer rather than a silent misparse waiting to surface.

## Missing authoring paths

- **`Study.protocols` has no path in the Study Designer UI.** Parse and resolve are public and the field is plain, so a study can carry a protocol programmatically or from hand-authored JSON; the builder emits an empty list, because the row type has no protocol variant and **inventing one ahead of the first real manifest would be designing against imagined authoring.**

  **The trigger fired on 2026-08-27**: a real engineer wrote a real manifest against a real DUT, driving its Batch Data Service through 34 request/pump/consume cycles on a live link. It was authored by hand and resolved programmatically, exactly as this said was possible — and **the study was built by a throwaway Rust program calling this crate rather than by anything in the suite**, which is the gap. Now with a worked example of what the missing path would have to produce. Two things that first manifest taught are recorded in [interfaces/eap.md](interfaces/eap.md).

## Scoped narrow on purpose

- **The GATT extractor is scoped to one firmware's macro convention** — generic at the trait boundary, deliberately narrow at the implementation, at the repo owner's explicit call. A second firmware's extractor is new work, **not a generalization of this one**. Narrowed further by decision 57: the hardcoded filenames are gone, so what remains project-specific is only the convention that a 128-bit UUID reaches its type through a particular macro shape. The name is kept because it is a value in real configs and because that remaining assumption is real.
- **Live BLE dispatch of every action this crate declares is dev-bench's scope, not this crate's** — a deliberate split, and the same one that shipped the discovery and monitoring wire types here while the radio work happened there.

## Not exercised by any routine check

- **Nothing proves the FFI staticlib actually cross-links.** CI covers six feature cells on every push (decision 64), and `--features ffi` type-checks the `extern "C"` surface on the host — but what dev-bench consumes is a `--crate-type staticlib` for a Cortex-M33 soft-float triple with a panic handler, and **that build root does not exist**, so no step can assert it. A cross-compile job added before the toolchain would be a step unable to fail for the reason it was added. **Closed by the dev-bench cross-build landing**, not by this repo alone.
