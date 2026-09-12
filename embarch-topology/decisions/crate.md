# embarch-topology decisions: One crate, called live

**Status:** active, 2026-09-02.

Why topology is a linked library rather than a tool, a file, or a service.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — This is a resolution/abstraction layer, not just a checker

The rest of the suite should be able to say "give me dev-bench" or "what's my base URL" and **get a resolved answer**, rather than each independently re-implementing VID heuristics or a WSL2-gateway probe. **A deliberate step further than a read-only diagnostic: it is the thing that produces the answer, not just the thing that flags when the answer looks wrong.**

### 2 — A shared crate `embarch-core`, `embarch-api` and `embarch-umbrella` all link and call in-process

All detection, resolution, enrollment and validation lives in one crate; the three consumers call its functions directly, live, whenever they need an answer. Its own CLI is a thin wrapper over the same functions.

**Reversed from this session's own earlier decision**, which picked a doctor-style standalone tool specifically to avoid a shared library, **reasoning that the suite had deliberately kept mirrored copies of cross-repo logic instead of extracting crates.** That reasoning held right up until working through mismatch detection surfaced the actual cost of *not* sharing code: **Core still needed either a written-ahead file or a manual override to know the current answer — and a manual override left unmaintained is exactly what caused the motivating incident.** A shared crate Core calls live removes the need for either.

**This is not a reintroduction of the rejected standalone-service option.** That was rejected because **a network or IPC dependency in the hardware-operation path is a new thing that can be down**; a compiled-in library call carries no such risk, since it is just code running in Core's own process. There is already suite precedent for this shape of sharing — **`embarch-study-designer` extends it from shared *data types* to shared *logic*.**

### 3 — Live, in-process, on every call — no write-ahead file for anything auto-detectable

Per request for anything that can change while a process runs (dev-bench's port, on unplug/replug); once at startup for anything that cannot (a bind address, fixed for the life of the socket). **There is no resolve-then-write step and therefore nothing that can go stale between a write and a read.**

**Reversed**, same session, alongside decision 2: the earlier framing had this crate write resolved answers into files the consumers read. **That solved "the file might be missing" but did not remove the *incentive* for a manual override to exist in front of it** — which is what decision 9 was built to detect and is now retired to prevent instead. **The only state that still needs writing is a human's declared intent that detection cannot derive at all**, and it lives inside the crate's own storage, not as a file any consumer parses.

### 4 — Both software and hardware topology, in one pass, not hardware-first

The board-identity gate, its storage, the dev-bench port heuristic, **and** the software-class detection then mirrored between `embarch-api` and `embarch-umbrella` all move here as the sole implementation. **The mirrored-copy CI diff job becomes obsolete: there is nothing left to mirror once everyone links the same crate.**

**Qualified 2026-09-08** (`tasks/topology/020`, from `api/038`'s finding): "the sole implementation" and "nothing left to mirror" describe the crate's own boundary, not its callers. `embarch-api/crates/embarch-core-client` already linked this crate and still ran a second, narrower predicate (`token_discovery::is_wsl2`) beside the call it never made to `detect_wsl2` — closed by `api/038` (`embarch-api` decision 62, `861f30f`), which made it delegate. Linking the crate stops a mirrored *copy* of its own logic; it does not stop a caller writing an unrelated second predicate next to a call it never makes. A third copy, `embarch-umbrella/src/token.rs`, closed the same way: `umbrella/036` (2026-09-08, `e1a5e7c`/`444f84d`) replaced it with a direct call to `embarch_core_client::token_discovery::resolve_token`. No live mirror of *this crate's logic* remains now — never the point; nothing here can cheaply detect the next one (see `open.md`).

**Qualified again 2026-09-12** (`tasks/suite/020`): "nothing left to mirror once everyone links the same crate" was still false in a second way, about **data** rather than logic. `embarch-api/crates/embarch-core-client` links this crate and nonetheless hand-mirrors seven of its wire types, because until decision 31 those types were only reachable through the `hardware` feature — which that crate must never enable. Linking the crate is not sufficient when the thing you need is behind a gate you are forbidden to open. Decision 31 removed the gate; the mirrors themselves come out in `tasks/suite/035`, and **until that lands this sentence is still not true as written.**

### 6 — `doctor`'s topology-relevant checks call the crate directly, in-process

They become thin wrappers translating a crate call into pass/fail/warn.

**Reversed**, same session: originally `doctor` was going to shell out to a CLI with its own JSON contract, **mirroring the precedent set for the target-count check.** That precedent fit when this was a separate process; **once it is a linked crate, calling it directly is simpler and consistent with how Core and the API consume it — no process spawn, no JSON boundary to keep in sync.**

### 8 — One implementation, multiple call sites — not two independent layers

A human running the CLI **sees precisely the validation Core enforces live, because it *is* that validation — there is no way for the two to disagree, since there is only one of them.** Concretely: whatever port or probe an operation is about to use, one shared `validate()` confirms the device is currently enumerated and still matches the identity recorded for its role, and **returns a specific error naming what is stale** if it does not.

**Reversed** from an earlier framing that described an ahead-of-time check and Core's live re-check as **two independent, separately-reasoned mechanisms that happened to agree.** They are not independent once both are calls into the same crate.

**Qualified 2026-09-08** (`tasks/topology/020`): "there is no way for the two to disagree, since there is only one of them" holds only inside the crate's own boundary — a statement about the crate, not about whether a caller actually calls it. `api/038` found `embarch-api`'s own client still ran a second, narrower WSL2 predicate beside a call it never made to this crate's `detect_wsl2`, and closed that instance by making it delegate. Whether anything should detect a caller declining to call the crate at all: see `open.md`.

**Qualified again 2026-09-12** (`tasks/suite/020`): the same correction decision 4 takes above applies here, for data instead of logic. `embarch-core`'s `api.rs` serves `EnrolledBoard`, `Alert`, `DetectedPort` and `SignalLink` verbatim, and `embarch-core-client` describes the same JSON from its own hand-kept definitions — so "there is no way for the two to disagree" was false for every one of those shapes, and both sides typecheck perfectly while disagreeing (`EnrolledBoardResponse` has already silently dropped `link_port_interface`). Decision 31 makes the real types reachable without `probe-rs`; `tasks/suite/035` is what actually makes this sentence true.

**A real gap this surfaced:** the live-identity recheck covered only JTAG-capable roles. **The dev-bench runtime *link* had no equivalent live check** — which is what absorbing that logic had to close here rather than leave behind in Core.

### 31 — The `hardware` gate is drawn around the machinery, not around the module: a `wire` feature carries the types alone

**Decided 2026-09-12** (`tasks/suite/020`, from the 2026-09-06 suite review pass, dimensions 1 and 4).

`serde` used to be listed under the `hardware` feature alongside `probe-rs` and `serialport`, and `lib.rs` gated the whole `hardware` module on it. The types behind that gate need neither: `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route` and `SignalDirection` are plain serde data — the facts `embarch-core` serves over HTTP — while it is the **functions** below them in the same files that read a probe, enumerate a serial port or write `enrollment.toml`.

So the gate now names the machinery rather than the module. A new `wire` feature turns on `serde` and nothing else; `hardware` implies it, so `embarch-core` is unchanged. Under `wire` alone the `hardware` module compiles to its types, and every function, storage path and probe call in it is `#[cfg(feature = "hardware")]`-ed out. `cargo tree -e normal --no-default-features --features wire` is `anyhow`, `serde`, `tracing` — no `probe-rs`, no `serialport`, no C toolchain.

**The rule this does not touch, and must not:** nothing outside `embarch-core` links `probe-rs`/`serialport`. That rule is right. What it was costing was seven hand-mirrored wire types in `embarch-api/crates/embarch-core-client`, each with a comment explaining that the real type was unreachable — two definitions of one JSON shape, in two repos, with the compiler unable to compare them. Honouring the rule should not require duplicating the data it is drawn around.

**One type changed shape to make this possible.** `DetectedPort::detected_by` was `&'static str` and is now `String`: a borrowed-static field cannot implement `Deserialize`, and a wire type a client cannot deserialize is not a wire type. Every value it holds is still one of the same four constants.

**Types in place, not moved.** Moving the six types to a top-level module was considered and rejected: their rustdoc carries `super::`-relative intra-doc links throughout, so a move turns a mechanical change into a large non-verbatim diff in a crate four repos build against. `hardware/mod.rs` already `pub use`s all of them, so gating in place is invisible to every consumer.

**This is the enabling half only.** Retiring the mirrors in `embarch-core-client` is `tasks/suite/035`, and it is a separate unit on purpose — those mirrors are `*Response` types with their own contracts, `client.rs:1875-2126` is a block of deliberate mirror-pinning tests (`api/032`) that exists to catch exactly the drift this removes structurally, and `embarch-core-client` is a shipped crate, so retiring them changes a public API.

### 13 — Started as a design-only doc with no repo

Matching how `embarch-umbrella` and `embarch-dev-bench` both started. Flagged at the time because **a shared crate needs *somewhere* for three consumers to depend on**, which pulls "when does a real repo need to exist" earlier than a design-only doc's usual timeline. The repo is real now: [gabrieltetar/embarch-topology](https://github.com/gabrieltetar/embarch-topology), depended on as a **plain path dependency** — exactly `embarch-study-designer`'s precedent — with the hardware feature added only by Core.

**Release CI needed a real fix beyond the dependency line.** Each consumer's release workflow **only ever checked out itself**, so a relative path dependency could never resolve; fixed by checking out every path-dependency repo as a named sibling and building from inside the consumer's own subdirectory. **The same gap already existed for `embarch-study-designer`** — added days earlier and never exercised by a green release run — and was fixed in the same pass. Whether the Docker-based aarch64 cross build can see siblings outside the crate root was **researched against the tool's own history rather than assumed** (it auto-mounts any path dependency the metadata can see) and then **confirmed by a real tagged release run**, not by research alone.

