# 206 — The client's prompt types carry a Test run prompt's kind and answer value

**State:** open
**Source:** EMB-575 — CoreClient prompt types carry a Test run prompt's kind, outputs and answer value
**Issue:** EMB-575
**Scope:** api
**Hardware:** none
**Owner:** no

## What

In a Test run, Core's pending prompt and its `PromptPending` event carry
`kind`, `observation` and `switched_on` (core decision 138,
`embarch-doc/embarch-core/interfaces/host-studies.md`). `embarch-core-client`'s
`PendingPrompt` and `StudyEvent::PromptPending`
(`crates/embarch-core-client/src/client.rs`) have none of them, so serde drops
them, and `PromptAnswerRequest` has no `value`, which an observation's answer
needs (a declared choice or a number). The UI's prompt modal (`tasks/ui/124`,
blocked on this) holds only the typed client, so it can neither show a prompt's
kind nor send an observation's answer. When this is done:

- `PendingPrompt` and `StudyEvent::PromptPending` carry `kind`, `observation`
  and `switched_on`, each `#[serde(default)]`, typed to match what Core sends
  (read Core's own types; a `serde_json::Value` is acceptable where Core's
  shape is open).
- `PromptAnswerRequest` carries `value`, skipped when absent.
- A host study's prompt and its answer serialize and deserialize byte for byte
  as they do today.

**This is a shared crate** (`embarch-core-client`, consumed by `embarch-ui`
and `embarch-umbrella`): additive fields only, nothing renamed or removed.

## Where to look

- `crates/embarch-core-client/src/client.rs` — `PendingPrompt`,
  `PromptAnswerRequest`, `StudyEvent`
- `embarch-core/src/` — Core's pending prompt and `PromptPending` (read only)
- `embarch-doc/embarch-core/decisions/host-prompt.md` (138) — read only

## Where the doc goes

A new api decision in `decisions/client-crate.md`, or an amendment to the
client crate's interface doc. **`embarch-api/spec.md` is in reserve** (1,110 B
left; its compaction `tasks/api/201` is blocked): do not write it.
`check-doc-size.py --pressure` lists `lease#90`, `test-plans#134` (over),
`ledger#98`, `bench-exchange#89` and `failure-reporting#67` near or over their
limits: do not grow them.

## Done when

- [ ] The three types carry the fields, with a test that a host study's prompt
      and answer are byte for byte what they were, and one that a Test run's
      prompt keeps `kind`, `observation` and `switched_on`.
- [ ] Gate green (`cargo build --workspace`, `test --workspace`,
      `clippy --workspace --all-targets -- -D warnings`).
