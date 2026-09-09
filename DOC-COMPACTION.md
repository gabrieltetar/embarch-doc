# embarch-doc: compaction protocol

**Status:** active, 2026-09-02.

## 1. The invariant

**Keep what a reader acts on, drop the rest, and let git hold it.** Efficiency and modularity are the goal; losslessness is not — the first version of this protocol was lossless about facts, was followed faithfully, and produced a 2.66 MB corpus with single files at 311 KB. **A doc nobody can load whole is a doc nobody reads.** The first pass took it to 887 KB.

**Git is not a fallback here, it is the design:** every deletion is one `git log -p` away, forever, and that is what makes these deletions safe rather than reckless.

**Lossy licences dropping a whole topic; it never licences dropping a clause inside a topic you are keeping.** The reader of a dropped topic knows to go to git. The reader of a quietly shortened paragraph does not know anything was shortened, and on 2026-09-09 read a live API parameter out of `embarch-ui` decision 11 that way — so "only invariants matter, texture is allowed to go" is **rejected**, and [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md)'s *summarising instead of choosing* failure mode was already the same rule from the other end.

Three practices:

1. **Every file has a size cap by role**, enforced as a ratchet (§2).
2. **A sub-project is four small files, not one big one** (§3).
3. **History does not live in a doc at all** — `changelog.d/` fragments, assembled into `history/` (§4).

**Three files, and this is the first.** This one is the invariant and the shape of the corpus: why compaction happens at all, and what a compacted sub-project looks like when it is done. [DOC-BUDGET.md](DOC-BUDGET.md) is what a doc may *weigh* — the caps table, the ratchet, the reserve, the debt ledger, the per-decision cap. [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md) is how a doc is actually made smaller — the procedure, the gate, the failure modes and the hot/cold test.

**So this file alone cannot tell you whether a given doc should be compacted today, and since 2026-09-07 it is not meant to:** that answer is a byte count, and the byte counts left with §2. What it answers alone is the question that comes first and that a session gets wrong — what compaction is *for*, and therefore which of two files to write. Deciding needs this one and `DOC-BUDGET.md` together; compacting needs all three.

## 2. The budget

**Moved to [DOC-BUDGET.md](DOC-BUDGET.md)** — the caps table, the ratchet, the
reserve, the debt ledger and the per-decision cap. Split out 2026-09-07 rather
than squeezed, under this file's own rule; every `§2` reference elsewhere still
points here.

## 3. Four files per sub-project

Split by *when a reader needs it*, so the default load is small:

- **`spec.md` (10 KB)** — what is true now, and nothing about how it got that way. Purpose in three sentences; the invariants as a list; the interfaces (endpoints, types, actions, wire shapes) or a pointer to `interfaces.md`; the constants table with `[measured <date>]`/`[assumed]` on each; **what this component deliberately does not do**; pointers out. **This is what an agent loads to work on the component, usually the only file.**
- **`decisions.md` (25 KB)** — why, one entry per decision (§5). Loaded when someone asks "why is it like this" or is about to change it.
  **Where they do not fit one file, split them by mission** into `decisions/<topic>.md` (12 KB each), leaving `decisions.md` as a ~2 KB index: mission → file → the decision numbers in it. **A session is usually there for one mission**, and a component owning several distinct jobs will not compress into 25 KB **without cutting the rejected alternatives the budget exists to protect.** **Do not split preemptively: one `decisions.md` is better while it fits.**
- **`open.md` (5 KB)** — unresolved questions and known limitations, each with what would unblock it. `collect-open-questions.py` reads these.
- **`interfaces.md` (15 KB)** — only where the reference doesn't fit in `spec.md`, splitting into `interfaces/<topic>.md` the way decisions do. Not preemptively.

A milestone doc is not on this list: a shipped one folds into the four and is deleted.

## 4. History

Not in a doc. Every change drops a one-line fragment in `changelog.d/` (`<scope>-<slug>.<category>.md`, 200 B — [its README](changelog.d/README.md)); `build_changelog.py` assembles them per sub-project into `history/<scope>.md`.

What survives a compaction as history, and nowhere else:

- **Reality-driven reversals** — [embarch-decision-reversals.md](embarch-decision-reversals.md), one row: what was assumed, what reality showed, which decision owns it. A *design* doc, not history: it is predictive — which assumptions to distrust. **It does not restate a correction's mechanism** — that is the owning decision's job — but it keeps the *transferable* clause, which usually exists nowhere else. It is an index plus `reversals/rows-<a>-<b>.md`; **a row number is a permanent identity, so a range never re-splits an existing row** — a new range is appended, an unbalanced one left unbalanced. The index carries the recurring *shapes* across the rows, **the one thing no individual row holds.**
- **Measurement provenance** — a measured number keeps its date and the conditions it was taken under, inline in the constants table. A constant that silently loses its provenance is the failure mode this suite keeps hitting.

Everything else about the past is dropped: amendment chains, schema-bump re-derivations, "**Implemented 2026-08-25**", review-item numbers, "this pass", "the same session".

## 5. What a decision entry looks like

Target **400 B**, ceiling **1,200 B**. A number-first heading stating the claim, then the constraint, the prohibitions, one clause per rejected alternative. [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md) is what belongs in it and what does not.

**The number is permanent and an entry may own several** — `### 20, 21, 25, 27 — Streaming capture, batched, with units` is one entry owning four, because four decisions converged. Never renumbered, never reused, and a retired one becomes a tombstone keeping its number: [DOC-CONVENTIONS.md](DOC-CONVENTIONS.md) owns that rule and the two ways it has broken.
