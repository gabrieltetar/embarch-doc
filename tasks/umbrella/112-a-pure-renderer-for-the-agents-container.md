# 112 — A pure renderer for the agent's container

**State:** open
**Source:** EMB-444 — no code renders the agent's container, its mounts or its hardening
**Issue:** EMB-444
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

No suite repo holds container code. The HIL design fixes the agent container's
hardening, mounts and tokens (`embarch-doc/notes/hil/12-prevention.md`, "A
person's act: what a UI card can prove, and what it cannot"). When this is
done, a new module `src/agent.rs` holds a typed plan and two pure renderers,
with no I/O:

- `AgentContainer { name, repo, west_workspace, class, runtime, image_tag,
  core_port, agent_token, dev_agent_token, definition_dir, exchange_dir }`;
  `container_toml(&plan) -> String` and `run_args(&plan, core_addr) ->
  Vec<String>`.
- **The mounts**, each one line of the vector: the definition folder read-only
  at `/etc/embarch-agent/`; `exchange.git` read-write at `/exchange.git`;
  `outbox/` read-write at `/outbox`; `claude-config/` read-write at
  `/home/agent/.claude`; the person's repo read-only at `/person/repo`; the work
  volume `embarch-agent-<name>` at `/work`, the west projects read-only under
  it; the agent token file alone, read-only at `/run/embarch/token`, and the
  development Core's agent token at `/run/embarch/dev-token` when it exists;
  the canonical bin dir read-only at `/opt/embarch/bin`.
- **The hardening**: `--security-opt no-new-privileges`; `--cap-drop ALL` with
  only what the root entrypoint needs added; no `--privileged`,
  `--network host`, `--pid host`, `--ipc host`, `--uts host`, `--userns host`,
  `--device`; no mount of a runtime socket, of `$HOME`, of `/mnt/c` or a drive
  root; `--env` only the variables the plan names, never `SSH_AUTH_SOCK`,
  `GIT_ASKPASS`, `VSCODE_*` or `REMOTE_CONTAINERS*`.
- **A forbidden-input test**: a fixed list of options and path suffixes scanned
  in every rendered vector; it fails on any of them, on a mount whose source is
  a token folder, and on any path ending in `person-token`.
- **Topologies**: `linux` and `wsl-host` (the owner verifies these later);
  `docker-desktop` and `macos` rendered and marked unverified in
  `container.toml`.
- `container.toml` records the vector's SHA-256, so a later `embarch agent
  status` can tell a hand-edited definition.

The owner may strike the shape: it is the plan's recommended one (plan choices
1, 2, 4, 5, 11, 24), and the decision must say so. Nothing here starts a
container, writes a file or touches `embarch init`; those are later units
(EMB-445 to EMB-448).

## Why now

EMB-444 is the root of the container chain: the firewall (EMB-445), the image
(EMB-446), `embarch init --container` (EMB-447) and starting the container
(EMB-448) all render into or start from it. Style for pure renderers:
`src/init.rs`'s `render_config`; token paths per topology: `src/setup.rs`'s
`token_path_for`, `data_dir_for`.

## Where the doc goes

A new decision file, `embarch-doc/embarch-umbrella/decisions/agent-container.md`,
naming each mount and why it is read-only or read-write. **`open.md` is in
reserve (4,634 of 5,120 B, 486 B left)** and its compaction task
`tasks/umbrella/111` is parked: do not grow `open.md`. If you must record an
open item (the unverified topologies, say), first move a section of `open.md`
verbatim into an `open/<topic>.md` file, carrying 111's `Must not delete:`
list, and leave 111 as it is. **Decisions near their per-decision limit:**
`prune-policy.md` 26, `deploy.md` 32, `mirrors.md` 20, `budgets.md` 44,
`sticky-host.md` 48, `probe-vendors.md` 49; do not grow them.

## Done when

- [ ] `run_args` is golden-tested for `linux`, `wsl-host`, `docker-desktop` and
      `macos`.
- [ ] The forbidden-input test fails when any listed option, a token folder or
      a `person-token` path is added to a plan, one case each.
- [ ] `container_toml` round-trips and records the vector's hash.
- [ ] The decision file names each mount and why it is read-only or read-write.
