# 012 — `embarch-dev-bench/decisions/ble.md` is 710 bytes from its cap

**State:** claimed — leg 050, 2026-09-08, dispatched as a **split only**
**Source:** `check-doc-size.py --pressure`, run during `tasks/dev-bench/009` — decision 23's
amendment pushed the file to 94.2% of its cap (11,578/12,288 B); `DOC-COMPACTION.md` §2
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

**Compacts:** embarch-dev-bench/decisions/ble.md, embarch-dev-bench/spec.md, embarch-dev-bench/open.md
**Size debt due:** 2026-09-22
**In flux:** yes — this file has taken two live corrections recently: decision 31 (16-bit UUIDs
reported two bytes out of place) and decision 23's amendment landed by this same commit. BLE is an
active area of the dev-bench firmware; do not compact ahead of the next correction landing, and
re-check this file's content against `git log` immediately before writing anything shorter.
**Must not delete:** decision 23's amendment sentence naming that the crate-side statement was not
yet true when the decision first claimed it, and what `embarch-study-designer` `79a4c00` actually
put in `src/ids.rs` — dropping either turns the amendment back into an unfalsifiable claim, which
is the exact defect this decision exists to correct. Decision 31's specific byte positions (which
two bytes, which direction) — a vaguer "some bytes were wrong" restates the bug this doc exists to
prevent a reader from reintroducing. Decision 34/37's "Just Works needs no auth callbacks was
wrong" sentence and the fact the original comment was deleted rather than amended — it is named as
"the load-bearing kind of wrong" for a reason.

## What

`embarch-dev-bench/decisions/ble.md` is in reserve (last 10% of its 12,288 B cap). Compact it per
`DOC-COMPACTION.md` and `DOC-COMPACTION-PASS.md`, keeping every decision number and the load-bearing
content of each entry — this is a shortening pass, not a content change.

## Why now

`check-doc-size.py` fails the gate on a file in reserve with no task naming it. This task is that
filing, dropped in the same commit that spent the reserve (decision 23's amendment).

## Done when

- [ ] `embarch-dev-bench/decisions/ble.md` clear of the 90%-of-cap reserve line.
- [ ] Every `Must not delete:` item above is still readable, verbatim or faithfully restated.
- [ ] No decision number renumbered; `check-decision-refs.py` still resolves every citation.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.

**Spent further by `tasks/dev-bench/013`, same day.** Decision 44 (the advertiser census's Manufacturer Specific Data element) was kept in `ble.md` rather than misfiled to a peer file with headroom, per `DOC-COMPACTION.md`'s own warning against a cap moving a decision instead of a worker shortening one — `ble.md`'s topic line already names scanning. Current numbers: `ble.md` 12,282/12,288 B (6 B left), `spec.md` 9,386/10,240 B (854 B left), `open.md` unchanged at 4,576/5,120 B (544 B left). `In flux: yes` still holds — this compaction should not start until whatever lands after decision 44 is also in hand.
