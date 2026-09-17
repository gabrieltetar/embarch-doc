# 087 — Decision 64 still quotes the decision-62 language that decision 66 retired

**State:** open
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

- [ ] Decision 64's quoted or paraphrased decision-62 language no longer describes the duplication
      as temporary or as waiting on a queued follow-up, and points at decision 66 for what it
      actually resolved to.
- [ ] **Decision 64's own closing claim is re-read while you are there.** `suite/044` recorded that
      64 once claimed serving spans closed the `embarch-ui` gap, and `ui/065` measured that it did
      not; check whether that tombstone survives anywhere in 64's current text.
- [ ] `decisions/stream-index.md` still under its 90% reserve line (11,059 B of 12,288) — it was
      10,853 B after `core/086`, so this has room, but check before you write.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment only if the correction is reader-facing beyond the fix itself.

## Not yours

- **Do not reopen decision 66 or re-litigate the permanence.** `core/085` settled it and `suite/044`
  propagated it suite-wide; this task brings one decision's prose into line with that, nothing more.
- **Do not touch `embarch-ui`.** `tasks/ui/067` carried that side and has landed.
