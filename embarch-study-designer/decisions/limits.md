# embarch-study-designer decisions: Bounded collections and type size

**Status:** active, 2026-09-02.

Why every collection is fixed-capacity, and the two passes that shrank the types. The values themselves: [../interfaces/limits.md](../interfaces/limits.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 15 — Fixed-capacity `heapless` collections, not `alloc`-based `Vec`/`String`, with a concrete constant per field

Decisions 5 and 3 committed the crate to `no_std` and an allocator-free encoding **but neither constrained its own data types**: as first drafted every collection field **required a global heap allocator somewhere in whatever links the crate — not something bare-metal C firmware guarantees.** Fixed-capacity collections pair with postcard **with no allocator anywhere in the chain**, and force a concrete ceiling onto every field — **which also serves the fuzzing case directly: a fuzzer has an explicit bound to generate within instead of being able to build a study no real MCU could hold.**

Every constant lives in one `limits` module. **Every value, with its provenance: [../interfaces/limits.md](../interfaces/limits.md).**

### 46 — `Study.steps` is a heap `Vec` on the host and stays `heapless::Vec<Step, MAX_STEPS_PER_STUDY>` on the `no_std` build

The actual fix for a stack overflow. The largest action variant carries a 512-byte payload, and **a 64-slot fixed-capacity vector is an inline array *regardless of how many steps are populated*** — [measured] roughly 38 KB moved on the stack every time a study is passed around, **for a real two-step self-test.** That crashed a debug API serving a live status call.

The mitigation that shipped (a big-stack runtime thread) works and is why a release build survived, **but it is a workaround sized against today's code and optimization level rather than against the type.** Behind an allocator feature the field becomes a heap vector and the 38 KB collapses to a pointer; **the `no_std` build keeps the fixed-capacity form it needs.**

**No schema bump.** `Vec` and `heapless::Vec` serialize identically under both postcard and `serde_json` — a length prefix then elements — so nothing crosses either hop differently and neither constant moves. Stated explicitly because "the type changed" reads like a wire change and is not one.

*Rejected: boxing each step* — shrinks the container, **adds an allocation per step, and still needs the same feature gate**, paying its cost without the simplification. *Rejected: shrinking the step limit*, the cheapest possible change, because **it reduces a real authoring limit to serve an implementation detail exactly as studies get longer** — and dev-bench's own unilateral shrink to 16 is a cautionary tale in the same pass, **since a 20-step study then passes every host check and is refused on the wire.** That divergence is dev-bench's to close; **this decision is why the host side has no reason to shrink to meet it.**

### 49 — Decision 46's newtype generalised to `Bounded<T, N>` and applied to the result types

Decision 46 fixed `Study.steps` and stopped, on the reasoning that it was the field that had actually crashed something. [Measured 2026-08-25] immediately afterwards, that was far too narrow:

| Type | Before | After |
|---|---:|---:|
| `StudyResult` | 1,293,608 | 9,024 |
| `StepResult` | 20,200 | 696 |
| `DevBenchMessage` | 20,208 | 2,128 |

`StudyResult.steps` was a 64-slot inline array of 20 KB `StepResult`s — **1.29 MB**, in a type Core assembles and `embarch-api` deserializes. `StepResult` was 20 KB because `gatt_activity` inlined 32 × 536-byte records and `gatt_services` 8 × 296, whether or not the step captured any.

**This is the one that matters most, and decision 46 did not address it at all.** Core sets a 64 MiB thread stack, and its own comment records why: **the first real study submission crashed the *release* Windows service with a stack overflow on the result path, not the study one. Decision 46's fix could not have prevented that crash.**

The newtype leaves decision 46's call sites unchanged. The captured-data field is **deliberately left alone**: at 528 bytes it is 0.5% of the old size and would touch dozens of byte-level sites for no gain — **the cut is where the inline arrays are big, not everywhere they exist.**

Still no schema bump, **now asserted for more than one element type.** One round-trip test **encodes from the newtype and decodes into the plain fixed-capacity shape — the host-encodes/bench-decodes case in miniature, and the first test here to *prove* the two agree rather than assert it in prose.** And the opposite direction is asserted too: a test **requires the `no_std` result type to stay large**, so **"make it smaller" can never be applied to the one build with no allocator to make it smaller with.**

---

