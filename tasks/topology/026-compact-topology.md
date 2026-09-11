# 026 — `embarch-topology/decisions/links.md` is in reserve after `api/042`'s fold

**State:** open
**Source:** `api/042`'s fold, leg 074, 2026-09-10. **The supervisor spent this reserve, not a
worker.** Consuming `api/042`'s `status.d/` fragment meant annotating decision 18 in another
sub-project's decisions file — a write only the supervisor may make (`protocol.md` §3) — and that
annotation crossed the reserve line. `DOC-COMPACTION.md` §2: the commit that spends the reserve is
the one that files the debt, and this is that filing.
**Scope:** topology
**Hardware:** none
**Owner:** no

**Compacts:** embarch-topology/decisions/links.md
**Size debt due:** 2026-09-24
**In flux:** no. Decision 18's subject — the DUT signal link, its route, and the deliberate absence
of a CLI mirror *in this crate* — has been stable since it landed, and the annotation added at this
fold settles the one question that was live about it (whether `embarch-api` surfacing the same
routes contradicts it: it does not). Decision 17 and decision 24 are likewise closed. Nothing in
this file is currently being rewritten by anything in the queue.
**Must not delete:**
- **Decision 18's stated cost, verbatim:** *"a bench with no Core running has no terminal path to
  declare a signal, inconsistent with decision 17's CLI, and stays that way rather than being
  retired on speculation."* It is the one thing `embarch-api` decision 67 did **not** fix, and the
  annotation beside it exists to stop a reader assuming otherwise. Deleting either without the
  other re-opens exactly the misreading that cost three docs a correction.
- **The second-writer distinction** in that same annotation — that what decision 18 refuses is a
  CLI in *this crate* writing the store directly, not a CLI that calls Core over HTTP. Two
  documents generalised the refusal past what it said (`embarch-ui/decisions/topology-tab.md`
  decision 10 and `suite/studies-guide.md`), and both had to be corrected at this fold. The
  distinction is what keeps that from happening a third time.
- **Decision 18's "Scope held deliberately narrow" paragraph**, naming the three shapes that are
  *not* modelled (fan-out to two destinations, between two DUTs, host-to-DUT stimulus). A reader
  who loses this reads an extensible table as an unfinished one.
- **Decision 24's `DECLARED_SERIAL` reasoning** — that the constant exists because a *different*
  rule ran, not because the VID matched. It is an honesty property about a label, and the
  paragraph is the only place the distinction from `"vid-match"` is written down.

## What

`embarch-topology/decisions/links.md` is **11,478 B against a 12,288 B cap, 810 B left against a
1,229 B floor** — 419 B inside reserve. It was 10,941 B before this fold and not in reserve; the
annotation added 537 B, already trimmed once (from ~1,020 B) when the gate went red, which is why
the remainder is small rather than nothing.

## Why the supervisor did not just trim it to zero

**It trimmed twice and stopped at the point where further cutting would have deleted the content.**
The first draft ran ~1,020 B and was cut to 537 B in place. What is left is four clauses, each
load-bearing and each listed above. A third pass would have had to start removing one of them —
and the immediately preceding leg's log entry records a supervisor doing exactly that kind of thing
and flagging it as worth pushing back on. Filing a dated debt is the mechanism that exists for this
case; using it is cheaper and more honest than shaving a paragraph that three documents now depend
on.

## Done when

- [ ] `embarch-topology/decisions/links.md` is out of reserve (below 11,059 B), or a verbatim
      mission split by decision has been done — 17, 18 and 24 are natural seams and a split
      restates nothing, so `DOC-COMPACTION.md` §2's split-first preference applies here before a
      squeeze does.
- [ ] Every `Must not delete:` item above still present and still saying what it said.
- [ ] Whoever runs this answers `DOC-COMPACTION-PASS.md`'s question in the log entry, in their own
      words: can `embarch-topology/spec.md` alone answer what someone needs to work on this
      component today? Note that `spec.md` is itself in reserve and parked under
      `tasks/topology/024`, so the honest answer may well be "no, and that is a second debt."
