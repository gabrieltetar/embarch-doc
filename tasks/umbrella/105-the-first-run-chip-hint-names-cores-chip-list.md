# 105 — The first-run chip hint names Core's chip-list

**State:** done — both strings now name embarch-core chip-list
**Source:** suite review audit, 2026-11-23: umbrella still sends a newcomer to a second toolchain install that Core decision 34 replaced
**Issue:** EMB-310
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Two first-run strings in `embarch-umbrella` tell a newcomer to run
`cargo install probe-rs-tools && probe-rs chip list | grep -i <your soc>` to
find their chip's name: the fix line `embarch doctor` prints (`src/doctor.rs`,
near line 1412) and the comment `embarch init` writes into the `embarch.toml`
it scaffolds (`src/init.rs`, near line 543). Core ships `embarch-core
chip-list <soc-substring>` for exactly this (`ChipList` in
`embarch-core/src/main.rs`; `embarch-core` decision 12 in
`decisions/chip-mapping.md`, and `suite/user-guide.md` already point at it),
so the detour asks for a second toolchain install on the first-run path for
nothing.

When this is done both strings name `embarch-core chip-list <soc-substring>`,
and neither mentions `probe-rs-tools`. Check the exact argument shape against
Core's `ChipList` before writing it; do not change Core.

## Why now

The doctor fix line and the scaffolded config are what a newcomer reads first.
`grep chip-list src` in umbrella finds nothing today.

**Burndown leg: no new numbered decision.** None should be needed. Any test
that pins the old string changes with it. Doc-size reserve: no umbrella file
is in reserve.

## Done when

- [x] Neither the doctor fix line nor the scaffolded config mentions
      `probe-rs-tools`; both name `embarch-core chip-list`.
- [x] `spec.md` or `interfaces/` updated only where they quote either string.
- [x] `changelog.d/` fragment dropped.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
