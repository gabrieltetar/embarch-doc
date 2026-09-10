# `outpost_manifest.rs` is undocumented, and two source comments cite a Core decision that does not exist

**State:** claimed by agent/core/008-outpost-manifest-module, 2026-09-10 14:09
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

## Dispatch note from the supervisor, leg 063

**Doc-size reserve in your scope.** `embarch-core/open.md` is at **94.0%** — 4,813 of 5,120 B,
**307 B of headroom** — and its compaction is already filed as `tasks/core/022-compact-core.md`
(`open`, due 2026-09-26), so you do **not** file a second one for that file. Write your `open.md`
entry tersely or, better, *close* an entry this unit answers rather than adding one. If you push any
other `embarch-core` doc into its last 10%, file `tasks/core/<next NNN>-compact-core.md` in the same
commit.

`embarch-core/spec.md` has room: `core/030` (2026-09-09) lifted §5's constants table out verbatim
into the new `embarch-core/interfaces/constants.md`, taking `spec.md` from 9,148 B to **7,977 B**.
So §4's new module row is affordable — but note that the split means **`interfaces.md`'s table now
has rows for `interfaces/` files**, and a module row belongs in `spec.md` §4, not there.

**Two cautions on the citation half.** The task says the decision meant is 36; verify that against
`embarch-doc/embarch-core/decisions/flashing.md` yourself before rewriting either comment — a
citation asserted confidently and wrongly is the defect this unit exists to remove, and `api/052`
found six of exactly that shape by trusting a filed number. Use the citation convention `api/052`
settled: a same-repo citation reads bare `decision 36` with no `design.md` and no section number; a
cross-repo one names the repo as a plain qualifier, `` `embarch-topology` decision 23 ``.

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
