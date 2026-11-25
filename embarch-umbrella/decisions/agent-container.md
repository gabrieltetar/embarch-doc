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
