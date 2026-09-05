# embarch-doc: documentation protocol

**Status:** active, 2026-07-20.

## 1. Purpose

How docs in this repo are organised and kept in sync while work happens in any EmbArch sub-project repo, so the behaviour doesn't need re-explaining in chat. A sub-project's `CLAUDE.md` points here once (§6); this file carries the rest. **Sizes and the file split:** [DOC-COMPACTION.md](DOC-COMPACTION.md); how a doc is made *smaller*: [DOC-COMPACTION-PASS.md](DOC-COMPACTION-PASS.md). **The shapes scripts parse** — the `**Status:**` line, decision entries and how to cite one, retiring one, measured vs. assumed: [DOC-CONVENTIONS.md](DOC-CONVENTIONS.md).

## 2. Repo layout

`embarch/` is the parent; every sub-project is a sibling directory alongside `embarch-doc` itself, so a sub-project's docs are always reachable from its own repo as `../embarch-doc/<sub-project>/`. No submodule, symlink, or absolute path — which holds only as long as that sibling relationship does. A repo cloned somewhere that breaks it invalidates this section first.

```
embarch/
├── embarch-core/           embarch-topology/     (implemented)
├── embarch-api/            embarch-ui/           (implemented)
├── embarch-study-designer/ embarch-outpost/      (implemented)
├── embarch-dev-bench/      embarch-promptu/      (planned, no repo)
├── embarch-umbrella/       embarch-atlas/        (paused, no repo)
├── embarch-fleet/          the agent fleet's own repo: its rules, scripts and
│                           agent definitions. A leg never checks it out
└── embarch-doc/
    ├── DOC-PROTOCOL.md      this file
    ├── DOC-COMPACTION.md    sizes, file split, how a doc shrinks
    ├── <sub-project>/       spec.md, decisions.md, open.md, [interfaces.md]
    ├── suite/               overview, index, roadmap, features, glossary, user-guide
    ├── embarch-decision-reversals.md
    ├── changelog.d/         one-line history fragments
    ├── features.d/          one fragment per feature-inventory row
    ├── status.d/            pending edits to a shared suite-level doc
    ├── tasks/               the background agents' work queue
    ├── history/             assembled per sub-project, + archive/
    └── scripts/             the CI checks, plus the fleet's own tools
```

Suite-level docs are mid-migration into `suite/`; several still sit at the root. **`embarch-fleet/` is the one sub-project directory that is a single file**, and deliberately: its `decisions.md`, `open.md` and reference all exist in the framework repo itself, and a second copy here would be a second source of truth about the rules an agent is running under. Creating the directory at all also created a `fleet` *worker scope*, which `check-ownership.py` refuses outright and `fleet.toml` reserves — a doc-layout convention had quietly opened a door back into the fleet's own rules. [embarch.md](embarch.md) §6 is the authoritative index either way.

## 3. Where a doc lives

Three tiers, and one non-tier:

- **A sub-project** (`<sub-project>/`) is **four capped files** — `spec.md`, `decisions.md`, `open.md`, and `interfaces.md` only where the reference doesn't fit; each splits into `<topic>/` files by mission when it outgrows one. What each holds, and the caps: [DOC-COMPACTION.md](DOC-COMPACTION.md) §2–3. Every sub-project, existing or planned, gets a directory.
- **Suite-level** docs cover what spans more than one sub-project: the overview and index, the roadmap, the feature inventory, the glossary, [embarch-token.md](embarch-token.md), [embarch-dev-workflow.md](embarch-dev-workflow.md), [embarch-decision-reversals.md](embarch-decision-reversals.md), and [suite/user-guide.md](suite/user-guide.md) — the one doc written for a reader not already inside the project, and therefore the one place §5's link-don't-restate rule does not apply.
- **A proposal** (`*-proposal.md`, 15 KB) is a cross-repo design awaiting acceptance. **The policy: if it is not fully closed, it is still open** — its `Status:` stays `proposal`, never `accepted` or `half-accepted`, because **a doc marked half-done reads as done to everyone who didn't write it.** Delete it only when fully absorbed. **An accepted piece is deleted from it, not restated**, or the proposal becomes a second source of truth — as in [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md), inbound half folded into five docs, outbound half still proposed.
- **A milestone doc is not a tier.** While a milestone runs, `<sub-project>/milestone-N.md` holds the execution plan. Once it ships, it **folds into the four files and is deleted** ([DOC-COMPACTION.md](DOC-COMPACTION.md) §3) — git holds it, and a completed plan left intact competes with `spec.md` for the reader who wants current truth.

## 4. When to update a doc

Proactively, without being asked, whenever work produces: a design decision (a new invariant, a rejected alternative, a changed data flow); a shipped feature or changed interface; a status change; a new open question or known limitation. Formatting, dependency bumps, typo fixes, and refactors with no externally-visible effect need nothing.

Those triggers are reactive — they fire when work happens, and don't catch a doc that goes quiet while its siblings move. So **before marking any milestone step or roadmap milestone done**, two checks:

- **Status.** Grep the suite-level docs for anything the step you're closing just made false: a stale `Proposed`/`design-only`/`Todo`, command name, or example. `scripts/check-staleness.py` checks two tables ([embarch.md](embarch.md) §3, [suite/features.md](suite/features.md)) in CI; **the roadmap's prose isn't structured enough, so that one wants a human pass.** Failure signature: a Status line still reading "design-only, no code yet" after four implementation passes.
- **Open questions.** Neither check above looks at an open-questions bullet. One pass found two stale against shipped work, and **both lived in a different sub-project's doc from the one that shipped it**, which is why closing those milestones never surfaced them. `scripts/collect-open-questions.py` prints the whole suite's set in one pass. This stays a human step: **a resolved open question has no mechanical signature the way a superseded status word does.**

## 5. How to update

- **Edit the body**, so the doc stays a description of current reality. Never append.
- **No changelog.** History does not live in a doc: drop a one-line fragment in `changelog.d/` (`<scope>-<slug>.<category>.md`, 200 B hard limit) and `scripts/build_changelog.py` assembles it into `history/<scope>.md`. Why, and the **642 KB** of in-doc `## Changelog` sections it replaced: [changelog.d/README.md](changelog.d/README.md).
- **Update suite-level facts in the same pass** — *unless you are a background worker, which drops a `status.d/` fragment instead ([the protocol](../embarch-fleet/protocol.md) §9)* — [embarch.md](embarch.md) §3's status table, a [roadmap](suite/roadmap.md) bucket. A **[features](suite/features.md) row is different**: it is assembled from `features.d/<scope>-*`, which a worker owns, so the row lands with the work rather than as a request. A sub-project doc and the suite-level docs must never disagree about status.
- **Link, don't restate.** [suite/features.md](suite/features.md) and [suite/roadmap.md](suite/roadmap.md) point at a decision rather than duplicating it. Exception: [suite/user-guide.md](suite/user-guide.md), where a getting-started guide that only links is useless.
- **Adding a top-level file?** Add it to [embarch.md](embarch.md) §6 in the same edit — an index is useful only while exhaustive.
- **Run the checks.** `scripts/check-docs.py` runs the whole gate in one command; it and CI run the same set ([DOC-COMPACTION.md](DOC-COMPACTION.md) §7). `collect-open-questions.py` and `queue-status.py` are read-only indexes, not gates.

## 6. How a sub-project repo hooks into this

Each sub-project's own `CLAUDE.md` carries a short pointer plus the suite's git rule:

```markdown
## Docs
**Four files, not one.** Current truth: ../embarch-doc/<sub-project>/spec.md. Why it is
that way: decisions.md — an index over decisions/, and a decision number addresses this
sub-project, not a file. Unresolved: open.md. [Reference: interfaces.md, where there is one.]
Update them proactively per ../embarch-doc/DOC-PROTOCOL.md whenever a notable design
decision, feature, or status change happens here — §4 says when, §5 says how, and
history goes in a changelog.d/ fragment rather than into a doc.

## Git
Work directly on `main` — no feature branches, no PRs (2026-08-25). Overrides the
general "branch before committing to the default branch" default, for this suite only;
ends when the repo owner explicitly says so. See ../embarch-doc/embarch-dev-workflow.md §6.
```

This is what makes §4–5 happen without re-explaining it: `CLAUDE.md` loads every session and points here. **A new repo needs both sections, and it is worth checking an existing one has them** — one sub-project ran for five days with no `CLAUDE.md` at all, so nothing there pointed at its own design doc, and nothing here had ever checked.

**And having them is not enough: on 2026-09-05 all eight pointed at `design.md`, a file the four-file split deleted a week earlier**, two of them at a milestone doc deleted with it. So every agent session in every sub-project repo opened on a dead pointer to its own design doc, and the §6 hook that exists to make §4–5 automatic had been silently disconnected the whole time. **`check-links.py` cannot see this** — it runs inside this repo and a sub-project's `CLAUDE.md` lives in that sub-project's repo, which is exactly why it went a week unnoticed. Nothing mechanical guards it, so **changing the shape of a sub-project's docs means sweeping the eight `CLAUDE.md` files in the same pass.**
