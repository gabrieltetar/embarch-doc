# embarch-doc: compaction protocol

**Status:** active, 2026-09-02.

## 1. The invariant

**Keep what a reader acts on, drop the rest, and let git hold it.** Efficiency and modularity are the goal; losslessness is not — the first version of this protocol was lossless about facts, was followed faithfully, and produced a 2.66 MB corpus with single files at 311 KB. **A doc nobody can load whole is a doc nobody reads.** The first pass took it to 887 KB.

**Git is not a fallback here, it is the design:** every deletion is one `git log -p` away, forever, and that is what makes these deletions safe rather than reckless.

Three practices:

1. **Every file has a size cap by role**, enforced as a ratchet (§2).
2. **A sub-project is four small files, not one big one** (§3).
3. **History does not live in a doc at all** — `changelog.d/` fragments, assembled into `history/` (§4).

**How a doc is made smaller is [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md)** — the procedure, the gate, the failure modes and the hot/cold test. This file is the budget every session writing a doc needs; that one is needed only while compacting.

## 2. The budget

`scripts/check-doc-size.py` enforces this in CI. A file may shrink freely; it may never grow past `min(cap, its baseline)`.

| Role | Cap | Path |
|---|---|---|
| Spec — what is true now | **10 KB** | `<sub-project>/spec.md` |
| Decisions — why | **25 KB** | `<sub-project>/decisions.md` |
| One decision group, where they outgrow a file | **12 KB** | `<sub-project>/decisions/<topic>.md` |
| Open questions | **5 KB** | `<sub-project>/open.md` |
| Interface reference, only where big | **15 KB** | `<sub-project>/interfaces.md` |
| One interface group, where they outgrow a file | **12 KB** | `<sub-project>/interfaces/<topic>.md` |
| Suite-level doc | **10 KB** | `suite/*.md` |
| A complete inventory table — every row must be there | **15 KB** | `suite/roadmap.md` |
| An assembled inventory — the budget is per row, not per file | **20 KB** | `suite/features.md`, from `features.d/` |
| A narrative guide | **25 KB** | `suite/{user,studies}-guide.md` |
| A protocol doc | **12 KB** | `DOC-*.md` |
| Reversals index | **10 KB** | `embarch-decision-reversals.md` |
| Reversal range | **20 KB** | `reversals/rows-<a>-<b>.md` |
| Assembled history | **20 KB** | `history/*.md`, rolled to `history/archive/` |

**Nothing is over cap and the baseline holds no exceptions.** A file that is somehow pinned reaches its cap, retires its entry, and is capped from then on. `--report` shows the corpus, `--update` records progress and **refuses a regression**, `--pressure` lists what is near its limit **before** a task that must write there is dispatched. Per-sub-project overrides tighten a cap where [the second pass](DOC-COMPACTION-PASS.md) has landed.

**An inventory of a suite still being built has no quiet state**, so the in-flux warning's wait never comes and no pass helps — every row must be there. `suite/features.md` is therefore **assembled**, one fragment per row, and the budget it answers to is the row's ([features.d/](features.d/README.md)).

**The last 10% of a limit is the RESERVE, and it is writable** — a cap a worker meets only when its edit is refused turns unrelated work into a compaction task mid-flight. A file in reserve still passes the gate but must be named on a `**Compacts:**` line of an open task **in the scope directory of the doc being compacted**, not `tasks/doc/`, **filed by whoever spends it, in the same commit**: that actor alone can answer the in-flux question ([DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md)). `--pressure` lists the reserve, filed and unfiled; `tasks/README.md` has the shape.

**A parked compaction task is a deferral, not a wall.** `In flux: yes` correctly refuses a *separate* compaction pass — but it does nothing about the reserve, so the next unit to write there hits the cap mid-flight anyway, which is what the reserve exists to prevent. On 2026-09-05 it did something worse than that: `embarch-api/decisions/zephyr.md` had 96 bytes left, so a decision that belonged in it was **filed in `decisions/shape.md` instead** — the first time in this suite a byte cap moved a decision rather than shortening one. **A cap that misfiles is worse than a cap that refuses**, because nothing fails and the reader never learns.

So when a file is in reserve and its task is `blocked` on `In flux: yes`, **the compaction rides in the unit that is about to write that file** — same actor, same commit, carrying the parked task's `Must not delete:` list and closing only that file's item. That actor is the one *making* the flux, so it is the only one who can shorten a paragraph without writing a clean statement of something about to be wrong. **Splitting is the other move and it is cheaper still**: a `decisions/<topic>.md` or `interfaces/<topic>.md` split by mission (§3) moves entries verbatim, so the in-flux objection does not apply to it at all — it restates nothing. Prefer it whenever the file holds more than one mission.

**The cap is the design constraint, not a target to approach.** A budget forces the question "is this the most valuable 10 KB I can write about this component", never asked before there was one.

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
