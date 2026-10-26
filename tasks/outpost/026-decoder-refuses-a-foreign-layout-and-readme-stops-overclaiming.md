# 026 — The reference decoder refuses a record layout it does not speak, and the README stops claiming more than the tests and measurements show

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-outpost findings 2 and 5, plus the README half of finding 4), verified by Opus against embarch-outpost@2968f0c1
**Scope:** outpost
**Hardware:** none — host Python (`tests/decoder_unit.py`, stdlib only and already in CI) and prose.
**Owner:** no

## What

`scripts/decode_outpost.py` compares only `build_id` (`:429`). It reads the header's `record_layout_version` (`:170,178`), then parses every records frame with the layout-3 grammar whatever that number says. It never checks the number against its own layout or against the manifest's `record_layout_version`. A stream in a later layout would decode into a whole capture of plausible, wrong rows, and `open.md` already names a layout-4 record shape. When done, the decoder refuses a stream whose layout it does not speak, and refuses a manifest whose layout disagrees with the header. Each refusal names the numbers involved, which is the posture the Rust decoder already has (`embarch-study-designer` `src/outpost.rs`, `ManifestRefusal::LayoutVersion`). Decision 24 says the two existing `--allow-*` flags are the entire override mechanism, so this adds no third flag.

In the same pass, two README claims stop overstating:

- `README.md:215-217`, and the same sentence in `Kconfig:4-6`, say no outpost byte has ever crossed a real UART and that every wire constant is unmeasured. `spec.md` §4 and `interfaces/integration.md` have recorded measurements from a real nRF54L15 at 460800 baud since 2026-08-27.
- `README.md:207` says the end-to-end test proves "every record kind appears". `tests/native_sim_stream/assert_stream.py:69-71` asserts 7 of the 11 kinds. `thread_create` is required only indirectly (`:98-105`), and `thread_name`, `gpio_dispatch` and `gpio_callback_done` are never asserted. `tests/native_sim_stream/README.md` claims every kind "the build has enabled", yet `TRACE_GPIO` defaults on and the test has no GPIO device. The fix is either that the test asserts what it can and the README says where the rest is covered (the GPIO record's literal bytes in `tests/unit`), or that the sentences narrow.

## Why now

`README.md:142-144` promises this refusal ("or whose record layout version is not this decoder's. Both refusals are the feature."). `interfaces/wire.md:30` says the header's version byte is "what makes that a refusal instead" of a capture of wrong rows. Only one of the suite's two decoders keeps that promise, and the layout-4 change `open.md` plans is the event that would expose the other. The README's Status section is the first thing a new reader sees, and it currently points them at a risk that was retired two months ago.

## Done when

- [ ] `decoder_unit.py` feeds a header whose layout is not 3, built from literal bytes. The decoder exits non-zero, renders no record rows, and names both layouts on stderr.
- [ ] A manifest whose `record_layout_version` disagrees with the header is refused the way a build-ID mismatch is, and a test covers it. The existing build-ID and arrival-join tests pass unchanged.
- [ ] `tests/cross_decoder.py` still agrees with the Rust decoder on the committed layout-3 fixtures.
- [ ] README's Status section and the Kconfig file header say what is measured and what is still assumed, in agreement with `interfaces/integration.md`'s provenance column.
- [ ] Every README sentence about what `native_sim_stream` proves is true of `assert_stream.py`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
