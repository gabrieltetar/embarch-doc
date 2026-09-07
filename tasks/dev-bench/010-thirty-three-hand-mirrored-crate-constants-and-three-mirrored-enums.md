# 010 — 33 `embarch-study-designer` constants and three wire enums are hand-typed in dev-bench's C headers, and the deriving mechanism already exists in the same CMakeLists for exactly one of them

**State:** open
**Source:** suite review pass 2026-09-06, dimension 2 (DRY across modules). Code-confirmed.
**Scope:** dev-bench
**Hardware:** toolchain — the change is CMake and headers, and this repo's Zephyr tree is gitignored, so a worker's worktree cannot build it (`tasks/README.md`, Hardware field). In the main checkout the `app/tests/serial_protocol` ztest suite builds for `native_sim` in about a minute.
**Owner:** no

## What

`app/src/serial_protocol.h:21-25` states the standing promise: *"Mirrors embarch-study-designer's
`limits::MAX_FIRMWARE_VERSION_LEN` / `MAX_LOG_LINE_LEN` / … — **kept in sync by hand until
decision 8's west-module wiring lets this firmware pull the constants directly from that
crate**."* Decision 8 landed; the pull did not.

Counted: **27 distinct crate constants, spelled 37 times across four headers** —
`serial_protocol.h:26,30,31,32,33,56,57,62,63,87,100,113,575` (13),
`ble_bridge.h:64,65,66,153,216,217,236,434` (8), `study_ffi.h:49-52` (4),
`eap.h:66-71,79,92-95,101` (12). Each carries a `/* mirrors limits::X */` comment and nothing
else. `eap.h:56-60` says *"Every count below is the **crate's own** value except
`EAP_MAX_EVENT_ARMS_PER_STATE`."*

**Plus three hand-mirrored wire enums, which are the sharper half.**
`embarch-study-designer/src/decoder.rs:52-71` declares `pub enum ScalarType { U8, I8, U16Le, …
F64Be }` with **no explicit discriminants** — postcard's wire value is the declaration index —
while `app/src/eap.h:108-127` pins `EAP_SCALAR_U8 = 0 … EAP_SCALAR_F64BE = 17` and
`EAP_OP_LITERAL = 0 … EAP_OP_SPAN_LEN = 3` by hand. Same for `Operand`
(`embarch-study-designer/src/eap.rs:190-202`, implicit) against `enum eap_operand_kind`. Insert a
variant anywhere but the end and the wire silently renumbers while the bench keeps decoding with
the old table — a running state machine branching on the wrong field.

**The mechanism exists, works, and is used once.** `app/CMakeLists.txt:135-147` reads
`DEV_BENCH_WIRE_SCHEMA_VERSION` out of `${ESSD_DIR}/src/schema_version.rs` at configure time with
`CMAKE_CONFIGURE_DEPENDS` on that file — and `ESSD_DIR` is resolved unconditionally at `:95-121`
*"for **every** target, not just the ones that cross-compile it"*, so the crate's source tree is
already located for every board.

The only cross-language pins that exist are
`embarch-study-designer/tests/firmware_test_vectors.rs` (CRC-32 values over a fixed study — the
*encoding*, not the *bounds*) and one `_Static_assert(sizeof(struct eap_operand) == 10)`
(`eap.h:145`). There is no header-versus-`limits.rs` check anywhere.

Candidate direction: extend the configure-time read so that every C constant claiming to mirror
`limits.rs` is **derived** rather than typed, and every enum whose discriminants cross the wire is
pinned against the crate's declaration order. **Three deliberate forks must survive as forks** —
`DBM_MAX_STEPS_PER_STUDY` 16, `DBM_MAX_STREAM_CHUNK_BYTES` 256, `EAP_MAX_EVENT_ARMS_PER_STATE` 2
— and a mechanism that cannot express "≤ the crate's, deliberately" is the wrong mechanism.

## Why now

`embarch-dev-bench/decisions/platform.md` decision 20 **is** this mechanism, applied once, and it
states the lesson verbatim: *"A comment saying 'nothing checks this' was not a mechanism for
checking it."* Thirty-seven constants next door still carry exactly that comment. The suite has
already paid three times — `embarch-decision-reversals.md` rows 30 (a forked step cap "reconciled
by nothing"), 44 (*"a note describing a gap is not a mechanism for closing one"* — the mirrored
constant went stale again one bump later) and 63. Every existing check is blind: the CRC vectors
pin one study's encoding, `native_sim` links no crate at all, and a real board links the staticlib
but never compares a `#define` against a `const`.

## Done when

- [ ] Every `/* mirrors limits::X */` in `app/src/` is either derived from the crate at build time
      or fails the build when it disagrees — or is relabelled as a deliberate fork with its
      reason.
- [ ] `ScalarType`, `Operand` and the operator kinds cannot renumber on one side without the other
      side failing.
- [ ] The three deliberate forks are still forks, and still say so.
- [ ] `app/tests/serial_protocol` ztest suite green on `native_sim`; `serial_protocol.h:21-25`'s
      promise is either kept or withdrawn.
- [ ] Gate green; `changelog.d/dev-bench-*` fragment.

**Read before dispatching:** the four `study_ffi.h` constants in this count may disappear entirely
with the `suite-retire-the-ffi-staticlib…` drop in this batch. That leaves 33 in the other three
headers, which is the real target here.
