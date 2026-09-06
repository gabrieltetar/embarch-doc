# Remove every reference to `design.md`, and two comments asserting a retired live push

**State:** open
**Source:** owner's repo survey, 2026-09-06 — commit `9a56959` fixed `CLAUDE.md` for this and stopped there
**Scope:** topology
**Hardware:** none
**Owner:** no

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
