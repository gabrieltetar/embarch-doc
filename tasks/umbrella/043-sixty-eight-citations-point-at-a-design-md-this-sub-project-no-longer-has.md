# 043 — 68 citations in the `embarch-umbrella` crate point at a `design.md` this sub-project no longer has

**State:** open
**Source:** found by the supervisor while landing `umbrella/035`, leg 060, 2026-09-09. The one line
`035` edited (`Cargo.toml`'s boundary comment) ended in `(design.md §1)`; fixing that one citation
in the fold turned up 67 more.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-umbrella/` holds `spec.md`, `open.md`, `decisions.md` and `decisions/` —
**there is no `design.md`**, and there has not been since the sub-project's docs were split. The
crate still cites it 68 times, almost all in the form `design.md §N.N decision M`:

| file | hits | | file | hits |
|---|---|---|---|---|
| `src/setup.rs` | 12 | | `src/main.rs` | 4 |
| `src/doctor.rs` | 11 | | `src/config.rs` | 4 |
| `src/init.rs` | 10 | | `src/deploy.rs` | 3 |
| `src/locate.rs` | 9 | | `src/state.rs` | 3 |
| `src/install.rs` | 6 | | `src/env.rs`, `src/manifest.rs`, `src/zephyr.rs` | 1 each |

(That accounts for 65 in `src/`; the remaining three are outside it — `Cargo.toml`'s was fixed in
`035`'s fold, so **re-count before starting** rather than trusting this table.)

Nothing catches it. `check-decision-refs.py` reads markdown, not Rust doc comments, and this crate
keeps `cargo doc` warnings out of its gate.

## This is the third instance of one class, and the earlier two teach it

- `study-designer/018` was filed for 290 occurrences in 23 files and **landed 522 lines across 32**.
  Expect more than a `src/` grep predicts.
- `api/052` is the same task for `embarch-api`'s 320 occurrences and is **still open** — check
  whether it has landed first, because whatever convention it settles on should be the one used here
  rather than a second one invented independently.
- **`api/031`'s fold found the failure mode that makes a mechanical sweep dangerous.** A citation
  stripped of its qualifier can land on a *real but wrong* decision: that unit's `probe_serial`
  comment cited "decision 9" meaning `embarch-core`'s, while `embarch-api`'s own decision 9 is
  unrelated — a citation that reads as authoritative and survives every check. **So resolve every
  `§N.N decision M` against the current `decisions/` index and confirm the decision it lands on is
  the one the comment is actually about, before rewriting it.** A `sed` over this is the wrong tool.

## Done when

- [ ] No occurrence of `design.md` remains in the `embarch-umbrella` repo, counted by grep over the
      whole tree and not only `src/`.
- [ ] Each rewritten citation names a file that exists **and** a decision whose subject matches what
      the comment claims — spot-check the substance, do not just re-point the path.
- [ ] Where a decision number is ambiguous across repos, the repo is named explicitly.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/umbrella-*` fragment.
