# 030 — `doctor` gives `/dev-bench/hello` the same 500 ms as `GET /status`, so checks 11 and 13 can never finish

**State:** open
**Source:** supervisor bench unit `umbrella/027`, 2026-09-06 — three live `doctor` runs against the
primary `wsl-host` bench with both boards attached
**Scope:** umbrella
**Hardware:** none — the diagnosis is already measured; the fix and its test are host-side
**Owner:** no

## What was measured

Three `embarch doctor` invocations (two plain, one `--json`) all reported:

```
[11] WARN … dev-bench wire: unavailable — request to http://172.22.128.1:4884/dev-bench/hello failed: error sending request for url (…)
[13] WARN dev-bench firmware matches the local checkout — skipped — request to … failed
```

**Core did the work every time.** `C:\ProgramData\embarch\logs\dev-bench.log.2026-09-07`, read
directly, holds three handshakes at `00:23:55.53`, `00:24:17.16` and `00:24:33.90` UTC — one per
invocation, each `--- link opened on COM17 (firmware 49958d34, wire schema v15) ---` followed by
`uptime … at handshake, reset cause 0x00000000`. So the endpoint answers; `doctor` stops waiting.

**The mechanism is a source fact, not an inference.** `src/doctor.rs:1606` fetches
`/dev-bench/hello` through `authed_get`, and `authed_get` unconditionally sets
`.timeout(AUTHED_GET_TIMEOUT)` — **500 ms** (`src/doctor.rs:448`), a constant whose own doc-comment
describes it as "an *authenticated* request to an already-resolved `base_url`". There is no other
timeout on that path. `/dev-bench/hello` **opens a serial link and completes a board handshake**;
`doctor.rs:2805`'s own comment says so.

**What is *not* proven** and should not be written as though it were: the client-side error string
is reqwest's `Display`, which drops the source, so "timed out" versus "connection failed" is not
readable from the message alone. The evidence for the timeout is (a) the same client, base URL and
token succeeded on `GET /status` in the same run — check 4 `200`, check 3 pass — and (b) the source
has exactly one timeout on the path and it is 500 ms. Settle it for free by logging the error's
source chain, or by timing one authenticated `curl` of the endpoint.

## Why it matters more than a slow check

`/dev-bench/hello` is the **only** source of Core's `compatible` verdict on the bench's wire schema.
`embarch-umbrella/open.md` has carried that verdict as "the last live unknown, needing a bench" for
weeks. **A bench was never what it needed.** Two boards were attached, enrolled, validated and
handshaking, and the check still could not read the field.

**Why it sat unnoticed is *not* that the error looked like an absent bench** — `decisions/schema-skew.md`
decision 33 requires each missing-number reason to be its own named `Warn`, and the code holds it:
`HelloOutcome` has a distinct `NoBench` variant, `404` maps to it, and check 11 renders that as
`no dev-bench plugged in`, plainly different from the `unavailable — request … failed` this run
printed. **The real reason is duller:** telling the two apart requires knowing a bench was attached
*and* that Core answered, and nobody had put those two facts beside each other. It took reading
Core's own `dev-bench.log` in the same minute as the run.

Check 13 (dev-bench firmware versus the local checkout) is dark for the same reason.

## Done when

- [ ] `/dev-bench/hello` gets a budget sized for a serial handshake, distinct from the
      already-resolved-`base_url` GET budget, with the two constants separately named and each
      one's doc-comment saying what it is sized for.
- [ ] A `doctor` run on the primary bench reports check 11's **`compatible` verdict** and check 13's
      real comparison, and both are recorded — this closes `open.md`'s standing item and
      `decisions/schema-skew.md` decision 35's live debt.
- [ ] The error path distinguishes *timed out* from *could not connect* in what it prints. Today
      both render as "request … failed", which is what let this sit unnoticed.
- [ ] `decisions/reporting.md` or `decisions/schema-skew.md` records that a check whose remote call
      does real hardware work needs its own budget — the general rule, not just this call.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
