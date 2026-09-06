# embarch-api decisions: Reaching Core

**Status:** active, 2026-09-06.

Address resolution, artifact transfer, the shared client crate, and the stack that had to move.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 11 — `base_url = "auto"`, resolved per-process at first use
The WSL2⟷Windows split reaches Core at a host-gateway IP that **changes across WSL2 restarts**, so a literal address in config is guaranteed to go stale — and did. Resolution belongs here rather than in a setup step precisely because the value has to be right **at the moment a build is flashed**, not at the moment setup last ran, and this is the process present then. It does not weaken decision 7: `auto` makes localhost merely one candidate, and an explicit URL still wins outright. Mechanism: [../spec.md](../spec.md) §4.

### 14 — Starting with Core unreachable is a warning, not a refusal
The eager check previously **refused to start the MCP server at all**, which meant every tool vanished from the agent's view with no way to learn why — directly contradicting the rule that failures should come back as text an agent can reason about. The check still runs and still warns; every hardware-facing tool now fails per-call with that message plus the resolved-candidate list, rather than never being callable. `list_projects` is unaffected either way.

### 15 — Artifact transfer branches on topology class, not on a guess about shared filesystems
Originally scoped to trigger only for a genuinely remote Core, on the theory that local and WSL2-host topologies always share a filesystem. **That premise was false for WSL2 specifically**, when Core runs as the installed Windows service rather than in the foreground — and every earlier "confirmed working" claim for the UNC mechanism had been validated against a *foreground* Core. Both WSL2-host and remote now upload bytes; only a same-machine or explicitly-addressed Core keeps sending a path. `artifact_path_for_core` and its UNC computation are **fully retired rather than left unchanged as originally planned** — [../spec.md](../spec.md) §4 has the Session 0 mechanism and the failure signature.

### 17 — Checking Core's contract version where the schema version is already checked
The status call now also compares a compiled-in expected contract version, **warning rather than refusing** — matching the suite's existing posture on version skew — in the same log line the schema check already produces.

### 26 — `serial_log`'s port falls back to Core's dev-bench port, and the stated intent was corrected
The fallback chain gained a final step before erroring. **The correction matters more than the mechanism:** this decision originally justified it by calling a DUT's own serial console "a different, project-specific port that config already covers" — treating DUT-UART capture as a real intended use on par with the bench's. That premise was **never true**: Core's serial link was only ever meant to reach the bench. A project's `serial_port` field existing does not mean pointing it at a DUT was ever a supported goal, just that nothing in code stops it.

### 36 — The whole runtime moves onto a dedicated 512 MiB-stack thread
A real GATT-sized status call reproduced a known deserialization stack overflow **in production**, crashing the live MCP server repeatedly — each crash silently respawning a fresh process, so the client saw only a closed connection.

***Rejected, because it does not work:* `Builder::thread_stack_size`.** It only sizes threads the *runtime* spawns. The top-level future driven by `block_on` runs on whatever thread calls it, which for `#[tokio::main] fn main` is the process main thread, at the OS default, **with no knob to change it**.

So `main` spawns the runtime on a thread it sizes itself. **64 MiB was empirically insufficient against a real payload; 512 MiB was needed.** A release build overflowing on any subcommand, even `list-projects`, was the same non-resizable-calling-thread issue surfacing through release-mode inlining — one fix, two bugs.

### 37, 38 — `embarch-core-client` extracted, and given the two wrappers nothing here needed
`embarch-ui` needed to reach Core exactly as this crate does — bearer injection, per-call timeouts, the topology-branched flash transport, typed error mapping — so the choice was between it duplicating that logic or **both depending on one implementation**. The latter follows the suite's one-implementation-many-call-sites shape rather than reintroducing the mirrored-copy risk that shape exists to eliminate. A plain path dependency, not a Cargo workspace, matching how this repo already depends on its sibling crates.

Two Core endpoints then turned out to have **no client wrapper anywhere**, because this crate never needed either: enrolled-board listing and dev-bench port. The gap surfaced the moment `embarch-ui` routed *every* hardware-adjacent read through Core rather than only mutations. The port wrapper treats Core's 404 as `Ok(None)` rather than an error, so a caller rendering "not connected" does not have to match an error string to do it.

Later additions followed the same rule and exposed its cost: the signal-route wrappers are **mirrors** of the topology crate's types rather than those types, because the real ones sit behind the feature that links `probe-rs`, and this crate never links hardware. That leaves a coupling **no crate in the suite can typecheck**, so it is pinned from each side against the same JSON literal, each test naming the other. The alert and enrolled-board mirrors still have that coupling unpinned.

### 48 — `lagged` is a fact, a dropped stream is a mode change, and neither is an error
Core emits `event: lagged` *deliberately* when a subscriber falls behind its broadcast buffer, in preference to silently skipping messages. A client that surfaced that as a stream error would destroy the thing it was built for: it is a fact about **this subscriber**, and the study's own record on disk is untouched. So it is reported and counted, the stream continues past it, and both front-ends say in as many words that the complete record is still `GET /study/{id}`.

**A stream that drops falls back to polling rather than reconnecting.** Core's handler subscribes to a `tokio::sync::broadcast` channel and reads no `Last-Event-ID`, so a reconnect would resume at "now" with a hole of unknown size and nothing to notice it — exactly what `lagged` exists to prevent. Polling reads the authoritative record instead, and every fallback announces itself and why. A refused subscription (an older Core, a proxy) takes the same path; the only genuine failure is neither mechanism answering.

**Subscribe first, then poll once.** Core holds the stream open indefinitely, so a study that finished *before* the subscribe emits no `StatusChanged` and would hang a listener; the opening poll is what catches it. The order is load-bearing the other way too — polling first leaves a gap an event can fall into.

**Two kinds of incompleteness, reported as two.** Core's `lagged` and this crate's own `max_events` cap ([decision 47](surface.md)) are different facts with different remedies, and a caller told only "some events are missing" cannot tell them apart.

### 49 — The event-stream client lives in `embarch-core-client`, and Core's `StudyEvent` is mirrored there
Same argument as decisions 37/38: `embarch-ui` reaches Core the same way this crate does, and a second SSE implementation there would be the mirrored-copy risk that extraction exists to remove. It also buys testability without widening this package's own `lib` surface ([decisions](tests.md) 46) — the decoder and the follow loop are `pub` in a library crate `tests/` can already reach, so nothing had to move out of the binary.

**Core's `StudyEvent` is mirrored rather than shared.** The real type lives in Core's binary crate and is `Serialize`-only; lifting it into `embarch-study-designer` is a cross-repo wire change and not one sub-project's to make. The mirror's cost is that a variant Core grows and this does not is undecodable — paid down by treating an unknown `kind`, an unknown `event:` name and unparseable data as **one reported "I did not understand this frame"** rather than an error. Core has already grown one variant (`GattTranscript`) that `embarch-core/interfaces.md` still does not list, so this is not hypothetical.

The SSE wire decoder is a separate byte-fed module with no I/O at all, because every framing failure worth fearing — a frame split across TCP reads, a `\r\n` straddling that split, a keep-alive comment between frames — is a pure function of a byte sequence and should be testable as one.

### 43 — One rolling per-machine logfile, because there is no process to ask
Core's log endpoints assume a long-running service. This crate is the opposite: spawned per session as an MCP server, or run once as a CLI and gone. **By the time anyone wants to look at a one-shot's output the process has exited.** Every invocation appends to one rolling file, each line tagged with pid and mode so interleaved sessions stay separable. This works for the one-shot case specifically because **the record outlives the process**, which is the property no endpoint-based design can have here.

*Rejected: shipping lines to Core over a log-sink endpoint.* It would reuse mediation Core already has, and it breaks the invariant that Core has no idea this crate exists — load-bearing well beyond logging. *Also rejected: doing nothing*, on the grounds that an MCP client surfaces its server's stderr and a CLI prints to the terminal. Both true, and neither survives the case that matters: wanting to know what an agent's run did twenty minutes ago, in a session that is closed.

**Per-user, not machine-wide.** The machine data dir works for Core, which runs as a service; it does not work here, because this runs as the engineer and `/var/lib` is root-owned. Both alternatives were worse: hard-failing makes logging depend on a one-time `sudo`, and "machine dir if writable, else per-user" is a runtime probe that can land the writer and the reader in **different places**. Nothing is lost, since single-engineer scope means there is no second user to be machine-wide for.

**Both modes had to be given something to log:** a one-shot CLI run emitted nothing at all, since no subcommand calls the tracing macros on its own. Two lines now bracket every run. **The file gets two layers rather than one teed writer** — Core tees a single ANSI-coloured stream to both stderr and its logfile, so every line in its deployed log carries escape sequences a UI renders as garbage. The two-layer form has **no filter of its own**, so the first build wrote `hyper` and `reqwest` trace output into the file; it needs one stated explicitly.

### 55 — One funnel applies the bearer token; nine routes were exempt from the rule that said so
`send`/`send_no_content` consume the response, so the nine routes giving a status its own meaning (a `404` for "not enrolled", a `409` for a topology mismatch) and the SSE stream could not use them; each applied `.bearer_auth(…)` itself. All nine did send it; `client.rs`'s comment said none existed. **A convention nine of twenty-five sites are exempt from is not one** — and the comment was the worse half: a new route copies the hand-written form while the sentence a reader trusts says it cannot.

So the funnel moves down. `dispatch` applies the token and the timeout and sends; `send`/`send_no_content` are thin readers over it; a route needing typed status handling hands it a `RequestBuilder` and reads the status itself. `bearer_token()` is **retired**. The guard is decision 50's shape applied to auth: one `.bearer_auth(…)` in the crate, no send site outside `dispatch`, both red by mutation.

***Rejected: `default_headers` on the `ClientBuilder`.*** It attaches the token to every request the `reqwest::Client` makes, not to this client's *routes*, and `http()` hands that handle out. It also hides the credential from every call site, leaving the sweep ([decisions](tests.md) 54) nothing to assert. **Nothing was unauthenticated before this**; the wire is unchanged.
