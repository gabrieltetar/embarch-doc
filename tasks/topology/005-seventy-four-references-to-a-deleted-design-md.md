# Remove every reference to `design.md`, and two comments asserting a retired live push

**State:** done
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

- [x] `grep -rn "design\.md" .` over the repo (excluding `target/`) returns nothing.
- [x] `README.md`, `Cargo.toml`'s description and `src/lib.rs`'s header point at
      `spec.md`/`decisions.md`/`open.md`.
- [x] The live-push claims in `src/hardware/mod.rs` and `Cargo.toml` are corrected, and
      `release.yml`'s header no longer describes the retired web UI.
- [x] No reference to a deleted `milestone-N.md` remains without saying it is recoverable from git.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Report

All 74 `design.md` occurrences removed. Mechanical rewrite per DOC-CONVENTIONS.md: own-repo
decision citations became bare `decision N`; cross-repo citations became `embarch-<repo>
decision N`. Section-only citations (not a decision number) were judged individually — mapped to
`spec.md`, `open.md`, or (for two cross-repo cases: `embarch-study-designer`'s `StreamSource::Signal`
and `embarch-outpost`'s TX-only claim) verified against those repos' own current docs before citing
them by decision number / file name instead.

Two decision-number citations in the original comments were missing their cross-repo prefix
(`src/hardware/validate.rs`'s `POST /validate` note cited bare "decision 28", which is
`embarch-core` decision 28, not one of topology's own 1-22; `src/hardware/enrollment.rs`'s port-
migration note cited `embarch-core/design.md decision 21`, which does resolve — `embarch-core`
decision 21's body covers exactly the dedicated-UART port migration described). Both verified
against `embarch-core/decisions.md` and its decision files before citing; no decision number failed
to resolve.

The two live-push corrections: `src/hardware/mod.rs`'s `validate_serial` doc comment no longer
claims a live push to a running UI (decision 19 retired it; the durable log plus `embarch-ui`'s poll
is now what's described). `Cargo.toml`'s two comments justifying the `tokio`/`serde_json` dependency
shape no longer describe `alert.rs`'s loopback push as current — both now say it's retired
(decision 19) while keeping the (still-true) rationale for why those crates are needed anyway.
`release.yml`'s header no longer says the binary serves a local web UI.

Every `embarch-ui/milestone-1.md §4.9` citation (a doc that no longer exists in `embarch-ui`)
replaced with `decision 5`, which is topology's own record of the same retirement and carries the
full history milestone-1.md used to.

Comment/doc-only change: `cargo build`, `cargo test` (60 tests), and
`cargo clippy --all-targets --all-features -- -D warnings` all clean, no behavior changed.

No `features.d/` fragment created (per the doc-size reserve note above) — this unit doesn't warrant
a feature row; it's comment/citation hygiene, not a feature.

No `status.d/` fragment: nothing suite-level was made false by this change — it corrects stale
citations and two doc-comments that had drifted from an already-landed decision (19), it doesn't
change any current truth.
