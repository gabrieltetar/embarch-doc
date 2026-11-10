# 042 — A kind override reaches a prepped document's doc.json

**State:** claimed by agent/atlas/042-a-kind-override-reaches-a-prepped-documents-doc-json, 2026-11-09 20:17
**Source:** Linear issue EMB-31, filed by a session
**Issue:** EMB-31
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

After `embarch-atlas missing --kind <file> <kind>`, or the kind change `missing --confirm reference-manual` makes, an already-prepped document's `docs/<doc_id>/doc.json` carries the new kind — or the command prints that `doc prep <pdf>` must run again and names the document. Either way `doc.json` and the manifest stop disagreeing silently.

Today the override is recorded in `inventory/answers.toml` and the manifest is rewritten (`_refresh_manifest` runs `inventory.run`), but `doc.json`'s `kind` is written only by `doc prep`, so readers of it — `Atlas.find_doc`, which ranks `appnote` documents last — keep the old kind.

## Why now

Filed from distilling real documents: an override looked applied and was not.

## Where to look

- `src/embarch_atlas/missing.py` `_cmd_match` (the `args.kind` branch), `_refresh_manifest`, `_confirm_rm`
- `src/embarch_atlas/pdftext.py` `prep` — the only writer of `doc.json`'s `kind`
- `src/embarch_atlas/query.py` `Atlas.find_doc` — a reader
- `src/embarch_atlas/answers.py` `record_document` — the override, keyed by `sha256[:12]`

## Dispatch notes

- No `embarch-atlas` doc is in reserve and none is near a decision limit (`check-doc-size.py --pressure`, 2026-11-09 20:16).
- This leg runs in burndown: no new numbered decision. If the fix needs one, stop and say so in this file rather than writing it.

## Done when

- [ ] After `missing --kind` on a prepped document, `doc.json`'s `kind` equals the manifest's, or the command prints that `doc prep` is needed and for which document.
- [ ] The same for `missing --confirm reference-manual`.
- [ ] A test in `tests/test_matching.py` or `tests/test_inventory.py` covers the prepped and the not-yet-prepped case, on a synthetic PDF.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); `DESIGN.md` updated if it describes the override; `changelog.d/` fragment dropped.
