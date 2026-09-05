# 001 — embarch-dev-bench's spec.md and open.md are in reserve

**State:** open
**Source:** scripts/check-doc-size.py --pressure
**Scope:** dev-bench
**Hardware:** none
**Compacts:** embarch-dev-bench/spec.md, embarch-dev-bench/open.md
**In flux:** no
**Must not delete:** open.md's *Rejected: a 16-byte TX boundary* clause — there is no such boundary, the number came from mixing a delimiter-inclusive length with a delimiter-exclusive one, and it was the whole basis of a wrong diagnosis somebody will otherwise repeat; the six-part failure signature above it, which is what says "crash" rather than "transport fault"; the uptime pair (899,843 ms then 46,320 ms) that proves it.

## What

`spec.md` is at ~94% of 10 KB and `open.md` at ~95% of 5 KB. `open.md` had a
sentence-level pass on 2026-09-04 (5113 → 4843) and every item was kept, so the
easy half is spent there; `spec.md` has not had a §9 pass.

Run `scripts/check-duplication.py embarch-dev-bench` first. It reports five
overlaps, including `tx_scratch` stated in both `open.md` and `spec.md` and the
`dbm_study_start` union sizing in both `open.md` and `decisions/dispatch.md`.
One of those is a fact in the wrong file; the report says which pair, §3 says
which file owns it.

## Why now

In reserve, and `open.md` is where the unfixed reset root-cause lives — the item
most likely to be edited next.

## Done when

- [ ] Both files out of reserve.
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/dev-bench-*` fragment dropped.
