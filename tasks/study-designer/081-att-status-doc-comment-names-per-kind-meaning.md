# 081 — The `att_status` doc comment says it is always an ATT error code

**State:** claimed by agent/study-designer/081-att-status-doc-comment-names-per-kind-meaning, 2026-11-10 03:58
**Source:** the reviewer of `dev-bench/044` (2026-11-10), which started emitting disconnected transcript rows with the HCI reason in this byte (`embarch-dev-bench` decision 53)
**Issue:** EMB-130
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`embarch-study-designer/src/gatt.rs` documents `GattTranscriptEntry::att_status` as "Raw ATT error code, `0` when there was none". Two event kinds already carry something else in that byte, and `interfaces/gatt-types.md` says so: a characteristic-discovered entry carries the raw properties byte, and a disconnected entry carries the HCI disconnect reason. Someone reading the type rather than the interface doc is told the wrong thing.

Make the doc comment say the byte's meaning depends on the event kind, naming the three meanings or pointing at `interfaces/gatt-types.md`. Comment only: no change to the type, its serialization or the schema version.

## Done when

- [ ] The doc comment on `att_status` in `embarch-study-designer/src/gatt.rs` names the per-kind meanings or points at `interfaces/gatt-types.md`, and no longer says it is always an ATT error code.
- [ ] `cargo build`, `cargo test` and `cargo clippy --all-targets -- -D warnings` green in the crate, per `../../embarch-fleet/gate.md`.
- [ ] `changelog.d/` fragment dropped; `interfaces/gatt-types.md` still agrees with the comment.
