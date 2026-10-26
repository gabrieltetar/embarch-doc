# 075 — A Notify or Indicate row built in the UI waits for its notification instead of timing out at once

**State:** claimed by agent/study-designer/075-notify-wait-budget, 2026-10-26 04:13
**Dispatch note (2026-10-26):** `embarch-study-designer/open.md` is in reserve at 4,473 / 5,120 B (647 B left), filed against `tasks/study-designer/026` (blocked); put the meaning of the operation's `timeout_ms` in `interfaces/types.md` and a decision, not `open.md`. This is a shared crate that `embarch-core`, `embarch-api` and `embarch-ui` build against: keep its public API source-compatible. Before making `Notify`/`Indicate { timeout_ms: 0 }` a validation refusal, grep the sibling repos read-only for committed studies, fixtures or tests carrying one, and name every hit in this file; I run the consumers' tests against your branch before landing it.
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-study-designer finding 1), verified by Opus against embarch-study-designer@b9a2d5df
**Scope:** study-designer
**Hardware:** verify-only
**Owner:** no

## What

`build_study` lowers every `Notify` or `Indicate` row, whether `Raw`, `Vendor` or `Registered`, to `GattOperation::Notify { timeout_ms: 0 }` (or `Indicate`). The comments beside both sites say the step's own `timeout_ms` is the wait budget. dev-bench does not read 0 that way. It treats the operation's `timeout_ms` as a deadline of its own and waits until whichever comes first, that deadline or the step's. With 0 it calls `k_sem_take` with `K_NO_WAIT`, so the step reports `TimedOut` unless a notification already arrived while the step was subscribing. When done, a study built from a Notify or Indicate row carries a wait budget that matches what the row's author set. One direction: the builder copies the row's `timeout_ms` into the operation, and study validation refuses a `Notify`/`Indicate` whose own `timeout_ms` is 0, so a hand-written study cannot reach the same state. If the worker instead decides that 0 should mean "use the step's budget", that is a dev-bench change and goes through an inbox drop, not this unit.

## Why now

- `src/study_builder.rs:887-891` (`literal_operation`) and `:904-913` (`resolve_operation`) emit `timeout_ms: 0`, and their comments say otherwise.
- `embarch-dev-bench app/src/ble_bridge_real.c:2347-2357` passes `deadline_from(op_timeout_ms)` to `await_notification`. `:2308-2312` takes the earlier of the two deadlines, and `:451-456` turns a past deadline into `K_NO_WAIT`.
- `interfaces/types.md` line 52 defines the operation's `timeout_ms` as "bounded independently of the step's own budget", which is what dev-bench implements and what the builder's comments contradict.
- The Study Designer's registration dialog offers Notify and Indicate (`embarch-ui assets/index.html:555-556`), so a user can build this step without editing JSON. Nothing in the builder's tests covers a Notify or Indicate row.

## Done when

- [ ] A builder test: a `Raw`, a `Vendor` and a `Registered` row each with operation Notify (and one with Indicate) and `timeout_ms: 5000` produce a study whose operation's wait budget is nonzero and no longer than the step's.
- [ ] A study carrying `Notify { timeout_ms: 0 }` or `Indicate { timeout_ms: 0 }` is refused at validation with a named error, or `interfaces/types.md` states what 0 means and dev-bench already does that. Whichever is chosen is written down, and an inbox drop is filed if dev-bench must change.
- [ ] Bench check (debt): a UI-built study with a Notify row against a DUT that notifies within the row's timeout reports `Pass`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated (`interfaces/types.md` for the meaning of the operation's `timeout_ms`), `changelog.d/` fragment dropped, `status.d/` fragment for anything suite-level it made false.
