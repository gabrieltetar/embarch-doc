# 012 — `embarch-dev-bench/decisions/ble.md` is 710 bytes from its cap

**State:** done
**Unparked 2026-09-28 by the supervisor, at claim.** It was `blocked` from 2026-09-09 on `In flux:
yes`; the unpark condition that field named — "or the 2026-09-22 clock, whichever comes first" —
fired six days ago, and the flux it cited has ended on the evidence (see the `In flux:` field).
This is the oldest *payable* overdue ledger entry: the one older, `tasks/suite/030`, is still
blocked on owner-reserved `tasks/doc/045`.
**Dispatch note (supervisor, 2026-09-28):** reserve is `max(1200 B, 10%)` from the top, so the
floors are `spec.md` **9,040 B** (now 9,460 — 420 B to shed) and `open.md` **3,920 B** (now 4,782
— 862 B to shed). `decisions/link.md` (11,241/12,288) is also in reserve but belongs to
`tasks/dev-bench/014` — **leave it alone.** Out of reserve, or the task says why not: a squeeze
that has to delete an open question to reach the floor stops short and says so.
**Partially closed**: leg 050, 2026-09-08, dispatched and closed as a **split only**.
`decisions/ble.md` split verbatim into `decisions/ble.md` (pairing/security: 11, 15, 33, 34, 37;
7.7 KB) and the new `decisions/scanning.md` (addressing/scan-time discovery: 17, 23, 31, 32, 44;
4.8 KB), both out of reserve. `spec.md` and `open.md` are still in reserve and untouched — those
are squeezes. This task stays alive for that remaining half.
**Source:** `check-doc-size.py --pressure`, run during `tasks/dev-bench/009` — decision 23's
amendment pushed the file to 94.2% of its cap (11,578/12,288 B); `DOC-COMPACTION.md` §2
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

**Compacts:** embarch-dev-bench/spec.md, embarch-dev-bench/open.md
**Size debt due:** 2026-09-22

**`decisions/ble.md` was struck off this line by leg 057 on 2026-09-09, and it is paid.** It is
**7,902 B against a 12,288 B cap (64.3%)**, well clear of reserve — the split leg 050 ran did the
work. `check-doc-size.py --pressure` had been printing `PAID … close its item` for it and nothing
was closing it. **It was removed from the `Compacts:` line rather than annotated in place**, because
that line is parsed: leg 057's first attempt struck it through with `~~…~~` and prose, and
`check-doc-size.py` then failed the whole gate reporting `spec.md` and `open.md` as *in reserve with
no debt filed* — the parser had stopped recognising the line at all. The `Compacts:` line is data.

**The two items that remain** are `spec.md` at 9,460/10,240 B (92.4%) and `open.md` at 4,782/5,120 B
(93.4%). Both were added by the 2026-09-07 reserve-floor change, and **neither is covered by the
`In flux: yes` block below, which describes `decisions/ble.md`** — the file that is now paid. Read
that park against `DOC-BUDGET.md`'s split-first rule before assuming it blocks these two; a verbatim
split restates nothing, so `In flux` cannot forbid one.
**In flux:** no — **re-checked 2026-09-28 by the supervisor at claim.** `git log` shows neither
`spec.md` nor `open.md` changed since 2026-09-08 (twenty days), and the two advertiser-census tasks
this field named as the live cause, `007` and `008`, are both gone from the queue (`008` folded
2026-09-10 as decision 46). The 2026-09-09 answer below is kept as history, and the worker still
re-checks `git log` immediately before shortening anything.
**Was:** **yes for both files still on the line — but re-argued, because the block that used to
carry this answer was about a file that has left it.** Corrected 2026-09-09 by `tasks/doc/030`,
which found `In flux:` is answered *per file* and that this field had been left behind by
`decisions/ble.md` when leg 057 struck it off `Compacts:`. The paragraph directly above already
said so. **The answer for `spec.md` and `open.md` is still yes, on the `## Blocked` section's own
grounds and not on the quoted block's:** five `dev-bench` tasks are open, two of them
(`007`, `008`) are advertiser-census work that amends exactly these files, and both remaining items
are squeezes with no seam — so shortening either ahead of that lands a clean statement of something
about to change. **What unparks it:** the next `dev-bench` unit to write `spec.md` or `open.md`
compacts it in the same commit carrying the `Must not delete:` list below (`DOC-BUDGET.md`'s
ride-along rule), or the 2026-09-22 clock, whichever comes first. Kept verbatim below because it is
the live answer the moment `decisions/ble.md` re-enters reserve:

> **Was `In flux: yes` for `decisions/ble.md`:** this file has taken two live corrections recently: decision 31 (16-bit UUIDs
> reported two bytes out of place) and decision 23's amendment landed by this same commit. BLE is an
> active area of the dev-bench firmware; do not compact ahead of the next correction landing, and
> re-check this file's content against `git log` immediately before writing anything shorter.
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

- [x] `embarch-dev-bench/decisions/ble.md` clear of the 90%-of-cap reserve line. Closed by the
      2026-09-08 split: `ble.md` 7.7 KB, new `scanning.md` 4.8 KB, both well clear.
- [x] Every `Must not delete:` item above is still readable, verbatim or faithfully restated —
      moved byte-for-byte, verified by diffing every decision body against the pre-split file.
- [x] No decision number renumbered; `check-decision-refs.py` still resolves every citation.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) for the split.
- [x] `spec.md` squeezed 9,460 → 9,038 B (floor 9,040), no topic dropped — every invariant,
      constant (with its `[measured]`/`[assumed]` tag) and constraint reason kept; only "why"
      duplicated with `decisions.md`, or wording redundant with `open.md`/its own constants table,
      was cut. `check-doc-size.py --pressure` now reports it `PAID … out of reserve` at 88.3%.
- [x] `open.md` squeezed 4,782 → 3,916 B (floor 3,920), no open question dropped — 14 bullets
      before, 14 after (`collect-open-questions.py` diff count unchanged, spot-checked verbatim);
      every failure signature, rejected alternative and "why not" clause kept, only provenance
      narrative (leg numbers, dates, derivation arithmetic) and cross-file duplication (the log
      buffer overrun, already in `spec.md` §5) trimmed. Now `PAID … out of reserve` at 76.5%.

## Closed 2026-09-28

`In flux` re-checked against `git log` immediately before editing: neither file had moved since
2026-09-08 (twenty days), and the two advertiser-census tasks (`007`, `008`) the old `In flux: yes`
named as the live cause are both gone from the queue — consistent with the supervisor's dispatch
note. Both files are squeezes with no seam, so every cut was prose-tightening against the
hot/cold test (`DOC-COMPACTION-PASS.md`), never a deleted topic; neither had to stop short of its
floor. Full gate (`check-docs.py`) is RED only on the three pre-existing, not-mine files named in
the dispatch note (`embarch-core/decisions/handshake.md`, `embarch-ui/decisions/shell.md`,
`embarch-ui/open.md`) — unchanged by this unit. `check-ownership.py` clean in both worktrees;
`check-client-names.py` clean. Code repo (`embarch-dev-bench`) carries 0 commits, as expected for
a doc-only squeeze.

**Widened 2026-09-07 by the reserve floor.** `check-doc-size.py`'s reserve was 90% of a limit; a percentage of a small cap is not runway, and the corpus reached `suite/features.md` with 36 bytes left and `embarch-api/decisions/core-link.md` with 22. Reserve is now `max(1200 B, 10%)` from the top, so the paths added to the `**Compacts:**` line above crossed on the rule change, not on an edit. **Prefer a SPLIT** — [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2: a split restates nothing, so it costs no argument, and a file warned 1.2 KB out still has a seam to cut. Squeeze only where there is none.

**Spent further by `tasks/dev-bench/013`, same day.** Decision 44 (the advertiser census's Manufacturer Specific Data element) was kept in `ble.md` rather than misfiled to a peer file with headroom, per `DOC-COMPACTION.md`'s own warning against a cap moving a decision instead of a worker shortening one — `ble.md`'s topic line already names scanning. Current numbers: `ble.md` 12,282/12,288 B (6 B left), `spec.md` 9,386/10,240 B (854 B left), `open.md` unchanged at 4,576/5,120 B (544 B left). `In flux: yes` still holds — this compaction should not start until whatever lands after decision 44 is also in hand.
