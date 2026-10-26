# 136 — Make two documented api behaviours true: the MCP startup warning, and a stream 404 that names the declared taps

**State:** open
**Source:** DeepSeek V4 Pro review 2026-10-25 (embarch-api findings 2 and 3), verified by Opus against embarch-api@6d664853
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The docs describe two things that the code does not do.

1. **The MCP startup check.** `spec/implementation.md` §4 says "the startup check is MCP-mode-only… That check warns, it does not refuse". Decision 14 says "the check still runs and still warns", and decision 17 says the status call "also compares a compiled-in expected contract version… in the same log line the schema check already produces". `async_main` makes no `GET /status` call in MCP mode, and the only callers are the `status` tool and the CLI. Decision 17 cannot be built as written either way, because Core deliberately serves no contract version.
   Pick one: build a non-blocking, warn-only probe at MCP start, or amend the spec and decisions 14 and 17 to say no startup check runs. Retracting looks like the better default, because a startup log line reaches the logfile and never the agent, while per-call failures already carry the message. The worker decides and records why.
2. **The stream 404.** `study_stream_data`'s description promises "a 404 names the taps the study did declare". `get_study_csv` replaces Core's 404 body with its own fixed sentence, so the declared-tap list never arrives, and the agent needs a second `list_study_streams` call. `get_study_stream_arrivals` goes through the same helper, and its own doc comment says Core's 404 body says which of three cases applies. When this is done, both calls keep Core's 404 body in the error they return.

## Why now

- `src/main.rs:655-746`: no `status()` call on the MCP path. The only callers are `src/tools.rs:814` and `src/cli.rs:339`.
- `spec/implementation.md:26`; `decisions/core-link.md` 14 and 17.
- `embarch-core` `src/api.rs:281-285` (at `40a58cc`): "There is deliberately no separate hand-bumped `contract_version`". The same is said in this repo's `decisions/surface.md:14`.
- `crates/embarch-core-client/src/client.rs:2042-2065` (`get_study_csv` drops the body on 404), `:2095-2100` and `:2116-2125` (both callers); `src/tools.rs:1753` (the promise).
- `embarch-core` `src/study.rs:4157-4166`: Core's body is "study '…' declares no stream tap named 'x' — it declared: a, b, c".

## Done when

- [ ] Nothing in `embarch-api`'s spec or decisions describes a startup check that the code does not perform. If a probe is built, a test shows MCP start against an unreachable Core logs one warning and still serves `list_projects`. If it is retracted, the decisions say so and why.
- [ ] Decision 17 no longer describes comparing a contract version that Core does not serve.
- [ ] Against the mock Core, `study_stream_data` for an undeclared tap returns an error containing Core's declared-tap list. The other two 404 causes ("no captured streams", and a declared tap that captured nothing) each come through with Core's own wording.
- [ ] The same holds for `get_study_stream_arrivals`'s three 404 cases.
- [ ] `study_stream_data`'s tool description matches what the call now returns.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
