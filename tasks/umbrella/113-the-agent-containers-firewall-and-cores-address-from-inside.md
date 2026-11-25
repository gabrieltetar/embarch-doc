# 113 — The agent container's firewall, and Core's address from inside

**State:** claimed by agent/umbrella/113-the-agent-containers-firewall-and-cores-address-from-inside, 2026-11-25 06:51
**Source:** EMB-445 — nothing limits the agent container's network to Core and the model API
**Issue:** EMB-445
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

The agent's container may reach Core's port and the model's API and nothing
else, embarch-ui's port above all, since the UI holds the person's token; the
rules are set before the agent starts, by a root half the agent cannot change
(`embarch-doc/notes/hil/12-prevention.md`, the boundary's rules). Nothing
renders such rules. When this is done, `src/agent.rs` (from `umbrella/112`)
has, pure and with no I/O:

- `render_entrypoint_root(&plan) -> String`, a POSIX shell script run as root
  before anything else: set `OUTPUT` and IPv6 `OUTPUT` to drop; allow loopback
  and established flows; allow DNS to the resolver in `/etc/resolv.conf`; allow
  TCP to Core's address and port only; resolve each allowlisted host now and
  allow TCP 443 to those addresses; then check one: a connection to Core
  succeeds and one to an address off the list fails, else exit non-zero so the
  container never reaches the agent. Then drop to the agent user (uid 1000)
  with no capabilities, inheritable, ambient and bounding sets cleared, and
  exec the agent half. From the issue, unverified: `iptables`, `ipset` and
  util-linux `setpriv` do this, and the root half needs `NET_ADMIN`,
  `NET_RAW`, `SETUID`, `SETGID` and `SETPCAP`. `run_args`'s `--cap-add` list
  takes exactly those, which adds `SETPCAP` to decision 62's four.
- **The allowlist is data** in `container.toml` (`[network] allow`), which only
  the person's account writes: Core's `addr:port`, and the model API's hosts,
  `api.anthropic.com` plus the hosts a login needs (from the issue, to be
  measured later). `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` in the agent's
  environment (from the issue, unverified). `parse_container_toml` round-trips
  it.
- `core_addr_from_container(class, runtime, wsl_gateway, bridge_gateway) ->
  Result<String>`, a pure table: `linux`, the runtime bridge's gateway, with an
  error or note that Core must be bound to it or to `0.0.0.0`; `wsl-host`, the
  WSL gateway the host side finds with
  `embarch_topology::software::parse_default_gateway`; `docker-desktop` and
  `macos`, `host.docker.internal` (unverified). Mirrored networking is a row a
  later measurement fills; leave it out or refuse it, and say which.
- **No rule names any port on Core's host but Core's own.**

The owner may strike this: plan choices 7, 8 and 9. The decision must say so.
Nothing here starts a container or writes a file; `embarch agent up` (EMB-448)
calls these later.

## Why now

EMB-445 and EMB-446 are the two links after `umbrella/112` on the container
chain: `embarch init --container` (EMB-447) waits on both. Design:
`embarch-doc/notes/hil/14-implementation-plan.md`; `embarch-topology`'s
`recommended_bind_address` for the bind each class expects; umbrella decision
22 (`decisions/bind.md`) for the bind checks a container topology adds to.

## Where the doc goes

**`decisions/agent-container.md`'s decision 62 is already 60 B over its
per-decision limit** (`check-doc-size.py --pressure`): do not grow it. Write a
new decision 63 in the same file for the firewall's rules, the address table
and the capability list, saying it supersedes 62's capability clause, and say
that the agent half holds no capability at all. **`open.md` is in reserve
(4,634 of 5,120 B, 486 B left)** and its compaction task `tasks/umbrella/111`
is parked: do not grow `open.md`. If you must record an open item (the
mirrored-networking row, the login hosts), first move a section of `open.md`
verbatim into an `open/<topic>.md` file, carrying 111's `Must not delete:`
list, and leave 111 as it is. **Other decisions near their limit:**
`prune-policy.md` 26, `deploy.md` 32, `mirrors.md` 20, `probe-vendors.md` 49,
`sticky-host.md` 48, `budgets.md` 44; do not grow them.

## Done when

- [ ] The root script is golden-tested for each topology, with the allowlist
      from a fixture `container.toml`.
- [ ] A test fails when a rendered rule allows a port on Core's host other
      than Core's.
- [ ] The rendered script exits non-zero on a failed check, read as text in
      the test.
- [ ] `core_addr_from_container` has one test per row, and the `linux` row's
      note about Core's bind is in its error text.
- [ ] The decision names every capability the root half holds and says the
      agent half holds none.
