# embarch-api decisions: The bench lease client

**Status:** active, 2026-10-26.

The client half of `embarch-core` decision 93 (`/lease`: one session holds both boards across calls; a hardware request without its token is `409` by name). What Core does: [../../embarch-core/decisions/lease.md](../../embarch-core/decisions/lease.md). Tools: [../interfaces/tools-lease.md](../interfaces/tools-lease.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 90 — The token travels in `EMBARCH_LEASE_TOKEN`, sent by the one funnel on every Core call; the MCP server renews on a timer, and a refusal surfaces as Core's text

**An environment variable, not a per-process lease the server takes for itself.** `embarch-atlas` reaches Core only by running the `embarch-api` CLI as a subprocess (`embarch_atlas/live.py`, `subprocess.run`), so a variable `CoreClient` reads on every request reaches atlas's live calls and a subagent's with **no change to `embarch-atlas`** and no per-call argument. A lease the MCP server took privately would be invisible to every other process of the same session, which is the exact hole the field's `mkdir` lock had (atlas calls could not see it). `dispatch`, the one place a request is authenticated and sent (decision 55), attaches `X-Embarch-Lease` beside the bearer: a request cannot go out without it by construction, and the existing sweep proves the route list.

**The precedence is the process's own token, then the variable**, read per request so a later `export` is seen by a long-lived process. `lease_take` stores the token in the process that took it; the result also carries it once (Core shows it once) with the variable's name, and the CLI prints an `export` line. **Exporting it into atlas's environment is the session's act**: a token taken through an MCP tool lives in the server process and reaches no subprocess until exported there. No file or other channel was added, because a token on disk outlives the lease and the session that took it. A value that is not a valid header value is an error naming the variable, not a silent unauthenticated call.

**Renewal does not depend on a model.** `CoreClient::lease_keepalive`, spawned once by the MCP server, wakes each second and renews whichever token the process sends when a third of its TTL has passed (an inherited token of unknown TTL renews at once and learns it). The default MCP TTL is 900 s, so a crashed session frees the bench within 15 minutes; **[assumed]**, not measured against any session length. The CLI has no process to renew for it, so its default TTL is 3600 s and `lease-renew` exists. A failed renew is logged and retried a third of a TTL later, never fatal: the next call's `409` or `404` says what happened.

**A lease `409` is told apart from the three other `409`s by its text.** `validate` (topology mismatch), `post_study` (a study in flight) and `dev_bench_hello` (dev-bench busy) each give a `409` its own meaning, and a plain-text lease refusal fell into each as a misleading lead ("a study is already in flight"). Core's refusal begins `bench leased by `, which no other body does, so `LeaseHeldError` carries it verbatim ahead of those branches; every other route already reported the body unchanged. Matching prose is the cost: `error_kind` stays retired (decision 50), and a Core that rewords the refusal degrades to the old, still-verbatim message.

**`status` is where `last_images` is read**, with `lease`, so one call answers "who has the bench and is my image on it": an absent chip means unknown, never "nothing flashed" (the field is in Core's memory). Both are optional with defaults, so an older Core still parses. Not applied automatically: a client that skipped a reflash because a hash matched would be inferring a DUT fact (spec §2); the session compares.

**Not done: a per-board lease or auto-take at first hardware call.** Core's lease is one for the whole bench; and a server that took one silently would hold the bench against sessions that never asked it to, with the model unaware.
