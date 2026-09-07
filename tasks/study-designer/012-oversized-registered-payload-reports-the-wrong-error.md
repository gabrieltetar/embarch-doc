# Report an over-long registered-action payload as `PayloadTooLong`, not `TooManySteps`

**State:** done by leg 023, 2026-09-06 — `agent/study-designer/012-payload-too-long`
**Source:** owner's repo survey, 2026-09-06 — `src/registry.rs:243-249`'s own stated posture, unimplemented on one path
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Doc-size reserve for `study-designer` (supervisor, leg 023)

Exact numbers, because a previous leg's reserve line in this fleet was wrong by
generalising and the worker had to catch it. Caps here are 12 KB for a
`decisions/<topic>.md`, 10 KB for `spec.md`, 5 KB for `open.md`:

- `decisions/crate.md` — **11,267 / 12,288 B, 91.7%, in reserve.** Its compaction
  task `study-designer/006` is **blocked** on `In flux: yes`, so the reserve is
  parked and nothing will pay it down before you.
- `decisions/limits.md` — 8,184 / 12,288 B (66.6%). Room.
- `decisions/payload-meaning.md` — 5,295 B. Room.
- `spec.md` — 9,080 / 10,240 B (88.7%). Close, not in reserve.
- `open.md` — 4,331 / 5,120 B (84.6%). Room.

**Choose the decisions file yourself, on the merits, and say in your report which
one you chose and why.** I am deliberately not steering you to one: the last two
legs of this fleet each had a supervisor pick a file to route around the blocked
`crate.md` reserve and only afterwards find an argument for it, and that is a bad
way to decide where a rule lives. If the right home genuinely is `crate.md`, use
it — **and file `tasks/study-designer/<NNN>-compact-study-designer.md` in the same
commit**, per `tasks/README.md`. Same rule if you push `spec.md` over its line.

**`suite/features.md` is at 20,259 / 20,480 — 221 bytes** — with its compaction
blocked on the owner. This unit routes an existing error to the variant that was
already written for it, so it almost certainly owes a `changelog.d/` entry and
**no `features.d/` row**. Do not write one for completeness. If you believe a row
is genuinely owed, say so in your report and leave it to me.

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

- [x] `resolve_write_payload` returns `PayloadTooLong { max: MAX_PAYLOAD_LEN, actual }` and the
      reused-`TooManySteps` comment is gone.
- [x] A test builds a registered Write whose fields exceed `MAX_PAYLOAD_LEN` and asserts the variant
      and its rendered message.
- [x] `ActionRegistry::validate` rejects a field whose `byte_offset + byte_len` exceeds
      `MAX_PAYLOAD_LEN` (or overflows), with a named error and a test over a hand-written registry.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features study-ui`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## What landed

- `resolve_write_payload` bounds `max(byte_offset + byte_len)` against
  `MAX_PAYLOAD_LEN` **before the allocation** and returns `PayloadTooLong`; the
  reused-`TooManySteps` comment is gone. `saturating_add`, so an offset near
  `usize::MAX` is refused on both profiles rather than panicking in debug and
  wrapping in release.
- `RegistryError::FieldRangeTooLong` refuses the same range in
  `ActionRegistry::validate`. **Confirmed it fires at validate time, not only at
  build time:** `load` calls `validate()` after `toml::from_str`, `save` calls it
  as its first statement — and the test proves it through `ActionRegistry::load`
  of a hand-written file on disk, not through `validate()` alone.
- `TooManySteps` is cited nowhere but its own step-count site and test; no doc in
  this repo quotes its `Display`.
- Decision **66** in `decisions/authoring.md` — chosen over `decisions/limits.md`
  (that file is about type size and stack cost, not about where a bound is
  checked) and over the in-reserve `decisions/crate.md`. No compaction task owed:
  `authoring.md` is 9,910 / 12,288 and `spec.md` 9,177 / 10,240, both outside
  reserve, and `check-doc-size.py` reports every reserve file already filed.
- **No `features.d/` row.** Nothing shipped, retired or changed maturity — the
  registry and the raw-payload path were already `Shipped` rows, and this routed
  an existing error and tightened an existing validate.
- **No `status.d/` fragment.** Nothing suite-level asserted either behaviour:
  `study-actions.toml`, `byte_offset`, `PayloadTooLong` and `TooManySteps` appear
  nowhere under `suite/`, `embarch.md` or `embarch-glossary.md`.
- Dropped `inbox/study-designer-overlapping-registry-fields.md`: `validate` still
  does not refuse two fields of one action whose byte ranges **overlap**, and
  `resolve_write_payload` lets the later declaration silently win — the same
  failure decision 35's duplicate-name rule exists to prevent, applied to offsets.
