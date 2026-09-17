# 079 — Compact embarch-core/decisions/surfaces.md

**State:** blocked — `In flux: yes`, so nothing here is dispatchable yet.
**Renumbered 078 → 079 by leg 137 at this unit's landing.** The `core/077` worker filed this as
`078` from a branch based before the same leg's refill commit, which had already taken that number
for `tasks/core/078-a-content-hash-on-status-...`. Both are real tasks and neither is a duplicate;
the collision is an artifact of two actors picking "next free number" against different views of
`main` within the same twenty minutes, and `check-task-numbers.py` would have refused the merge.
Nothing else about this task changed.
**Size debt due:** 2026-09-24 (one week out — this is the file's second
amendment inside a week; re-check the churn rate then and either compact or
extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/077` (2026-09-17):
`embarch-core/decisions/surfaces.md` at 11253/12288 B (91.6%, 1035 B left),
no debt filed.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/surfaces.md`

Shorten `decisions/surfaces.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding. The file crossed
90% of its reserve when decision 59 gained its second amendment (`core/077`):
`embarch-topology` decision 34 made five more failure points reach
`TopologyMismatch`, and this crate decided to keep collapsing all of them
into `kind: "not_attached"` rather than add a third `kind` value — recorded
in full, alongside the corrected doc comments and lead text it required in
`api.rs`/`study.rs`.

**In flux:** yes. Decision 59 has now been amended twice in six days
(`core/074`, `core/077`), both times because `embarch-topology` changed what
reaches `TopologyMismatch` out from under this crate's classifier. Decision
12's deferred `{code, message, cause}` body — the general case this file's
own decision 59 is one route's special case of — is still an open trigger,
not a closed question; the next thing that trips it (a second route needing
to distinguish two error kinds under one status) lands here too.

**Must not delete:** decision 12's own scope/trigger paragraph and its
citation of decision 59 as "the trigger firing for one route alone"; decision
59's original resolution (the `kind` field, the `503`/`409` split, the
`fix_it_url: None` reasoning); `core/074`'s correction (which failures used to
fall through un-downcastable, and via which four call sites); `core/077`'s
settlement (why collapsing stays a considered choice, the downstream-handling
argument from `.claude/leg.md`'s binary split, the wire-change cost that was
weighed and not paid, and the `embarch-api` "plug it in" gap it surfaced and
filed to `inbox/` instead of fixing here).

## Why now

`check-doc-size.py` names this file with no filed debt; per protocol §5 item
5, that failure must be filed rather than left silent.

## Done when

- [ ] `embarch-core/decisions/surfaces.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving, every "Must not
      delete" item above still present in substance.
- [ ] `scripts/check-doc-size.py` clean.
- [ ] Gate green.
