# 226 — `embarch-core-client` takes Core's wire types from Core's wire crate

**State:** open — `core/194` landed the crate (`embarch-core/crates/embarch-core-wire`, core decision 164, `embarch-core` `a7cec14`)
**Source:** EMB-295 — Core's wire types are hand-mirrored in core-client with uneven drift guards
**Issue:** EMB-295
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`crates/embarch-core-client` re-declares five of Core's wire families:
`StudyEvent` (`src/study_events.rs`), the dev-bench hello answer
(`HelloAckResponse`, `src/client.rs`), the outpost load answer (`LoadAnswer`,
`LoadSummary`, `LoadSubject`, `src/client.rs`) and the `LEASE_GATED` table
(`src/lease_gate.rs`). `tasks/core/194` moves Core's own definitions into
`embarch-core/crates/embarch-core-wire`.

When this is done, `embarch-core-client` path-depends on that crate and its
mirrors are gone: the client uses Core's definitions, re-exported under the
names it exports today so `embarch-umbrella` and `embarch-ui` build unchanged.
What is the client's alone stays here (`render_hello_ack`, any caller-side
field; core/194's decision says which). The `lease_gate.rs` test that reads
`../../../embarch-core/src/lease.rs` and passes when it is absent is deleted,
since there is nothing left to compare.

`decisions/study-events.md` (decision 49) records the outcome: the mirror it
deferred is lifted, and where the one definition lives. Amend any other
decision that names a mirror in place.

**Not yours:** every other repo, `embarch-core` included. You never touch
hardware.

## Why now

Decision 49 deferred this as cross-repo scope, not on merit; EMB-295's other
half lands first.

## Where to look

- `crates/embarch-core-client/Cargo.toml`, `src/study_events.rs`,
  `src/client.rs`, `src/lease_gate.rs`
- `embarch-core/crates/embarch-core-wire` (read only), and core decision 164
  (`embarch-core/decisions/wire.md`), whose last paragraphs say what the
  client keeps. Two things it settled differently from this file's first
  draft: the crate depends on `serde`, `serde_json` and
  `embarch-study-designer` (feature `alloc`), not `serde` alone; and the
  shared `StudyEvent` is strict, with no unknown-variant fallback, because the
  client's frame decoder (`StudyStreamItem::Unrecognized`) already keeps an
  unknown frame's data. **Decide and write down** the older-Core tolerance:
  the client's mirrors made `StepCompleted`'s three stamps, `core_rx_utc_ms`
  on `SampleBatch`, `GattTranscript` and `StreamText`, and four newer hello
  fields `Option` with `#[serde(default)]`; the shared types require them, so
  an older Core's frame would read as `Unrecognized`. Either accept that and
  say so in decision 49, or keep a lenient client type for exactly those.
- **Dispatch setup:** the path dependency is
  `../../../embarch-core/crates/embarch-core-wire`, so the api worktree's parent
  needs an `embarch-core` link to the main checkout. So will every later
  `embarch-ui` and `embarch-umbrella` worktree, which build this crate.
- `embarch-doc/embarch-api/decisions/study-events.md`
- **Size:** `decisions/client-crate.md` is in reserve (456 B left,
  `tasks/api/222`); if this changes what it says, compact it in the same unit.

## Done when

- [ ] The five families come from `embarch-core-wire`; the client's copies and
      the skipping `lease_gate.rs` test are gone.
- [ ] No public name the client exports today is gone (the supervisor builds
      `embarch-umbrella` and `embarch-ui` against the branch at landing).
- [ ] Decision 49 records the outcome.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`, `cargo
      clippy --workspace --all-targets -- -D warnings`); `changelog.d/`
      fragment.
