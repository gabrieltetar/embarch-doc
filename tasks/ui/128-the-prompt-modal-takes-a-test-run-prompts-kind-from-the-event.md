# 128 — The prompt modal takes a Test run prompt's kind from the event

**State:** claimed by agent/ui/128-the-prompt-modal-takes-a-test-run-prompts-kind-from-the-event, 2026-11-26 22:55
**Source:** EMB-591 — The prompt modal takes a Test run prompt's kind from the event, not a study read
**Issue:** EMB-591
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

On each `PromptPending` the Live follow in `src/live_study.rs` spawns
`add_prompt_kind`, which reads `GET /study/{id}` and, when the same prompt id has
a kind, sends a second `prompt` frame so the modal redraws in place (embarch-ui
decision 113, `decisions/operator-prompt.md`). The event itself now carries the
kind. Quoted from `embarch-api/crates/embarch-core-client/src/study_events.rs`
on `origin/main`:

```rust
/// A Test run's prompt only (`embarch-core` decision 138). On this
/// event Core writes the prompt's kind as `prompt_kind`, since `kind`
/// is the event's own tag (`embarch-core` decision 151); absent for a
/// host study's or a session's prompt, and from a Core older than 151,
/// which wrote a second `kind` this variant cannot parse.
#[serde(default, skip_serializing_if = "Option::is_none")]
prompt_kind: Option<embarch_study_designer::host_study::PromptKind>,
```

and `StudyEvent::as_pending_prompt` copies it into `PendingPrompt.kind`
(`kind: *prompt_kind`). So the `PromptPending` arm of `ingest` already puts the
kind into the first `prompt` frame whenever the event has one.

When this is done, an event carrying `prompt_kind` opens the modal with its kind
in one `prompt` frame and spawns no study read. For an event without one, decide
and say which in the decision: keep the read (it is still the only way a host
study's or older Core's prompt could get a kind, though a host study's prompt
has none), or drop `add_prompt_kind` and `apply_polled_kind` if nothing else
needs them. Either is acceptable; the `Done when` below holds for both.

**Not yours:** `embarch-api` (the client crate is already right), and
`embarch-doc/embarch-chat/`. A separate `ui` task (`tasks/ui/129`) will later
edit `decisions/launcher.md`; do not touch that file.

## Where to look

- `src/live_study.rs`: the `follow_study` callback (the `announced` /
  `tokio::spawn(add_prompt_kind(...))` lines and their comment naming `ui/124`),
  `add_prompt_kind` and its doc comment ("carries no `kind` until Core's
  EMB-577 lands", now false), `apply_polled_kind`, the `ingest`
  `PromptPending` arm, and the test helper `prompt_event` (`prompt_kind: None`).
- `embarch-doc/embarch-ui/decisions/operator-prompt.md` decision 113, the bullet
  "The kind is read from `GET /study/{id}`'s `pending_prompt`, not the event",
  and its "Measured" / "Not measured" line (the event-versus-read ordering
  assumption goes away for an event that carries the kind).

## Where the doc goes

Amend decision 113 in place (`operator-prompt.md`, 10.5 of 12 KB: rewrite the
bullet, do not add one beside it). No `spec.md` change unless a sentence there
says the kind is polled. No file of yours is in reserve.

## Done when

- [ ] A unit test: a Test run `PromptPending` event with `prompt_kind` set gives
      one `prompt` frame whose `pending.kind` is that kind, and the follow
      spawns no study read for it.
- [ ] An event without `prompt_kind` gets its kind by the read as today, or
      shows none, per what the decision says; a test covers that branch.
- [ ] No comment in `src/` still says the event carries no kind.
- [ ] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`).
- [ ] Decision 113 amended; `changelog.d/` fragment.
