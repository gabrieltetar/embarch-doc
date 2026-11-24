# 179 — An idle-released lease drops the held token and refuses the next hardware call

**State:** open
**Source:** notes/hil/07-procedure-doc.md — "Before any hardware": an agent takes the lease with a purpose before any hardware call
**Issue:** EMB-256
**Scope:** api
**Hardware:** none
**Owner:** no

**Dispatch note (reserve):** `embarch-api/open.md` is in reserve (4,204 of
5,120 B, 916 B left), filed as `api/181` (blocked; its flux is the live-log
item only). If you add to `open.md`, first move its longest items *other than*
the live-log item into `open/` verbatim, keeping `api/181`'s Must not delete,
and say in your report whether the file is at or under 3,919 B. Do not edit
`api/181`; the supervisor closes it at the fold if the file left reserve.

## What

Core now releases a lease after 30 minutes with no hardware call (`embarch-core`
decision 123, `tasks/core/141`); after that, renew, release and `GET /lease`
answer `404` naming the holder and "released after 30 min with no hardware
call". `embarch-api`'s `lease_keepalive` logs a failed renew and retries a third
of a TTL later, keeping the held token. With no lease live Core admits every
call (`embarch-core` decision 93), and only `EMBARCH_REQUIRE_LEASE` refuses on
the client (decision 101), so the session keeps reaching hardware unleased.
When this is done:

- When a renew answers that no lease is live (Core's `404`, idle-release reason
  or not), the keepalive clears the held token and keeps the reason.
- The next hardware call from that process refuses **before** reaching Core,
  with Core's reason and "take it again with `lease_take`" (`lease-take` on the
  CLI), the way `LeaseRequiredError` refuses.
- A token given by `EMBARCH_LEASE_TOKEN` is handled the same way.
- `lease_take`'s and `lease_show`'s descriptions and the CLI's lease help say
  Core releases a lease after 30 minutes with no hardware call.

Where: `crates/embarch-core-client/src/client.rs` (`lease_keepalive`,
`HeldLease`, `refuse_without_a_live_lease`, `LeaseRequiredError`),
`src/lease.rs`, `src/tools.rs`, `src/main.rs`. The client crate is shared with
`embarch-ui` and `embarch-umbrella`: keep the change additive where you can, and
say in the report what a consumer sees.

## Why now

An agent in a Live session must take the lease again with a purpose, not drift
into unleased hardware calls. Core's half landed as `tasks/core/141`.

**Burndown leg: no new numbered decision.** Amend decisions 90 and 101 in
place. If the work needs a new decision, stop and say so in this file and your
report.

## Done when

- [ ] Against a fake Core whose renew answers the idle release, the next
      `mem_read` refuses with the reason and sends nothing to Core.
- [ ] `lease_show` then reports that this process holds no token.
- [ ] A `lease_take` after it works, and hardware calls go through again.
- [ ] The lease tools' descriptions and `interfaces/tools-lease.md` name the
      30-minute idle release.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
