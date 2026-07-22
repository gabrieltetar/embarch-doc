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
├── embarch-dev-bench/      (planned, no repo yet)
├── embarch-promptu/        (planned, no repo yet)
├── embarch-atlas/          (paused, no repo yet)
└── embarch-doc/
    ├── CLAUDE.md
    ├── embarch.md
    ├── embarch-roadmap.md
    ├── embarch-features.md
    ├── embarch-user-guide.md
    ├── embarch-token.md
    ├── DOC-PROTOCOL.md          <- this file
    ├── embarch-core/design.md
    ├── embarch-core/milestone-1.md
    ├── embarch-api/design.md
    ├── embarch-api/milestone-1.md
    ├── embarch-dev-bench/design.md
    ├── embarch-promptu/design.md
    └── embarch-atlas/design.md
```

Because every sub-project sits as a sibling of `embarch-doc`, its docs are always reachable by relative path from inside that sub-project's own repo: `../embarch-doc/<sub-project>/design.md`. No submodule, symlink, or absolute path is needed — that only holds as long as the layout above is preserved. If a sub-project ever gets cloned or moved somewhere that breaks the sibling relationship, this section needs revisiting first.

## 3. Where a doc lives

Two tiers:

- **Suite-level docs** (`embarch-doc/` root): [embarch.md](embarch.md) (suite overview + sub-project index), [embarch-roadmap.md](embarch-roadmap.md) (Now/Next/Later across the whole suite), [embarch-features.md](embarch-features.md) (feature inventory across the whole suite), [embarch-user-guide.md](embarch-user-guide.md) (day-to-day usage of the assembled suite), [embarch-token.md](embarch-token.md) (`EMBARCH_TOKEN`'s full lifecycle, since it's shared across `embarch-core` and `embarch-api`). These cover things that span more than one sub-project.
- **Sub-project docs** (`embarch-doc/<sub-project>/`): every existing or planned sub-project gets a subfolder. `design.md` is the one required file — the durable, living source of truth for that sub-project's architecture, decisions, and open questions, per [embarch.md](embarch.md) §5's "design doc as source of truth" principle. Add more files to a subfolder later (e.g. `api-reference.md`) if `design.md` grows unwieldy — don't split preemptively.
- **Milestone docs** (`embarch-doc/<sub-project>/milestone-N.md`): when a roadmap milestone (see [embarch-roadmap.md](embarch-roadmap.md)) touches a sub-project, that sub-project's half of the execution plan — concrete, ordered steps, a definition of done, open questions carried into execution — lives in its own `milestone-N.md`, separate from `design.md`. This keeps `design.md` as the architecture-of-record (what's true now) distinct from a milestone doc's job (what to do next, and why); once a milestone's steps actually ship, fold whatever they resolved back into `design.md` per §5 below rather than leaving the decision only recorded in the milestone doc.

## 4. When to update a doc

Proactively, without being asked, whenever work in a sub-project repo produces one of:

- An architecture or design decision (a new invariant, a rejected alternative, a changed data flow)
- A shipped feature, a changed API/tool surface, or a resolved open question
- A status change (Planned → Shipped, Paused → Active, etc.)
- A new open question or known limitation surfacing

Trivial/mechanical changes — formatting, dependency bumps, typo fixes, refactors with no externally-visible or architectural effect — don't need a doc update.

## 5. How to update

- Edit the relevant numbered section of `<sub-project>/design.md` directly, so the doc stays a living description of current reality — not an append-only log. The trailing `## Changelog` section is for a one-line dated pointer to *what* changed and *why*, not a substitute for updating the body.
- Add that dated bullet to `## Changelog` for every substantive edit.
- If the change also affects suite-level facts — the status table in [embarch.md](embarch.md) §3, a Now/Next/Later bucket in [embarch-roadmap.md](embarch-roadmap.md), a row in [embarch-features.md](embarch-features.md) — update those in the same pass. A sub-project doc and the suite-level docs should never disagree about status.
- Don't restate detail across docs — [embarch-features.md](embarch-features.md) and [embarch-roadmap.md](embarch-roadmap.md) link to the specific section of a design doc rather than duplicating its content (see `embarch-features.md`'s own header note).
- Adding a new top-level file to `embarch-doc`? Add it to [embarch.md](embarch.md) §6 (Index) in the same edit — the index is only useful if it stays exhaustive.

## 6. How a sub-project repo hooks into this

Each sub-project repo's own `CLAUDE.md` carries a short "Docs" pointer, e.g.:

```markdown
## Docs
Design doc: ../embarch-doc/embarch-core/design.md — source of truth for this project's architecture/design.
Update it proactively per ../embarch-doc/DOC-PROTOCOL.md whenever a notable design decision, feature, or status change happens here.
```

This is the mechanism that makes §4–5 happen without re-explaining it in chat — `CLAUDE.md` loads automatically every session and points here.

## Changelog

- 2026-07-20 — Initial draft, written alongside the embarch-doc per-sub-project restructure.
- 2026-07-21 — Added `embarch-token.md` to the suite-level docs list (§3) and the repo layout tree (§2).
