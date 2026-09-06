# Stop routing unlisted nRF54L chip names to the classic `FICR.DEVICEID` address

**State:** open
**Source:** owner's repo survey, 2026-09-06 — the crate's own "an unrecognized chip is a named error, never a guess" has a hole
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`src/hardware/hardware_id.rs:396-400` matches four exact nRF54L names first, then falls through to
`c.starts_with("nRF5")` → the classic `0x1000_0060` pair. So `nRF54L47`, `nRF54LM10`, or a lowercase
`nrf54l15_cpuapp` reads the wrong registers rather than `FICR.INFO.DEVICEID`. `:493-497` duplicates
that same arm set in `is_nordic_deviceid_chip`, so such a chip also gets the Nordic self-report
projection applied to that value. The suite already accepts exactly those spellings on the flash
path (`embarch-core/src/flash_backend.rs:512`, `:524`).

One classifier should decide a chip's family, with both `read` and the self-report relation derived
from it, so the two cannot disagree. Any `nRF54L*` / `nRF54H*` name reaches the `INFO.DEVICEID` arm
or a named unrecognized-chip error — never the classic address.

**Read-only, host-side:** this is register *selection* logic and its unit tests. Nothing here needs
a probe.

## Why now

`hardware_id.rs:372-373` states the rule — "an unrecognized chip is a named error, never a guess" —
and topology decision 21 rests on the Nordic arm being derived for exactly the set `read` handles.
Today a one-character-different chip name silently leaves that set.

## Done when

- [ ] A single `fn` classifies a chip name into a family, and `read` plus `is_nordic_deviceid_chip`
      both call it.
- [ ] Tests cover `nRF54L47`, a lowercase/suffixed nRF54L spelling, and `nRF52840`, asserting which
      register pair each selects, and that an unknown chip is still the named error.
- [ ] `unrecognized_chip_is_a_named_error_not_a_guess` (`:723-731`) asserts against the real
      classifier instead of re-implementing the match inline.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
