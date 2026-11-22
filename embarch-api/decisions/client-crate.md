# embarch-api decisions: The shared client crate

**Status:** active, 2026-09-12.

The runtime stack `embarch-core-client` needed, its extraction out of this repo's own
`core_client.rs`/`config.rs`/`token_discovery.rs`, the one auth-and-send funnel it centralizes,
how it parses an older Core, and the two token scopes. Its home, its one WSL2 predicate and the topology types it names are in [client-crate-types.md](client-crate-types.md) (decisions 62, 66, 72). Split out of [core-link.md](core-link.md) on
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

Later additions exposed the cost — six hand-written mirrors of topology types. **Retired by decision 72** ([client-crate-types.md](client-crate-types.md)).

### 55 — One funnel applies the bearer token; nine routes were exempt from the rule that said so
`send`/`send_no_content` consume the response, so the nine routes giving a status its own meaning (a `404` for "not enrolled", a `409` for a topology mismatch) and the SSE stream could not use them; each applied `.bearer_auth(…)` itself. **A convention nine of twenty-five sites are exempt from is not one** — and the comment was the worse half, since a new route copies the hand-written form while the sentence a reader trusts says it cannot exist.

So the funnel moves down. `dispatch` applies the token and the timeout and sends; `send`/`send_no_content` are thin readers over it; a route needing typed status handling hands it a `RequestBuilder` and reads the status itself. `bearer_token()` is **retired**. The guard: one `.bearer_auth(…)` in the crate, no send site outside `dispatch`. ***Rejected: `default_headers`*** — it authenticates every request the `reqwest::Client` makes rather than this client's *routes*. **Nothing was unauthenticated before this**; the wire is unchanged.

### 58 — Parsing an older Core is a rule of the crate, not a per-field judgement call
`client.rs` had already made this choice many times before `validate` broke it: `link_port_interface` and `study_designer_schema_version` among others are `#[serde(default)]` on an `Option<T>`, and `an_older_core_body_missing_link_port_interface_still_parses` is a test whose name states the rule out loud. `api/045` added `ValidateResponse::validated_at_utc_ms` as a bare required `u64` — the one field breaking the pattern, not a considered exception to it. Against an `embarch-core` predating that field, every `validate` call then failed at deserialization instead of returning the timestamp Core does send, indistinguishable from a broken client rather than a version skew — on a machine where deployed Core and this crate are known not to move together (the MCP-binary-goes-stale gotcha).

So: **every response field this crate deserializes that Core may not yet send is `Option<T>` with `#[serde(default)]`** — matching the existing fields in shape, not merely in having a default. `None` is never presented as a fabricated "validated at 1970" nor silently dropped: a reader is told in words that this Core did not report the value, which is a different fact from validating at an unknown time.

**Applied `api/139`.** `SignalExchangeResponse`'s `bytes_read`/`echo_seen`/`written`/`port_lost` (`api/138`) had shipped as bare defaults, so an old Core's exchange showed `written: false`, the value decision 85 exists to stop being read as "safe to resend"; they are `Option` now, skipped when `None`. `FlashResponse.erased` is `Option<Vec<String>>` too, not recorded as an exception: an empty list on an old Core would read as "nothing erased" after `erase: true`, which is a claim Core never made; `Some(empty)` is Core saying so.

**The check, corrected `api/072`.** The frozen numbers 13/14 are retired: a plain `grep -c 'serde(default)'` counts prose quoting the attribute too, so it drifts as the file grows. The check that stays correct is anchored to the attribute's position: `grep -c '^\s*#\[serde(default)\]' crates/embarch-core-client/src/client.rs`.

### 109 — The client resolves either of Core's two tokens by scope; the MCP server and the CLI send only the agent's

`embarch-core` decision 109 gave Core an agent token and a person token. `embarch-core-client` now names the choice: `TokenScope::{Agent, Person}`, `token_discovery::resolve_token_for(scope, ..)`, `CoreConfig::resolve_token_for(scope)` and `CoreClient::new_with_scope(config, scope)`. **`resolve_token`, `CoreConfig::resolve_token` and `CoreClient::new` are unchanged and mean the agent's**, so its consumers build as before.

**The person's order** is config `person_token_env`, config `person_token`, the `EMBARCH_PERSON_TOKEN` variable Core itself reads, then `person-token` beside the agent's file (same WSL2 mapping as the agent's). **It never falls back to the agent's token**: no person token is an error naming its sources.

**Only a library caller reaches the person's.** The MCP server and every CLI verb build their client through `agent_core_client`, which names `TokenScope::Agent`, and a test pins that a configured `person_token` does not change it. No flag asks for the person's: the surfaces that act for the engineer (`tasks/ui/111`) call `new_with_scope`. A flag would be one more way for an agent to ask for the wrong scope. The scope is fixed at construction; `CoreClient::scope()` reads it.

**Measured:** unit tests per source, and `new` is the agent's. **Not run:** the WSL2 `person-token` path against a live Core.
