# 173 — `embarch-api/interfaces/publish.md` is in reserve

**State:** done
**Source:** api 171 (EMB-226) filled `verify`'s table rows for checks 4, 6 and 9, leaving `interfaces/publish.md` at 11,437 of 12,288 B (reserve from 11,059 B).
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/interfaces/publish.md
**Size debt due:** 2026-12-06
**In flux:** no. `verify` is still moving, but the move this task asks for is a verbatim split, which restates nothing (`DOC-BUDGET.md`'s split-first rule), so the flux cannot forbid it. Set by the supervisor at `api/172`'s fold, 2026-11-23.
**Must not delete:** the `verify` table's per-check statements of what is and is not recomputed, the decision pointers (118 to 125), and the "not checkable offline" line of check 8.

## Dispatch notes

- **Unparked at `api/172`'s fold** (supervisor, 2026-11-23). Its condition fired: `api/172` edited the `verify` table (check 5's cell) and landed, and the compaction rode in it only halfway. It moved the publish section "What publish reads of Core before the manifest exists" verbatim to `interfaces/publish-pending-reads.md`, which left `interfaces/publish.md` at 11,070 B, still 11 B inside the reserve (out at 11,059 B). Its worker reported 11,040 B; `check-doc-size.py --pressure` reads 11,070.
- Do what **What** says: the `verify` section to `interfaces/verify.md` verbatim, with a link left. Change no wording, and keep every **Must not delete** item, moved or in place.

## What

Bring `interfaces/publish.md` out of reserve: split the `verify` section into `interfaces/verify.md` verbatim (the page is two surfaces under one name), update the links, and leave `publish.md` with the publish half. Never shorten a sentence that states what a check does not do.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [x] `scripts/check-doc-size.py --pressure` does not list `embarch-api/interfaces/publish.md`.
- [x] The moved text is byte-identical in its new file; `check-links.py` green.
- [x] Gate green (`../../embarch-fleet/gate.md`).

## Result

`publish.md` 11,070 -> 6,951 B (out of reserve); new `verify.md` 4,370 B holds the `verify` section byte-identical under a 3-line header. publish.md keeps a `## verify` pointer heading (so old `#verify` anchors still resolve); its status line now links verify.md. Links updated: `spec.md`, `decisions/verify.md`, `decisions/verify-report.md`, `features.d/api-370-verify.md`. `suite/features.md` left stale for the fold. Every Must-not-delete item moved with the section, unedited.

**Can `spec.md` alone answer what someone needs to work on the publish and verify surfaces today?** Not alone. It states what each does, the nine checks in one sentence, the refusals and the pointers, enough to know what exists and not to re-derive it. Building or changing a check, the zip layout, revisions or the exact recompute rules needs `interfaces/publish.md`, `interfaces/verify.md` and the decisions; the detail is by design in those, so spec.md is the map, not the working text.
