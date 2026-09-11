# `dev_bench_hello` will be the first `embarch-core-client` route whose call waits on a board, and the timeout it inherits by inertia is `status_timeout`

**State:** claimed — leg 075, `agent/api/037-dev-bench-hello-timeout`
**Source:** `umbrella/030` (2026-09-06) — noticed while splitting `doctor`'s own budgets after
the same miscategorisation cost `embarch-umbrella` weeks of dark checks
**Scope:** api
**Hardware:** none — a constant, its doc comment, and where a new route picks one
**Owner:** no

## What

`tasks/api/036` asks for an MCP tool over `GET /dev-bench/hello`. Whoever builds it adds a route
to `embarch-core-client`, and that crate's convention is to reuse one of five named budgets with
a doc comment saying why — a convention it applies well: `status_timeout` is reused at nine call
sites, each one carrying its own justification (*"a pure local-file read on Core's side, no
hardware"*, *"Core only reads USB descriptors the OS already has"*).

**`/dev-bench/hello` is the one route where that sentence cannot be written.** Core opens the
bench's serial link, completes the `Hello`/`HelloAck` handshake, takes the boot log the bench
flushes *only after* that ack (`embarch-core` decision 37) and closes the link, before it has
anything to answer with. `status_timeout` is 10 s and would probably work; `serial_timeout` is
15 s and is the budget on the only other route over the same physical link. The ask is that the
choice is **made and stated**, not inherited.

## Supervisor's dispatch note, leg 075, 2026-09-10

**The route exists now** — `tasks/api/036` landed, and `dev_bench_hello` is at
`crates/embarch-core-client/src/client.rs:1810`. So this is no longer "before the route exists":
read what budget it currently uses and either justify it in a doc comment or change it. The
"stated, not inherited" half of the ask is the whole unit.

**Do not measure the handshake.** The two carried-over notes above mention a timed `curl` on the
bench — that is hardware, and this is a host-side unit. **You never touch hardware.** If you
choose a value, it is stated as **assumed** with the reasoning, never as measured. Leaving the
measurement owed is the correct outcome; say so in the task's own words and in your
`changelog.d/` fragment.

**Doc reserve in `embarch-api`, so you plan rather than discover:**
`decisions/tool-wrapping.md` has **66 B left** (12,222/12,288) and its compaction task
`api/047` is **blocked** — do not file a decision there. `open.md` is 4,124/5,120 and **204 B
inside its reserve floor**, with `tasks/api/060` just landed against it and blocked: if you must
add an `open.md` line, keep it to one clause. Prefer `decisions/core-link.md`'s topic area for a
timeout decision — but note that file is 13,164/12,288, **over cap**, with `api/061` blocked, so
if a new decision is warranted pick a topic file with headroom and argue the placement in the
decision itself, exactly as `api/042`'s worker did. If your work spends reserve anywhere, file
`tasks/api/<next free NNN>-compact-api.md` in the same commit.

Before the route exists, because after it exists the reuse comment is already written. The
`embarch-umbrella` version of this shipped and sat: `authed_get` set one 500 ms budget for every
caller, `/dev-bench/hello` inherited it, and `doctor` checks 11 and 13 reported *unavailable* on a
bench that was handshaking, for weeks, while the constant's own doc comment described its callers
accurately and said nothing about what answering costs
(`embarch-umbrella/decisions/budgets.md` 44, 45).

Two things from that unit are worth carrying over and cost nothing here:

- **No handshake *duration* has ever been measured**, on this bench or any other, so both 10 s and
  15 s are assumed. One timed authenticated `curl` of the endpoint on the primary bench sizes
  every copy of this constant in the suite at once.
- **`reqwest::Error`'s `Display` drops its source**, so a timed-out request and a refused
  connection render as the same sentence apart from the URL [measured host-side 2026-09-06]. If
  this crate's error mapping carries only that `Display`, a wrong budget here will be as
  unreadable as it was there.

## Done when

- [ ] The `dev_bench_hello` route (whenever `tasks/api/036` lands it) names a budget with a doc
      comment that says what Core does before it can answer — link-open and handshake, not a read
- [ ] Whether that is `serial_timeout`, a new named constant, or a justified `status_timeout` is
      the author's call; what is not open is inheriting one silently
- [ ] If a handshake duration gets measured on the bench, the chosen value is stated as measured
      rather than assumed
