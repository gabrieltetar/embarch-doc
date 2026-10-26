# 001 — `Client::upload` ends when the offset stops progressing, not only when it stops moving, and the spec names Core as its consumer

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-smp findings 1 and 2), verified by Opus against embarch-smp@92363628
**Scope:** smp
**Hardware:** none — a scripted server behind `Read + Write` covers every case, the same way the existing tests do.
**Owner:** no

## What

`Client::upload` (`embarch-smp/src/client.rs:181-225` at `9236362`) gives up only when the server returns the same offset `max_stalls` times in a row (`client.rs:207-216`). There is no other bound. A server whose offset keeps changing without getting anywhere loops forever, because each reply arrives within its per-chunk timeout. Examples are `8 → 16 → 8 → 16`, or one that keeps returning to `0`, which also makes the client re-send `len`, `image` and `upgrade` every other chunk. The consequence lands in Core. `POST /bootload` runs the upload inside `spawn_blocking` while holding `hw_lock` (`embarch-core/src/api.rs:656-685`), so such a server hangs the request with nothing to read, and every `/flash` and `/reset` is refused `503` until Core restarts.

When this is done, an upload that stops making forward progress ends with an error naming the offsets it saw. One possible direction: abandon when the highest offset reached has not advanced for N replies, or cap the request count at a stated multiple of what the image needs. The one legitimate restart the reference allows, where the server asks for offset 0 again, must keep working.

In the same pass, correct `embarch-doc/embarch-smp/spec.md:7`. It says "Nothing in the suite links it yet: Core's `POST /bootload` is the first consumer, and it is not built". Core depends on the crate (`embarch-core/Cargo.toml:44`), routes `POST /bootload` (`api.rs:142`), imports `Client`, `Fragmentation`, `ImageInfo` and `UploadOptions` (`bootload.rs:16-17`), and drives the whole flow against `embarch_smp::sim` in its tests. `embarch.md:27` and `embarch-core/spec.md:55` already say so.

## Why now

Decision 9 (`decisions.md:38`) departed from the reference precisely so that "an upload whose offset does not move for five replies is abandoned, where the reference loops forever". This is the same defect in a shape the guard does not catch. No real bootloader has answered this client yet (`open.md`), so the first hardware run will be the first time a server the simulator does not model replies to it. Note for whoever files this: `embarch.md:90` records `embarch-smp` as not yet in the fleet's repo set.

## Done when

- [ ] A scripted server whose offset alternates between two values makes the upload fail, within a bound the test states, with an error naming the offsets.
- [ ] A server that asks for offset 0 once and then completes still succeeds (`a_server_asking_for_offset_zero_again_gets_len_but_not_sha` passes), and all 18 reference uploads still send identical bytes.
- [ ] `spec.md`'s status line names Core's `POST /bootload` as the built consumer, and decision 9's list of deviations states the new rule.
- [ ] `cargo test --all-features` and `cargo clippy --all-targets -- -D warnings` are clean in embarch-smp, since the merge gate does not reach this repo yet (`embarch.md` §5).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
