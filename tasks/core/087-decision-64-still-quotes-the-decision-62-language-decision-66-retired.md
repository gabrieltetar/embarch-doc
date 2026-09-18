# 087 — Decision 64 still quotes the decision-62 language that decision 66 retired

**State:** done — worker, 2026-09-17, branch `agent/core/087-decision-64-retired-language`. The stale
quote was reason (3) of decision 64's "yes, serve them" call: *"decision 62 already named this
duplication 'known to be temporary... until the queued follow-up.'"* Not fixed by either `core/085`
(added decision 66, corrected only 64's closing sentence) or `core/086` (restored two dropped
sentences in decision 62's own text, corrected nothing in 64). Reworded to past tense, pointed at
decision 66 as the follow-up's actual outcome, and stated that outcome as permanent rather than a
closure: *"decision 62 had named this duplication 'known to be temporary... until the queued
follow-up' — decision 66 is that follow-up's actual outcome, and it settled the duplication as
permanent, not the closure this reason anticipated."* Decision 64's closing-claim tombstone (checked
per box 2) does not survive anywhere in 64's current text — the only occurrence of the original
"closes the gap" sentence is inside `core/085`'s own "Corrected 2026-09-17" paragraph, quoted as
*"originally read"*, not asserted live. `embarch-core/decisions/stream-index.md`: 10,853 B -> 10,986
B, still under the 11,059 B reserve line — no compaction task owed.
**Doc-size reserve for `core`** (leg 142, before dispatch): `embarch-core/decisions/auth.md` 932 B
left, filed against blocked `tasks/core/046-compact-core.md`. **`embarch-core/decisions/stream-index.md`,
the file this unit edits, is not in reserve** (leg 141's `core/078` took `decisions/surfaces.md` out
of reserve; `stream-index.md` was never in it). If this unit pushes any file into the last 10% of
its cap, file `tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** `embarch-reviewer` on landed unit `core/086` (`embarch-doc@e75618d0`), leg 140,
2026-09-17. **The reviewer deliberately did not file this as a finding** — it predates `core/086`,
contradicts nothing that unit did, and it flagged it as context rather than as a fault in the diff
it was reading. That judgement was right and the gap is still real, so it becomes an ordinary queue
entry rather than disappearing into a review transcript.
**Scope:** core
**Hardware:** none — one quoted clause in one decision, settled by reading two decisions in the same
file against each other.
**Owner:** no

## What

`embarch-core/decisions/stream-index.md` decision **64** still quotes the *pre-085* decision-62
language — the phrasing around *"known to be temporary… until the queued follow-up"* — describing
the `Lane`/`Span`/`Gap` duplication between `embarch-core/src/outpost_load.rs` and
`embarch-ui/src/trace.rs` as a temporary state with a pending resolution.

**Decision 66 settled that it is permanent**, and `suite/decisions/placement.md` §4 was narrowed on
2026-09-17 (`suite/044`) for the same reason. `core/086` corrected decision **62**'s own text — it
removed an "until then" that decision 66 had made false — but decision 64 sits one paragraph away
in the same file and still carries the retired framing.

## Why now

Cheap, and it is one paragraph from a sentence this leg already corrected. A reader who arrives at
decision 64 first — which is likely, since 64 is what shipped the spans route and is the entry
`embarch-ui`'s docs cite — gets the answer decision 66 retired, from the same file that also holds
the correction. That is the stale-pointer class `tasks/ui/042`/`048`/`063` and `core/086` itself all
exist to clear.

## Done when

- [x] Decision 64's quoted or paraphrased decision-62 language no longer describes the duplication
      as temporary or as waiting on a queued follow-up, and points at decision 66 for what it
      actually resolved to.
- [x] **Decision 64's own closing claim is re-read while you are there.** `suite/044` recorded that
      64 once claimed serving spans closed the `embarch-ui` gap, and `ui/065` measured that it did
      not; check whether that tombstone survives anywhere in 64's current text. — It does not; the
      only surviving copy of that sentence is inside `core/085`'s "Corrected 2026-09-17" paragraph,
      quoted as the thing that was wrong, not asserted.
- [x] `decisions/stream-index.md` still under its 90% reserve line (11,059 B of 12,288) — it was
      10,853 B after `core/086`, so this has room, but check before you write. — 10,986 B after this
      edit, still ~73 B under the line.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment only if the correction is reader-facing beyond the fix itself. —
      Filed (`changelog.d/core-decision-64-retired-framing.fixed.md`): a reader landing on decision
      64 without this fix would still be told the duplication is temporary, which decision 66 says
      is false.

## Not yours

- **Do not reopen decision 66 or re-litigate the permanence.** `core/085` settled it and `suite/044`
  propagated it suite-wide; this task brings one decision's prose into line with that, nothing more.
- **Do not touch `embarch-ui`.** `tasks/ui/067` carried that side and has landed.
