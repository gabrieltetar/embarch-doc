# Stop routing unlisted nRF54L chip names to the classic `FICR.DEVICEID` address

**State:** claimed by agent/topology/007-chip-family-classifier, 2026-09-07 17:31
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

## Doc-size reserve for `topology` — supervisor, leg 040

`scripts/check-doc-size.py --pressure` at this leg's start puts one `topology` file in reserve:

- `embarch-topology/open.md` — **4322/5120 B, 798 B left** (84.4%), filed against
  `tasks/topology/014-compact-topology.md`, which is **open** (not blocked), so the debt is
  already scheduled and you should not file a second one for this file.

`embarch-topology/decisions/*` and `spec.md` are **not** in reserve, so a numbered decision here
has room. **If your work pushes a different file into reserve, or leaves one there that nothing has
filed, file `tasks/topology/<NNN>-compact-topology.md` in the same commit** (`tasks/README.md` has
the shape; the path is `tasks/topology/`, never `tasks/doc/`) — recording the debt, not paying it.

## Done when

- [x] A single `fn` classifies a chip name into a family, and `read` plus `is_nordic_deviceid_chip`
      both call it. (`classify_chip` in `src/hardware/hardware_id.rs`.)
- [x] Tests cover `nRF54L47`, a lowercase/suffixed nRF54L spelling, and `nRF52840`, asserting which
      register pair each selects, and that an unknown chip is still the named error. (Also added
      `nRF54LM10` and an `nRF54H20` case, since the task's own wording covers `nRF54H*` too.)
- [x] `unrecognized_chip_is_a_named_error_not_a_guess` (`:723-731`) asserts against the real
      classifier instead of re-implementing the match inline.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), including
      `cargo test --no-default-features --features hardware`.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. (Decision 25 added to
      `decisions/validation.md`; no `status.d/` fragment — nothing suite-level went false; `spec.md`
      and `open.md` needed no change, since neither names the exact-match set this fixed. An
      `inbox/` drop records the option to unify this crate's classifier with
      `embarch-core/src/flash_backend.rs`'s own nRF54L matcher, which is `core`'s call, not
      `topology`'s.)

## Note

`embarch-core/src/flash_backend.rs:103-109` accepts a broader, lowercase-normalized `nrf54l`
spelling set (no `nrf54h` arm) for a related but separate decision (needs-vendor-tool). Not
unified here — that would touch `embarch-core`, outside this task's scope — see the `inbox/` drop
this task filed.
