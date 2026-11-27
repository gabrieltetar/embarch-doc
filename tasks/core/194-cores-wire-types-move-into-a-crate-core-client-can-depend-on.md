# 194 — Core's wire types move into a crate `embarch-core-client` can depend on

**State:** open
**Source:** EMB-295 — Core's wire types are hand-mirrored in core-client with uneven drift guards
**Issue:** EMB-295
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-api/crates/embarch-core-client` re-declares five of Core's wire
families by hand: `StudyEvent` (`src/study.rs`), `HelloAckInfo`
(`src/study.rs`), the outpost load answer (`LoadAnswer`, `LoadSummary`,
`LoadSubject` in `src/outpost_load.rs`), and the `LEASE_GATED` route table
(`src/lease.rs`). The guards differ, and one test skips silently when this repo
is absent. Today they match.

**The home is decided (supervisor, for EMB-295):** a small crate in this repo,
`crates/embarch-core-wire`, depending on `serde` alone, the way
`embarch-desk/crates/embarch-user-unit` (desk decision 94) and
`embarch-core-client` itself are built. The server owns its wire, so the one
definition lives beside the server. *Rejected:* `embarch-topology`'s `wire`
feature (topology carries the bench's hardware facts, and a run's events, a
lease table and a dev-bench handshake answer are not those); a `wire` feature
of `embarch-core-client` that Core depends on (Core would build against a
crate in one of its clients' repos).

When this is done, those five families are defined once, in that crate, and
Core uses them from there; the JSON on the wire is byte-for-byte what it is
today, pinned by a test in the crate for each family. Make the repo root a
cargo workspace with the crate as a member and the root package as a default
member, so a plain `cargo build`, `test` and `clippy` reach both, as
`embarch-desk` did; the crate also builds alone by `--manifest-path`.

`embarch-core-client`'s `StudyEvent` mirror has an `Unrecognized` fallback so
an older client reads a newer Core's event without failing. The shared type
needs the same behaviour for a client, while Core never writes it: decide how
(a `#[serde(other)]` variant, or another shape) and write why. Anything a
client adds that is not wire (a renderer, a caller-side field) stays in the
client; say in this file what `tasks/api/226` will need to keep.

Record it as a new core decision (where the wire types live, what the crate
may depend on, and that a wire change is now one edit), and name the crate in
`interfaces/modules.md`.

**Not yours:** every other repo, `embarch-api` included: `tasks/api/226`
switches the client over once this lands. You never touch hardware.

## Why now

`embarch-api` decision 49 (`decisions/study-events.md`) deferred lifting the
mirror as cross-repo scope, not on merit, and the suite's reversals page names
this shape (shape 4). Topology decision 31 retired six mirrors the same way.

## Where to look

- `src/study.rs` (`StudyEvent`, `HelloAckInfo`), `src/outpost_load.rs`,
  `src/lease.rs` (`LEASE_GATED`), `Cargo.toml`
- `embarch-api/crates/embarch-core-client/src/study_events.rs`,
  `src/client.rs`, `src/lease_gate.rs` (read only): the mirrors, and what a
  client parses
- `embarch-desk/Cargo.toml` and `crates/embarch-user-unit/Cargo.toml` (read
  only): the workspace shape to copy
- **Builds from outside:** `embarch-umbrella`'s `deploy-core` and the release
  workflow build this repo from its root; check that a root `cargo build
  --release` still produces the same binary at the same path, and say so.
- **Size:** `decisions/platform.md` (733 B left) and `spec.md` (1,158 B left)
  are in reserve under `tasks/core/186`; put the decision in the topic file it
  belongs to, not in either.

## Done when

- [ ] The five families are defined once, in `crates/embarch-core-wire`, and
      Core uses them; nothing Core sends changed, and a test per family pins
      its JSON.
- [ ] The crate depends on `serde` alone and builds by `--manifest-path`.
- [ ] A new core decision says where Core's wire lives; `interfaces/modules.md`
      names the crate.
- [ ] Gate green (`cargo build --workspace`, `cargo test --workspace`, `cargo
      clippy --workspace --all-targets -- -D warnings`); `changelog.d/`
      fragment.
