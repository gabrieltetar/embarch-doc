# 017 — Compact or split `embarch-outpost/decisions/testing.md` decision 22

**State:** done — leg 078, 2026-09-10, `agent/outpost/017-compact-outpost`
**Reserve for this scope:** nothing in `embarch-outpost` is in file-level reserve; the debt here is
the per-decision cap named below.
**Source:** filed by leg 076's supervisor against its own unit. `outpost/016` edited decision 22 and
grew it 4,258 B → 4,442 B against the 4,096 B per-decision cap. **It was already over before that
edit** — this is not a debt `outpost/016` created, but it is one `outpost/016` made worse and that
nothing had filed, which is the same obligation.
**Scope:** outpost
**Hardware:** none
**Owner:** no
**Compacts:** embarch-outpost/decisions/testing.md#22
**In flux:** no — decision 22's DECIDES clause (skip-not-fail) has been stable and `outpost/016`
explicitly did not touch it; what grew was the rejected-alternative prose around it.
**Size debt due:** 2026-09-24

## What

Decision 22 in [embarch-outpost/decisions/testing.md](../../embarch-outpost/decisions/testing.md)
is 4,442 B against a 4,096 B per-decision cap. Bring it under.

**Prefer a verbatim split** ([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2). The file is well
under its own file-level cap, so — as `api/062` found on this same leg — a split into two numbered
decisions **staying in the same file** is legal and is often the honest answer when one number has
accreted two separate judgments. Check whether that is what happened here before compacting prose.

**Must not delete:**
- the skip-not-fail DECIDES clause itself, which is what the decision is;
- the statement that `embarch-outpost` has no CI, "no, and never has been" per `embarch.md` §5;
- the fact that whether outpost should get a workflow is an open, unfiled suite-scope question —
  `outpost/016` deliberately left it unfiled rather than pointing at a task that did not cover it.

**A written "no safe cut" is an acceptable outcome**, with the argument and what a cut would have
destroyed.

## Why now

The per-decision cap is checked by `scripts/check-doc-size.py --decisions` and **the size ledger
cannot see it** — the ledger clocks files, so an over-cap decision inside an under-cap file has no
due date and nothing schedules it. That is the finding leg 076's refill sweep turned up, and it is
why this task carries an explicit `**Size debt due:**` of its own rather than relying on the ledger
to notice.

## Done when

- [x] `python3 scripts/check-doc-size.py --decisions` no longer reports
      `embarch-outpost/decisions/testing.md#22` as OVER, or the task closes with a written argument.
- [x] Every citation of outpost decision 22 still resolves; `scripts/check-decision-refs.py` green.
      If a split moves it to a new file, the half with out-of-scope citers keeps the filename.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment; `status.d/` fragment for anything suite-level this makes false.

## Resolution

Decision 22's title already carried two judgments — the `WEST`-guard ordering fix, and the
skip-not-fail/loud-restatement behavior of `cross_decoder.py` — bundled under one number because
they landed in the same edit, not because they are one decision. Split verbatim, in the same file
(`decisions/testing.md`), no prose squeezed:

- **22** — both toolchain-free legs run above the `WEST` guard (unchanged prose, retitled to its
  own half).
- **23** (new) — a missing sibling-repo fixture is a skip, not a failure, and that skip survives to
  the exit summary via the `EXIT` trap (unchanged prose, retitled to its own half).

Neither half needed a cut to fit the 4,096 B cap once separated — `#22` and `#23` both land well
under it. Updated: `decisions.md` index row (`22, 23`), `decisions/module.md`'s historical note
about the move, and `decisions/wire.md`'s citation of the skip-and-check convention (was pointing
at 22, correctly retargeted to 23 since that is the half it actually describes). `open.md`'s
citation of the ordering fix already pointed at 22 and needed no change. All three `Must not
delete` items — the skip-not-fail DECIDES clause, the "no CI, never has been" fact, and the unfiled
suite-scope CI-workflow question — are intact, now in decision 23's text.

`check-doc-size.py --decisions` no longer lists `testing.md#22` (or `#23`) as OVER.
`check-decision-refs.py` and the full `check-docs.py` gate are green.
`check-ownership.py --scope outpost` (doc worktree) and `--code-repo` (code worktree) both green.
`check-client-names.py --repo` against the code worktree: clean. The code worktree has no changes
— this task was doc-only.
