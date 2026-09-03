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

### 63 — `cargo test` runs the allocator-free shape, so the crate ships a 64 MiB harness stack rather than shrinking a type that must stay big

**`cargo test` aborted on `main`** — `thread 'tests::dev_bench_message_discriminants_are_pinned' has overflowed its stack`, SIGABRT, part-way through the run. Not a flaky test: it made this crate's merge gate structurally unenforceable, so a branch either landed on a red gate by exception or nothing landed at all.

The cause is the collision of two things decisions 46 and 49 each got right separately. **`cargo test` builds with *default* features, which is the allocator-free `no_std` shape dev-bench links** — the one configuration where the inline arrays are mandatory and where `the_no_std_build_keeps_its_fixed_capacity_arrays` deliberately forbids shrinking them. Decision 49's table reports the host shape; the default shape is a different set of numbers entirely:

| Type | default (`no_std`) | `alloc` / `std` |
|---|---:|---:|
| `DevBenchMessage` | 75,288 | 2,128 |
| `Study` | 83,512 | 1,080 |
| `StudyResult` | 202,536 | 824 |

All [measured 2026-09-02]. A debug-profile test that builds four `DevBenchMessage`s copies each of them tens of times, and libtest gives every test thread 2 MiB. [Measured] on rustc 1.97.1: 2 MiB and 3 MiB abort, 4 MiB passes 108/108.

**So the type is genuinely oversized and that is the requirement, not the defect** — under `alloc` it is already 2 KB, and the 75 KB form exists precisely because dev-bench has no allocator. Of the three fixes available, two are unavailable here: *shrinking the type* reverses decision 15 for the only build that cannot afford it, and *boxing the value in the test* needs `alloc` that this configuration does not have, fixes one test, and leaves every other test that touches a `StudyStart` sitting on the same cliff — the measured margin says the worst one was already within 1 MiB of it. The remaining fix is `.cargo/config.toml` setting `RUST_MIN_STACK`.

**64 MiB, because that is the number `embarch-core`'s runtime already uses for this same class of value** (decision 49) — one figure to remember rather than two, and 16x over the 4 MiB actually needed, deliberately, since the measured need moves with the debug profile and the compiler version. Thread stacks are reserved and not committed, so it costs address space. Cargo resolves config from the invocation directory, so it applies to developing this crate and **not** to `embarch-core`/`embarch-api` building it as a dependency. `force` is off, so `RUST_MIN_STACK=2097152 cargo test` still reproduces the overflow.

**This is the fix decision 46 warned about, and it is chosen with that warning read.** Decision 46 called Core's big-stack mitigation "a workaround sized against today's code rather than against the type", and it was right — because on the host the type *could* be shrunk, and was. Here it cannot be, so the same shape of mitigation is the answer rather than the deferral. What keeps it from silently papering over unbounded growth is a **ceiling test on the `no_std` `DevBenchMessage`**, the counterpart to decision 49's floor: the inline shape may be big, but past ~3.5x today's size it fails as a named assertion instead of as a SIGABRT that takes the whole binary down mid-run.

---

