# 020 — `embarch-topology`'s `hardware` gate is drawn around the module rather than the machinery, so its one linked consumer hand-mirrors seven plain data types

**State:** open — announced 2026-09-12 10:23 by leg 099, `ops.md` §4 window `ts` `1789230186.693679`.
No objection as of that leg's last poll. **The next leg completes this window rather than restarting
it**: if 30 minutes have passed since that `ts` and `fleet-read.py --thread 1789230186.693679` shows
no objection, run it.
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
