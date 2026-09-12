# 031 — `suite/decisions.md` entered its reserve on its second decision, and the file is two decisions old

**State:** open
**Source:** `tasks/suite/028`'s own fold, leg 087, 2026-09-11. `DOC-COMPACTION.md` §2 — the commit
that spends the reserve is the one that files the debt, and this is that filing.
**Scope:** suite
**Hardware:** none
**Owner:** no

**Compacts:** suite/decisions.md
**Size debt due:** 2026-10-11
**In flux:** no. Decision 1 has been stable since 2026-09-06 and was moved here verbatim on
2026-09-10; decision 2 was just decided and its reversal condition is written. Neither is
mid-change. The file is not in flux — it is disproportionate.
**Must not delete:** decision 1's **command-spelling analysis** — that bare `cargo fmt`,
`cargo fmt --all` and per-crate `--check` reach three different sets of files, that `--all` reaches
*sideways through path deps into sibling repos*, and that `fmt` follows `members` while
`clippy --all-targets` follows `default-members`. That is the part nobody will re-derive, and it
fails **silently** when got wrong, which is why it is worth its bytes. Also keep decision 1's
**reversal condition** and decision 2's, and decision 2's **cross-decoder rationale** — that a leg
which can only ever skip is worse than an absent one, because a permanent skip reads as coverage.

## What

`suite/decisions.md` is **9,472 of 10,240 B — 92.5% of cap, 768 B of headroom** — after
`tasks/suite/028` added decision 2. It holds **two decisions**, so the cap is not being reached by
accumulation; decision 1 alone is roughly 4.3 KB of one paragraph.

**Read `DOC-BUDGET.md`'s split-first rule before squeezing anything.** A two-decision file is the
worst possible candidate for a topic split — there is no second topic yet — so this one probably
*is* a compaction of decision 1 rather than a split, which makes it the unusual case the ledger
calls "one sprawling decision". `scripts/check-doc-size.py --decisions` will say which shape the
file is in when this is picked up, and by then there may be a third decision that changes the
answer.

The specific shape of decision 1's sprawl: it is a **single unbroken paragraph** carrying a
sequencing decision, a measurement history across six crates and eleven commits, a reversal
condition, a four-way command-spelling analysis, and a per-repo audit of which crates each spelling
reaches. Every one of those is worth keeping (see `Must not delete:`), and **none of them is
findable**, which is the actual defect — the bytes are less of a problem than the fact that a
reader looking for the spelling trap has to read a measurement history to reach it. Structure it
before shortening it, and the shortening may mostly follow.

## Why now

This file exists because a suite-wide call had nowhere to go and kept accumulating inside a
principle bullet in `embarch.md` §5 (`tasks/suite/008`). It was created to be the place those go —
so a file that is nearly full at two entries will push the third one back into exactly the habit it
was built to end.

## Done when

- [ ] `suite/decisions.md` is out of reserve (below 90% of its 10,240 B cap) with nothing on the
      `Must not delete:` list removed or weakened.
- [ ] Decision 1's content is navigable — the measurement history, the reversal condition and the
      command-spelling trap are each findable without reading the other two.
- [ ] Whoever runs this answers `DOC-COMPACTION-PASS.md`'s human question in the supervisor's log
      entry, in their own words.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.
