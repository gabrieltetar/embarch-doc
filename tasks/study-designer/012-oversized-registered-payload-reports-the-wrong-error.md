# Report an over-long registered-action payload as `PayloadTooLong`, not `TooManySteps`

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `src/registry.rs:243-249`'s own stated posture, unimplemented on one path
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

`src/study_builder.rs:632` maps a payload that will not fit `MAX_PAYLOAD_LEN` onto
`BuildStudyError::TooManySteps { max: MAX_PAYLOAD_LEN, actual: buffer_len }`, whose `Display`
(`:230`) renders it as "study has 600 steps, but the limit is 512". The correct variant
`PayloadTooLong { max, actual }` exists at `:207` with the right wording at `:259`, and is already
used for the identical condition on the raw-payload path at `:544`.

Separately, `resolve_write_payload` sizes its buffer from `max(byte_offset + byte_len)` (`:609-614`)
with no bound on either, and `ActionRegistry::validate` (`src/registry.rs:211-227`) checks only value
lengths — so a hand-edited `study-actions.toml` with a large `byte_offset` allocates it. That should
be a named `RegistryError` at validate time.

## Why now

`registry.rs:243-249` states the rule this breaks: "a hand-edited TOML file's mistakes … become a
named `RegistryError` here". The misrouting variant is a one-line fix sitting next to the variant
that was written for it.

## Done when

- [ ] `resolve_write_payload` returns `PayloadTooLong { max: MAX_PAYLOAD_LEN, actual }` and the
      reused-`TooManySteps` comment is gone.
- [ ] A test builds a registered Write whose fields exceed `MAX_PAYLOAD_LEN` and asserts the variant
      and its rendered message.
- [ ] `ActionRegistry::validate` rejects a field whose `byte_offset + byte_len` exceeds
      `MAX_PAYLOAD_LEN` (or overflows), with a named error and a test over a hand-written registry.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features study-ui`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
