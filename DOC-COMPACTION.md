# embarch-doc: compaction protocol

**Status:** draft, 2026-08-31.

## 1. Purpose

[DOC-PROTOCOL.md](DOC-PROTOCOL.md) says how a doc gets *written* while work happens. This file says how a doc gets *compacted* once that work has landed.

The two need separating because they pull opposite ways. During design and implementation the correct bias is to write everything down: a rejected alternative, a constant nobody has measured yet, an amendment stacked onto an earlier decision. Losing a fact costs more than carrying a redundant one, so nothing is deleted and the doc grows by accretion. That bias is right, and it has a measurable cost — as of 2026-08-31:

- [embarch-study-designer/design.md](embarch-study-designer/design.md) is 343 KB across 1001 lines. Its §3 alone (locked-in decisions) runs from line 39 to line 610.
- [embarch-core/design.md](embarch-core/design.md) is 314 KB; [embarch-outpost/design.md](embarch-outpost/design.md) is 160 KB after five weeks of existence.
- `embarch-study-designer/design.md` §3 needed its own **decision index** table, added 2026-08-15, whose stated reason is that "this list outgrew comfortable linear reading well before decision 30" — a navigation aid bolted onto a section that had stopped being readable.
- Individual decisions read as their own edit history rather than as a statement of what is true. Decision 12 there is three stacked paragraphs each opening `**Hello also now …**`; the index marks decision 10 `Amended by 20, 24, 25` and decision 15 `Amended (grows a constant per new field, incl. 25/27)`. A reader wanting the current wire behavior has to reconstruct it from four entries written weeks apart.

Compaction is the pass that pays that debt down. **Its one invariant: compaction is lossless about facts and lossy only about chronology.** Every fact in the doc survives; the record of the order in which the facts arrived does not. Git history holds the pre-compaction text, so chronology stays recoverable without living in the doc — that is why this protocol has no `*.compaction-archive.md` counterpart to §5's changelog archive.

## 2. The contract

A compaction pass is admissible only if all four hold:

1. **No fact is lost.** Anything the pre-compaction doc could answer, the post-compaction doc can still answer, at the same specificity. Not "at the same length" — at the same *specificity*.
2. **No fact is added.** Compaction does not introduce a claim, resolve an open question, or update a status. If you learn something while compacting, that is a separate edit and a separate commit (§7).
3. **No identifier changes meaning.** Decision numbers, section numbers, and heading anchors that other docs point at keep pointing at the same thing (§6).
4. **The diff is reviewable as "same content, better shape."** If a reviewer cannot tell whether the meaning changed, the pass is too large — split it.

The reason 2 is stated as strictly as 1: a pass that both reorganizes 500 lines and quietly changes three claims is unreviewable, and the claims are what matter. Keep the two kinds of change in separate commits even when they touch the same paragraph.

## 3. When to compact

Compaction is a phase, not a habit. It runs at the transition from "we are deciding this" to "this is what is true":

- **A sub-project's `design.md`:** when a milestone touching it closes *and the work has shipped and been exercised*. This is the same moment [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3 already says to fold a milestone's resolutions back into `design.md` — compaction is the other half of that fold.
- **A `milestone-N.md`:** once its steps have shipped, the doc's remaining job is nearly zero. **Fold what it resolved into `design.md` and delete it** — that is the rule, not the preference. Keep it only if it holds something `design.md` genuinely cannot: work deliberately deferred with the reason, or a deferred item still gating something. Then it survives as that short record, not at full length. A completed execution plan left intact competes with `design.md` for the reader who wants current truth, and git history holds it either way.
- **Suite-level docs:** [embarch-features.md](embarch-features.md) and [embarch-roadmap.md](embarch-roadmap.md) are already tabular and compact by growing rows, not paragraphs. Their compaction target is different (§10).

**Do not compact:**

- A doc for a subsystem still in flux. Compaction makes a doc a clean statement of current truth; doing it mid-design produces a clean statement of something that is about to be wrong, and destroys the accreted alternatives you are about to need.
- Anything whose facts have not been exercised against reality. An unvalidated constant compacts into looking authoritative. If it has not run on hardware, it stays marked as unvalidated (§4).
- More than one doc in a pass. One doc, one commit.

**Signals a doc is due** (none of these is a hard limit — they are the shapes that showed up in this repo):

- A section needs an index or a status table to be navigable at all.
- A single decision's text describes its own amendment history, or two-plus paragraphs open with "also now".
- Byte count badly out of proportion to line count — this repo writes one paragraph per line, so 300 KB across 1000 lines means the paragraphs themselves have grown, not that there are more of them.
- The same fact is stated in three places in one file, each with slightly different hedging.
- A "current" statement is only reachable by reading an earlier entry plus its later corrections.

## 4. What must survive

Treat this as a checklist, not prose. A compaction that drops any of these is a defect, not a trade-off:

- **Every invariant, constraint, and interface fact that is currently true** — names, wire formats, message enums, endpoint paths, file paths, capacities, timeouts, baud rates, env var names.
- **Every rejected alternative, with the reason it was rejected.** This is the highest-value and most-at-risk content in the repo: it reads as historical, so it is the first thing a careless compaction deletes, and it is the only thing that stops the same alternative being re-proposed in six months. A rejected alternative is a *current fact* about the design, not chronology.
- **Every reality-driven correction's lesson.** An assumption reality overturned predicts which remaining assumptions to distrust — that is the whole premise of [embarch-decision-reversals.md](embarch-decision-reversals.md). The *narrative* of the correction can go; the *lesson* stays. Before deleting one, confirm decision-reversals has the row; if it does not, add it in a prior commit (that is a §2-rule-2 content change, so it is its own commit).
- **The measured/assumed distinction.** A number that came off real hardware and a number somebody picked must stay visibly different after compaction, along with the conditions the measured one was measured under. Flattening those into one confident table is the worst single outcome of a bad compaction.
- **Every open question and known limitation**, with what would unblock it. `scripts/collect-open-questions.py` gives you the before/after set to diff (§8).
- **Anything another doc links to**, by file, section number, decision number, or heading anchor (§6).
- **Any fact that exists only in this doc.** Before deleting a paragraph because it "belongs in another doc," check the other doc actually says it. Moving a fact is fine; assuming it is already elsewhere is how facts die.

## 5. What gets discarded

- **The chronology of a decision's arrival.** Intermediate states, superseded phrasings, "originally X, then Y, now Z" — the doc states Z.
- **Amendment bookkeeping** (`Amended by 20, 24, 25`, `**X also now carries…**`) — once the entry's text states the current behavior directly and completely, the bookkeeping has nothing left to point at.
- **Restatement.** A fact stated once in its owning section, linked from elsewhere per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §5's link-don't-restate rule.
- **Meta-narration about the doc's own editing** — "closing item 37 of the 2026-08-15 review", "added in the same pass as", "see the changelog entry below" — unless it carries a lesson, in which case §4 applies and it moves to wherever that lesson belongs.
- **Hedging and self-justification.** "It is worth noting that", "this is deliberate rather than accidental", "as described above". Say the thing.
- **Navigation aids the compaction makes unnecessary** — a decision index that existed because the list was unreadable comes out when the list becomes readable. Do not compact around an index; compact the thing the index was compensating for.
- **Superseded designs whose replacement fully covers the ground**, subject to §4's rejected-alternatives and decision-reversals rules. "Superseded" is a much higher bar than "old".

## 6. Entries become sections — without breaking 1335 cross-references

This is the transform the compaction exists to perform: an append-only numbered list is a *log format*, and the compacted doc should be a *topic format* — sections named for what they describe, each stating what is true once.

The hazard is that decision numbers are load-bearing across the whole repo. A grep for `§N decision M`-shaped references on 2026-08-31 returns **1335 hits**, spread across every design doc, [embarch-features.md](embarch-features.md), [embarch-roadmap.md](embarch-roadmap.md), and every row of [embarch-decision-reversals.md](embarch-decision-reversals.md). `scripts/check-links.py` does not and cannot catch these — it validates file paths, explicitly skipping in-page anchors, and a prose reference to "decision 39" is not a link at all. Renumbering silently invalidates cross-references that nothing checks.

So the rule is: **decision numbers are permanent identifiers. Never renumber, never reuse, never renumber-and-remap.** Compaction reorganizes *around* the numbers:

- **Group, don't renumber.** Add topical `###` subsections and move whole entries under them, keeping each entry's number in its own heading (`### 39 — Stream taps`). The list stops needing linear reading because the grouping carries the navigation; the numbers survive untouched. Out-of-order numbers within a section are the intended outcome, not untidiness.
- **Merge an amendment chain into its base entry.** Decision 12 plus its three "also now" paragraphs becomes one entry 12 stating current behavior. If a later-numbered decision (20, 24, 25) amended an earlier one, the earlier entry states the current truth and keeps a one-clause pointer to the later number — the later entry is still a real referent for the 1335 references and cannot be absorbed away.
- **Retire, don't delete, a superseded entry.** A number that no longer describes anything true becomes a one-line tombstone: what it said, that it is retired, and which entry replaced it. A dangling prose reference then lands on an explanation instead of a gap.
- **Section numbers are identifiers too.** `§4.7`, `§3.10`, `§5.1` are cited across docs the same way. Renumbering sections is a link-breaking change: prefer adding `###` depth inside a section over renumbering its siblings, and if a section number must change, grep the repo for it and fix every citation in the same commit.
- **Never let a heading anchor a doc links to disappear silently.** Six in-page anchor links exist today; grep `](#` before rewriting headings.

The conventions this transform produces — number-first `#### N — Title` entry headings, the sub-project-scoped reference form, and the retirement tombstone — are stated once in [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §7.2–7.4 rather than restated here. The one that changes what compaction is *allowed* to do: **a decision number addresses a sub-project, not a file and not a section** (§7.3). That is what makes DOC-PROTOCOL.md §3's extraction threshold safe — a decisions section past 40 entries or ~120 KB moves to `<sub-project>/decisions.md` **as part of the compaction pass**, not as its own churn event, and the 1335 existing `§3 decision N` references survive the move because the `§3` was never the address. `scripts/check-decision-refs.py` verifies this, and is the reason the pass is checkable at all.

## 7. Procedure

Pre-flight:

1. Working tree clean and pushed. Git history is the archive for what you are about to delete — if the pre-compaction text is not committed, it is not recoverable.
2. Capture the baselines: `scripts/collect-open-questions.py > /tmp/oq-before.txt`, and an identifier inventory of the target doc (§8).
3. Read the whole doc first. Compaction decided paragraph-by-paragraph produces a doc that is locally tidy and globally redundant — the merges that matter are between paragraphs 200 lines apart.

The pass:

4. Decide the target section structure before editing anything. Write it down (even as a scratch list of headings) — that is what makes the pass a transform rather than a cleanup.
5. Do the structural move first: group entries, no rewording. Then merge amendment chains. Then delete redundancy. Three sweeps, not one, so that a deletion is never made before you have seen where the fact landed.
6. Update the doc's own status line and heading numbering if they changed; grep-and-fix every cross-reference the pass invalidated (§6), in this same commit — a link-breaking commit that fixes links in a follow-up leaves `main` broken in between, and this repo commits straight to `main` ([embarch-dev-workflow.md](embarch-dev-workflow.md) §6).

Close-out:

7. Run the verification gate (§8). Fix, do not rationalize, anything it flags.
8. Add one `## Changelog` bullet per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §5, stating that the pass was a compaction, what the new section structure is, and — explicitly — what was deleted as chronology. A compaction changelog entry is the one place a reader is told that absence of text is deliberate.
9. Commit alone. No compaction commit also changes a fact, a status, or another doc's content beyond the cross-reference fixes §6 requires.

## 8. The verification gate

Mechanical, cheap, run every time:

- `scripts/check-links.py` — every relative link still resolves.
- `scripts/check-decision-refs.py` — every `decision N` reference in the repo still resolves to an entry that exists. This is the check that makes §6 enforceable rather than a request.
- `scripts/check-staleness.py` — the compacted doc's status facts still agree with [embarch.md](embarch.md) §3 and [embarch-features.md](embarch-features.md).
- `scripts/collect-open-questions.py`, diffed against the pre-flight capture. **Every open question that disappeared must be one you can name as answered.** A compaction has no business resolving open questions (§2 rule 2), so in practice the correct diff is empty, and any deletion is a bug.
- **Identifier inventory diff.** Before and after, extract the doc's concrete nouns and numbers and diff the sets — every identifier that vanished must be explainable as a duplicate mention, never as the only mention:

  ```sh
  # symbols, paths, env vars, quoted names
  grep -ohE '`[^`]+`' <doc> | sort -u > /tmp/ids-before.txt
  # numbers with units, and bare constants
  grep -ohE '[0-9]+(\.[0-9]+)?\s*(ms|s|us|Hz|kHz|MHz|KB|MB|bytes?|baud|B/s)' <doc> | sort -u >> /tmp/ids-before.txt
  ```

  This is the check that catches the failure this whole protocol is guarding against, and it takes thirty seconds.
- Byte and line delta, recorded in the changelog bullet. A pass that removes 40% of the bytes and 0 facts is the shape you want; one that removes 5% has probably only tidied.

Human, and not skippable:

- **The restoration question, per deleted block:** which surviving sentence carries this fact? If the answer is "the reader can infer it", restore it.
- **Re-read as a stranger.** Pick three questions the original doc answered — a specific constant, a specific "why not X", a specific failure mode — and answer them from the compacted doc alone.
- **Check the rejected alternatives are still there.** Count them before and after if you have to. This is the failure mode that does not announce itself.

## 9. Failure modes

- **Summarizing instead of compacting.** "Handles the error cases" replacing four named error cases. Compaction removes *redundancy*, never *specificity* — the rule that catches it: never replace a concrete noun with its category.
- **Deleting the "why not".** §4 and §8's last human check exist for this one.
- **Flattening measured into assumed.** A compacted table reads authoritative whether or not its numbers came off hardware.
- **Renumbering.** §6. Cheap to avoid, invisible to detect, 1335 references deep.
- **Compacting a doc that is still arguing with itself.** If two sections disagree, that is a content bug — fix it as a content change first, in its own commit, then compact. Compaction must never be the pass that silently picks a winner.
- **Scope creep into a rewrite.** A compaction that touches everything is not reviewable, and this repo pushes straight to `main`. One doc, three sweeps, one commit.
- **Compacting to a length target.** The target is one statement per fact. Whatever length that produces is the right length.

## 10. Per-doc-type notes

- **`<sub-project>/design.md`** — the main case; §§3–9 are written for it. Its §3-equivalent decision list is where nearly all the recoverable bytes are.
- **`<sub-project>/milestone-N.md`** — after shipping, fold into `design.md` and delete (§3). It survives only to hold what `design.md` cannot: deferred work and its reason.
- **[embarch-features.md](embarch-features.md) / [embarch-roadmap.md](embarch-roadmap.md)** — already tabular. Their bloat is not entry accretion but per-row prose and changelog length; `scripts/archive-changelog.py` handles the latter. Rows for shipped features can lose their execution detail and keep a link.
- **[embarch-decision-reversals.md](embarch-decision-reversals.md)** — do **not** compact by merging or dropping rows. Its value is the count and the specificity: each row is one reality-driven correction, and the list's length is itself the signal. Only the header prose is compactable.
- **[embarch-glossary.md](embarch-glossary.md)** — already a compacted form by construction (a term, a one-line definition, a link to the owning doc). If an entry has grown an explanation, the explanation belongs in the owning doc.
- **[embarch-user-guide.md](embarch-user-guide.md)** — the one doc written for an outside reader, and [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3 already exempts it from link-don't-restate. Restatement there is a feature; compact it for *reading order* and dead paths, not for redundancy.
- **[DOC-PROTOCOL.md](DOC-PROTOCOL.md) and this file** — same rules, same gate. Both are already accreting the shape §3 warns about.

## 11. A worked pass: `embarch-study-designer` §3

The first real exercise of this protocol, 2026-08-31, kept here because the numbers and the two things the gate caught are more useful than the rules restated.

**The target.** §3 of [embarch-study-designer/design.md](embarch-study-designer/design.md): 62 decisions, 183,569 bytes, 572 lines, and — since 2026-08-15 — its own status-table index whose stated reason was that "this list outgrew comfortable linear reading well before decision 30".

**What it became.** [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md), extracted per [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §3's threshold in the same pass: 12 topical groups plus one for removals, each entry a `### N — Title` heading, 142,263 bytes. `design.md` went 343,229 → 160,756 bytes; the two files together, 343,229 → 303,019, **−12%**.

**−12% is the honest number and it is smaller than it looks like it should be.** Almost all of §3's bulk was *facts* — 24 capacity constants with their sizing reasons, ~60 rejected alternatives, measured numbers with the conditions they were measured under — and this protocol forbids touching any of that (§4). The recoverable bytes were the chronology: stacked amendments, the index, meta-narration, hedging. A pass on a doc whose bulk is genuinely content should come back with a modest byte win and a large navigability win, and if it comes back with 50% it is worth asking what left. The win here is that a reader looking for the wire framing rule reads one group of five entries instead of scanning 572 lines for entries 3, 4, 10, 24 and 25.

**The shape of the transform, on the worst entry.** Decision 12 (schema versioning) was, before: an entry, then a "this is a detector not a negotiator" paragraph, then `**Hello also now doubles as a hard reset.**`, then `**Hello also now carries host_utc_ms.**`, then a 2026-08-25 amendment splitting one constant into two, then an implementation note, then a *second* amendment reporting that the split's prediction held, then a "three things implementation settled" list. A reader wanting the current handshake had to reconstruct it from eight blocks written across three weeks. After: one entry stating both constants and what bumps each, the detector-not-negotiator rule, the compile-time assertion that holds the invariant, the three implementation findings, and a closing paragraph on `Hello`'s two other jobs. **Every fact survived; the order in which they were learned did not.** The "why one constant became two" reasoning is kept in full — it is a rejected alternative (dropping validation from the trigger list) with a real consequence attached, which §4 protects.

**What the identifier diff caught, which is the whole reason §8 has one.** First run: 751 backticked identifiers before, 152 gone. Most were artifacts — `MAX_NAME_LEN = 32` "vanished" because the name and the value now sit in adjacent table cells. **Seventeen were real**: concrete nouns replaced by their category, which is §9's first named failure mode, committed by the same pass that wrote §9 down.

- "provisioning stays a separate `embarch-api` step" had eaten `build_and_flash`/`build_and_flash_dev_bench`
- "(Batch Data Service)" had eaten `bds_ctrl_char_uuid`/`bds_status_char_uuid`/`bds_data_char_uuid` and `ble_def.h:141-147`
- "the v14 test vector pins" had eaten `tests/firmware_test_vectors.rs`
- "a blank one is a separate pre-flight failure" had eaten `Requirements::validate`
- and similarly `crc.rs`, `StreamTapTooLargeError`, `validate_study`/`validate_taps`, `STUDY_FFI_STUB_SCHEMA_VERSION`, `csv_escape_ok`, `zephyr-dc4cc07-current.bin`, two commit hashes, `extern crate alloc`, `impl GattConfigExtractor`, `[study_designer]`, and two `milestone-11.md` implementation pointers

All restored. Of the rest, the ones that genuinely appear nowhere in the compacted text were checked individually against the doc that owns them — `GattConfigExtractor`'s method signature, `steps_crc()`'s signature and the `"completed"` status string are all still in `design.md` §4/§5, which own the type shapes, so removing them from a decision entry is §5's link-don't-restate rule rather than a loss. The retired validation type family (`ValidationSource::*`, `PostHocValidation`, `ContentValidity::*`) is gone deliberately, tombstoned at entries 19 and 28.

**The open-questions diff was empty**, which is the correct result: a compaction has no business resolving one (§2 rule 2).

**The gate also caught a bug in the gate.** `scripts/check-decision-refs.py` read entries only from a `## N. …decisions…` section heading, so a standalone `decisions.md` — whose groups are plain `##` headings — contributed **zero** entries, and the run came back with 342 "unresolved" references. Nothing was actually wrong with the compacted doc; the check that was supposed to prove the extraction safe could not see the extracted file. Fixed (a `decisions.md` is the decisions section end to end, and an entry heading may be `###` or `####`), and [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §7.2 now states the heading rule as a *level relative to the group* rather than a fixed depth. The lesson is narrow and worth keeping: **the first real use of a checker is also the first real test of it**, and a green run on the old shape proved nothing about the new one.

**After the fix: 3,426 references resolve, and `embarch-study-designer` still defines 62 entries numbered 1..62.** That is the property the whole of §6 exists to protect, and it is now a mechanical fact rather than a claim.

## Changelog

- 2026-08-31 — **§11 added: the first real pass, and it found seventeen defects in its own output.** Compacting `embarch-study-designer` §3 (62 decisions, 183,569 bytes) into [embarch-study-designer/decisions.md](embarch-study-designer/decisions.md) exercised every rule here. §8's identifier diff caught seventeen concrete nouns replaced by their category — §9's own first failure mode, committed by the pass that wrote §9 — all restored. §7.3's rule that a decision number addresses a sub-project rather than a file held: all 62 numbers survived the move to a different file with none of the references touched. And the run exposed a blind spot in `scripts/check-decision-refs.py` itself, which could not see a standalone `decisions.md` at all. §3's milestone-doc rule also tightened from "prefer folding and deleting" to "fold and delete", at the repo owner's call on efficiency.

- 2026-08-31 — Initial draft. Written because the design/implementation phases' correct append-only bias had produced a 343 KB `design.md` whose §3 needed its own index to stay navigable, and there was no stated rule for the pass that pays that down — so "compact this doc" was a judgment call re-made from scratch every time, with no protection for the content that most needs it (rejected alternatives, the measured/assumed line, and the 1335 prose `§N decision M` cross-references no script checks). Registered in [DOC-PROTOCOL.md](DOC-PROTOCOL.md) §2/§3 and [embarch.md](embarch.md) §6 in the same pass, per DOC-PROTOCOL.md §5.
