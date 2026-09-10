# `outpost_manifest.rs` is undocumented, and two source comments cite a Core decision that does not exist

**State:** done (agent/core/008-outpost-manifest-module, 2026-09-10)
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

- [x] `spec.md` §4's table has one row per `mod` declared in `main.rs`, verified against that file.
      14 `mod` declarations enumerated from `main.rs`; `outpost_manifest` was the only one missing,
      confirmed by diff against the table. New row added.
- [x] No `decision 48` remains in `embarch-core/src`; `flashing.md` 36 is what the two comments name.
      Verified against `decisions/flashing.md:25` (the task's number was right); both comments now
      cite bare `decision 36`, the api/052 same-repo convention.
- [x] Every `milestone-N.md` citation in `embarch-core/src` either resolves or is replaced by the
      doc that absorbed it. Five citations found (not two): four to the deleted
      `embarch-ui/milestone-1.md` (`logs.rs` x2, `api.rs` x2), one to the deleted
      `embarch-umbrella/milestone-6.md` (`service.rs`). Neither file exists any more — both were
      folded and deleted in `6f22dd6`/`b74d29f`. The `embarch-ui` ones now name the milestone
      (`embarch-ui milestone 1`), the suite's own established convention for the 122 references the
      original fold commit converted the same way (`embarch.md`'s "deleted, not indexed" note). The
      `embarch-umbrella` one cited content that the fold commit's own message says moved verbatim
      into `embarch-core/decisions.md` decision 3 (verified: `decisions/platform.md` §3) — cited as
      bare `decision 3`.
- [x] `spec.md` stays inside its size cap. 8,212 of 10,240 B.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`/`test`/`clippy --all-targets
      -- -D warnings` clean in the code worktree; `scripts/check-docs.py` all 11 checks green in the
      doc worktree; both `check-ownership.py` invocations OK. Native Windows build not attempted —
      standing debt, needs the owner's machine (protocol.md's own note on this).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. `spec.md` updated; `decisions.md`/`open.md`
      untouched — nothing here answers or invalidates an existing entry in either, and `open.md` is
      at 94.0% per leg 063's dispatch note, so nothing was added to it. `changelog.d/` fragment
      dropped. No `status.d/` fragment: no suite-level doc's facts changed.
