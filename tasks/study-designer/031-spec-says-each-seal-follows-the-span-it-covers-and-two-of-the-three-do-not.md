# 031 — `spec.md` says each seal is carried immediately after the span it covers, and two of the three are not

**State:** done
**Source:** refill sweep for scope spread, leg 090, 2026-09-11. The line numbers below are as the
sweep reported them — **re-verify every one against the source before you act on it.**
**Scope:** study-designer
**Hardware:** none.
**Owner:** no

## What

`embarch-study-designer/spec.md:63` describes the three CRC seals as:

> **Three sibling seals, not one widened one**, each carried immediately after the one contiguous
> span it covers, so a hand-written C decoder digests one run of bytes per seal and a mismatch names
> **which third** arrived wrong.

`struct Study` (`src/study.rs`) declares them in this order — and postcard encodes in declaration
order, so declaration order **is** the byte order:

```
108: steps
123: streams
126: steps_crc
141: streams_crc
163: protocols
177: protocols_crc
```

Only `protocols_crc` immediately follows its own span. `steps_crc` sits after `streams`, and
`streams_crc` after `steps_crc`. The real layout is `steps, streams, steps_crc, streams_crc` — the
first two seals are **grouped**, not interleaved.

## Why it costs something

That sentence exists to tell someone writing a decoder in C how to stream the digest: one run of
bytes, then its seal. Following it literally produces a decoder that digests `steps` and then reads
`streams`' first bytes as `steps_crc`. The claim is load-bearing precisely for the reader least able
to check it, and the "which third arrived wrong" property it justifies still holds — it is the
*placement* that is wrong, not the three-seal design.

## What to do

**Move the doc, not the struct.** Reordering fields to match the prose is a wire change and a schema
bump; correcting the sentence is neither. Say what the layout actually is — the two step/stream
seals carried together after both spans, `protocols_crc` after its own — **after deriving the order
yourself** from `src/study.rs`'s declaration order, and confirm nothing reorders it (no serde
rename/flatten/skip on those fields). Keep the paragraph's actual argument: three sibling seals over
three contiguous spans, so a mismatch still names which third.

If your reading finds the encoded order is *not* declaration order after all, **stop and say so
here** rather than rewriting the sentence a second wrong way.

## A second, related omission in the same file set

`interfaces/types.md`'s `Study` field table (lines 10-18) and `spec.md` §4's "What a study carries"
table both appear to omit `Study.record_checks` (`src/study.rs:240`), which exists, is host-only, and
is described only in `decisions/payload-meaning.md:37`. Add the row to both tables **if and only if**
you can state what it carries from that decision's own body and from the type — do not compose a
meaning. If the two sources disagree, report it here and leave the tables alone.

## Done when

- [x] `spec.md:63` states the real seal placement, derived from `src/study.rs`'s declaration order.
- [x] The three-sibling-seals argument and the "which third" property are still stated.
- [x] No code change, no field reordering, no wire or schema change, no new numbered decision.
- [x] `record_checks` is either added to both field tables with a sourced meaning, or the reason it
      was left out is written here.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.

## Done

Confirmed `src/study.rs`'s declaration order is `steps, streams, steps_crc, streams_crc,
protocols, protocols_crc` — all six fields are `#[serde(default)]` (or, for `steps`/`streams`,
plain positional), none carry a serde `rename`/`flatten`/`skip`, so declaration order is the
encoded order. Rewrote `spec.md`'s "Three sibling seals" paragraph to state that the two
step/stream seals are carried *together* after both spans, with `protocols_crc` alone
immediately after its own — keeping the "one run of bytes per seal, mismatch names which
third" argument intact (it holds regardless of whether the two leading seals are adjacent to
each other or each to its own span).

`record_checks` (`src/study.rs:240`, `MAX_STREAMS_PER_STUDY`-bounded `Vec<RecordCheck>`):
added to both `spec.md` §4's table and `interfaces/types.md`'s `Study` field table. Meaning
sourced from `decisions/payload-meaning.md`'s decision 70 (host-only, names a tap by `id`,
records begin with a magic and end with a CRC-32/ISO-HDLC over the preceding bytes, checked
by Core after the run, sealed by neither CRC, never transmitted) and cross-checked against
the field's own doc comment in `src/study.rs` — the two agree.

`spec.md` crossed into its last-10% size reserve (91.3%) from this edit; filed
`tasks/study-designer/032-compact-study-designer.md` (blocked, §4 still in flux) in the same
commit, per `DOC-COMPACTION.md` §2.
