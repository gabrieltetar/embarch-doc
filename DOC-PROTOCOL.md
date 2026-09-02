# embarch-doc: documentation protocol

**Status:** active, 2026-07-20.

## 1. Purpose

How docs in this repo are organised and kept in sync while work happens in any EmbArch sub-project repo, so the behaviour doesn't need re-explaining in chat. A sub-project's `CLAUDE.md` points here once (§6); this file carries the rest. Sizes, file split, and how a doc gets *smaller* are [DOC-COMPACTION.md](DOC-COMPACTION.md).

## 2. Repo layout

`embarch/` is the parent; every sub-project is a sibling directory alongside `embarch-doc` itself, so a sub-project's docs are always reachable from its own repo as `../embarch-doc/<sub-project>/`. No submodule, symlink, or absolute path — which holds only as long as that sibling relationship does. If a repo is ever cloned somewhere that breaks it, this section needs revisiting first.

```
embarch/
├── embarch-core/           embarch-topology/     (implemented)
├── embarch-api/            embarch-ui/           (implemented)
├── embarch-study-designer/ embarch-outpost/      (implemented)
├── embarch-dev-bench/      embarch-promptu/      (planned, no repo)
├── embarch-umbrella/       embarch-atlas/        (paused, no repo)
└── embarch-doc/
    ├── DOC-PROTOCOL.md      this file
    ├── DOC-COMPACTION.md    sizes, file split, how a doc shrinks
    ├── <sub-project>/       spec.md, decisions.md, open.md, [interfaces.md]
    ├── suite/               overview, index, roadmap, features, glossary, user-guide
    ├── embarch-decision-reversals.md
    ├── changelog.d/         one-line history fragments
    ├── status.d/            pending edits to a shared suite-level doc
    ├── tasks/               the background agents' work queue
    ├── history/             assembled per sub-project, + archive/
    └── scripts/             the six CI checks
```

Suite-level docs are mid-migration into `suite/`; several still sit at the root. [embarch.md](embarch.md) §6 is the authoritative index either way.

## 3. Where a doc lives

Three tiers, and one non-tier:

- **A sub-project** (`<sub-project>/`) is **four capped files**: `spec.md` (what is true now), `decisions.md` (why — split by mission into `decisions/<topic>.md` where it outgrows one file, leaving an index), `open.md`, and `interfaces.md` only where the reference doesn't fit. Caps and contents: [DOC-COMPACTION.md](DOC-COMPACTION.md) §2–3. Every sub-project, existing or planned, gets a directory.
- **Suite-level** docs cover what spans more than one sub-project: the overview and index, the roadmap, the feature inventory, the glossary, [embarch-token.md](embarch-token.md), [embarch-dev-workflow.md](embarch-dev-workflow.md), [embarch-decision-reversals.md](embarch-decision-reversals.md), and [suite/user-guide.md](suite/user-guide.md) — the one doc written for a reader who isn't already inside the project, and therefore the one place §5's link-don't-restate rule does not apply.
- **A proposal** (`*-proposal.md`, 15 KB) is a cross-repo design awaiting acceptance. **The policy: if it is not fully closed, it is still open** — its `Status:` stays `proposal`, never `accepted` or `half-accepted`, because **a doc marked half-done reads as done to everyone who didn't write it.** Delete it only when fully absorbed. **An accepted piece is deleted from it, not restated**, or the proposal becomes a second source of truth: [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md) is the case that forced this tier, its inbound half folded into five docs and its outbound half still proposed.
- **A milestone doc is not a tier.** While a milestone runs, `<sub-project>/milestone-N.md` holds the execution plan. Once it ships, it **folds into the four files and is deleted** ([DOC-COMPACTION.md](DOC-COMPACTION.md) §3) — git holds it, and a completed plan left intact competes with `spec.md` for the reader who wants current truth.

## 4. When to update a doc

Proactively, without being asked, whenever work produces: a design decision (a new invariant, a rejected alternative, a changed data flow); a shipped feature or changed interface; a status change; or a new open question or known limitation. Formatting, dependency bumps, typo fixes, and refactors with no externally-visible effect need nothing.

Those triggers are reactive — they fire when work happens, and don't catch a doc that goes quiet while its siblings move. So **before marking any milestone step or roadmap milestone done**, two checks:

- **Status.** Grep the suite-level docs for anything the step you're closing just made false: a stale `Proposed`/`design-only`/`Todo`, command name, or example. `scripts/check-staleness.py` checks two tables ([embarch.md](embarch.md) §3, [suite/features.md](suite/features.md)) in CI; **the roadmap's prose isn't structured enough, so that one wants a human pass.** Its first run found a Status line still reading "design-only, no code yet" after four implementation passes.
- **Open questions.** Neither check above looks at an open-questions bullet, and one pass found two stale against shipped work. **Both lived in a different sub-project's doc from the one that shipped the work**, which is exactly why closing those milestones never surfaced them. `scripts/collect-open-questions.py` prints the whole suite's set in one pass. This stays a human step: **a resolved open question has no mechanical signature the way a superseded status word does.**

## 5. How to update

- **Edit the body**, so the doc stays a description of current reality. Never append.
- **No changelog.** History does not live in a doc: drop a one-line fragment in `changelog.d/` (`<scope>-<slug>.<category>.md`, 200 B hard limit) and `scripts/build_changelog.py` assembles it into `history/<scope>.md`. Why, and the **642 KB** of in-doc `## Changelog` sections it replaced: [changelog.d/README.md](changelog.d/README.md).
- **Update suite-level facts in the same pass** — *unless you are a background worker, which drops a `status.d/` fragment instead ([embarch-parallel-agents.md](embarch-parallel-agents.md) §9)* — [embarch.md](embarch.md) §3's status table, a [roadmap](suite/roadmap.md) bucket, a [features](suite/features.md) row. A sub-project doc and the suite-level docs must never disagree about status.
- **Link, don't restate.** [suite/features.md](suite/features.md) and [suite/roadmap.md](suite/roadmap.md) point at a decision rather than duplicating it. Exception: [suite/user-guide.md](suite/user-guide.md), where a getting-started guide that only links is useless.
- **Adding a top-level file?** Add it to [embarch.md](embarch.md) §6 in the same edit — an index is useful only while exhaustive.
- **Run the checks.** All six run in CI on every push: `check-links.py`, `check-staleness.py`, `check-decision-refs.py`, `check-doc-conventions.py`, `check-doc-size.py`, and `build_changelog.py --check`. Run them locally for fast feedback. `collect-open-questions.py` is a read-only index, not a gate.

## 6. How a sub-project repo hooks into this

Each sub-project's own `CLAUDE.md` carries a short pointer plus the suite's git rule:

```markdown
## Docs
Spec: ../embarch-doc/embarch-core/spec.md — what is true now. Decisions: decisions.md.
Update proactively per ../embarch-doc/DOC-PROTOCOL.md whenever a notable design
decision, feature, or status change happens here.

## Git
Work directly on `main` — no feature branches, no PRs (2026-08-25). Overrides the
general "branch before committing to the default branch" default, for this suite only;
ends when the repo owner explicitly says so. See ../embarch-doc/embarch-dev-workflow.md §6.
```

This is what makes §4–5 happen without re-explaining it: `CLAUDE.md` loads every session and points here. **A new repo needs both sections, and it is worth checking an existing one has them** — `embarch-topology` ran 2026-08-21 to 08-25 with no `CLAUDE.md` at all, so nothing there pointed at its own design doc, and nothing here had ever checked.

## 7. Doc conventions

The shapes scripts parse and cross-references depend on.

### 7.1 `**Status:**` line

First line after the title: `**Status:** <state>, <yyyy-mm-dd>` followed by any prose. Only the token and the date are machine-readable, and `scripts/check-doc-conventions.py` deliberately does not look past them.

`<state>` is one of `draft` · `active` · `done` · `planned` · `paused` · `proposal` · `retired` · `superseded-by:<path>`. The date is when the doc last *changed state*. `half-accepted` is deliberately absent (§3).

This exists because `check-staleness.py` is a heuristic over two tables — guessing at status no doc stated readably. No doc is `draft` any more. **A `done` asserted over an unmarked Definition of Done is the status claim §4 exists to prevent** — the last milestone doc deliberately stayed `active` for exactly that reason, until its residue moved into [embarch-umbrella/open.md](embarch-umbrella/open.md) and the doc was deleted.

### 7.2 Decision entries

Number-first headings, one level below their topical group: `### 20, 21, 25, 27 — Streaming capture, batched, with units`. A group is a section of `decisions.md` or a whole `decisions/<topic>.md`; the checker reads both. **Numbers are permanent** — unique per sub-project, never renumbered or reused, and an entry may own several where decisions were merged. Groups can be renamed, reordered, split, and moved between files freely; numbers cannot, so out-of-order numbers in a group are intended. Entry shape and length: [DOC-COMPACTION.md](DOC-COMPACTION.md) §5.

### 7.3 Referring to a decision

**A decision number addresses a sub-project, not a file and not a section.** Within that sub-project's own docs: `decision 39`. Across: `embarch-study-designer decision 39`, or a link plus `decision 39`. Legacy `§3 decision 39` still parses, unmaintained — which is what let §3's decisions move to their own file untouched.

`check-links.py` structurally cannot see one of these — it validates paths and skips anchors, and "decision 39" is not a link. `scripts/check-decision-refs.py` resolves every one, and has found two real classes of breakage:

- **A number an insertion renumbered.** Two entries looked deleted while other docs cited them (`embarch-api` 31, `embarch-umbrella` 27). Neither was: **a commit inserted a decision in the middle and renumbered the entry below it**, so every reference to the old number silently pointed elsewhere. **This is why a number is permanent here** (DOC-COMPACTION.md §5); both entries own both numbers.
- **A reversal row cited and gone.** It resolves `reversals ... row N` against the union of `reversals/rows-*.md`, because 47 rows were deleted along with a `## Changelog` heading they sat below and **fifteen citations went on pointing at them with nothing to notice.**

### 7.4 Retiring an entry

A decision that stops describing anything true is **retired, not deleted** — a one-line tombstone naming what it said and what replaced it:

```markdown
### 19 — Two-tier validation (retired 2026-08-25, see decision 48)
Post-hoc content validation alongside the real-time per-step `Outcome`. Removed
outright; the real-time half stands and is decision 48's subject.
```

A dangling reference then lands on an explanation instead of a gap, which is what keeps §7.3's never-reused promise cheap.

### 7.5 Measured vs. assumed constants

Every load-bearing constant says which it is, inline: `460800 baud [measured 2026-08-30, DK VCOM1 over the bridge]`, `250 ms step timeout [assumed]`.

The bracket earns its place on an **inventoried** constant — one in a table or declared list, where provenance would otherwise be vague. It does **not** earn its place where prose already derives a constant precisely ("244, one full 247-byte ATT MTU minus the 3-byte ATT header"): a bracket there is noise. Sweeping it found only **five** sites repo-wide, not the dozens the rule's wording implied. So: mark an inventory, leave good prose alone, and mark the rest as each doc reaches a compaction pass — where its constants get inventoried anyway.
