# embarch-doc: documentation protocol

**Status:** draft, 2026-07-20.

## 1. Purpose

This is the instruction set for how docs in this repo get kept in sync while work happens in any EmbArch sub-project repo. It exists so the behavior doesn't need to be re-explained in chat every session — a sub-project's `CLAUDE.md` points here once (§6), and this file carries the rest.

## 2. Repo layout

`embarch/` is the parent folder; every suite sub-project is a sibling directory directly under it, alongside `embarch-doc` itself:

```
embarch/
├── embarch-core/
├── embarch-api/
├── embarch-study-designer/ (types/tools implemented; embarch-dev-bench firmware not started)
├── embarch-dev-bench/      (scoping in progress, repo created empty)
├── embarch-umbrella/       (design-only, repo created empty)
├── embarch-promptu/        (planned, no repo yet)
├── embarch-atlas/          (paused, no repo yet)
└── embarch-doc/
    ├── CLAUDE.md
    ├── embarch.md
    ├── embarch-roadmap.md
    ├── embarch-features.md
    ├── embarch-user-guide.md
    ├── embarch-token.md
    ├── embarch-glossary.md      <- suite-wide term index, added 2026-08-15
    ├── embarch-decision-reversals.md  <- assumptions reality has overturned, added 2026-08-15
    ├── embarch-dev-workflow.md  <- local dev iteration across the 3 code repos, added 2026-08-17
    ├── DOC-PROTOCOL.md          <- this file
    ├── embarch-core/design.md
    ├── embarch-core/milestone-1.md
    ├── embarch-api/design.md
    ├── embarch-api/milestone-1.md
    ├── embarch-study-designer/design.md
    ├── embarch-study-designer/milestone-3.md
    ├── embarch-dev-bench/design.md
    ├── embarch-umbrella/design.md
    ├── embarch-umbrella/milestone-6.md
    ├── embarch-promptu/design.md
    └── embarch-atlas/design.md
```

Because every sub-project sits as a sibling of `embarch-doc`, its docs are always reachable by relative path from inside that sub-project's own repo: `../embarch-doc/<sub-project>/design.md`. No submodule, symlink, or absolute path is needed — that only holds as long as the layout above is preserved. If a sub-project ever gets cloned or moved somewhere that breaks the sibling relationship, this section needs revisiting first.

## 3. Where a doc lives

Two tiers:

- **Suite-level docs** (`embarch-doc/` root): [embarch.md](embarch.md) (suite overview + sub-project index), [embarch-roadmap.md](embarch-roadmap.md) (numbered milestones plus Next/Later across the whole suite), [embarch-features.md](embarch-features.md) (feature inventory across the whole suite), [embarch-user-guide.md](embarch-user-guide.md) (getting started and day-to-day usage of the assembled suite — the one doc in this repo written for a reader who isn't already inside the project, so it explains rather than links), [embarch-token.md](embarch-token.md) (`EMBARCH_TOKEN`'s full lifecycle, since it's shared across `embarch-core` and `embarch-api`), [embarch-glossary.md](embarch-glossary.md) (added 2026-08-15 — load-bearing terms used across more than one sub-project doc, each linking to its owning doc rather than restating it), [embarch-decision-reversals.md](embarch-decision-reversals.md) (added 2026-08-15 — a standing list of assumptions reality has already overturned, across every sub-project; update it in the same pass as any decision correction, per §5 below), [embarch-dev-workflow.md](embarch-dev-workflow.md) (added 2026-08-17 — how to iterate locally across `embarch-core`/`embarch-api`/`embarch-umbrella` without cutting a release or a debug build touching a real machine's install). These cover things that span more than one sub-project.
- **Sub-project docs** (`embarch-doc/<sub-project>/`): every existing or planned sub-project gets a subfolder. `design.md` is the one required file — the durable, living source of truth for that sub-project's architecture, decisions, and open questions, per [embarch.md](embarch.md) §5's "design doc as source of truth" principle. Add more files to a subfolder later (e.g. `api-reference.md`) if `design.md` grows unwieldy — don't split preemptively.
- **Milestone docs** (`embarch-doc/<sub-project>/milestone-N.md`): when a roadmap milestone (see [embarch-roadmap.md](embarch-roadmap.md)) touches a sub-project, that sub-project's half of the execution plan — concrete, ordered steps, a definition of done, open questions carried into execution — lives in its own `milestone-N.md`, separate from `design.md`. This keeps `design.md` as the architecture-of-record (what's true now) distinct from a milestone doc's job (what to do next, and why); once a milestone's steps actually ship, fold whatever they resolved back into `design.md` per §5 below rather than leaving the decision only recorded in the milestone doc.

## 4. When to update a doc

Proactively, without being asked, whenever work in a sub-project repo produces one of:

- An architecture or design decision (a new invariant, a rejected alternative, a changed data flow)
- A shipped feature, a changed API/tool surface, or a resolved open question
- A status change (Planned → Shipped, Paused → Active, etc.)
- A new open question or known limitation surfacing

Trivial/mechanical changes — formatting, dependency bumps, typo fixes, refactors with no externally-visible or architectural effect — don't need a doc update.

§4's triggers above are reactive — they fire when work happens. They don't catch a doc that just goes quiet while sibling docs move on around it. So: before marking any milestone step or roadmap milestone done, grep the suite-level docs (`embarch.md` §3, `embarch-features.md`, `embarch-roadmap.md`) for rows or mentions of that step/sub-project and confirm none of them still describe a now-superseded state (a status word like "Proposed"/"design-only"/"Todo" that the step you're closing just made false, a stale command name, a stale example). This is the same failure §5's "never disagree about status" rule exists to prevent — the difference is this check runs *before* closing the step, not after someone happens to notice the disagreement later. `embarch-features.md`'s own changelog (2026-08-04, 2026-07-22, 2026-08-11) already records three cases of exactly this drift being caught after the fact; catching it at close-time is cheaper than catching it later.

This manual grep now has an automated backstop: `scripts/check-staleness.py` (§5) runs the same cross-check mechanically on every push/PR via CI, and it isn't just theoretical — its first run found `embarch-study-designer/design.md`'s own Status line still reading "Design-only... no code yet" despite four implementation passes recorded in its own changelog since 2026-07-29 (fixed the same pass the script was written). It's a heuristic over two specific tables (`embarch.md` §3, `embarch-features.md`), not a replacement for the grep above — `embarch-roadmap.md`'s prose isn't structured enough to check mechanically, so that one still wants a human pass before closing a milestone.

## 5. How to update

- Edit the relevant numbered section of `<sub-project>/design.md` directly, so the doc stays a living description of current reality — not an append-only log. The trailing `## Changelog` section is for a one-line dated pointer to *what* changed and *why*, not a substitute for updating the body.
- Add that dated bullet to `## Changelog` for every substantive edit.
- If the change also affects suite-level facts — the status table in [embarch.md](embarch.md) §3, a Now/Next/Later bucket in [embarch-roadmap.md](embarch-roadmap.md), a row in [embarch-features.md](embarch-features.md) — update those in the same pass. A sub-project doc and the suite-level docs should never disagree about status.
- Don't restate detail across docs — [embarch-features.md](embarch-features.md) and [embarch-roadmap.md](embarch-roadmap.md) link to the specific section of a design doc rather than duplicating its content (see `embarch-features.md`'s own header note).
- Adding a new top-level file to `embarch-doc`? Add it to [embarch.md](embarch.md) §6 (Index) in the same edit — the index is only useful if it stays exhaustive.
- Renaming or moving a file, or editing anything link-heavy? `scripts/check-links.py` walks every `.md` file and reports any relative link that no longer resolves — it also runs automatically on every push/PR via `.github/workflows/docs-ci.yml`, so a broken link fails CI rather than waiting to be noticed; run it locally first if you want the fast feedback.
- Same workflow also runs `scripts/check-staleness.py`, the automated half of §4's pre-close grep — see §4 for what it does and doesn't cover.
- Changelog sections don't need manual trimming: `scripts/archive-changelog.py` keeps each doc's `## Changelog` down to its most recent entries and moves the rest into a sibling `*.changelog-archive.md`, ranked by each entry's own date rather than its position (some docs here prepend newest-first, others append oldest-first — see the script's own docstring). `.github/workflows/changelog-archive.yml` runs it weekly and opens a PR with whatever moved, rather than requiring anyone to remember to run it or pushing straight to main unreviewed.
- Want the suite-wide view of every open question instead of reading six-plus docs' own §7/§10/§12-equivalent sections one at a time? `scripts/collect-open-questions.py` (added 2026-08-15) walks every `design.md` (plus `embarch-token.md`) for its "Open questions" heading and prints every bullet, grouped by doc. Read-only and not a CI gate — an open question existing isn't a failure the way a broken link or a stale status word is; run it locally when you want the index.

## 6. How a sub-project repo hooks into this

Each sub-project repo's own `CLAUDE.md` carries a short "Docs" pointer, e.g.:

```markdown
## Docs
Design doc: ../embarch-doc/embarch-core/design.md — source of truth for this project's architecture/design.
Update it proactively per ../embarch-doc/DOC-PROTOCOL.md whenever a notable design decision, feature, or status change happens here.
```

This is the mechanism that makes §4–5 happen without re-explaining it in chat — `CLAUDE.md` loads automatically every session and points here.

## Changelog

- 2026-08-17 — Added [embarch-dev-workflow.md](embarch-dev-workflow.md) as a new suite-level doc (§2, §3): how to iterate locally across the three code repos without a release archive, and — the reason it was written now — how to avoid a debug `embarch-umbrella` build silently overwriting a real machine's canonical install/PATH while testing decision 28.
- 2026-08-15 — Closed three items from that day's design-improvement review (`.claude/design-improvements-2026-08-15.md`, local working notes): added `scripts/collect-open-questions.py` (§5) as a read-only suite-wide open-questions index; registered two new suite-level docs in §2's repo layout and §3's suite-level-docs list — [embarch-glossary.md](embarch-glossary.md) (load-bearing terms, one place) and [embarch-decision-reversals.md](embarch-decision-reversals.md) (assumptions reality has overturned, one page).
- 2026-08-11 — Automated the three manual chores §4/§5 had been describing as human steps: (1) `scripts/check-links.py` and the new `scripts/check-staleness.py` (a mechanical cross-check of `embarch.md` §3 and `embarch-features.md` against each sub-project's `design.md`) now both run on every push/PR via `.github/workflows/docs-ci.yml`, rather than "run this before committing" — `check-staleness.py`'s first-ever run found and fixed a real instance of the exact drift §4 warns about, in `embarch-study-designer/design.md`'s Status line. (2) New `scripts/archive-changelog.py` moves each doc's Changelog entries beyond the most recent few into a sibling `*.changelog-archive.md`, run weekly by `.github/workflows/changelog-archive.yml` (opens a PR rather than pushing straight to main). §4 and §5 updated to point at all three.
- 2026-08-11 — Added `scripts/check-links.py` (§5) and a pre-close staleness-check rule (§4): before marking a milestone step done, grep suite-level docs for now-superseded status mentions instead of waiting for the disagreement to surface later. Prompted by finding `embarch-features.md`'s `doctor` and suite-release-archive rows still marked `Proposed, design-only` after both had shipped (fixed there the same pass).
- 2026-07-20 — Initial draft, written alongside the embarch-doc per-sub-project restructure.
- 2026-07-21 — Added `embarch-token.md` to the suite-level docs list (§3) and the repo layout tree (§2).
- 2026-08-05 — Added `embarch-umbrella` to §2's repo layout tree (design-only, no repo yet). Also qualified §3's suite-level-docs entry for [embarch-user-guide.md](embarch-user-guide.md): it's the one doc here written for an outside reader, so the "don't restate detail across docs, link instead" rule in §5 doesn't apply to it the way it does everywhere else — a getting-started guide that only links is useless. §3's roadmap description was also corrected from "Now/Next/Later" to match what that file actually contains (numbered milestones plus Next/Later).
- 2026-07-28 — Added `embarch-study-designer` to §2's repo layout tree, now that its repo exists ([gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), empty).
