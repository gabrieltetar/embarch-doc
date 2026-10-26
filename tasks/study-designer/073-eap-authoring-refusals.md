# 073 — The .eap parser refuses three authoring errors it now accepts in silence

**State:** done (decision 84); claimed by agent/study-designer/073-eap-authoring-refusals, 2026-10-26 04:54
**Dispatch note:** `open.md` is at 4,473/5,120 B (647 B left) and parked under `tasks/study-designer/026` (blocked, nothing payable): add nothing to it unless you also remove as much. `decisions/protocols.md` is 10,876/12,288 B and `decisions/gatt-extract.md` 11,053 B; if a new decision would push either into the last 10% (above 11,059 B), put it in a file with headroom instead. `interfaces/eap.md` is 8,368 B. This crate is shared: `embarch-core`, `embarch-api`, `embarch-ui` and `embarch-umbrella` path-depend on its main checkout, so a new error kind must not break an exhaustive `match` in any of them. If an existing public enum gains a variant, check those three repos with `grep` and say in your report what you found.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-study-designer findings 5, 6 and 9), verified by Opus against embarch-study-designer@b9a2d5df
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

A `.eap` manifest with any of these errors parses, resolves and validates. It then behaves differently from what the author wrote, and nothing reports the error:

1. **`on_timeout` and `retry` literals wrap.** `p.int()? as u32` and `p.int()? as u8` accept any `i64`. With `on_timeout -5ms retry 300`, the state waits about 49 days and retries 44 times. Offsets and match bytes already refuse out-of-range values with `BadInteger`.
2. **A `write` field may declare a float width.** `validate_protocol` checks that fields are integers for frame fields only. `ScalarType::write_i64` returns `None` for a float width, so every run of the protocol ends with "protocol write operand did not resolve". The operand did resolve, so the message names the wrong cause, and the error appears on the bench instead of while the manifest is written.
3. **A `repeat` may name a struct that does not exist.** No resolve step checks a `repeat`'s element name. `lower_layout` turns an unknown name into `LowerGap::NotFlat`, so the frame looks unrenderable in the same way a legitimately complex frame does. Today this is latent, because nothing outside the crate's tests calls `render_layout`. It becomes a silent missing CSV once a renderer does.

When done, each of these is a named authoring-time error with the manifest's line number, matching the parser's existing posture (`BadInteger`, `NonIntegerField`, `Unknown`). The worker chooses the error kinds.

## Why now

- `src/eap_parse.rs:971` and `:974` cast silently. The sibling `u16v` at `:590-597` refuses. spec.md §2: "A capacity limit refuses; it never truncates."
- `src/eap_parse.rs:986-1006` accepts any `ScalarType`. `src/eap.rs:496-500` checks frame fields only, and `:525-537` checks `on_enter` writes for operand shape but not width. The runtime failure is at `src/decoder.rs:289-292` and `src/eap_interp.rs:139-146`.
- `src/eap_parse.rs:1335-1338` stores a `repeat` without resolving its element, and `:1674` maps a missing struct to `NotFlat`. `render_layout` (`:1202-1211`) then returns `Ok(None)`, which is the case the crate already retired for the four deferred primitives (open.md, "Parsed and pinned, with no consumer").

## Done when

- [x] An `on_timeout` value outside `u32` or a `retry` outside `u8`, negative values included, is refused with the line it is on. A test covers a negative value and an overflow for each.
- [x] A float width on any write field is refused at parse or validation with a named error. A test covers `f32le` in an `on_enter` write.
- [x] A `repeat` whose element names no struct in scope is refused with the line and the name. A test covers a misspelled struct name.
- [x] The worked protocols in `tests/` and `interfaces/eap.md` still parse unchanged.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated (`interfaces/eap.md` for the new errors), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
