# 064 — `embarch-core` decision 44 (logging.md) is over the per-decision cap, unpinned, and retired

**State:** done — decision 44 compacted from 4,352 B to 2,438 B (1,658 B margin under the 4,096 B
cap); `logging.md` whole-file size (11,005 B -> 9,091 B) means `embarch-core/decisions.md`'s
`logging.md` size column moves 10.7 KB -> 8.9 KB. Both inbound `decision 44` citations
(`embarch-core/interfaces/logs.md`, `history/core.md`) still resolve to the claim they cite: the
hold-past-`\n` offset rule. Gate green.
**Reserve (leg 118):** `embarch-core/decisions/auth.md` is at 92.4% — 932 B left of 12288 — and is
already filed against `tasks/core/046-compact-core.md`, which is **blocked**. Do not write into
`auth.md` at all in this unit; you have no reason to. If your work does spend reserve anywhere in
`embarch-core`, file `tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** `core/063`, 2026-09-16 — while compacting decision 30, `check-doc-size.py --decisions`
(via `decision_state()` directly, since `--decisions` only prints its top 20 by size) showed
`embarch-core/decisions/logging.md#44` at **4,352 B**, over the 4,096 B per-decision cap and
**unpinned** — the same shape of gap `core/063` closed for decision 30, found in the course of that
same run rather than searched for. `core/063` was scoped to decision 30 only; this is the sibling
finding, filed rather than fixed so it is not lost.
**Scope:** core
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy.
**Owner:** no
**Compacts:** `embarch-core/decisions/logging.md`
**In flux:** no — decision 44 documents a route (`GET /logs/stream`) that was **retired by
`tasks/core/021`** and is already headed `*(retired)*`. Nothing about it is moving.

## What

Decision 44 is a full, unshortened entry (5 paragraphs) for a route that no longer exists. Unlike
decision 30 (`core/063`), this one is not "several arguments under one head" — it is one retired
decision, stated at full pre-retirement length, with a closing retirement paragraph appended rather
than the entry being cut down. **Prefer compacting over splitting** — a new decision number is the
most expensive thing in this suite to reverse, and a retired entry with no live consumer is exactly
the shape `DOC-COMPACTION-PASS.md`'s hot/cold test is for: the corrected offset-advance rule, the
"why hold rather than publish" reasoning, and the retirement itself are what a reader might still
need (hot); the specific incident narrative, the UTF-8 torn-character walkthrough, and the
"originally priced the case as..." self-correction are provenance and investigation log (cold).

**Read it before compacting.** `embarch-core/decisions/logging.md`, decision 44 (`### 44`).
`DOC-COMPACTION-PASS.md` applies in full if compacted, including quoting every cut hunk verbatim.

## Why now

Same reason as `core/063`: the per-decision cap has no ledger entry and no pin here, so an over-cap
decision is invisible except to someone who happens to read `decision_state()` directly (`--decisions`
only prints its 20 largest). Filing this now, while it is in hand, is cheaper than it being found a
second time by accident later.

## Watch for

- **Do not add a pin to `scripts/decision-size-baseline.json` to make the number go away.**
  `scripts/` is owner-reserved.
- **Decision 44 may be cited from outside `embarch-core`.** Grep the whole doc repo for
  `decision 44` before touching the text (`core/063`'s method: `grep -rn "decision 44\b"` across the
  doc repo, cross-checked against `check-decision-refs.py`).
- **This is retired, not live** — the retirement paragraph itself (`**Retired by
  `tasks/core/021`.**`) and the corrected rule it retired are the load-bearing part; the incident
  detail underneath is the more compactable half.

## Compaction taken

**Compacted, per `DOC-COMPACTION-PASS.md`'s hot/cold test, exactly on the split this task's `## What`
already named.** Kept: the corrected offset-advance rule and its bug description (the fix
paragraph), the "why hold rather than publish" reasoning in full (the failure signature an
`embarch-ui` reader would get wrong is load-bearing per the pass's own hot list), and the retirement
paragraph in full (cited externally by `interfaces/logs.md`). Cut: the UTF-8 torn-character
walkthrough (a distinct paragraph, entirely provenance for a decode-safety claim nothing outside this
entry cites), the "originally priced the case as..." anchor paragraph (a self-correction narrative
about an edge case in code that no longer exists — the retirement paragraph's own "the rule it wrote
governs nothing" applies here too, since nobody can re-hit a `/logs/stream` anchor bug), and one
meta-lesson clause in the fix paragraph.

**Grep across the whole doc repo first** (`grep -rn "decision 44\b" --include="*.md" .`): 26 hits, but
decision numbers are **per-sub-project**, not global (`check-decision-refs.py`'s own header) — all but
five hits are a *different* sub-project's own decision 44 (`embarch-dev-bench`, `embarch-umbrella`,
`embarch-api`, `embarch-study-designer`, `suite/*` citing `embarch-dev-bench`'s), untouched by this
compaction. The five that are `embarch-core`'s decision 44: `embarch-core/interfaces/logs.md:13` and
`history/core.md:63` (live doc citations, checked below), plus `tasks/core/021`, `tasks/core/063`, and
this task file itself (historical/self-referential, not live citations `check-decision-refs.py`
requires to resolve to *current* wording).

**What was cut, quoted verbatim and complete:**

- From the fix paragraph, a meta-lesson clause (cold per `DOC-COMPACTION-PASS.md`'s own cold list):
  `— which is the kind of claim a later reader builds on`
- The whole UTF-8 paragraph: `Reading bytes rather than `read_to_string` is what makes the UTF-8 half
  true instead of asserted: `0x0A` cannot occur inside a multi-byte sequence, so a slice ending at a
  `\n` is character-boundary-clean by construction, and a torn character can no longer reach the
  decoder. Genuinely invalid bytes — nothing this crate writes produces them — are now replaced rather
  than raised, because the old `read_to_string` error path never advanced the offset and would have
  re-read the same bad bytes every 750 ms forever.`
- The whole anchor/self-correction paragraph: `**One anchor is left uncovered on purpose, and it is
  reached more often than this entry first said:** the file length taken when `poll_in` finds a file
  it was not already following. If *that* read lands inside a torn write the anchor sits mid-line and
  one short line surfaces. **That branch is `first tick` as well as `rotated`** — a fresh
  `FollowState` has no path, so **every new `/logs/stream` subscriber anchors this way, on whatever
  file Core is writing, however old and however hot.** This entry originally priced the case as "a
  750 ms tick inside a microsecond window on a file created moments earlier", which describes the
  rotation half and not the common one; **it is once per subscriber, not once per rotation, and the
  file is not new.** What did not change is the cost: one short line, once, at the head of a tail
  nobody has read yet. Closing it needs a "we started mid-line" flag carried across ticks, and that is
  still not worth a field — but the reason is the size of the loss, not the rarity of the case, and
  the entry should not have leaned on the rarity. **`read_recent`/`tail_lines` are unchanged and still
  return a trailing partial as a line** — correct for "show me the tail as it stands now," and
  `embarch-ui`'s `diff_new_lines` already has a documented fallback for a window whose last entry
  changes under it.`

4,352 B → 2,438 B, 1,914 B cut, 1,658 B of margin left under the 4,096 B cap. `logging.md` whole file:
11,005 B → 9,091 B (10.7 KB → 8.9 KB in the index table).

**Citations checked, not just grepped.** `embarch-core/interfaces/logs.md:13` cites "the hold-past-`\n`
rule that surface needed" — still exactly what the kept fix paragraph states ("advances the offset
only past the last `\n`"). `history/core.md:63` cites "its offset advances past a `\n` or not at all"
— same claim, unchanged wording kept. Neither cites the UTF-8 mechanism or the anchor edge case, so
neither goes stale.

**No pin added to `scripts/decision-size-baseline.json`** — not needed; the entry is under cap, and
`scripts/` is owner-reserved regardless.

## Done when

- [x] `embarch-core` decision 44 is at or under 4,096 B. (2,438 B.)
- [x] `embarch-core/decisions.md`'s index table's `logging.md` size column matches. (10.7 KB → 8.9 KB.)
- [x] Every inbound `decision 44` citation still resolves to the claim it was citing. (Verified above:
  `embarch-core/interfaces/logs.md`, `history/core.md`.)
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). (`check-docs.py`: 11/11 green;
  `check-ownership.py --scope core`: OK; `check-ownership.py --code-repo`: OK, 0 paths changed;
  `check-client-names.py`: clean; `cargo build`/`test`/`clippy --all-targets -- -D warnings` in the
  code repo: green, 209 passed 0 failed, though this unit made no code-repo changes.)
