# embarch-doc: running a compaction pass

**Status:** active, 2026-09-04. How a doc is made smaller: the procedure, the gate, the failure modes, and the hot/cold test. Split out of [DOC-COMPACTION.md](DOC-COMPACTION.md) §6–§9 on 2026-09-04 when that doc reached its size cap ([DOC-COMPACTION.md](DOC-COMPACTION.md) §3). **Bare `§N` references below are that doc's**; anything else names its doc.

That file is the budget — what a doc may weigh, which of the four files it is, what an entry looks like — and every session writing a doc needs it. This one is needed only when actually compacting, which is why the two stopped sharing a file.

## Procedure

Working tree clean and pushed first — **git is where everything you delete goes.** Snapshot `collect-open-questions.py` before and after.

`scripts/check-duplication.py` first: the cheapest bytes are a claim held in two of the four files, which is a §3 error rather than a cold sentence. Then **read the whole doc**, because **the merges that matter are between paragraphs 200 lines apart.** Then **write `spec.md` from scratch, to its cap** — not by deleting from the old doc, **because compaction by deletion preserves the old doc's shape, which is the problem** — and check the old one afterwards for facts you missed. Then `decisions.md` (§5, and the hot/cold test below), then `open.md`.

**Delete the old files and fix every inbound link in the same commit**: this repo commits straight to `main` and **must not be left broken in between.** One sub-project per commit, with a `changelog.d/` fragment.

## The gate

**Mechanical, in CI**, all at once via `scripts/check-docs.py`: `check-doc-size.py` (caps and the ratchet), `check-decision-refs.py` (**every `decision N` still resolves — what makes merging and file-moving safe**), `check-links.py`, `check-staleness.py`, `check-doc-conventions.py`, `build_changelog.py --check`. Plus a diff of `collect-open-questions.py`: **a question may disappear only if you can name it as answered.**

**Human, and not skippable — one question, asked honestly:**

> Can `spec.md` alone answer what someone needs to work on this component today?

**If yes, the pass is done, whatever it deleted. If no, the pass moved bytes rather than choosing between them.**

**Never replace a name with the kind of thing it is** — "provisioning is a separate step" instead of `build_and_flash`; drop the sentence instead. An identifier-set diff catches it, advisory only: under a lossy regime an identifier is *allowed* to go.

## Failure modes

- **Summarising instead of choosing.** "Handles the error cases" for four named ones. A budget is spent by *dropping whole topics*, not by making every sentence vaguer.
- **Deleting the "why not".** One line each, always. §5.
- **Flattening measured into assumed.** §4.
- **Renumbering.** §5. 2,362 references, invisible to detect.
- **Compacting a doc whose subsystem is still in flux** — you would write a clean statement of something about to be wrong, and destroy the alternatives you are about to need. Wait for the milestone to close.
- **Moving bytes instead of choosing between them.** Four files that add up to 300 KB is the old problem with more filenames. *The gate*'s human question above is the check.

## The second pass: keep the hot half, delete the cold

The first pass made every doc loadable — every sub-project and every suite-level doc, one commit each. **It did not separate what an agent must not break from what merely justifies it**, and decision prose remained the largest thing an agent loads.

**The test, per sentence: would someone about to change this code make a wrong move without it?** **Yes → hot, it stays. No, it only answers "how do we know?" → cold, it goes** — git holds it, and **a cold item worth keeping at all earns a 250 B row on [embarch-decision-reversals.md](embarch-decision-reversals.md), cited by number, not a paragraph here.**

**Hot, none of it negotiable:** the claim · the constraint that makes it necessary · the invariant or prohibition · **rejected alternatives, one clause each with their reason** · **the failure signature**, what it looks like when this is wrong, which is what makes a rule actionable · any live property of another component a reader would get wrong.

**Cold:** provenance and dates · the incident narrative · the investigation log · measurements · validation records · superseded reasoning · meta-lessons. **A reference table is not cold — it moves to `interfaces/`, loaded deliberately.**

**The refinement that keeps this from gutting the docs: "why" is two things and only one is cold.** A *constraint* reason — *"a serial cannot help here: that one probe exposes two VCOMs under one serial"* — **is hot, because a reader who does not know it re-proposes the fix that was already rejected.** The evidence behind that rule is cold. **Rejections and constraints never go:** the reversals page is largely a record of already-rejected things being re-proposed, so deleting the rejections would grow it.

**The decisions layer bottoms out near 350 KB, and past that the cuts take rules.** A sub-project at ~900 B per decision has no cold half left. **Run this pass on one that has not had it; do not run it twice** — measured across all eight, deletable cold is ~18% by sentence and the deletion recovers less again, almost all of it from sub-projects that have never had a pass at this density. Projecting that figure from a single entry gave ~210 KB and was wrong: reversals row 18's trap.

**Caps tighten per sub-project as its pass lands**, via `TIGHTENED` in `check-doc-size.py` — a finished migration cannot drift back, and an unfinished one is not failed by a cap it has not been given yet.
