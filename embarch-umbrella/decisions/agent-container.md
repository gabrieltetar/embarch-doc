# embarch-umbrella decisions: the agent's container

**Status:** active, 2026-11-25.

What the agent's container is made of, as one pure function. Index: [../decisions.md](../decisions.md). Design: [notes/hil/12-prevention.md](../../notes/hil/12-prevention.md), "A person's act".

### 62 — The container is rendered by pure functions in `src/agent.rs`, and the person's token is never one of its mounts

**This is the plan's recommended shape (plan choices 1, 2, 4, 5, 11, 24), not an owner-struck one; the owner may strike it.** `AgentContainer` is a typed plan; `run_args(&plan, core_addr)` and `container_toml(&plan)` return text and do nothing else. Starting the container, writing files and `embarch init` are later units (EMB-445 to EMB-448). `try_run_args` is the entry a caller that will act must use: it refuses a vector `forbidden_findings` names. Each mount is one `--mount=type=...` element, so a path with a colon cannot split it.

**The mounts, and why each is read-only or read-write:**

| Target | Source | Mode | Why |
|---|---|---|---|
| `/etc/embarch-agent` | the definition folder (`~/.config/embarch/agents/<name>/`) | read-only | It is what the person approved; an agent that could edit it could widen its own container. |
| `/exchange.git` | `<exchange>/exchange.git` | read-write | The one door out: the agent pushes, the person fetches, and nothing the clone holds runs on the host. |
| `/outbox` | `<exchange>/outbox/` | read-write | The writable `embarch/` copy, on a folder the person's tools never build in. |
| `/home/agent/.claude` | `<exchange>/claude-config/` | read-write | The agent CLI's own state; it must write it, and it is nowhere the host reads. |
| `/person/repo` | the person's repo | read-only | The agent reads it; its writes must not reach what the host builds. |
| `/work` | volume `embarch-agent-<name>` | read-write | The agent's clone lives in a volume the container owns, so no host path holds its working tree. |
| `/work/<project>` | each west project | read-only | The toolchain's modules are inputs, and a write there would be code the host later builds. |
| `/run/embarch/token` | the agent token file alone | read-only | The only token it holds. A file, never a folder. |
| `/run/embarch/dev-token` | the development Core's agent token | read-only | Rendered only when the plan names one (the file exists). |
| `/opt/embarch/bin` | the canonical bin dir | read-only | A writable binary the person later runs would be an escape. |

**The hardening:** `no-new-privileges`; `--cap-drop=ALL` and then `NET_ADMIN`, `NET_RAW`, `SETUID`, `SETGID` for the root entrypoint that applies the firewall and drops to the agent user (**assumed, not measured**: EMB-445 and EMB-446 settle the list). `--env` carries only `EMBARCH_*` variables and the plan's own `env`. The scan refuses `--privileged`, a `host` network, pid, ipc, uts or user namespace, `--device`, a `--cap-add` or `--security-opt` outside the list, `--env-file`, an inherited `--env NAME`, `SSH_AUTH_SOCK`, `GIT_ASKPASS`, `VSCODE_*`, `REMOTE_CONTAINERS*`, a runtime socket, a home folder or drive root as a mount source, a token folder, a token file anywhere but the two token targets, a mount that should be read-only and is not, a target the plan does not name, and any path ending in `person-token`.

**Topologies.** `linux` and `wsl-host` are the ones the owner verifies later; `docker-desktop` and `macos` are rendered and `container.toml` marks them `topology_verified = false`. They differ only in `--add-host=host.docker.internal:host-gateway`, which Docker Desktop and the macOS VMs already resolve. **The WSL host's Core address is the caller's to resolve** (decision 9), as `core_addr`.

**`container.toml` records the vector's SHA-256, taken with the Core address replaced by a placeholder**, since the address is re-resolved at every use and never persisted (decision 6). It records the vector too, so `embarch agent status` can tell a hand-edited definition by re-hashing it.

**Where the unit departs from the task's field list:** the plan also carries `bin_dir` (the canonical bin dir has no other source) and `env` (the "variables the plan names"); `west_workspace` is a list of named projects, each mounted read-only under `/work`; `container_toml` takes no `core_addr`, for the reason above. **Unverified:** no container was started; every mount, capability and flag is rendered from the design, never run.

### 63 — The firewall is a root script rendered from data, the capabilities are five, and the agent half holds none

**This is the plan's recommended shape (plan choices 7, 8 and 9), not an owner-struck one; the owner may strike it.** It **supersedes 62's capability clause**: the root half holds `NET_ADMIN`, `NET_RAW`, `SETUID`, `SETGID` and **`SETPCAP`** (`run_args` adds the fifth; `setpriv` needs it to clear the bounding set). **The agent half holds no capability**: the script ends in `setpriv` to uid 1000 with the inheritable, ambient and bounding sets cleared and `no-new-privs`, and `--cap-drop=ALL` stays. **Assumed, not measured:** no container was started; `iptables`, `ipset`, `nc`, `getent` and util-linux `setpriv` are assumed to be in the image.

`render_entrypoint_root(&plan, core_host)` returns a POSIX script, pure text. It sets IPv4 and IPv6 `OUTPUT` to drop, then allows loopback, established flows, DNS to the IPv4 resolvers in `/etc/resolv.conf`, TCP to Core's resolved address on Core's port, and TCP 443 to an `ipset` of the allowlisted hosts' addresses (resolved at start). It then checks, and exits 1 before the drop if a connection to Core fails or one to `192.0.2.1:443` succeeds, so a bad firewall never reaches the agent. `core_host` is a parameter beside the plan, as `core_addr` is to `run_args`: the address is never persisted (decision 6). **No rule names a port on Core's host but Core's:** an allowlisted host that resolves to Core's own address is skipped, and `core_host_findings` is the test's scan for any other rule naming it. The check does not probe another port on Core's host; the rules are asserted as text, not exercised.

**The allowlist is data.** `container.toml` holds `[network] allow`: `<core-addr>:<port>` (the placeholder, like the hash) and the model API's hosts, `api.anthropic.com` plus the hosts a login needs (**to be measured**). `parse_container_toml` round-trips it. The agent's environment gains `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` (**unverified**).

**`core_addr_from_container(class, runtime, wsl_gateway, bridge_gateway)`** returns a host with no port: `linux` the runtime bridge's gateway, an error naming that **Core must be bound to it or to `0.0.0.0`** when none is given (`embarch_topology::recommended_bind_address` is the bind; decision 22's checks are not extended here); `wsl-host` the WSL gateway (`parse_default_gateway`), an error when none; `docker-desktop` and `macos` `host.docker.internal` (**unverified**). **Mirrored WSL networking is left out**, not refused: it is not a class, and a later measurement adds its row.
