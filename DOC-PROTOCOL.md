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
├── embarch-topology/       (implemented and pushed 2026-08-21: gabrieltetar/embarch-topology)
├── embarch-ui/             (in progress, added 2026-08-24: gabrieltetar/embarch-ui, empty)
├── embarch-outpost/        (implemented 2026-08-26: gabrieltetar/embarch-outpost)
└── embarch-doc/
    ├── CLAUDE.md
    ├── embarch.md
    ├── embarch-roadmap.md
    ├── embarch-features.md
    ├── embarch-user-guide.md
    ├── embarch-token.md
    ├── embarch-glossary.md      <- suite-wide term index, added 2026-08-15
    ├── embarch-decision-reversals.md  <- assumptions reality has overturned, added 2026-08-15
    ├── embarch-dev-workflow.md  <- local dev iteration across the 3 code repos, added 2026-08-17; §4a (deploying Core to the live Windows service) added 2026-08-25
    ├── embarch-stream-pipeline-proposal.md  <- proposal (not accepted): one generic stream pipeline, added 2026-08-24
    ├── DOC-PROTOCOL.md          <- this file
    ├── DOC-COMPACTION.md        <- how a doc gets compacted once its work has landed, added 2026-08-31
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
    ├── embarch-atlas/design.md
    ├── embarch-topology/design.md
    ├── embarch-topology/milestone-1.md
    ├── embarch-ui/design.md
    ├── embarch-outpost/design.md
    └── embarch-outpost/milestone-1.md
```

Because every sub-project sits as a sibling of `embarch-doc`, its docs are always reachable by relative path from inside that sub-project's own repo: `../embarch-doc/<sub-project>/design.md`. No submodule, symlink, or absolute path is needed — that only holds as long as the layout above is preserved. If a sub-project ever gets cloned or moved somewhere that breaks the sibling relationship, this section needs revisiting first.

## 3. Where a doc lives

Two tiers:

- **Suite-level docs** (`embarch-doc/` root): [embarch.md](embarch.md) (suite overview + sub-project index), [embarch-roadmap.md](embarch-roadmap.md) (numbered milestones plus Next/Later across the whole suite), [embarch-features.md](embarch-features.md) (feature inventory across the whole suite), [embarch-user-guide.md](embarch-user-guide.md) (getting started and day-to-day usage of the assembled suite — the one doc in this repo written for a reader who isn't already inside the project, so it explains rather than links), [embarch-token.md](embarch-token.md) (`EMBARCH_TOKEN`'s full lifecycle, since it's shared across `embarch-core` and `embarch-api`), [embarch-glossary.md](embarch-glossary.md) (added 2026-08-15 — load-bearing terms used across more than one sub-project doc, each linking to its owning doc rather than restating it), [embarch-decision-reversals.md](embarch-decision-reversals.md) (added 2026-08-15 — a standing list of assumptions reality has already overturned, across every sub-project; update it in the same pass as any decision correction, per §5 below), [embarch-dev-workflow.md](embarch-dev-workflow.md) (added 2026-08-17 — how to iterate locally across `embarch-core`/`embarch-api`/`embarch-umbrella` without cutting a release or a debug build touching a real machine's install; §4a, added 2026-08-25, covers the opposite trip — getting a Core change onto the live Windows service). These cover things that span more than one sub-project.
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

§4's checks — the manual pre-close grep and `check-staleness.py` — both watch **status tables**. Neither looks at an "Open questions" bullet, and a suite-wide design pass on 2026-08-25 found two that had gone stale in exactly the way §4 exists to prevent: `embarch-api/design.md` still described `enroll_probe` as design-only and blocked on a dependency, months after it shipped in both the CLI and the MCP surface and enrolled both of this bench's real boards; and `embarch-umbrella/design.md` still asked whether the EmbArch UI should be a native app, a web page, or a tray item, a day after `embarch-ui` shipped as a web page with all five tabs live-validated. Both are recorded as [embarch-decision-reversals.md](embarch-decision-reversals.md) row 32.

So: **when a milestone step closes, also grep the open-questions sections** — not just the status tables — for bullets the step just answered, in every doc, not only the one you were working in. Both stale bullets above live in a *different* sub-project's doc from the one that shipped the work, which is precisely why nobody hit them while closing the milestone. `scripts/collect-open-questions.py` (§5) prints the whole suite's set in one pass and is the cheap way to do this; it was written as a read-only index and turns out to be the right pre-close instrument too. This stays a human step for now — a resolved open question has no mechanical signature the way a status word does, which is why it is stated here as a rule rather than added to `check-staleness.py`.

## 5. How to update

- Edit the relevant numbered section of `<sub-project>/design.md` directly, so the doc stays a living description of current reality — not an append-only log. The trailing `## Changelog` section is for a one-line dated pointer to *what* changed and *why*, not a substitute for updating the body.
- Add that dated bullet to `## Changelog` for every substantive edit.
- If the change also affects suite-level facts — the status table in [embarch.md](embarch.md) §3, a Now/Next/Later bucket in [embarch-roadmap.md](embarch-roadmap.md), a row in [embarch-features.md](embarch-features.md) — update those in the same pass. A sub-project doc and the suite-level docs should never disagree about status.
- Don't restate detail across docs — [embarch-features.md](embarch-features.md) and [embarch-roadmap.md](embarch-roadmap.md) link to the specific section of a design doc rather than duplicating its content (see `embarch-features.md`'s own header note).
- Adding a new top-level file to `embarch-doc`? Add it to [embarch.md](embarch.md) §6 (Index) in the same edit — the index is only useful if it stays exhaustive.
- Renaming or moving a file, or editing anything link-heavy? `scripts/check-links.py` walks every `.md` file and reports any relative link that no longer resolves — it also runs automatically on every push/PR via `.github/workflows/docs-ci.yml`, so a broken link fails CI rather than waiting to be noticed; run it locally first if you want the fast feedback.
- Same workflow also runs `scripts/check-staleness.py`, the automated half of §4's pre-close grep — see §4 for what it does and doesn't cover.
- Changelog sections don't need manual trimming: `scripts/archive-changelog.py` keeps each doc's `## Changelog` down to its most recent entries and moves the rest into a sibling `*.changelog-archive.md`, ranked by each entry's own date rather than its position (some docs here prepend newest-first, others append oldest-first — see the script's own docstring). `.github/workflows/changelog-archive.yml` runs it weekly and opens a PR with whatever moved, rather than requiring anyone to remember to run it or pushing straight to main unreviewed.
- Everything above describes how a doc gets *written* while work happens, and its bias is deliberately append-only: during design and implementation, carrying a redundant fact costs less than losing one. [DOC-COMPACTION.md](DOC-COMPACTION.md) (added 2026-08-31) covers the opposite pass — how a doc gets compacted once its work has shipped, so the accretion turns into organized sections without losing a fact. It is a phase, not a habit: it runs at a milestone close, on one doc, in its own commit, and it is lossless about facts and lossy only about chronology.
- Want the suite-wide view of every open question instead of reading six-plus docs' own §7/§10/§12-equivalent sections one at a time? `scripts/collect-open-questions.py` (added 2026-08-15) walks every `design.md` (plus `embarch-token.md`) for its "Open questions" heading and prints every bullet, grouped by doc. Read-only and not a CI gate — an open question existing isn't a failure the way a broken link or a stale status word is; run it locally when you want the index.

## 6. How a sub-project repo hooks into this

Each sub-project repo's own `CLAUDE.md` carries a short "Docs" pointer plus the suite's git rule, e.g.:

```markdown
## Docs
Design doc: ../embarch-doc/embarch-core/design.md — source of truth for this project's architecture/design.
Update it proactively per ../embarch-doc/DOC-PROTOCOL.md whenever a notable design decision, feature, or status change happens here.

## Git
Work directly on `main` — no feature branches, no PRs (2026-08-25). Overrides the general "branch before committing to the default branch" default, for this suite only; ends when the repo owner explicitly says so. See ../embarch-doc/embarch-dev-workflow.md §6.
```

This is the mechanism that makes §4–5 happen without re-explaining it in chat — `CLAUDE.md` loads automatically every session and points here. **A new sub-project repo needs both sections**, and it is worth checking an existing one actually has them: `embarch-topology` ran without a `CLAUDE.md` at all from its creation (2026-08-21) until 2026-08-25, so nothing in that repo pointed at its own design doc and §4–5 depended on whoever was working there already knowing. Nothing in this protocol had ever checked.

## Changelog

- 2026-08-31 — Added [DOC-COMPACTION.md](DOC-COMPACTION.md) (§2's tree, §5's list): the pass this protocol never described. §4–5's append-only bias is right while work is happening and had produced a 343 KB `embarch-study-designer/design.md` whose §3 needed its own index to stay navigable, plus decisions readable only as their own amendment history. Compaction was therefore a judgment call re-made from scratch every time, with nothing protecting the content most at risk from it — rejected alternatives, the measured/assumed distinction, and the 1335 prose `§N decision M` cross-references `check-links.py` structurally cannot see (it validates file paths and skips in-page anchors). The new file's hard rule on that last point: decision and section numbers are permanent identifiers, grouped under topical headings rather than renumbered.

- 2026-08-26 — §2's tree: `embarch-outpost` moves from *design-only, created empty* to *implemented* (Milestone 7 Phase C). §6's "a new sub-project repo needs both sections, and it is worth checking an existing one actually has them" was followed rather than assumed this time — the repo's first commit carries a `CLAUDE.md` with the docs pointer and the git rule, which is the gap `embarch-topology` ran four days with and which nothing in this protocol had ever checked before it was written down.

- 2026-08-25 — **§4 gained an open-questions half.** Its pre-close grep and `check-staleness.py` both only ever watched status tables; a suite-wide design pass found two open-questions bullets that had gone stale against shipped work, each in a different sub-project's doc from the one that shipped it — which is why closing those milestones never surfaced them. `scripts/collect-open-questions.py`, written as a read-only index, is named as the pre-close instrument. Kept a human step deliberately: a resolved open question has no mechanical signature the way a superseded status word does.

- 2026-08-25 — **§6 gained the suite's git rule alongside the docs pointer** — work directly on `main`, no feature branches, until the repo owner ends it ([embarch-dev-workflow.md](embarch-dev-workflow.md) §6). Put here because §6 is already the mechanism that gets a standing rule into every repo's session context without re-explaining it in chat, and a branching policy has exactly that shape. Adding it surfaced a gap this protocol had never checked for: **`embarch-topology` had no `CLAUDE.md` at all** — created 2026-08-21, four days without anything pointing at its own design doc — so §6 now says to verify an existing repo has both sections rather than assuming.

- 2026-08-25 — §2's tree gained `embarch-outpost/milestone-1.md`, which existed but had never been listed. Registered while closing its Phase A; §5's "add a new top-level file to the index in the same edit" rule covers `embarch.md` §6 (where it *was* listed) but says nothing about this tree, which is why one of the two drifted and the other didn't.

- 2026-08-25 — Added `embarch-outpost` to §2's repo layout tree (design-only, [repo](https://github.com/gabrieltetar/embarch-outpost) created empty): a Zephyr module compiled into a DUT's own debug firmware, emitting an MCU-load timeline out a TX-only UART. Note for §3's tier question raised by the 2026-08-24 entry below: [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md) is now **half-accepted** — its inbound direction folded into five `design.md`s, its outbound direction still proposed — so the file stays at the root with a status line saying which half is which, rather than being deleted as its own §10 planned. A proposal that gets partially accepted is a second shape the missing fourth tier would need to handle.

- 2026-08-24 — Added `embarch-stream-pipeline-proposal.md` to §2's repo layout tree: a root-level **proposal**, not an accepted design — one generic stream pipeline (DUT log capture, power/waveform capture, and an authored shell-write step as instances of it), spanning `embarch-study-designer`/`embarch-dev-bench`/`embarch-core`/`embarch-api`. It sits at the root rather than in one sub-project's folder per §3's suite-level rule (it spans four), and per §5 it is registered in [embarch.md](embarch.md) §6 in the same pass. Note the tier it occupies isn't one §3 names: neither a living `design.md` nor a milestone execution plan, but a cross-repo design awaiting acceptance, with its own §10 saying exactly which decision number in which doc each piece folds into when it is. If proposals become a recurring shape rather than a one-off, §3 should grow a fourth tier for them rather than leaving each one to explain itself.

- 2026-08-24 — `embarch-ui` moved from design-only to in progress in §2's repo layout tree: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui) created (empty), execution plan drafted ([embarch-ui/milestone-1.md](embarch-ui/milestone-1.md)).
- 2026-08-24 — Added `embarch-ui` to §2's repo layout tree: design-only, no repo yet. One consolidated human-facing UI for the whole suite, replacing `embarch-topology`'s `ui` subcommand, `embarch-study-designer`'s `study-designer-ui` binary, and `embarch-core`'s `/enroll` page outright. See [embarch-ui/design.md](embarch-ui/design.md) and `embarch.md`'s own changelog entry for the full account.
- 2026-08-21 — `embarch-topology` implemented the same day it was scoped, then pushed to [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology) (the user created the repo after this session's own `gh repo create` was blocked as an outward-facing action; §2's tree updated, `milestone-1.md` added). `embarch-core`/`embarch-api`/`embarch-umbrella` all wired to depend on it, each still on its own local, unmerged branch — see `embarch-topology/design.md` §4/§6 for what shipped and `embarch-topology/milestone-1.md` for what's left.
- 2026-08-21 — Added `embarch-topology` to §2's repo layout tree — a new sub-project scoped this day (design-only, no repo yet): the suite's missing single abstraction for both software topology (where processes run relative to each other) and hardware topology (what's physically wired to what), prompted by a real incident (a stale `EMBARCH_DEV_BENCH_SERIAL` registry value surviving a runtime-link port migration undetected). See [embarch-topology/design.md](embarch-topology/design.md).
- 2026-08-17 — Added [embarch-dev-workflow.md](embarch-dev-workflow.md) as a new suite-level doc (§2, §3): how to iterate locally across the three code repos without a release archive, and — the reason it was written now — how to avoid a debug `embarch-umbrella` build silently overwriting a real machine's canonical install/PATH while testing decision 28.
- 2026-08-15 — Closed three items from that day's design-improvement review (`.claude/design-improvements-2026-08-15.md`, local working notes): added `scripts/collect-open-questions.py` (§5) as a read-only suite-wide open-questions index; registered two new suite-level docs in §2's repo layout and §3's suite-level-docs list — [embarch-glossary.md](embarch-glossary.md) (load-bearing terms, one place) and [embarch-decision-reversals.md](embarch-decision-reversals.md) (assumptions reality has overturned, one page).
- 2026-08-11 — Automated the three manual chores §4/§5 had been describing as human steps: (1) `scripts/check-links.py` and the new `scripts/check-staleness.py` (a mechanical cross-check of `embarch.md` §3 and `embarch-features.md` against each sub-project's `design.md`) now both run on every push/PR via `.github/workflows/docs-ci.yml`, rather than "run this before committing" — `check-staleness.py`'s first-ever run found and fixed a real instance of the exact drift §4 warns about, in `embarch-study-designer/design.md`'s Status line. (2) New `scripts/archive-changelog.py` moves each doc's Changelog entries beyond the most recent few into a sibling `*.changelog-archive.md`, run weekly by `.github/workflows/changelog-archive.yml` (opens a PR rather than pushing straight to main). §4 and §5 updated to point at all three.
- 2026-08-11 — Added `scripts/check-links.py` (§5) and a pre-close staleness-check rule (§4): before marking a milestone step done, grep suite-level docs for now-superseded status mentions instead of waiting for the disagreement to surface later. Prompted by finding `embarch-features.md`'s `doctor` and suite-release-archive rows still marked `Proposed, design-only` after both had shipped (fixed there the same pass).
- 2026-07-20 — Initial draft, written alongside the embarch-doc per-sub-project restructure.
- 2026-07-21 — Added `embarch-token.md` to the suite-level docs list (§3) and the repo layout tree (§2).
- 2026-08-05 — Added `embarch-umbrella` to §2's repo layout tree (design-only, no repo yet). Also qualified §3's suite-level-docs entry for [embarch-user-guide.md](embarch-user-guide.md): it's the one doc here written for an outside reader, so the "don't restate detail across docs, link instead" rule in §5 doesn't apply to it the way it does everywhere else — a getting-started guide that only links is useless. §3's roadmap description was also corrected from "Now/Next/Later" to match what that file actually contains (numbered milestones plus Next/Later).
- 2026-07-28 — Added `embarch-study-designer` to §2's repo layout tree, now that its repo exists ([gabrieltetar/embarch-study-designer](https://github.com/gabrieltetar/embarch-study-designer), empty).
