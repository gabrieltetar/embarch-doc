# 098 — A prior-art lookup returns a US grant's independent claims as text

**State:** blocked
**Unparks when:** tasks/atlas/097
**Source:** Fleet Ready issue: agents read a US grant's claims page by page from image-only PDFs
**Issue:** EMB-136
**Scope:** atlas
**Hardware:** none
**Owner:** required — the owner holds the patent prior-art scan (2026-11-23): no leg takes it, whatever EMB-248 says, until the owner lifts the hold

## What

Once a prior-art scan has its hit table (`atlas/097`), the few documents that
matter have to be read claim by claim. For a US grant the issue's author
downloaded the office's PDF, found it image-only, and read the claims as
rendered pages, which is slow and token-heavy. When this is done one command
(the issue suggests `prior-art doc <number>`) returns the independent claims of
a given US grant as text, in the same verb and output conventions `atlas/097`
settled.

Which source gives the text is the worker's to find and record: the issue names
DEPATISnet's full-text PDF for recent US publications; the office's own
full-text search and other public pages may carry claims as text. An
independent claim is one that refers to no other claim.

## Constraints

- `atlas/097`'s constraints hold here unchanged: bounded live requests with
  generic numbers and terms, a source's terms for automated access read and
  recorded first, no network in tests.
- **No OCR and no new system tool.** Installing one is the owner's. A grant no
  text source covers is reported as such, naming what was tried, never as an
  empty claim list.

## Where

- The module and `cli.py` entry `atlas/097` created.
- `embarch-atlas/DESIGN.md` and `embarch-doc/embarch-atlas/design.md`.

## Done when

- [ ] One command returns the independent claims of a given US grant as text.
- [ ] A grant with no text source is reported as such, not as zero claims.
- [ ] Tests cover the claim split and the no-source case from recorded
      responses, with no network.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `DESIGN.md` and `embarch-doc/embarch-atlas/design.md` updated,
      `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false.
