# `outpost_manifest.rs` is undocumented, and two source comments cite a Core decision that does not exist

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `spec.md` §4's module table lists 14 of 15 modules
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/main.rs:11` declares `mod outpost_manifest` — 951 lines in `src/outpost_manifest.rs` — and the
string `outpost_manifest` appears nowhere in `embarch-doc/embarch-core/`. `spec.md` §4's module
table lists 14 of the 15 modules.

Separately, `src/flash_backend.rs:2` and `src/hardware.rs:184` both cite "design.md §3 decision 48".
Core's decisions stop at 41, and the entry meant is **36** (`embarch-doc/embarch-core/decisions/flashing.md:25`,
and `spec.md:55` says 36). The stale `milestone-1.md` / `milestone-6.md` citations in the same files
name docs that were deleted (`embarch.md:114`).

`spec.md` §4 gains a row for `outpost_manifest` saying what it owns, in the one-line style of its
neighbours, so `spec.md` §2's "a manifest that does not verify costs the *names* in a trace"
invariant points at the module that implements it.

## Why now

`embarch.md` §3 makes `spec.md` "what is true now" for each sub-project. A 951-line module absent
from the module map, plus two references resolving to nothing, is the exact drift
`scripts/check-decision-refs.py` catches in docs and cannot see in source.

## Done when

- [ ] `spec.md` §4's table has one row per `mod` declared in `main.rs`, verified against that file.
- [ ] No `decision 48` remains in `embarch-core/src`; `flashing.md` 36 is what the two comments name.
- [ ] Every `milestone-N.md` citation in `embarch-core/src` either resolves or is replaced by the
      doc that absorbed it.
- [ ] `spec.md` stays inside its size cap.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
