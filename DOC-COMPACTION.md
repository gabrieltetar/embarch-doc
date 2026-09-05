# embarch-doc: compaction protocol

**Status:** active, 2026-09-02.

## 1. The invariant

**Keep what a reader acts on, drop the rest, and let git hold it.** Efficiency and modularity are the goal; losslessness is not — the first version of this protocol was lossless about facts, was followed faithfully, and produced a 2.66 MB corpus with single files at 311 KB. **A doc nobody can load whole is a doc nobody reads.** The first pass took it to 887 KB.

**Git is not a fallback here, it is the design:** every deletion is one `git log -p` away, forever, and that is what makes these deletions safe rather than reckless.

Three practices:

1. **Every file has a size cap by role**, enforced as a ratchet (§2).
2. **A sub-project is four small files, not one big one** (§3).
3. **History does not live in a doc at all** — `changelog.d/` fragments, assembled into `history/` (§4).

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
| A complete inventory table — every row must be there | **15 KB** | `suite/features.md`, `suite/roadmap.md` |
| A narrative guide | **25 KB** | `suite/{user,studies}-guide.md` |
| This file, and DOC-PROTOCOL.md | **12 KB** | `DOC-*.md` |
| Reversals index | **10 KB** | `embarch-decision-reversals.md` |
| Reversal range | **20 KB** | `reversals/rows-<a>-<b>.md` |
| Assembled history | **20 KB** | `history/*.md`, rolled to `history/archive/` |

**Nothing is over cap and the baseline holds no exceptions.** A file that is somehow pinned reaches its cap, retires its entry, and is capped from then on. `--report` shows the corpus, `--update` records progress and **refuses a regression**, `--pressure` lists what is near its limit **before** a task that must write there is dispatched. Per-sub-project overrides tighten a cap where §9's pass has landed.

**The cap is the design constraint, not a target to approach.** A budget forces the question "is this the most valuable 10 KB I can write about this component", which is the question that was never being asked.

## 3. Four files per sub-project

Split by *when a reader needs it*, so the default load is small:

- **`spec.md` (10 KB)** — what is true now, and nothing about how it got that way. Purpose in three sentences; the invariants as a list; the interfaces (endpoints, types, actions, wire shapes) or a pointer to `interfaces.md`; the constants table with `[measured <date>]`/`[assumed]` on each; **what this component deliberately does not do**; pointers out. **This is the file an agent loads to work on the component, and usually the only one.**
- **`decisions.md` (25 KB)** — why, one entry per decision (§5). Loaded when someone asks "why is it like this" or is about to change it.
  **Where they do not fit one file, split them by mission** into `decisions/<topic>.md` (12 KB each), leaving `decisions.md` as a ~2 KB index: mission → file → the decision numbers in it. **A session is usually there for one mission**, and a component owning several distinct jobs will not compress into 25 KB **without cutting the rejected alternatives the budget exists to protect.** **Do not split preemptively: one `decisions.md` is better while it fits.**
- **`open.md` (5 KB)** — unresolved questions and known limitations, each with what would unblock it. `collect-open-questions.py` reads these.
- **`interfaces.md` (15 KB)** — only where the interface reference genuinely doesn't fit in `spec.md`, splitting into `interfaces/<topic>.md` the way decisions do. Do not create one preemptively.

A milestone doc is not on this list: a shipped one folds into these four and is deleted.

## 4. History

Not in a doc. Every change drops a one-line fragment in `changelog.d/` (`<scope>-<slug>.<category>.md`, 200 B hard limit — [changelog.d/README.md](changelog.d/README.md)); `build_changelog.py` assembles them per sub-project into `history/<scope>.md`.

What survives a compaction as history, and nowhere else:

- **Reality-driven reversals** — [embarch-decision-reversals.md](embarch-decision-reversals.md), one row: what was assumed, what reality showed, which decision owns it. A *design* doc rather than history, because it is predictive: it says which remaining assumptions to distrust. **It does not restate a correction's mechanism** — that is the owning decision's job — but it keeps the *transferable* clause, which usually exists nowhere else. It is an index plus `reversals/rows-<a>-<b>.md`; **a row number is a permanent identity, so a range never re-splits an existing row** — a new range is appended, an unbalanced one left unbalanced. The index carries the recurring *shapes* across the rows, **the one thing no individual row holds.**
- **Measurement provenance** — a measured number keeps its date and the conditions it was taken under, inline in the constants table. A constant that silently loses its provenance is the failure mode this suite keeps hitting.

Everything else about the past is dropped: amendment chains, schema-bump re-derivations, "**Implemented 2026-08-25**", review-item numbers, "this pass", "the same session".

## 5. What a decision entry looks like

Target **400 B**, ceiling **1,200 B**. A number-first heading stating the claim, then the constraint, the prohibitions, and one clause per rejected alternative. §9 is what belongs in it and what does not.

### Numbers are permanent, and an entry may own several

A number addresses the **sub-project**, never a file or a section: `### 20, 21, 25, 27 — Streaming capture, batched, with units` is one entry owning four, because four decisions converged. **Never renumber and never reuse** — 2,362 prose references point at these, `check-decision-refs.py` resolves every one, and an insertion that renumbers the entry below it silently repoints every reference elsewhere (twice so far; DOC-PROTOCOL.md §7.3). A retired entry becomes a one-line tombstone keeping its number.

## 6. Procedure

Working tree clean and pushed first — **git is where everything you are about to delete goes.** Snapshot `collect-open-questions.py` before and after.

**Read the whole doc first**, because **the merges that matter are between paragraphs 200 lines apart.** Then **write `spec.md` from scratch, to its cap** — not by deleting from the old doc, **because compaction by deletion preserves the old doc's shape, which is the problem** — and check the old one afterwards for facts you missed. Then `decisions.md` (§5, §9), then `open.md`.

**Delete the old files and fix every inbound link in the same commit**: this repo commits straight to `main` and **must not be left broken in between.** One sub-project per commit, with a `changelog.d/` fragment.

## 7. The gate

**Mechanical, in CI**, all of them at once via `scripts/check-docs.py`: `check-doc-size.py` (caps and the ratchet), `check-decision-refs.py` (**every `decision N` still resolves — what makes merging and file-moving safe**), `check-links.py`, `check-staleness.py`, `check-doc-conventions.py`, `build_changelog.py --check`. Plus a diff of `collect-open-questions.py`: **a question may disappear only if you can name it as answered.**

**Human, and not skippable — one question, asked honestly:**

> Can `spec.md` alone answer what someone needs to work on this component today?

**If yes, the pass is done, whatever it deleted. If no, the pass moved bytes rather than choosing between them.**

An identifier-set diff is advisory — **under a lossy regime an identifier is *allowed* to go.** Run it for the one failure mode still a defect: **a concrete noun replaced by its category** — "provisioning is a separate step" instead of `build_and_flash`. **Never replace a name with the kind of thing it is; drop the sentence instead.**

## 8. Failure modes

- **Summarising instead of choosing.** "Handles the error cases" for four named ones. A budget is spent by *dropping whole topics*, not by making every sentence vaguer.
- **Deleting the "why not".** One line each, always. §5.
- **Flattening measured into assumed.** §4.
- **Renumbering.** §5. 2,362 references, invisible to detect.
- **Compacting a doc whose subsystem is still in flux** — you would write a clean statement of something about to be wrong, and destroy the alternatives you are about to need. Wait for the milestone to close.
- **Moving bytes instead of choosing between them.** Four files that add up to 300 KB is the old problem with more filenames. §7's human question is the check.

## 9. The second pass: keep the hot half, delete the cold

The first pass made every doc loadable — every sub-project and every suite-level doc, one commit each. **It did not separate what an agent must not break from what merely justifies it**, and decision prose remained the largest thing an agent loads.

**The test, per sentence: would someone about to change this code make a wrong move without it?** **Yes → hot, it stays. No, it only answers "how do we know?" → cold, it goes** — git holds it, and **a cold item worth keeping at all earns a 250 B row on [embarch-decision-reversals.md](embarch-decision-reversals.md), cited by number, not a paragraph here.**

**Hot, none of it negotiable:** the claim · the constraint that makes it necessary · the invariant or prohibition · **rejected alternatives, one clause each with their reason** · **the failure signature**, what it looks like when this is wrong, which is what makes a rule actionable · any live property of another component a reader would get wrong.

**Cold:** provenance and dates · the incident narrative · the investigation log · measurements · validation records · superseded reasoning · meta-lessons. **A reference table is not cold — it moves to `interfaces/`, loaded deliberately.**

**The refinement that keeps this from gutting the docs: "why" is two things and only one is cold.** A *constraint* reason — *"a serial cannot help here: that one probe exposes two VCOMs under one serial"* — **is hot, because a reader who does not know it re-proposes the fix that was already rejected.** The evidence behind that rule is cold. **Rejections and constraints never go:** the reversals page is largely a record of already-rejected things being re-proposed, so deleting the rejections would grow it.

**What it is worth, measured across all eight sub-projects rather than projected from one entry** — projecting from one gave ~210 KB and was wrong, reversals row 18's trap. Deletable cold is **~18% by sentence** and the deletion recovers less again, **almost all of it from sub-projects that have not had a pass at this density**: one gave −33%, those compacted hours earlier gave 5–10%.

**The decisions layer bottoms out near 350 KB, and past that the cuts take rules.** A sub-project at ~900 B per decision has no cold half left. **Run this pass on one that has not had it; do not run it twice.**

**Caps tighten per sub-project as its pass lands**, via `TIGHTENED` in `check-doc-size.py` — a finished migration cannot drift back, and an unfinished one is not failed by a cap it has not been given yet.
