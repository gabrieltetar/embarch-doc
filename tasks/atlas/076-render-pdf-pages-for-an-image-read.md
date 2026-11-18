# 076 — Render pages of any PDF to images an agent can read

**State:** claimed by agent/atlas/076-render-pdf-pages-for-an-image-read, 2026-11-18 03:19
**Outcome:** shipped as `pdf pages` (`src/embarch_atlas/pdfpages.py`), poppler only, no MCP tool; real-scan legibility was checked by reading generated PNG sizes, not a client scan.
**Source:** Fleet Ready issue: an agent reading a scanned PDF with no text layer improvised page rendering and tiling with throwaway shell and Python.
**Issue:** EMB-138
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

One `embarch-atlas` verb, for example `embarch-atlas pdf pages <file> --pages 4-7 --tiles 2x2 --dpi 80`, renders a page range of any PDF — including one with no text layer — to PNG files in a scratch directory that the image `Read` tool reads legibly at its default settings. It can split each page into a tile grid, or crop to a box given in PDF points. It prints one line per file (page, tile, pixel size) and, per page and first, whether a usable text layer exists, so a caller uses `pdftotext` when it can. It works outside an atlas build, on an arbitrary PDF, and is built on the poppler calls the atlas already makes (`pdfinfo`, `pdftoppm`, including its `-x -y -W -H` crop), not on a new imaging dependency: PIL is not installed on the machine that found the gap.

## Why now

The owner moved the issue to Fleet Ready. The atlas already flags pages that need an image `Read` inside a build and renders crops for its schematic ladder, but no agent can call that on a PDF of its own.

## Dispatch notes

- `embarch-atlas` keeps no numbered decisions; record the verb in its `DESIGN.md`/`README.md` and `embarch-doc/embarch-atlas/` as the recent `q` verbs were.
- If an MCP tool is added too, update every lookup count and the test that pins the tool count, as `atlas/075` did.
- Tests use a small generated PDF (with and without a text layer), never a client document. The public-name guard (`test_public_guard`) must run, not skip: the supervisor links `.atlas-local` beside the worktree.
- No file of this sub-project is in reserve.

## Done when

- [x] One command renders a page range of a PDF with no text layer to PNG files that the image `Read` tool reads legibly at the default settings.
- [x] The command can split each page into a tile grid or a crop box given in PDF points.
- [x] The command reports, per page, whether a text layer exists.
- [x] It needs only poppler and the atlas's existing dependencies.
- [x] Gate green (`../../embarch-fleet/gate.md`, the Python bullet); docs updated, `changelog.d/` fragment dropped.
