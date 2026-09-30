# embarch-api decisions: Bootloading

**Status:** active, 2026-09-30.

The two tools that put a signed image on the DUT through its own bootloader, and where that image is found. What Core does with it: [`embarch-core` decision 77](../../embarch-core/decisions/bootload.md). What is still to build across the suite: [bootload-proposal.md](../../bootload-proposal.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 80 — `bootload` and `build_and_bootload` are their own tools, and every DUT fact they send is declared in `[projects.bootload]`

**Separate tools, not a `method` on `flash`.** They share no parameter that means the same thing — no probe, chip, format, base address or erase — and a mode flag that makes half of `flash`'s parameters meaningless is two tools sharing a name. They take `build`'s target selection and nothing else; `build_and_bootload` refuses `image_path` rather than ignoring it (decision 51's posture).

**No chip is resolved.** Target resolution stops at the build plan (`resolve::resolve_build`), split out of `resolve` for this: the bootloader is reached by the DUT's USB identity, which Core holds, so a SoC missing from Core's chip table must not stop a bootload.

**`[projects.bootload]` carries the DUT facts** — `entry_command`, `entry_line_ending`, `artifact`, `buffer_size` — because each is a property of the DUT's firmware that nothing can observe first ([embarch.md](../../embarch.md) §5). The table may be absent: a DUT already in its bootloader needs none of it. A value that cannot be honoured — an unknown line ending, an `artifact` with a path in it, a buffer too small to carry a frame, an unknown key — fails config load. **The ports are not here**: they are the bench's wiring, not the project's, and are declared through Core (`declare_bootload_ports`, `embarch-core` decision 78) where the enrollment file lives.

**`app_reappeared: false` is `success: true` with a `warning`.** Core reports it rather than raising it; an agent reading only `success` would otherwise miss the one outcome that says the image is on the DUT and not running. Its own client timeout, `bootload_timeout_secs` (300 s), because two re-enumerations and a default-buffer upload outlast `flash_timeout_secs`.

### 81 — The signed image is found by reading sysbuild's `domains.yaml`, and must be newer than the build that claims it

**Sysbuild-aware without assuming a layout.** A sysbuild build puts each image in its own directory and records them in `<build dir>/domains.yaml`; the application is the domain its `default` names, and the signed image is that domain's `zephyr/<artifact>`. With no `domains.yaml` the build is single-image and the image sits beside the flash artifact. A `domains.yaml` whose default names no listed domain is an error, not a guess. `flash`'s own artifact path is not yet sysbuild-aware; this does not change it.

**Freshness is the signed image's own mtime against the build's start**, not the flash artifact's, because a build can relink `zephyr.elf` without the signing step running. It is also located *after* the build, since a first sysbuild build is what writes `domains.yaml`. An image that did not move is refused — the same rule `build_and_flash` holds a flash artifact to.
