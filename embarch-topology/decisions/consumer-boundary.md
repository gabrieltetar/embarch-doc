# embarch-topology decisions: Consumer boundary

**Status:** active, 2026-09-12.

What a consumer may link, and what the crate owes a consumer that cannot link all of it.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 4 — Both software and hardware topology, in one pass, not hardware-first

The board-identity gate, its storage, the dev-bench port heuristic, **and** the software-class detection then mirrored between `embarch-api` and `embarch-umbrella` all move here as the sole implementation. **The mirrored-copy CI diff job becomes obsolete: there is nothing left to mirror once everyone links the same crate.**

**Qualified 2026-09-08** (`tasks/topology/020`, from `api/038`'s finding): "the sole implementation" and "nothing left to mirror" describe the crate's own boundary, not its callers. `embarch-api/crates/embarch-core-client` already linked this crate and still ran a second, narrower predicate (`token_discovery::is_wsl2`) beside the call it never made to `detect_wsl2` — closed by `api/038` (`embarch-api` decision 62, `861f30f`), which made it delegate. Linking the crate stops a mirrored *copy* of its own logic; it does not stop a caller writing an unrelated second predicate next to a call it never makes. A third copy, `embarch-umbrella/src/token.rs`, closed the same way: `umbrella/036` (2026-09-08, `e1a5e7c`/`444f84d`) replaced it with a direct call to `embarch_core_client::token_discovery::resolve_token`. No live mirror of *this crate's logic* remains now — never the point; nothing here can cheaply detect the next one (see `open.md`).

**Qualified again 2026-09-12** (`suite/020`, resolved by `suite/035` the same day): "nothing left to mirror once everyone links the same crate" was false in a second way, about **data** rather than logic. `embarch-core-client` linked this crate and still hand-mirrored seven of its wire types, because until decision 31 those types were reachable only through the `hardware` feature — which that crate must never enable. **Linking a crate is not sufficient when what you need is behind a gate you are forbidden to open.** Decision 31 removed the gate, `suite/035` removed the mirrors, and the sentence is true as written now (`embarch-api` decision 72).

### 8 — One implementation, multiple call sites — not two independent layers

A human running the CLI **sees precisely the validation Core enforces live, because it *is* that validation — there is no way for the two to disagree, since there is only one of them.** Concretely: whatever port or probe an operation is about to use, one shared `validate()` confirms the device is currently enumerated and still matches the identity recorded for its role, and **returns a specific error naming what is stale** if it does not.

**Reversed** from an earlier framing that described an ahead-of-time check and Core's live re-check as **two independent, separately-reasoned mechanisms that happened to agree.** They are not independent once both are calls into the same crate.

**Qualified 2026-09-08** (`tasks/topology/020`): "there is no way for the two to disagree, since there is only one of them" holds only inside the crate's own boundary — a statement about the crate, not about whether a caller actually calls it. `api/038` found `embarch-api`'s own client still ran a second, narrower WSL2 predicate beside a call it never made to this crate's `detect_wsl2`, and closed that instance by making it delegate. Whether anything should detect a caller declining to call the crate at all: see `open.md`.

**Qualified again 2026-09-12** (`tasks/suite/020`): the same correction decision 4 takes above applies here, for data instead of logic. `embarch-core`'s `api.rs` serves `EnrolledBoard`, `Alert`, `DetectedPort` and `SignalLink` verbatim, and `embarch-core-client` describes the same JSON from its own hand-kept definitions — so "there is no way for the two to disagree" was false for every one of those shapes, and both sides typecheck perfectly while disagreeing (`EnrolledBoardResponse` has already silently dropped `link_port_interface`). Decision 31 made the real types reachable without `probe-rs` and `suite/035` landed the switch-over on 2026-09-12, so **the sentence holds now**: one type, named by both sides, the compiler keeping them equal (`embarch-api` decision 72). What it still does not cover is a Core *already deployed*, which is why that crate keeps its pinned JSON literals.

**A real gap this surfaced:** the live-identity recheck covered only JTAG-capable roles. **The dev-bench runtime *link* had no equivalent live check** — which is what absorbing that logic had to close here rather than leave behind in Core.

### 31 — The `hardware` gate is drawn around the machinery, not around the module: a `wire` feature carries the types alone

**Decided 2026-09-12** (`tasks/suite/020`, from the 2026-09-06 suite review pass, dimensions 1 and 4).

`serde` used to be listed under the `hardware` feature alongside `probe-rs` and `serialport`, and `lib.rs` gated the whole `hardware` module on it. The types behind that gate need neither: `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route` and `SignalDirection` are plain serde data — the facts `embarch-core` serves over HTTP — while it is the **functions** below them in the same files that read a probe, enumerate a serial port or write `enrollment.toml`.

So the gate now names the machinery rather than the module. A new `wire` feature turns on `serde` and nothing else; `hardware` implies it, so `embarch-core` is unchanged. Under `wire` alone the `hardware` module compiles to its types, and every function, storage path and probe call in it is `#[cfg(feature = "hardware")]`-ed out. `cargo tree -e normal --no-default-features --features wire` is `anyhow`, `serde`, `tracing` — no `probe-rs`, no `serialport`, no C toolchain.

**The rule this does not touch, and must not:** nothing outside `embarch-core` links `probe-rs`/`serialport`. That rule is right. What it was costing was seven hand-mirrored wire types in `embarch-api/crates/embarch-core-client`, each with a comment explaining that the real type was unreachable — two definitions of one JSON shape, in two repos, with the compiler unable to compare them. Honouring the rule should not require duplicating the data it is drawn around.

**One type changed shape to make this possible.** `DetectedPort::detected_by` was `&'static str` and is now `String`: a borrowed-static field cannot implement `Deserialize`, and a wire type a client cannot deserialize is not a wire type. Every value it holds is still one of the same four constants.

**Types in place, not moved.** Moving the six types to a top-level module was considered and rejected: their rustdoc carries `super::`-relative intra-doc links throughout, so a move turns a mechanical change into a large non-verbatim diff in a crate four repos build against. `hardware/mod.rs` already `pub use`s all of them, so gating in place is invisible to every consumer.

**This is the enabling half only.** Retiring the mirrors in `embarch-core-client` is `tasks/suite/035`, and it is a separate unit on purpose — those mirrors are `*Response` types with their own contracts, `client.rs:1875-2126` is a block of deliberate mirror-pinning tests (`api/032`) that exists to catch exactly the drift this removes structurally, and `embarch-core-client` is a shipped crate, so retiring them changes a public API.
