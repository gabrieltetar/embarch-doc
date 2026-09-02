# embarch-doc: documentation protocol

**Status:** active, 2026-07-20.

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
    ├── embarch-study-designer/decisions.md  <- §3 extracted + compacted, 2026-08-31
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
- **Sub-project docs** (`embarch-doc/<sub-project>/`): every existing or planned sub-project gets a subfolder. `design.md` is the one required file — the durable, living source of truth for that sub-project's architecture, decisions, and open questions, per [embarch.md](embarch.md) §5's "design doc as source of truth" principle. Add more files to a subfolder later (e.g. `api-reference.md`) if `design.md` grows unwieldy — don't split preemptively. One split is no longer a judgment call: **a decisions section past 40 entries or ~120 KB moves to its own `<sub-project>/decisions.md`**, leaving `design.md` §3 as a one-line pointer. As of 2026-08-31 that threshold is met by `embarch-study-designer` (62 entries, 183 KB), `embarch-api` (44), `embarch-dev-bench` (43), and `embarch-core` (40) — and nothing fired, because "unwieldy" had no number attached to it. The extraction is not its own churn event: it happens as part of that doc's compaction pass ([DOC-COMPACTION.md](DOC-COMPACTION.md)), so the cross-reference fixes land once. §7.3's reference form is what makes it safe — a decision number addresses a sub-project, not a file or a section.
- **Milestone docs** (`embarch-doc/<sub-project>/milestone-N.md`): when a roadmap milestone (see [embarch-roadmap.md](embarch-roadmap.md)) touches a sub-project, that sub-project's half of the execution plan — concrete, ordered steps, a definition of done, open questions carried into execution — lives in its own `milestone-N.md`, separate from `design.md`. This keeps `design.md` as the architecture-of-record (what's true now) distinct from a milestone doc's job (what to do next, and why); once a milestone's steps actually ship, fold whatever they resolved back into `design.md` per §5 below rather than leaving the decision only recorded in the milestone doc.
- **Proposal docs** (`embarch-doc/` root, `*-proposal.md`): a cross-repo design awaiting acceptance — neither a living `design.md` nor a milestone execution plan. It states, in its own closing section, exactly which decision number in which doc each piece folds into when accepted. §2's changelog raised the need for this tier twice (2026-08-24, 2026-08-25) and left it open both times; [embarch-stream-pipeline-proposal.md](embarch-stream-pipeline-proposal.md) is the case that forced it, having been *half* accepted — inbound direction folded into five design docs, outbound direction still proposed.

  **The policy for a partially-accepted proposal: if it is not fully closed, it is still open.** Its `**Status:**` line stays `proposal` (§7.1) — not `accepted`, not `half-accepted` — until every piece has folded into an owning doc. A proposal is deleted only when fully absorbed, and its `Status:` line is the single place a reader has to look to know which it is. This exists because a doc marked half-done reads as done to everyone who didn't write it.

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
- Same workflow also runs two checks added 2026-08-31 alongside §7's conventions: `scripts/check-decision-refs.py` resolves every prose `decision N` reference in the repo against the entries its sub-project actually defines (§7.3 — the gap `check-links.py` structurally cannot see), and `scripts/check-doc-conventions.py` checks every doc's `**Status:**` state token and date (§7.1). The first one's first calibrated run found two decision entries that had been **silently deleted** while three other docs went on citing them — `embarch-api` decision 31 and `embarch-umbrella` decision 27, both lost in unrelated editing passes on 2026-08-23 and 2026-08-17, both restored verbatim from git history the same day. That is the class of drift §7.4's retire-don't-delete rule exists to prevent, and nothing had ever been able to see it.
- **History does not live in a doc.** Every change drops a one-line fragment in `changelog.d/` (`<scope>-<slug>.<category>.md`, 200 B hard limit) and `scripts/build_changelog.py` assembles those into `history/<scope>.md` under a dated window, rolling older windows into `history/archive/` at a 20 KB cap. `--check` runs in CI so a misnamed fragment fails loudly. This replaced the `## Changelog` section every doc carried: those had reached **642 KB, 25% of the corpus**, at a mean of 1,100 B per entry against this section's own "one-line dated pointer" rule — and `archive-changelog.py`, which was supposed to trim them to 8 entries, delivered its trims **as pull requests** into a repo whose standing rule is no PRs, so not one was ever merged and `embarch-core/design.md` reached 70 entries. Both the script and its weekly workflow are retired.
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

## 7. Doc conventions

These are the shapes scripts parse and cross-references depend on. They are stated as conventions rather than prose habits because each one is either already checked mechanically or is about to be.

### 7.1 `**Status:**` line

Every doc carries one, as its first line after the title, in the form:

```
**Status:** <state>, <date>. <free prose, optional>
```

`<state>` is a single lowercase token, first thing after the label, exactly one of:

| state | means |
|---|---|
| `draft` | written, not yet a settled record |
| `active` | current and maintained — the live source of truth |
| `done` | an execution/milestone doc whose work has closed |
| `planned` | scoped, not started |
| `paused` | started, deliberately stopped |
| `proposal` | awaiting acceptance — including *partial* acceptance, per §3 |
| `retired` | no longer describes anything true, kept for reference |
| `superseded-by:<relative-path>` | replaced by another doc |

`<date>` is when the doc last *changed state*, not when it was last edited — the changelog covers edits. **The token and the date are the whole machine-readable part**; whatever follows the date is free prose, and most docs here have some (`done, 2026-08-24, except §3.8 (real-hardware validation), gated on…`). `scripts/check-doc-conventions.py` checks the token and the date and deliberately does not look past them.

Two notes on what this vocabulary is *not*:

- **`half-accepted` is deliberately absent.** Per §3's proposal tier, a proposal that isn't fully closed is still `proposal`.
- **`draft` is now gone from this repo, swept 2026-08-31 at the repo owner's direction.** It had been the state of 28 docs, including every long-lived design doc — [embarch-core/design.md](embarch-core/design.md) said `draft, 2026-07-17` through every milestone it documents. 16 became `active` (the living sources of truth), 11 became `done` (execution plans whose milestone closed, each carrying the closure it is claiming), and one deliberately did **not**: [embarch-umbrella/milestone-6.md](embarch-umbrella/milestone-6.md) stays `active`, because its §3.8 is still in progress and five §4 items are unmarked even though Milestone 6 ships in the foundation. A `done` asserted over an unmarked Definition of Done would be exactly the kind of status claim §4 exists to prevent.

This convention exists because `scripts/check-staleness.py` is a heuristic over two tables and `embarch-core`'s `doctor` check 11 is a stub — both are guessing at status that no doc states in a form anything can read. One greppable token per doc is what lets them stop guessing.

### 7.2 Decision entries

A decisions section is a numbered list of entries. In a doc that has been through a compaction pass, entries are grouped under topical `###` headings and each entry is its own heading:

```markdown
## Serialization, framing, and the link          <- a group

### 10 — COBS-framed postcard, versioned by an append-only enum
...
### 12 — Two hand-bumped schema constants, checked at both connection points
...
```

Two rules, both load-bearing:

- **The number comes first in the heading**, so every entry is greppable and individually addressable by anchor. The heading *level* is one below its group's, whatever that is — `##`/`###` in a standalone `decisions.md` (as above), `###`/`####` where the section still sits inside `design.md` at `##`. `scripts/check-decision-refs.py` accepts either.
- **Numbers are permanent, unique within the sub-project, and never reused** — including for entries that get retired (§7.4). Groups can be reordered, renamed, or split freely; numbers cannot. Out-of-order numbers inside a group are the intended outcome of grouping, not untidiness.

Pre-compaction docs use `N. **Title.** …` list items instead. Both forms are accepted and both parse; the heading form is what a compaction pass produces.

### 7.3 Referring to a decision

**A decision number addresses a sub-project, not a file and not a section.** The canonical forms:

- Within the same sub-project's own docs: `decision 39`.
- Across sub-projects: `embarch-study-designer decision 39`, or a link to the owning doc plus `decision 39`.
- Legacy, still accepted: `§3 decision 39`. The `§3` is redundant under this convention and is not maintained — a decisions section that moves to `decisions.md` (§3) does not invalidate it.

This matters more than it looks: a grep for `§N decision M`-shaped references across this repo on 2026-08-31 returned **1335 hits**, and `scripts/check-links.py` structurally cannot see one of them — it validates file paths and explicitly skips in-page anchors, and a prose reference to "decision 39" is not a link at all. `scripts/check-decision-refs.py` (§5) closes that gap: it resolves every reference against the entries that actually exist in the named sub-project, and runs in CI.

### 7.4 Retiring an entry

A decision that stops describing anything true is **retired, not deleted**. Its number keeps a one-line tombstone naming what it said, that it is retired, and what replaced it:

```markdown
#### 19 — Two-tier validation (retired 2026-08-25, see decision 48)
Post-hoc content validation, alongside the real-time per-step `Outcome`. Removed outright; the real-time half stands and is decision 48's subject.
```

A dangling reference then lands on an explanation instead of a gap. Retiring is also what keeps §7.3's "never reused" promise cheap to honor.

### 7.5 Measured vs. assumed constants

Every load-bearing constant carries which one it is, inline, in a bracket:

- `460800 baud [measured 2026-08-30, DK VCOM1 over the bridge]`
- `250 ms step timeout [assumed]`

Prose hedging ("the acceptable drift between resyncs is an open item, same posture as this doc's other hardware-unvalidated constants") carries the same information today and is invisible to grep — and, worse, it is exactly the kind of phrasing a compaction pass smooths away.

**Where this applies, established by sweeping it 2026-08-31.** The bracket earns its place on an **inventoried** constant — one in a table or a declared list, where provenance would otherwise be absent or vague. Two such inventories exist and both are now marked: [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md)'s 24-row `limits` table, and [embarch-outpost/design.md](embarch-outpost/design.md) §5.3's Kconfig table, which gained a Provenance column and the two symbols §7 measured into existence but never listed. It does **not** earn its place on a constant whose prose already derives it precisely — `DBM_MAX_TRANSCRIPT_PAYLOAD_LEN` is "244 (one full 247-byte ATT MTU minus the 3-byte ATT header)", and a bracket there is noise. A repo-wide scan for vague hedging within 90 characters of a constant found exactly **five** sites; three were worth marking, one was a retired constant, one a historical note. So the honest scope of this convention is: mark an inventory, and leave good prose alone. Everything else gets marked as its own doc reaches a compaction pass, where the constants get inventoried anyway. [DOC-COMPACTION.md](DOC-COMPACTION.md) §4 requires the measured/assumed distinction to survive a compaction; that requirement is only enforceable if the distinction has a shape. Given [embarch-decision-reversals.md](embarch-decision-reversals.md)'s length, being able to grep every `[assumed]` in the suite is worth having independent of compaction.
