# 001 — embarch-dev-bench's spec.md and open.md are in reserve

**State:** done
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

- [x] Both files out of reserve.
- [x] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [x] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [x] Gate green, `changelog.d/dev-bench-*` fragment dropped.

## Shipped

`spec.md` 9,628 → 9,061 B (94.0% → 88.5%). `open.md` 4,843 → 4,576 B
(94.6% → 89.4%). `decisions/ble.md` 11,057 → 11,037 B as a side effect of the
duplication fix. Both target files PAID out of reserve.

**Cut from `spec.md` (§9 cold):** the five-point ESP32-C5 SRAM percentage
history (90.87 / 98.44 / 99.18 / 81.12 / 87.04) — superseded measurements, and
the two overflow narratives they came from are decisions 27 and 38 in
`decisions/dispatch.md`; the superseded bound sizes (`19,887` inbound, `9,270`
outbound) and the ~10.5 KB they freed; the `gatt_activity` deletion; the
`SCAN_SEEN_MAX` census narrative; "decision 43 reversed the ESP32-C5 retarget".
The current 87.04% figure and "has overflowed three times" stayed — that is the
live constraint.

**Moved, not deleted:** the `tx_scratch` / `struct dbm_study_start` lever now
lives only in `open.md` (§3: a known limitation is open.md's, not spec's);
`spec.md` keeps a one-clause pointer so the SRAM paragraph still names the
lever. The `.eap` byte-cap rationale collapsed to a pointer at decision 41, and
the no-I/O-capability restatement was removed from `decisions/ble.md`, leaving
its pointer at `open.md`. `check-duplication.py` went 5 overlaps → 1, and that
one is the four-file split working (a spec invariant, a decision explaining it).

**Kept verbatim in substance, per `Must not delete:`** the six-part failure
signature, the *Rejected: a 16-byte TX boundary* clause with all six short-by
counts and the seventh complete frame, and the 899,843 ms / 46,320 ms uptime
pair. Untouched.

**`open.md` is close to "bytes can only come from rules".** Every one of its 17
bullets survives in `collect-open-questions.py`; the 267 B came entirely from
mechanism clauses that `decisions/` already owns (the union sizing → decision
38, the fatal-path sink → spec §4, Just Works/L4 → decisions 34 and 37, the
per-study-verbosity history → decision 39) plus one provenance clause. There is
no second pass of that kind left in it: what remains is claims, rejections and
what-would-close-it. A future compaction of `open.md` would have to drop whole
items, and each would need naming as answered.

**§7's question, answered:** yes. `spec.md` alone now carries the board and its
`link_port_interface = 2` trap, the v1 boundary, the source tree and the west
layout rule, all ten invariants, the three-writer TX contract and the three sink
threading rules, and every live constant with its provenance and its failure
mode. What left it was how those numbers were arrived at, not what they are, and
nothing that left changes a decision someone would make today.
