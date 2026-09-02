# embarch-dev-bench decisions: Platform and build system

**Status:** active, 2026-09-02.

One RTOS, one shared application, one west topdir per vendor family — and how the Rust staticlib gets cross-compiled into it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1, 3 — Zephyr as the one common RTOS, with vendor SDK forks accepted per family
"One firmware project for any board" means "any board a Zephyr flavor supports", not "every vendor's native SDK behind a hand-written abstraction layer". The latter is effectively building a small cross-platform embedded framework from scratch and buys nothing this rig needs, since Zephyr already provides vendor-portable BLE host, GPIO and ADC APIs. It also means the upstream "firmware is C, not Rust, because the BLE host is a C API" decision needs no reopening for a wider vendor set — every mainstream vendor's BLE host under Zephyr *is* the same Zephyr host API.

A vendor fork (NCS) is often the only place brand-new silicon's HAL and controller support lands first, so insisting on vanilla everywhere would risk blocking on upstream timing for every new board. **Accepted trade-off:** `app/src/*.c` calls only stable vendor-neutral Zephyr APIs, never anything NCS-proprietary, so the same source survives a workspace swapping its pinned revision.

### 2 — One repo, multiple west workspaces, one shared application tree
A west manifest pins exactly one Zephyr revision at a fixed path, and a vendor's own fork pins its own — incompatible with mixing into one manifest. So each vendor family gets its own west topdir under `workspaces/`, while the application is written once and *referenced* by every workspace's build. That achieves the part of "one firmware project" that matters — one implementation, one repo, one history — without fighting west's one-manifest-one-Zephyr model. The pattern has now been load-bearing in both directions: two boards have each been the bench and been stood down, and each time the other workspace was still there to resume from (decisions 26, 43).

### 5 — `workspaces/nordic` pins NCS and the SoftDevice Controller
Follows from decision 3: nRF54-family support is NCS-first, often NCS-only for the newest parts. The SoftDevice Controller over Zephyr's open-source controller, for best coverage on Nordic silicon specifically — at the cost of that choice being Nordic-only, which is fine because a future non-Nordic workspace picks its own independently.

### 8 — The Rust staticlib cross-compiles as part of `west build`, via a path-based `cargo rustc`
A CMake custom target builds the crate for the board's target triple rather than requiring a separate manual publish step first — one build command, as intended. Deliberately *not* the formal west-managed-module plumbing this originally specified: the crate is edited locally far more often than pulled from a pinned revision, and a plain path invocation reaches the same outcome with less git plumbing.

**The board→triple mapping had one real footgun:** the nRF54L15's Cortex-M33 needs the **soft**-float `thumbv8m.main-none-eabi`, not `-eabihf`. This app's Zephyr build enables no hardware-FPU ABI, and a hard-float staticlib fails to link the moment any code path touches an `f32` — which includes `Sample`'s own field internally, not just the FFI-exposed signatures, none of which pass a float. Found by hitting that link error against the real board. The ESP32-C5's RISC-V core has only one ABI variant Zephyr builds it with, so no analogous trap.

### 9 — CI, reversing "no CI for now"
Originally deferred until more than one board built, so a compile-only matrix would have something to be useful across. Superseded: a `west build -b native_sim app` job is worth having with one board, being cheap and hardware-independent, and would have caught a real Zephyr BLE API breakage before it was found by hand. A cross-board matrix is still deferred.

### 16 — A `native_sim` workspace, with BLE stubbed as a separate file rather than `#ifdef`s
`native_sim` runs the application as a native Linux process, which exercises the serial/COBS parsing and the FFI glue without hardware. **Scoped narrowly:** no virtual-PTY transport — the parsing logic is unit-tested in-process, and framing correctness is the upstream crate's round-trip tests' job.

BLE is stubbed as `ble_bridge_stub.c` beside `ble_bridge_real.c`, both implementing the same small internal API, with each workspace's CMake picking one. That keeps the real BLE-host-calling code free of stub-only branches and vice versa, at the cost of keeping two files in signature-sync by hand — acceptable while the API mirrors the `Action` surface.

### 20 — The FFI stub split is permanent, and its schema number is now read from the crate
Bring-up compiled against a stub so that getting `main.c`/`ble_bridge_real.c`/`serial_protocol.c` running on real hardware did not wait on cross-compiling a Rust staticlib per target. Once decision 8 closed, the split became permanent rather than temporary: the stub stays forever on `native_sim` — a host-only sanity board does not need the real decode logic — while the real staticlib is linked on hardware workspaces.

**The stub's hand-mirrored schema constant went stale twice, and the second time is the lesson.** It was found **four bumps behind at v4**, fixed, and given a comment recording that nothing compares it against the crate — because by construction `native_sim` links no crate to compare to. That comment was accurate, stayed accurate, and **did not stop the number going stale again one bump later**. CMake now reads the constant out of the crate's own source at configure time, with that file as a configure dependency so an edit re-runs it. **A comment saying "nothing checks this" was not a mechanism for checking it.** This does not close the wider gap: only a build that links the real staticlib exercises the version call for real.
