# 141 — Core releases a lease after 30 minutes with no hardware call

**State:** claimed by agent/core/141-core-releases-a-lease-idle-for-30-minutes, 2026-11-23 17:21
**Source:** notes/hil/01-modes.md — "The lease": a Live lease is released at the end or after 30 min with no hardware call, which Core enforces itself whatever client renews
**Issue:** EMB-251
**Scope:** core
**Hardware:** none
**Owner:** no

## What

A lease today ends only on release, on TTL expiry or on a Core restart
(`src/lease.rs`, `LeaseSlot`), and Core keeps no time of a lease's last hardware
call. `embarch-api`'s keepalive renews every third of the TTL while its MCP
server runs, so an MCP-held lease never expires. When this is done, Core itself
releases a lease that has made no hardware call for 30 minutes, whatever client
renews it.

- A **hardware call** is a call to a `LEASE_GATED` route admitted with the
  lease's token; `lease_middleware` stamps its time on the lease. Renew, show,
  status and every lease-open route are not hardware calls, and a call refused
  for a wrong token does not count.
- Evaluated lazily, as expiry already is: a lease whose last hardware call, or
  its start, is 30 minutes old is released the next time anything asks. One
  named constant, 1800 s.
- **A lease is not idle while a study run is in flight** (`study_lock` held);
  the clock restarts when the run ends. A study's steps call no route, so
  without this a study over 30 minutes would lose its lease mid-run.
- Core keeps the last release's reason in memory, so a renew after it is
  refused naming "released after 30 min with no hardware call" and the holder,
  apart from a plain expiry. `GET /lease` shows the last hardware call's time
  while the lease is live.
- Applies to every lease, CLI-taken ones included.

`embarch-api`'s client learning of the release and stopping its renewals is a
separate unit (EMB-256), and so is any change to `embarch-api`'s lease tool
docs; this task changes Core and Core's docs only.

## Why now

The owner's HIL Live phase (`notes/hil/14-implementation-plan.md`;
`notes/hil/05-live.md`, "Reach and permission"; review round 4, owner
2026-11-20). A forgotten Live session otherwise holds the bench all day.

**Doc headroom:** decision 93 (`decisions/lease.md`) has about 180 B left, so
the rule will not fit there. Record it as a new decision and amend 93 by a short
pointer to it. `decisions/signing.md` decision 110 is already over its cap;
leave it alone.

## Done when

- [ ] A test with a forced clock: a lease renewed every minute with no hardware
      call is gone 30 minutes after its start.
- [ ] A hardware call with the token restarts the clock; a call with a wrong
      token does not.
- [ ] With a study in flight the lease is kept past 30 minutes, and released 30
      minutes after the study ends if no call came.
- [ ] A renew after the release is refused naming the idle release and the
      holder.
- [ ] Decision 93 is amended with the rule (by a pointer, per the headroom
      above).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment
      dropped, `status.d/` fragment for anything suite-level it made false.
