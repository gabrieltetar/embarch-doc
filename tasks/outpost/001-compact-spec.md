# 001 — embarch-outpost/spec.md is in reserve

**State:** done, 2026-09-04, agent/outpost/001-compact-spec
**Source:** scripts/check-doc-size.py --pressure
**Scope:** outpost
**Hardware:** none
**Compacts:** embarch-outpost/spec.md
**In flux:** no
**Must not delete:** §4's measured cost table with its provenance — the instrument's own overhead is the number every conclusion drawn from a trace rests on; the statement that **both clocks are on the wire and neither substitutes for the other**, which is what layout 3 changed and what §1–§2 went on contradicting for days after it landed.

## What

`spec.md` is at ~90% of 10 KB, the shallowest entry in the reserve, so this is
the least urgent of the seven and the one with the most room to be done well.

**This sub-project has already had the §9 pass** — it is the only entry in
`check-doc-size.py`'s `TIGHTENED` map, and its decision groups are held at 8 KB
because of it. §9 says do not run that pass twice: a sub-project at its hot
floor has no cold half left and further cuts take rules. So the answer here is
**not** another hot/cold sweep of `decisions/`. It is either a genuine
duplication (run `scripts/check-duplication.py embarch-outpost`, which reports
31 overlaps — by far the most in the suite, including a 36-word run between
`decisions/tracing.md` and `open.md`) or a reference table that belongs in
`interfaces/`, where `wire.md` and `integration.md` already are.

## Why now

Deepest in the reserve of the three specs, and the 31 overlaps say the bytes
are there without touching a rule.

## Done when

- [x] `spec.md` out of reserve, and the duplication count down.
- [x] No decision text is cut. Nothing under `decisions/` was touched.
- [x] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [x] Gate green, `changelog.d/outpost-*` fragment dropped.

## What shipped

`spec.md` **9235 → 8317 B** (90.2% → 81.2% of 10 KB, 1923 B of headroom). Only
`spec.md` changed; `decisions/`, `interfaces/` and `open.md` are untouched.
Duplication **31 → 29** overlaps, `spec.md`'s own share **9 → 7**.

Three cuts, all of them a claim another file already owns:

- **§1's purpose, ~1815 → ~900 B.** The illustration of the question (a GATT
  write, forty context switches, a 9.9 µs ISR) went whole — §4's resolution rows
  are the same fact as a number. The no-inference paragraph is one sentence now,
  keeping the claim, the mechanism and **"nothing here reads a DUT's source and
  guesses."**
- **§4 lost four rows** — self-trace 50.4%, link duty 94% → 37%, frame contents
  3.3 → 20.2, ring 512 → 2048. Each is the *measured provenance of a Kconfig
  default*, and each already sits verbatim against its own symbol in
  `interfaces/integration.md`, which §4 already pointed at and now points at by
  name. What the `Must not delete:` line protects stayed: the record's 9.92 B,
  both resolutions, the 1.6% CPU share **with the 78.1% host-clock misreading
  beside it**, the burst loss, and the dates.
- **§3 lost decision 1's rejection argument** ("an opinion about which UART
  instance … a fact about someone else's board"), replaced by a pointer to
  decision 1. The prohibition itself — *never here* — is absolute in `spec.md`
  with no discretion left to a reader, which is the test I applied.

Deliberately kept, against the duplication report: the *anti-footgun* clause of
every invariant that has one — the latency floor, the fabricated interpolation,
the trace shifted by three frames, and the relabelling manifest (tightened, not
dropped). §9 calls a constraint reason hot because a reader who does not know it
re-proposes the rejected fix, and each of these is a fix someone would propose.

Deliberately not touched: the three `open.md` ↔ `decisions/` overlaps, including
the 36-word one. `open.md` is not under pressure, and neither copy is the wrong
one — a decision stating its own limits and `open.md` tracking them as live is
DOC-PROTOCOL.md §3 working. Resolving them would have meant cutting either
decision text or a known limitation.

**§7's question — can `spec.md` alone answer what someone needs to work on this
component today?** Yes, and on one point better than before: what it lost was
evidence for numbers that are not its own, and every one of those numbers is now
exactly one file away, next to the knob it sets.
