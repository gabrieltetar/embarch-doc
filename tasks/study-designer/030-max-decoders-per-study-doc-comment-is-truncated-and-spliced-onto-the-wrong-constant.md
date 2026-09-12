# 030 — `MAX_DECODERS_PER_STUDY`'s doc comment is truncated mid-sentence and spliced onto a different constant

**State:** claimed — leg 089, 2026-09-11.

**Doc-size reserve for `study-designer`:** `embarch-study-designer/open.md` is at 89.2%
(4,569/5,120 B, 551 B left) and its compaction task `tasks/study-designer/026-compact-study-designer.md`
is blocked. Nothing else in this sub-project is in reserve, and this task should not need to touch
`open.md` at all. If your work does push a file into its last 10%, file
`tasks/study-designer/<NNN>-compact-study-designer.md` in the same commit.
**Source:** found by the `study-designer/029` worker as out-of-scope and correctly left alone;
verified against `src/limits.rs` by the supervisor before filing, leg 088, 2026-09-11.
**Scope:** study-designer
**Hardware:** none.
**Owner:** no

## What

`embarch-study-designer/src/limits.rs:98-104` reads, verbatim:

```rust
/// `Study.decoders` (decision 52) — named payload layouts one
/// study resolves out of the firmware repo's `study-structs.toml`. Bounded
/// by what a study can actually reference: a decoder is only reachable
/// through a tap's `StreamEncoding::Struct`, and there are at most
/// Longest record magic a [`crate::records::RecordFraming`] may declare.
/// `GWF1` and the WDS spill's are four bytes; eight leaves room without
/// letting a "magic" become a header.
pub const MAX_RECORD_MAGIC_LEN: usize = 8;
```

Two separate constants' prose has been spliced into one comment block. It ends
`"and there are at most"` — mid-sentence, with the number missing — and then runs straight into
`MAX_RECORD_MAGIC_LEN`'s own text. The block attaches to `MAX_RECORD_MAGIC_LEN`, so **the rendered
rustdoc for that constant opens with three lines about decoders and a sentence that stops.**

`MAX_DECODERS_PER_STUDY` itself is alive and correct at `:116`
(`pub const MAX_DECODERS_PER_STUDY: usize = MAX_STREAMS_PER_STUDY;`) — it is only its *documentation*
that went missing. Whatever comment it carries today should be read against this orphan before
anything is deleted.

## What to do

Restore the two comments to their own constants. **The truncated clause's ending is recoverable, not
a guess**: `interfaces/limits.md`'s row for `MAX_DECODERS_PER_STUDY` states the full argument —
*"the arity of the thing, not a guess: a decoder is reachable only through a tap's
`StreamEncoding::Struct`, and there are at most that many taps"* — so finish the sentence from there
rather than composing new reasoning.

**Check whether anything else in the file has the same shape.** A splice like this is the signature
of a bad edit rather than a typo, and one is rarely alone; report what a full pass finds in this task
file even if the answer is nothing.

## Why now

`limits.rs` is the file `interfaces/limits.md` is generated *from* by hand, and `study-designer/029`
just finished asserting that file is exhaustive. A constant whose rustdoc describes a different
constant is the one way that assertion can still mislead a reader who goes to the source to check it
— which is exactly what the doc tells them to be able to do.

## Done when

- [ ] `MAX_RECORD_MAGIC_LEN` and `MAX_DECODERS_PER_STUDY` each carry their own complete doc comment.
- [ ] No sentence in either ends mid-clause.
- [ ] No constant's value changes and no public item is added or removed.
- [ ] A pass over the rest of `src/limits.rs` for the same splice shape is reported here.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
