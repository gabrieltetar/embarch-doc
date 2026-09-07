# Remove every reference to `design.md`, and two comments asserting a retired live push

**State:** claimed by agent/topology/005-seventy-four-references-to-a-deleted-design-md, 2026-09-07 09:44
**Source:** owner's repo survey, 2026-09-06 — commit `9a56959` fixed `CLAUDE.md` for this and stopped there
**Scope:** topology
**Hardware:** none
**Owner:** no

## Doc-size reserve — supervisor, leg start 2026-09-07 09:44

**No `embarch-topology` doc is in reserve.** `check-doc-size.py --pressure` lists twelve files
across the suite and none of yours; `spec.md` came off its hard cap two legs ago and has room.
So you owe no compaction task **unless your own edits push a `embarch-topology/*` file into the
last 10% of its cap** — in which case file `tasks/topology/<NNN>-compact-topology.md` in the same
commit, per `tasks/README.md`.

**One suite-wide hazard applies to you: `suite/features.md` has 60 bytes of headroom** (20,420 of
20,480 B). It is *assembled* from `features.d/` fragments, so **a new `features.d/` fragment will
push it over its cap and turn the fold red.** This unit is comment-and-doc corrections and should
not be shipping a feature row at all — if you conclude it warrants one, **write the row's text into
this task file and do not create the fragment**, and say so in your report.

## What

74 occurrences of `design.md` remain across `embarch-topology` — `README.md:8` still calls it
"Design doc (source of truth)", `Cargo.toml`'s package `description` names it, `src/lib.rs:4`, and
`.github/workflows/release.yml:2`. Decision numbers survive file moves by design, so the mechanical
form is `design.md §3 decision N` → `embarch-topology decision N`; a reference to a *section* needs a
small judgement about which file now holds that content, and must not be `sed`'d blind.

**Two of those comments also assert retired mechanisms as live, and that is the half with real
evidence behind it.** `src/hardware/mod.rs:159` says a mismatch "live-pushes it to
`embarch-topology`'s UI if one is running", and `Cargo.toml:40-41` / `:58` describe `alert.rs`'s
loopback push — which `src/hardware/alert.rs:6-16` records as **deleted by decision 19**.
`release.yml`'s header still describes the retired UI binary.

Comment-only: `cargo test` and `clippy` should be unchanged.

## Why now

`decisions.md` states that decision numbers survive file moves precisely so references keep
resolving — but `design.md §3 decision 5` resolves to nothing. And `mod.rs:159` is exactly the
"working-looking code whose destination no longer exists" that decision 19 exists to have removed.

## Done when

- [ ] `grep -rn "design\.md" .` over the repo (excluding `target/`) returns nothing.
- [ ] `README.md`, `Cargo.toml`'s description and `src/lib.rs`'s header point at
      `spec.md`/`decisions.md`/`open.md`.
- [ ] The live-push claims in `src/hardware/mod.rs` and `Cargo.toml` are corrected, and
      `release.yml`'s header no longer describes the retired web UI.
- [ ] No reference to a deleted `milestone-N.md` remains without saying it is recoverable from git.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
