# embarch-core decisions: The idle lease release

**Status:** active, 2026-11-23 (`tasks/core/141`, `notes/hil/01-modes.md` "The lease"; `notes/hil/05-live.md` "Reach and permission"). Index: [../decisions.md](../decisions.md). Surface: [../interfaces/hardware.md](../interfaces/hardware.md). Sibling: [lease.md](lease.md) (decision 93, which this extends).

### 123 — Core releases a lease that has made no hardware call for 30 minutes, whatever client renews it

`embarch-api`'s keepalive renews every third of the TTL while its MCP server runs, so a lease held by a forgotten session never expired and parked the bench all day. TTL expiry cannot be the answer: a renew is exactly what a forgotten client still sends. The owner's rule is that a Live lease ends at the end or after 30 minutes with no hardware call, and **Core enforces it itself** so no client has to.

**A hardware call** is a request to a `LEASE_GATED` route admitted with the lease's token: `lease_middleware` (through `LeaseSlot::admit`) stamps it. Renew, show, status and the lease-open routes are not hardware calls, and a call refused for a wrong token stamps nothing. A lease with no call counts from its start.

**Lazy, like expiry** (decision 93): no timer; at each check a lease whose clock (`IDLE_RELEASE`, 1800 s, one constant) is 30 minutes old is not live. **[assumed]**: 30 minutes is the owner's figure, not measured. It applies to every lease, CLI-taken ones included.

**Not idle while a study runs** (`study_lock` held, for `/study`, `/host-studies` and hello): a study's steps call no route, so a study over 30 minutes would lose its lease mid-run. The clock restarts when the run ends: both run-ending sites call `LeaseSlot::study_ended` *before* clearing the lock, so no check can see the lock free with a stale clock. A lease taken during a study counts from the run's end.

**The reason is kept in memory**: the holder of the last lease that ended idle, until the next take or a release. A `PUT`, `DELETE` or `GET /lease` after it is `404` naming the holder and "released after 30 min with no hardware call", apart from a plain expiry's text. `GET /lease` shows `last_hardware_call_at` while live.

**2026-11-25:** a Test run holding the lease is never idle ([test-run-go.md](test-run-go.md), 135).

**Known gap:** a pending call-log read fold (decision 122) is not flushed by an idle release, as it is not by an expiry; the next different call or a clean stop writes it.

**The client half is `embarch-api`'s** (EMB-256): learning of the release and stopping its renewals.
