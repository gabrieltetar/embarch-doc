# 031 — `DOC-BUDGET.md` crossed into reserve, and it had 5 bytes before it did

**State:** open
**Scope:** doc
**Hardware:** none
**Owner:** required — `DOC-BUDGET.md` is on `fleet.toml`'s `reserved` list and is *"the one a
worker would most like to edit — it defines the caps"*. `queue-status.py` gates this out of the
dispatchable count. Filed here rather than in `inbox/` because `inbox/` is not committed, so a
debt filed there passes on the filer's machine and fails in CI (`tasks/README.md`).
**Source:** owner's session 2026-09-09, the commit closing `tasks/doc/030`. That change had to
document a new `check-doc-size.py` failure — a `blocked` debt with no due date — in the doc whose
own text says *"`scripts/check-doc-size.py` implements everything here"*, and the file had
**5 bytes** of clearance (11,054 B against an 11,059 B reserve line). Any correct edge was going
to cross it.

**Compacts:** DOC-BUDGET.md
**Size debt due:** 2026-09-23
**In flux:** yes — three policy changes landed in this file in three days (split-as-default,
the reserve byte floor, the assembled-file exemption), then the ledger and the per-decision cap,
then this. **State is `open` rather than `blocked` under the `Owner: required` exemption**
(`tasks/README.md`, `.claude/leg.md`): ownership already keeps every agent off it, so `blocked`
would protect nothing and would hide the debt from the only actor who can pay it. That is
`tasks/doc/024`'s argument, generalised by `tasks/doc/030` on the day this was filed.
**Must not delete:** the measured numbers each rule was set from — the 350 B / ~940 B / 1,548 B
amendment costs behind `RESERVE_FLOOR`, the `features.md` 20,444-of-20,480 and `core-link.md`
22-bytes states behind the assembled-file exemption, the 307-decision distribution behind the
4 KB per-decision cap, and `bind.md`'s decision 22 at 10,605 of 11,409 B. Each is the whole
evidence for a number that reads as arbitrary the moment its measurement goes. The
`ops.md` → `budget.md` worked example, which is the only place a split's 2,553 B saving is
compared against four squeeze passes that achieved nothing.

## The seam, stated, because the next amendment will need it

`DOC-COMPACTION.md` §2 makes a split the default remedy and this file has real `##` sections, so
the next edit here is a split someone has already thought about rather than a squeeze under time
pressure. **The seam is the per-decision cap** (`## The per-decision cap: 4 KB`, ~1.4 KB): it is a
different object from the rest of the file — every other rule here is about a *file*, that one is
about an *entry* — and it is cited by number nowhere, so moving it breaks no reference. Second
choice is `## The ratchet moves in steps`, which is mechanism rather than budget.

**Do not split the caps table, the reserve or the ledger apart from each other.** They are one
argument: a cap that refuses displaces growth, so there is a reserve; a reserve is only a warning,
so there is a ledger; a ledger parks, so there is a clock. Splitting mid-chain is how a reader gets
the rule without the reason it is bounded.

## Done when

- [ ] `DOC-BUDGET.md` is out of reserve — by the split above, another seam argued in its place, or
      a deliberate cap raise with the reason recorded. **The owner's call either way**, since
      `DOC-PROTOCOL.md` reserves structural decisions about the corpus.
- [ ] `DOC-COMPACTION.md` §2's pointer and every `§2` reference elsewhere still resolve (there were
      twelve when this file was split out); `scripts/check-links.py` and
      `scripts/check-decision-refs.py` green.
- [ ] The human question answered in the commit message, in the compactor's own words
      (`DOC-COMPACTION-PASS.md`): can this file alone answer what a doc may weigh and what counts
      as a debt?
- [ ] The `Must not delete:` list above survives, or each dropped item is named and argued.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
