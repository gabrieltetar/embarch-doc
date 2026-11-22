# embarch-api decisions: Where the shared client crate lives and what it names

**Status:** active, 2026-11-22.

The shared `embarch-core-client` crate's home inside this repo, the one WSL2 predicate it delegates, and the `embarch-topology` types it names rather than copies. Split out of [client-crate.md](client-crate.md) on 2026-11-22 (`api/165`), a verbatim move along a topical seam.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The crate's runtime stack, funnel, older-Core parsing and token scopes: [client-crate.md](client-crate.md).

### 62 — `token_discovery`'s WSL2 check delegates to `embarch_topology::software::detect_wsl2`, dropping its own third signal
This crate's private `is_wsl2` ran its own rule — `/proc/version` containing "microsoft" *or* "wsl", ignoring `$WSL_DISTRO_NAME` — while `resolve_software_topology`, in the same binary, used `detect_wsl2`'s union of kernel-string-or-env-var. The two could disagree: token discovery decides *where the token file is*, topology resolution *which Core to talk to*. No real WSL2 kernel is known to stamp "wsl" without "microsoft", so the extra branch covered no observed case; delegating removes the disagreement at no known cost.

`embarch-topology` decisions 4/8 (crate.md) claimed no two callers could disagree "since there is only one of them" — false while this crate linked the shared crate and ran a second predicate beside it; a crate cannot stop a caller writing one next to the call it never makes.

### 66 — The crate lives inside `embarch-api`'s own tree, not a tenth repo, and `embarch-ui` path-depends across a repo boundary to reach it
Decisions 37/38 settled that the shared Core client is one implementation, not where it lives. It sits at `crates/embarch-core-client` inside this repo, unlike `embarch-study-designer` (decision 8) and `embarch-topology` (decision 13), each of which got a standalone repo. **Only decision 8 states the FFI/C rationale** — two Cargo dependents plus one FFI/C consumer as the case a standalone shared crate is for. **`embarch-topology` decision 13 states no such reason**: only that a shared crate needs *somewhere* for three consumers to depend on. This crate's three consumers (`embarch-api`, `embarch-ui`, `embarch-umbrella`) are all plain Cargo path dependents, so decision 8's case does not hold — and the question was never taken up either way: 37/38 left the crate where the extraction happened.

The cost, stated rather than softened (`spec.md:48`): `embarch-ui` path-depends on it from outside this repo, so **a change made here reaches a repo this one does not own**, and `check-ownership.py` does not refuse that move — nothing in the fleet mechanism stops an `api` task editing a crate `embarch-ui` depends on. `suite/decisions.md` 1 documents the gate-spelling cost that follows.

Kept anyway: a tenth repo for Cargo-only consumers with no cross-language boundary pays a cost `embarch-study-designer`/`embarch-topology` accepted for a reason (FFI, independent hardware/software versioning) that does not hold here, and decision 56 already made the crate a workspace member with its own tests in this repo's gate. **Reverses** if a *fourth* Cargo consumer with its own release cadence appears, or an `api`-only change here breaks `embarch-ui` or `embarch-umbrella` silently.

### 72 — The six mirrored `embarch-topology` types are retired; the tests that pinned them are kept and re-scoped
Decisions 37/38 accepted six hand-written copies of `embarch_topology::hardware`'s `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route` and `SignalDirection`, because the originals sat behind that crate's `hardware` feature — which links `probe-rs`/`serialport`, dependencies this crate must never have. `embarch-topology` decision 31 split a `wire` feature out of it: the plain data types, pure serde, no C toolchain. So the copies are gone. This crate depends on `embarch-topology` with `default-features = false, features = ["software", "wire"]` and names the real types; the old `*Response` spellings survive as **aliases**, so no call site moves and the shipped crate keeps its public names.

**The cost was not hypothetical.** `EnrolledBoardResponse` silently dropped `link_port_interface` for a release — the field that exists because an nRF54L15DK's console is on the *higher* VCOM (`embarch-topology` decision 20) — and `tasks/api/032` exists to paper over it. Two structs in two crates that never meet are not comparable by any compiler, which is what "drift" means here.

**The pinning tests are kept, and that is the part that is not a refactor.** Deleting `client.rs`'s three round-trip literals along with the copies would have been natural — the compiler now proves this crate and Core agree, because they name one type. **It proves nothing about agreeing with a Core already deployed.** Rename a field on the shared type and both sides change together and compile clean, while every running Core and every `enrollment.toml` on disk still speaks the old spelling. The literals are the only thing positioned to notice, so they stay — re-scoped from "our copy matches theirs" to "the wire has not moved under a deployed Core".

***Rejected: keeping a mirror for the derives.*** `Alert`/`DetectedPort` lacked `PartialEq`/`Eq` the copies had; adding two derives upstream is smaller than a copy kept alive to carry them.

Naming the original also **gains** `guessed_among` — whether a port was picked among equally-plausible candidates rather than determined. The mirror had no such field, so a caller could not tell a guess from an answer.
