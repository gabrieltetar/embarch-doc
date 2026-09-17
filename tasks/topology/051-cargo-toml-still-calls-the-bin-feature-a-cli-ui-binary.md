# 051 — `Cargo.toml`'s `bin` feature comment still says "CLI/UI binary"; the UI was retired in August

**State:** done
**Source:** `topology/050`'s worker, 2026-09-16, which found and fixed the identical stale wording in
`src/hardware/validate.rs` and correctly declined to widen — `Cargo.toml:48` cites no decision
number, so it was outside a plural-citation sweep's mandate. Filed by the supervisor at that unit's
fold rather than left in a worker's report, because a finding nobody files is a finding nobody acts
on.
**Scope:** topology
**Hardware:** none — one comment in `Cargo.toml`. Nothing is built for a board, no probe, no live
Core, no deploy, no study.
**Owner:** no

## What

`embarch-topology/Cargo.toml:48` reads:

> `# \`bin\` (this crate's own CLI/UI binary) — never by embarch-api/ ...`

There is no UI. `bin/ui.rs` and its `Ui` subcommand were **retired outright on 2026-08-24**
(commit `7d13781`, "Remove bin/ui.rs, replaced by embarch-ui"), recorded as `embarch-topology`
decision 5 in `decisions/alerts.md` — *"The 413-line UI binary is deleted along with its
subcommand"*, and *"the HTTP dependencies went with it, since nothing left under that feature
serves HTTP"*. `embarch-ui`'s Topology tab covers the same ground now, over Core's HTTP API, and
never links this crate at all.

So the comment describes a feature gate as covering two binaries when it covers one, in the very
file whose dependency list was pruned *because* the second one went away.

Fix the wording the way `topology/050` fixed `src/hardware/validate.rs`: say what the `bin`
feature actually gates today. Check whether "CLI" alone is accurate for what survives before
writing it — `topology/050` made the same call and its reviewer was asked to check it, so read
that unit's entry in `../../embarch-fleet/supervisor-log.md` first rather than re-deriving.

## Why now

This is the second site of one stale sentence. `topology/050` fixed the first and left this one on
`main` with its reason recorded; the reason was right for that unit and is not a reason to leave it
standing. It is also a sentence about *what the dependency footprint is for*, sitting directly above
the dependency list that was cut when the UI went — the one place a reader checking "why is this
gated?" will land.

## Done when

- [x] `Cargo.toml:48`'s comment no longer claims a UI binary exists, and describes the `bin`
      feature's actual surface. Fixed to "own CLI binary" plus a one-line pointer to decision 5's
      2026-08-24 retirement, matching `topology/050`'s treatment of `validate.rs`.
- [x] A sweep of the rest of `embarch-topology` for the same stale `CLI/UI` phrasing — this is now
      two instances of one sentence, so check whether there is a third before closing. Grepped
      `CLI/?UI|CLI and UI|UI and CLI|UI binary|its own UI` case-insensitively across `.rs`/`.toml`/
      `.md`: zero remaining hits after this fix. This was the second and last site.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`,
      `cargo test` (including `--features hardware`), `cargo clippy --all-targets -- -D warnings`
      in `embarch-topology`, and `check-docs.py` in `embarch-doc`. All green; `cargo test --features
      hardware` 80 passing, matching `topology/050`'s baseline.
- [x] `changelog.d/` fragment dropped. No decision is created or amended: decision 5 already says
      the right thing.
