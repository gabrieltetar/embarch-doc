# embarch-outpost decisions: Manual markers

**Status:** active, 2026-09-10.

Build-registered marker IDs, and why the manifest table that names them keeps
getting deleted.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 6 — Manual markers with build-registered IDs, and the same registration generates the manifest

The engineer declares their markers in one place, and **that declaration is simultaneously what makes a marker call compile and what puts its name in the manifest. An unregistered ID is a build error, not a mystery integer on the host.** No strings cross the wire.

**Keeping that table in the image is a real problem, not a formality.** *Nothing in the firmware reads it* — the generator reads it out of the ELF — **so section garbage collection deletes it and the build still succeeds**, producing a manifest with zero markers and a trace whose markers are bare integers, **with no error anywhere to say why.** Two mechanisms fail: **the iterable-section API looks exactly right and has no effect on the template linker-script path both real targets use**, and a keep directive **survives the Zephyr link and is collected out again by the host link on a native build.** What holds everywhere is **a volatile pointer to the table, read once at init** — a relocation from a section the compiler may not elide.

*Rejected: also overriding Zephyr's stock marker API for compatibility with DUT code already using it.* That API takes a **runtime string pointer**, which means either interning strings on the DUT or putting them on the wire — **both re-introducing exactly the cost CTF was rejected over.** A DUT wanting outpost markers writes outpost markers.
