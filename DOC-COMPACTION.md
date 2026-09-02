# embarch-doc: compaction protocol

**Status:** active, 2026-09-02.

## 1. What changed, and why this file was rewritten

The first version of this protocol had one invariant: **lossless about facts, lossy only about chronology.** It was followed, and it worked — and it produced a 2.66 MB corpus with single files at 311 KB. A doc nobody can load whole is a doc nobody reads, so "we kept every fact" bought accuracy nobody was consuming.

**The invariant is now the opposite: keep what a reader acts on, drop the rest, and let git hold it.** Efficiency and modularity are the goal; losslessness is not. Git is not a fallback here, it is the design: every deletion below is one `git log -p` away, forever, and that is what makes the deletions safe rather than reckless.

Three practices, in force from 2026-09-02:

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
| Suite-level doc | **10 KB** | `suite/*.md` |
| User guide (the one narrative doc) | **25 KB** | `suite/user-guide.md` |
| This file, and DOC-PROTOCOL.md | **12 KB** | `DOC-*.md` |
| Reversals | **25 KB** | `embarch-decision-reversals.md` |
| Assembled history | **20 KB** | `history/*.md`, rolled to `history/archive/` |

**20 files are over cap today**, holding 1,615 KB. Each is pinned at its current size by `scripts/doc-size-baseline.json`; reaching its cap retires the baseline entry, and the file is capped from then on. `--report` shows the corpus, `--update` records progress.

**The cap is the design constraint, not a target to approach.** A budget forces the question "is this the most valuable 10 KB I can write about this component", which is the question that was never being asked.

## 3. Four files per sub-project

Split by *when a reader needs it*, so the default load is small:

- **`spec.md` (10 KB)** — what is true now, and nothing about how it got that way. Purpose in three sentences; the invariants as a list; the interfaces (endpoints, types, actions, wire shapes) or a pointer to `interfaces.md`; the constants table with `[measured <date>]`/`[assumed]` on each; **what this component deliberately does not do**; pointers out. This is the file an agent loads to work on the component, and for most sessions it is the only one.
- **`decisions.md` (25 KB)** — why, one entry per decision (§5). Loaded when someone asks "why is it like this" or is about to change it.
  **Where a sub-project's decisions do not fit one file, split them by mission** into `decisions/<topic>.md` (12 KB each), leaving `decisions.md` as a ~2 KB index: a table of mission → file → the decision numbers in it. This is the shape for a component that owns several distinct jobs, because a session is usually there for one of them — `embarch-core` is the case that forced it, with 40 decisions across seven missions (platform, probes, flashing, studies, streams, logging, surfaces) that would not compress into 25 KB without cutting the rejected alternatives the budget exists to protect. Splitting costs a little total size (per-file headers) and buys every file being loadable, which is the actual goal. Do not split preemptively: one `decisions.md` is better while it fits.
- **`open.md` (5 KB)** — unresolved questions and known limitations, each with what would unblock it. `scripts/collect-open-questions.py` reads these.
- **`interfaces.md` (15 KB)** — only where the interface reference genuinely doesn't fit in `spec.md`. Do not create it preemptively.

A milestone doc is not on this list. Per §7, a shipped one folds into these four and is deleted.

## 4. History

Not in a doc. Every change drops a one-line fragment in `changelog.d/` (`<scope>-<slug>.<category>.md`, 200 B hard limit — see [changelog.d/README.md](changelog.d/README.md)); `scripts/build_changelog.py` assembles them per sub-project into `history/<scope>.md`.

What survives a compaction as history, and nowhere else:

- **Reality-driven reversals** — [embarch-decision-reversals.md](embarch-decision-reversals.md), one row: what was assumed, what reality showed, which decision owns it. This stays a *design* doc rather than history, because it is predictive: it says which remaining assumptions to distrust. It is capped at 25 KB, which is ~250 B per row.
- **Measurement provenance** — a measured number keeps its date and the conditions it was measured under, inline in the constants table. A constant that silently loses its provenance is the failure mode this suite keeps hitting.

Everything else about the past is dropped: amendment chains, "reversed same day", schema-bump re-derivations, "**Implemented 2026-08-25**", "three things implementation settled", review-item numbers, and every "this pass"/"the same session"/"recorded rather than discovered later".

## 5. What a decision entry looks like

Target **400 B**, hard ceiling **1,200 B** for the few that earn it. Structure:

```markdown
### 8 — One implementation, multiple call sites
`embarch-topology`'s UI/CLI and Core/api/umbrella's live calls run the same
crate `validate()`, not two layers that agree: it confirms the device is
enumerated and still matches its role's recorded identity, erroring with what
is stale.
Rejected: two independent mechanisms that happen to agree — there is no way
for one implementation to disagree with itself.
Gap: Core checks JTAG roles only; the dev-bench link has none (open.md).
```

That is 430 B, from a 1,621 B original — and the original was the *median* entry.

- **The claim first, in the heading.** Number, em dash, what was decided.
- **Rationale as tightly as it can be said**, including the constraint that forced it.
- **`Rejected: <alternative> — <reason>.`** One line each. This is the one thing that gets kept in preference to almost everything else, because it is what stops the same idea being re-proposed — but one line, not the argument. The full argument is in git.
- **No history.** Not what it was before, not when it shipped, not which pass renumbered it.

### Numbers are permanent, and an entry may own several

There are **2,362 prose `decision N` references** across this repo and `scripts/check-decision-refs.py` resolves every one. So a number is never renumbered, reused, or dropped. But under a byte budget several small decisions about one thing should be **one entry**, so an entry may own a list:

```markdown
### 20, 21, 25, 27 — Streaming capture, batched, with units
```

Every listed number stays resolvable, so every reference keeps working. Merging is the main tool for fitting 62 decisions into 25 KB, and 62 decisions for one crate is itself a sign that entries accreted past what is load-bearing. Where merging is not enough, split the file by mission (§3) rather than cutting rationale to hit a number.

Retire an entry rather than deleting it, as a one-line tombstone naming what replaced it: a dangling reference should land on an explanation, not a gap.

## 6. Procedure

1. **Pre-flight.** Working tree clean and pushed — git is where everything you are about to delete goes. `scripts/collect-open-questions.py > /tmp/oq-before.txt`.
2. **Read the whole doc first.** The merges that matter are between paragraphs 200 lines apart.
3. **Write `spec.md` first, from scratch, to its cap.** Not by deleting from `design.md` — by writing what is true now and then checking the old doc for facts you missed. Compaction by deletion preserves the old doc's shape, which is the problem.
4. **Then `decisions.md`**, grouping under topical headings, merging where §5 says to, one line per rejected alternative.
5. **Then `open.md`**, from the old open-questions section, dropping anything the work has since answered.
6. **Delete the old files**, fix every inbound link, in the same commit — this repo commits straight to `main` and must not be left broken in between.
7. **Gate** (§7), then commit, one sub-project per commit, with a `changelog.d/` fragment.

## 7. The gate

Mechanical, all five in CI:

- `check-doc-size.py` — caps and the ratchet.
- `check-decision-refs.py` — every `decision N` still resolves. This is what makes merging and file-moving safe.
- `check-links.py`, `check-staleness.py`, `check-doc-conventions.py`.
- `build_changelog.py --check` — fragments are valid.

Plus a diff of `collect-open-questions.py` before and after: a question may disappear only if you can name it as answered.

Human, and not skippable — **one question, asked honestly:**

> Can `spec.md` alone answer what someone needs to work on this component today?

If yes, the pass is done, whatever it deleted. If no, the pass moved bytes rather than choosing between them.

The old identifier-set diff (`grep -ohE '\`[^\`]+\`'` before and after) is now advisory rather than a gate — under a lossy regime an identifier is *allowed* to go. Run it anyway when you want a list of what you dropped, and use it to catch the one failure mode that is still a defect: **a concrete noun replaced by its category.** "provisioning is a separate step" instead of `build_and_flash`. Never replace a name with the kind of thing it is; drop the sentence instead.

## 8. Failure modes

- **Summarising instead of choosing.** "Handles the error cases" for four named ones. A budget is spent by *dropping whole topics*, not by making every sentence vaguer.
- **Deleting the "why not".** One line each, always. §5.
- **Flattening measured into assumed.** §4.
- **Renumbering.** §5. 2,362 references, invisible to detect.
- **Compacting a doc whose subsystem is still in flux** — you would be writing a clean statement of something about to be wrong, and destroying the alternatives you are about to need. Wait for the milestone to close.
- **Moving bytes instead of choosing between them.** Four files that add up to 300 KB is the old problem with more filenames. §7's human question is the check.

## 9. Migration order

Biggest first, one per commit, `--update` after each:

| | Today | Target |
|---|---|---|
| ~~`embarch-core`~~ | ~~233 KB~~ | **done: 53 KB, 11 files** |
| ~~`embarch-dev-bench`~~ | ~~185 KB~~ | **done: 81 KB, 11 files** |
| ~~`embarch-api`~~ | ~~158 KB~~ | **done: 68 KB, 11 files** |
| ~~`embarch-study-designer`~~ | ~~232 KB~~ | **done: 156 KB, 24 files** |
| ~~`embarch-outpost`~~ | ~~129 KB~~ | **done: 76 KB, 14 files** |
| ~~`embarch-ui`~~ | ~~92 KB~~ | **done: 68 KB, 12 files** |
| `embarch-umbrella` | 86 KB | 40 KB |
| `embarch-topology` | 77 KB | 40 KB |
| suite-level docs | 220 KB | 70 KB |
| `embarch-decision-reversals.md` | 59 KB | 25 KB |
| DOC-PROTOCOL.md / this file | 24 + 12 KB | 12 + 12 KB |

Corpus **1.93 MB → ~450 KB**. Shipped milestone docs and implementation guides (11 marked `done`, ~200 KB) fold into the four files and are deleted as their sub-project is migrated.
