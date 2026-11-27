# embarch-api decisions: The shared client crate

**Status:** active, 2026-09-12.

The runtime stack `embarch-core-client` needed, its extraction out of this repo's own
`core_client.rs`/`config.rs`/`token_discovery.rs`, one WSL2 predicate it delegates, which topology types it names rather than copies, and the two token scopes. The funnel and the crate's home (55, 66) are in [client-crate-funnel.md](client-crate-funnel.md). Split out of [core-link.md](core-link.md) on
2026-09-11 (`api/067`) along a topical seam, not as a squeeze.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). Address
resolution and artifact transfer: [core-link.md](core-link.md).

### 36 — The whole runtime moves onto a dedicated 512 MiB-stack thread
A real GATT-sized status call reproduced a known deserialization stack overflow **in production**, crashing the live MCP server repeatedly — each crash silently respawning, so the client saw only a closed connection.

***Rejected, because it does not work:* `Builder::thread_stack_size`.** It sizes only threads the *runtime* spawns. The top-level future driven by `block_on` runs on whatever thread calls it, which for `#[tokio::main] fn main` is the process main thread, at the OS default, **with no knob to change it**.

So `main` spawns the runtime on a thread it sizes itself. **64 MiB was empirically insufficient against a real payload; 512 MiB was needed.**

### 37, 38 — `embarch-core-client` extracted, and given the two wrappers nothing here needed
`embarch-ui` needed to reach Core exactly as this crate does — bearer injection, per-call timeouts, the topology-branched flash transport, typed error mapping — so the choice was between duplicating that logic and **both depending on one implementation**. The latter follows the suite's one-implementation-many-call-sites shape rather than reintroducing the mirrored-copy risk that shape exists to eliminate. A plain path dependency, not a Cargo workspace.

Two Core endpoints then turned out to have **no client wrapper anywhere**, because this crate never needed either: enrolled-board listing and dev-bench port. The gap surfaced the moment `embarch-ui` routed *every* hardware-adjacent read through Core rather than only mutations. The port wrapper treats Core's 404 as `Ok(None)`, so a caller rendering "not connected" need not match an error string.

Later additions exposed the cost — six hand-written mirrors of topology types. **Retired by decision 72 below.**

### 58 — Parsing an older Core is a rule of the crate, not a per-field judgement call
`client.rs` had already made this choice many times before `validate` broke it: `link_port_interface` and `study_designer_schema_version` among others are `#[serde(default)]` on an `Option<T>`, and `an_older_core_body_missing_link_port_interface_still_parses` is a test whose name states the rule out loud. `api/045` added `ValidateResponse::validated_at_utc_ms` as a bare required `u64` — the one field breaking the pattern, not a considered exception to it. Against an `embarch-core` predating that field, every `validate` call then failed at deserialization instead of returning the timestamp Core does send, indistinguishable from a broken client rather than a version skew — on a machine where deployed Core and this crate are known not to move together (the MCP-binary-goes-stale gotcha).

So: **every response field this crate deserializes that Core may not yet send is `Option<T>` with `#[serde(default)]`** — matching the existing fields in shape, not merely in having a default. `None` is never presented as a fabricated "validated at 1970" nor silently dropped: a reader is told in words that this Core did not report the value, which is a different fact from validating at an unknown time.

**Applied `api/139`.** `SignalExchangeResponse`'s `bytes_read`/`echo_seen`/`written`/`port_lost` (`api/138`) had shipped as bare defaults, so an old Core's exchange showed `written: false`, the value decision 85 exists to stop being read as "safe to resend"; they are `Option` now, skipped when `None`. `FlashResponse.erased` is `Option<Vec<String>>` too, not recorded as an exception: an empty list on an old Core would read as "nothing erased" after `erase: true`, which is a claim Core never made; `Some(empty)` is Core saying so.

**The check, corrected `api/072`.** The frozen numbers 13/14 are retired: a plain `grep -c 'serde(default)'` counts prose quoting the attribute too, so it drifts as the file grows. The check that stays correct is anchored to the attribute's position: `grep -c '^\s*#\[serde(default)\]' crates/embarch-core-client/src/client.rs`.

### 62 — `token_discovery`'s WSL2 check delegates to `embarch_topology::software::detect_wsl2`, dropping its own third signal
This crate's private `is_wsl2` ran its own rule — `/proc/version` containing "microsoft" *or* "wsl", ignoring `$WSL_DISTRO_NAME` — while `resolve_software_topology`, in the same binary, used `detect_wsl2`'s union of kernel-string-or-env-var. The two could disagree: token discovery decides *where the token file is*, topology resolution *which Core to talk to*. No real WSL2 kernel is known to stamp "wsl" without "microsoft", so the extra branch covered no observed case; delegating removes the disagreement at no known cost.

`embarch-topology` decisions 4/8 (crate.md) claimed no two callers could disagree "since there is only one of them" — false while this crate linked the shared crate and ran a second predicate beside it; a crate cannot stop a caller writing one next to the call it never makes.

### 72 — The six mirrored `embarch-topology` types are retired; the tests that pinned them are kept and re-scoped
Decisions 37/38 accepted six hand-written copies of `embarch_topology::hardware`'s `EnrolledBoard`, `Alert`, `DetectedPort`, `SignalLink`, `Route` and `SignalDirection`, because the originals sat behind that crate's `hardware` feature — which links `probe-rs`/`serialport`, dependencies this crate must never have. `embarch-topology` decision 31 split a `wire` feature out of it: the plain data types, pure serde, no C toolchain. So the copies are gone. This crate depends on `embarch-topology` with `default-features = false, features = ["software", "wire"]` and names the real types; the old `*Response` spellings survive as **aliases**, so no call site moves and the shipped crate keeps its public names.

**The cost was not hypothetical.** `EnrolledBoardResponse` silently dropped `link_port_interface` for a release — the field that exists because an nRF54L15DK's console is on the *higher* VCOM (`embarch-topology` decision 20) — and `tasks/api/032` exists to paper over it. Two structs in two crates that never meet are not comparable by any compiler, which is what "drift" means here.

**The pinning tests are kept, and that is the part that is not a refactor.** Deleting `client.rs`'s three round-trip literals along with the copies would have been natural — the compiler now proves this crate and Core agree, because they name one type. **It proves nothing about agreeing with a Core already deployed.** Rename a field on the shared type and both sides change together and compile clean, while every running Core and every `enrollment.toml` on disk still speaks the old spelling. The literals are the only thing positioned to notice, so they stay — re-scoped from "our copy matches theirs" to "the wire has not moved under a deployed Core".

***Rejected: keeping a mirror for the derives.*** `Alert`/`DetectedPort` lacked `PartialEq`/`Eq` the copies had; adding two derives upstream is smaller than a copy kept alive to carry them.

Naming the original also **gains** `guessed_among` — whether a port was picked among equally-plausible candidates rather than determined. The mirror had no such field, so a caller could not tell a guess from an answer.

### 109 — The client resolves either of Core's two tokens by scope; the MCP server and the CLI send only the agent's

`embarch-core` decision 109 gave Core an agent token and a person token. `embarch-core-client` now names the choice: `TokenScope::{Agent, Person}`, `token_discovery::resolve_token_for(scope, ..)`, `CoreConfig::resolve_token_for(scope)` and `CoreClient::new_with_scope(config, scope)`. **`resolve_token`, `CoreConfig::resolve_token` and `CoreClient::new` are unchanged and mean the agent's**, so its consumers build as before.

**The person's order** is config `person_token_env`, config `person_token`, the `EMBARCH_PERSON_TOKEN` variable Core itself reads, then `person-token` beside the agent's file (same WSL2 mapping as the agent's). **It never falls back to the agent's token**: no person token is an error naming its sources.

**Only the engineer's surfaces reach the person's.** The MCP server and every CLI verb but `person` ([141](person-verb.md)) build their client through `agent_core_client`, which names `TokenScope::Agent`, and a test pins that a configured `person_token` does not change it. No flag asks for the person's: the UI (`tasks/ui/111`) calls `new_with_scope`. A flag would be one more way for an agent to ask for the wrong scope. The scope is fixed at construction; `CoreClient::scope()` reads it.

**Measured:** unit tests per source, and `new` is the agent's. **Not run:** the WSL2 `person-token` path against a live Core.

### 137 — The client's prompt types carry a Test run prompt's kind, outputs and answer value, additively

`PendingPrompt` gains `kind` (`embarch_study_designer`'s `PromptKind`), `observation` and `switched_on` (a new `SwitchedOn {target, line, step}`), each `#[serde(default)]` and skipped when absent or empty, so a host study's prompt reads and writes the bytes it did; `PromptAnswerRequest` gains `value`, skipped when `None`. `observation` is a `serde_json::Value`: Core's shape is the designer's (`{name, answers?, number?}`) and a surface only reads it. `value` is a string (a declared choice) or a number, `confirmed` only ([core 138](../../embarch-core/decisions/host-prompt.md)).

**The event has no `kind`.** Core flattens the prompt onto `PromptPending`, whose stream tag is also `kind`, and serde refuses a tagged variant that declares a field of that name. `StudyEvent::PromptPending` therefore carries `observation` and `switched_on` only; a prompt's kind is read from `GET /study/{id}`'s `pending_prompt`, which a follower polls anyway. `as_pending_prompt` yields `kind: None`. A Test run's event with both keys is refused by the client as a duplicate field; filed against Core (EMB-577).

**Source-breaking for struct literals:** a caller building `PromptAnswerRequest` names `value: None`; the three in this repo do.

**Measured:** `tests/prompt_types.rs`, a host prompt and answer byte for byte, a Test run's prompt round trip, the event with and without the colliding second `kind` (the client refuses the former). **Not run:** against a live Core's Test run.

### 139 — The client's `StatusResponse` carries Core's `mode` and `keyid`

`StatusResponse` gains `mode` (`"service"` or `"development"`) and `keyid` (the sealing key's fingerprint), each `Option<String>` with `#[serde(default)]`: Core already sends both ([core 129](../../embarch-core/decisions/)), and the client dropped them, so a surface could only infer the mode from the attestation's match result and read a development Core whose key was recorded as the installed one as `service`. `None` is a Core that predates them: unknown, never `service`. **Source-breaking for struct literals:** none exists in `embarch-api`, `embarch-ui` or `embarch-umbrella` (checked 2026-11-26). The UI switching its identity line to the reported mode is ui's follow-up.

**Measured:** a unit test parses a body with both and one with neither. **Not run:** against a live Core.
