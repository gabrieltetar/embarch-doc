# 020 — `embarch-topology`'s `hardware` gate is drawn around the module rather than the machinery, so its one linked consumer hand-mirrors seven plain data types

**State:** done (half (a)) — leg 100, 2026-09-12. Leg 099's `ops.md` §4 window (`ts`
`1789230186.693679`, opened 10:23) was **completed, not restarted**: re-polled at 10:49 and again
after it closed at 10:53, no objection and no human message in `#embarch-fleet` at all. Half (a) —
the `wire` feature — ran as leg 100's fourth unit. **Half (b), retiring `embarch-core-client`'s
mirrors, is `tasks/suite/035`** and carries its own announcement window when it runs.

## Scoping done by leg 099 before it parked this — read it before starting

**This is bigger than one unit and should be split into two, and the first half is separable,
low-risk and useful on its own.** What I read:

- **The seven types sit at the TOP of files whose lower halves need `probe-rs`/`serialport`** —
  `EnrolledBoard` at `enrollment.rs:23` above 9 storage functions, `DetectedPort` at `port.rs:77`
  above `select`/`detect`/`enumerate`, `SignalLink`/`SignalDirection`/`Route` at `signal.rs:43,62,71`
  above `resolve_port` (which is the first thing in that file to touch `serialport`, at `:226`),
  `Alert` at `alert.rs:44`. That layout is good news: the seam is clean and near the top of each
  file.
- **`hardware/mod.rs` already `pub use`s all seven**, so a move behind it is invisible to
  `embarch-core`, the one consumer that enables `hardware`.
- **The cost is the doc comments, not the types.** Every one of these carries heavy rustdoc with
  `super::`-relative intra-doc links (`[`SignalLink`](super::signal::SignalLink)`,
  `[`super::validate`]`, `[`DevBenchPort`]`, …). Moving the types to a top-level `wire` module means
  rewriting those paths, which turns a mechanical move into a large non-verbatim diff in a crate
  four other repos build against. **Budget for that, or keep the types in place and change only the
  gating.**
- **The `embarch-api` half is the risky half and is a unit of its own.** The mirrors are not plain
  duplicates: they are `*Response` types with their own contracts, and `client.rs:1875-2126` is a
  block of deliberate **mirror-pinning tests** (`api/032`'s work) that exist to catch exactly the
  drift this task wants to remove structurally. Deleting mirrors means deleting those tests, and
  `embarch-core-client` is a shipped crate, so this changes a public API. `client.rs` is 2,357 lines.

**Suggested split.** (a) `topology`: add a types-only feature (serde, no `probe-rs`/`serialport`)
that `hardware` implies, give `DetectedPort` a `Deserialize`, and stop `serde` being
`hardware`-optional — verifiable on its own by `cargo tree -e normal` showing no new `probe-rs`
anywhere. (b) `api`: switch `embarch-core-client` onto those types and retire the mirrors and their
pinning tests. (a) is pure enablement and unblocks the `suite-one-machine-data-root` drop as well;
(b) is where the judgement is. If the window is honoured and only one unit is available, **do (a)**.
**Source:** suite review pass 2026-09-06, dimensions 4 and 1 (two hunters, one finding). Code-confirmed.
**Scope:** suite
**Hardware:** none
**Owner:** no

## What

`embarch-topology/src/lib.rs:36-37` gates the whole module —
`#[cfg(feature = "hardware")] pub mod hardware;` — and `Cargo.toml:62-66` defines
`hardware = ["dep:probe-rs", "dep:serialport", "dep:serde", "dep:toml", "dep:serde_json"]`.
**`serde` is gated together with `probe-rs`.** The types behind that gate need neither:
`EnrolledBoard` (`src/hardware/enrollment.rs:22`), `Alert` (`alert.rs:44`), `SignalLink`,
`Route`, `SignalDirection` (`signal.rs:43,61,70`) and `DetectedPort` (`port.rs:76`) are pure
serde structs; `alert.rs` imports only `anyhow`, `serde`, `std::io`, and `serialport` is first
reached at `signal.rs:226` inside a resolution function. It is the **functions** that need
`probe-rs`.

The consequence: `embarch-api/crates/embarch-core-client/src/client.rs` hand-mirrors all seven at
`:273, :293, :320, :333, :346, :365, :501` — and it **already links `embarch-topology`**
(`crates/embarch-core-client/Cargo.toml`), so the real types are one `use` away and unreachable.
The comments say so plainly: `:269` — *"mirrors `embarch_topology::hardware::Alert`'s fields
**without depending on that crate's `hardware` feature** (this crate deliberately never links
`probe-rs`/`serialport`)"* — and `:1589` — *"[`SignalLink`] is a hand-maintained mirror of
`embarch_topology::hardware::SignalLink`, and no crate in the suite can [typecheck it]."*
`embarch-core/src/api.rs:628,743,810,831,971` serves the real types verbatim, so Core and its one
client describe the same JSON from two hand-kept definitions.

The rule that forces this — *never link `probe-rs`/`serialport` outside Core* — is right and is
not what is wrong. What is wrong is that honouring it currently costs seven duplicated wire types
with the compiler unable to see either side.

Candidate direction: a types-only feature (serde, no `probe-rs`/`serialport`) that `hardware`
implies, so the facts Core serves are reachable without the machinery that produces them. Small
known follow-ons: `DetectedPort` needs `Deserialize` added, and `serde` must stop being
`hardware`-optional.

## Why now

Adding or renaming a field on an enrolled board, an alert, a detected port or a signal route is
two edits in two repos today, with a JSON literal per side as the only link — and
`EnrolledBoardResponse` **has already dropped `link_port_interface`**, which is what
`tasks/api/032` exists to paper over. Nothing catches drift: the per-repo gates compile each side
alone, and both sides typecheck perfectly while disagreeing. `embarch-topology/decisions/crate.md`
decision 4 asserts this is already solved — *"the mirrored-copy CI diff job becomes obsolete:
there is nothing left to mirror once everyone links the same crate"* — and decision 8 says *"there
is no way for the two to disagree, since there is only one of them."* Both are false as written.

## Done when

- [ ] `embarch-core-client` uses `embarch-topology`'s own types for enrolled boards, alerts,
      signal links, routes and detected ports, without linking `probe-rs` or `serialport`.
- [ ] `cargo tree -e normal` still shows no `probe-rs`/`serialport` in `embarch-api`,
      `embarch-ui` or `embarch-umbrella`.
- [ ] No hand-maintained mirror of a `embarch_topology::hardware` type remains, or the one that
      does says why.
- [ ] `decisions/crate.md` decisions 4 and 8 are true as written, or amended.
- [ ] Gate green; `changelog.d/` fragments for both repos.

**Read before dispatching:** this makes `tasks/api/032`'s mirror-pinning work unnecessary rather
than duplicating it. If both are to be worked, this lands first and `api/032` shrinks to the
`link_port_interface` field itself. It also unblocks the `suite-one-machine-data-root…` drop,
which needs `paths.rs` reachable without the `hardware` feature.
