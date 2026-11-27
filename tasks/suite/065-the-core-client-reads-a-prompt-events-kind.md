# 065 — The core client reads a prompt event's `prompt_kind`

**State:** open
**Source:** EMB-584 — embarch-core-client reads PromptPending's prompt_kind
**Issue:** EMB-584
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

Core decision 151 writes a Test run's prompt kind on the `PromptPending` event
as `prompt_kind`, so the event's `kind` stays its tag. `embarch-core-client`'s
`StudyEvent::PromptPending` (`crates/embarch-core-client/src/study_events.rs`)
has no field for it, so a reader still polls `GET /study/{id}`'s
`pending_prompt.kind` (api decision 137). When this is done the variant carries
an optional `prompt_kind` (`#[serde(default)]`, absent for a host study's or a
session's prompt), and `as_pending_prompt` / `prompt_pending` carry it, so a
Test run's PromptPending event parsed by the client names its kind without the
poll. `tests/prompt_types.rs` stops feeding a duplicate-`kind` line.

## Why a `suite` task

Adding a field to the variant is source-breaking for a struct literal, and
`embarch-ui`'s `src/live_study.rs` builds one in its tests (`prompt_event`,
checked 2026-11-26), so `embarch-ui`'s `cargo test` and `clippy --all-targets`
go red the moment `embarch-api` lands alone. One sequenced pass: the client
change in `embarch-api`, then `prompt_kind: None` in `embarch-ui`'s literal,
then the docs (api decision 137's or the client-crate decision's line, and
`embarch-ui` only if its behaviour changes; it need not start reading the
field). `embarch-umbrella` has no `PromptPending` use (checked 2026-11-26).

## Done when

- [ ] A Test run's PromptPending event parsed by the client carries its prompt
      kind; a host study's parses with `None`.
- [ ] `embarch-api` and `embarch-ui` both green under `cargo build`, `test`
      and `clippy --all-targets -- -D warnings` on the merge result.
- [ ] The decision names the struct-literal break and the one caller fixed.
