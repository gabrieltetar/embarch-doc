# 010 — `firmware_version` means the bench's build on one surface and the DUT's on another, and `clamp_version` blames the wrong board

**State:** open
**Source:** suite review pass 2026-09-06, dimension 5 (cross-surface consistency). Code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

One field name covers two different boards' builds in the one flow that reads both.

- **Bench meaning.** `embarch-study-designer/src/protocol.rs:38-41` —
  `HelloAck.firmware_version` = *"Identifies which dev-bench firmware build replied"*. Served
  under that name by `GET /dev-bench/hello` (`embarch-core/interfaces.md:45`).
- **DUT meaning.** `embarch-study-designer/src/study.rs:246-249` —
  `Requirements { dev_bench_version, firmware_version }` — and `src/result.rs:44`'s
  `Provenance.firmware_version`.

The switch happens in one line: `embarch-api/src/reflash.rs:259` —
`outcome.dev_bench_version = Some(hello.firmware_version.clone());`. Core does the same at
`embarch-core/src/study.rs:1057`. And the doc comment on `Requirements`
(`embarch-study-designer/src/study.rs:232`) presents the collision as an alignment: *"Two
free-form strings, matching the shape `HelloAck.firmware_version` already uses."*

**The collision has already produced a wrong message, and this is the cheap half.**
`clamp_version` (`embarch-core/src/study.rs:489-492`) warns *"dev-bench reported a
firmware_version longer than {MAX_FIRMWARE_VERSION_LEN} bytes"* — and it is called on the
**DUT's** version too, at `:476`:
`Some(flashed) => (clamp_version(flashed), VersionSource::FlashedThisRun)`. An over-long
`flashed_firmware_version` is logged as dev-bench's fault and recorded empty.

Candidate direction: name the subject in the field wherever both can be in scope — the hello
surface's version is the bench's, and `Requirements`/`Provenance` already prove the suite has a
word for that (`dev_bench_version`). Split `clamp_version`'s message, or make it take the subject.
**Do the `clamp_version` half first**; it is a one-function fix in `embarch-core` and it is the
demonstrated defect.

## Why now

A caller or agent that reads `/dev-bench/hello`'s `firmware_version` and writes it into
`requires.firmware_version` has pinned the DUT requirement to the bench's build — and per
`embarch-core/src/study.rs:371-372` that requirement is only ever *checked* when
`flashed_firmware_version` is supplied, so in the normal no-reflash case it is silently accepted
and recorded as `Declared`. That is exactly the mislabelling `Provenance`'s source fields exist to
prevent: *"An unverified assertion must not look identical to a verified reading."*

## Done when

- [ ] `clamp_version`'s warning names the board whose version was over-long.
- [ ] No field named `firmware_version` can be read as either board's build on a surface that
      exposes both, or the ambiguity is named where a caller reads it.
- [ ] Gate green; `changelog.d/` fragments for each repo touched.
