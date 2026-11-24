# 015 — `embarch-promptu/spec.md` and `open.md` are in reserve

**State:** blocked
**Source:** promptu 013 (EMB-273) added the built `week pack` to `spec.md` (9,186 of 10,240 B, 1,054 B left) and `open.md` (4,055 of 5,120 B, 1,065 B left).
**Scope:** promptu
**Hardware:** none
**Owner:** no

**Compacts:** embarch-promptu/spec.md, embarch-promptu/open.md
**Size debt due:** 2026-12-07
**In flux:** yes. Step 4 is half-built: the rest of `promptu week` (EMB-274 to EMB-279) rewrites both files' step 4 text in each unit, and the status paragraph in `spec.md` and the step 1 to 3 items in `open.md` change when the owner installs and answers W1 to W11. A rewrite now would be restated within a unit or two.
**Unparks when:** step 4's last build unit (`week apply`, EMB-279) lands; the compaction rides in the next unit that writes either file past its reserve.
**Must not delete:** every decision and EMB citation, the unmeasured and unverified items in `open.md`, and the fork ids; move reference detail to `spec/` verbatim.

## What

Bring `spec.md` and `open.md` out of reserve by moving reference text into `spec/` verbatim, leaving links.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed.

## Done when

- [ ] `scripts/check-doc-size.py --pressure` does not list `embarch-promptu/spec.md` or `embarch-promptu/open.md`.
- [ ] Moved text is byte-identical in its new file; `check-links.py` green.
- [ ] Gate green (`../../embarch-fleet/gate.md`).
