# 014 — The FFI staticlib is cross-compiled on every board build to deliver one `u32`, and decision 7 is false in three ways

**State:** open — announced 2026-09-11 23:25 by leg 093, `ts` `1789190751.574569`, 30-minute window per
`embarch-fleet/ops.md` §4 (closes 23:55:51 local). If this leg ends before the window closes, **read the
thread and complete the window rather than restarting it.**
**Source:** suite review pass 2026-09-06, dimensions 6 and 1 (one finding from two sides). Code-confirmed, with a whole-suite caller grep.
**Scope:** suite
**Hardware:** none for the doc half. The CMake half cannot be built in a worker's worktree — see `Hardware` note below.
**Owner:** no

## What

Two halves of one thing, filed together because fixing either alone leaves the other reading as
true.

**1. The staticlib has collapsed to one constant accessor, and the constant already has a
cheaper, staleness-proof source in the same file.**
`embarch-dev-bench/app/CMakeLists.txt:162-202` cross-compiles
`cargo rustc --release --target … --features ffi --lib --crate-type staticlib` on **every
non-POSIX build**, re-invoked every build (`:190-192`: *"No CMake-tracked dependency list for
this custom target"*). `embarch-dev-bench/app/src/main.c` calls exactly one FFI function —
`study_ffi_schema_version()`, at `:1091` and `:1555` — which returns
`DEV_BENCH_WIRE_SCHEMA_VERSION`. The same `CMakeLists.txt` at `:120-146` **already reads that
constant out of `${ESSD_DIR}/src/schema_version.rs` at configure time** with
`CMAKE_CONFIGURE_DEPENDS` — currently gated `if(CONFIG_ARCH_POSIX)`, so the cheap mechanism
serves `native_sim` and the real boards pay a Rust cross-toolchain for the same number.

The two functions the ABI exists for have **no caller anywhere**: grepped all nine repos plus the
doc corpus for `essd_|study_ffi_|staticlib|cbindgen|--features ffi`; `essd_study_decode_and_verify`
and `essd_study_decode_full` appear only in their own definitions, their `study_ffi_real.c`
trampolines, and doc comments. `main.c:1341-1347` says why in the code: *"`steps_crc` was already
verified during decode … why this needs no FFI round-trip into that crate to get the identical
answer `essd_study_decode_and_verify` would."* And the surface can only decode a study shape the
Study Designer can no longer author — `src/ffi.rs:57-60` scopes it to `BleAdvertise`-only steps
*"for now (decision 21's initial pass)"* while `main.c:1330-1339` dispatches nine action kinds.

Retiring it removes, counted: the `add_custom_target` + `target_link_libraries` + the two-arm
board-to-triple map + the `ESSD_LIB` path derivation; the `ffi = []` Cargo feature
(`embarch-study-designer/Cargo.toml:79`) — enabled by no manifest in the suite; `src/ffi.rs`
(19,773 bytes) with its `#[panic_handler]`, `EssdStatus` and three `#[repr(C)]` study types; the
`ffi` cell in study-designer's CI matrix; `study_ffi_real.c`; `study_ffi.h`'s three mirrored
struct copies and **four** hand-mirrored `STUDY_FFI_MAX_*` constants; `study_ffi_stub.c`'s dead
sibling arms; the real-vs-stub CMake split; and `embarch-study-designer/open.md`'s standing
"nothing proves the FFI staticlib actually cross-links" obligation. **Nine moving parts plus four
mirrored constants.**

**2. `embarch-study-designer/decisions/crate.md:27` (decision 7) is false in three ways, and
those three claims are what make the staticlib read as load-bearing.**

- *"`cbindgen` generates the C header from the Rust source **so it cannot drift by hand**"* —
  `cbindgen` appears **nowhere in any repo**, except as an open to-do at
  `embarch-study-designer/README.md:52`. `study_ffi.h` is hand-written and re-declares the
  `essd_*` signatures a second time inside `study_ffi_real.c` (*"both sides are kept in sync by
  hand"*).
- *"C calls into it rather than re-implementing the wire format, which is what stops this
  becoming the three-independent-definitions problem decision 1 exists to avoid"* — the
  re-implementation is shipped and is roughly 3,000 lines: `serial_protocol.c` (2,066 lines of
  hand-written `pc_read_varint`/`pc_read_zigzag`/COBS/CRC-32 postcard decode), `eap.h` (333
  lines, *"Mirrors `embarch-study-designer/src/eap.rs` field for field"*) and `eap_interp.c`
  (609 lines).
- The reverse claim, also false: `embarch-study-designer/open.md:35` says the cross-link is
  unproven because *"that build root does not exist"*; `README.md:53` says the toolchain and
  header generation *"remain open, blocked on that hardware existing"*; `Cargo.toml:13` says the
  target and panic handler *"don't exist yet"*. All three landed —
  `embarch-dev-bench/decisions/platform.md:33` records decision 8 as closed on the shipping bench
  and `src/ffi.rs:38` has the panic handler.

**3. Cut the precedent loop at one end.** `src/ffi.rs:180-184` justifies keeping the no-caller
surface by citing `embarch-topology`'s posture toward `validate_signal`; and
`embarch-topology/decisions/links.md:41` justifies keeping `validate_signal` by citing *"the same
posture the suite takes toward `embarch-study-designer`'s advertise-scoped decode surface."* Each
cites the other; neither has an independent reason.

Candidate direction: retire the two no-caller decode functions and their mirrored C structs and
constants outright. Then settle whether the staticlib earns its place for one `u32` — lifting the
existing `schema_version.rs` read out of the `CONFIG_ARCH_POSIX` guard would serve every board
the same way and take a Rust cross-toolchain out of the firmware build. Correct decision 7's
three claims in the same pass, whichever way the staticlib goes. `validate_signal` then needs a
reason of its own or the same treatment.

## Why now

Whoever next bumps a wire type reads the owning crate's decision record and is told a generator
prevents C-side drift and that C does not re-implement the wire format — both false, in the
direction that makes the mirrors look safe. Every check is blind: nothing here is broken, it
compiles, it links, and it returns the right number. And a third vendor family cannot be ported
until someone adds a Rust target-triple arm (`CMakeLists.txt:184` is a `FATAL_ERROR`).

## Done when

- [ ] `essd_study_decode_and_verify` and `essd_study_decode_full` are gone, or a caller exists.
- [ ] `embarch-study-designer/decisions/crate.md` decision 7 states what the boundary actually
      is: no `cbindgen`, a hand-written C codec pinned by the cross-side byte tests, and a live
      staticlib link.
- [ ] `open.md`, `README.md` and `Cargo.toml`'s "does not exist yet" claims are retired.
- [ ] Whatever `study_ffi.h` still declares is **derived** from `limits.rs`, not typed — the
      `schema_version.rs` reader at `CMakeLists.txt:120-146` is the precedent.
- [ ] `embarch-topology`'s `validate_signal` keep-reason no longer cites this surface.
- [ ] Gate green; `changelog.d/` fragments for both repos.

**`Hardware:` note for the supervisor.** The `embarch-study-designer` half — retiring `ffi.rs`,
the Cargo feature, and decision 7's three claims — is `none` and dispatchable. The
`embarch-dev-bench` CMake half is `toolchain`: that repo's Zephyr tree is gitignored, so a
worker's worktree cannot build it (`tasks/README.md`, Hardware field). Split it if that is
cheaper than running the CMake half by hand.
