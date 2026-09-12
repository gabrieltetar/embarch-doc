# 031 — `spec.md` says each seal is carried immediately after the span it covers, and two of the three are not

**State:** claimed (leg 090, 2026-09-11)
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

- [ ] `spec.md:63` states the real seal placement, derived from `src/study.rs`'s declaration order.
- [ ] The three-sibling-seals argument and the "which third" property are still stated.
- [ ] No code change, no field reordering, no wire or schema change, no new numbered decision.
- [ ] `record_checks` is either added to both field tables with a sourced meaning, or the reason it
      was left out is written here.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
