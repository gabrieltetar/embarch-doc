# 117 — `embarch agent` starts, stops and checks the agent's container

**State:** done — embarch agent up/down/status/shell over a Docker/Podman adapter, tested against a fake runtime; decision 67
**Source:** EMB-448 — nothing starts, stops or checks the agent's container
**Issue:** EMB-448
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

`embarch init --container` writes the container's definition (decisions 62 to
66), but no suite code runs a container runtime: nothing builds the image,
starts the container with the rendered vector, or says whether the definition
was changed by hand. A plain Claude Code user also needs a way in
(`notes/hil/12-prevention.md`). When this is done, `embarch agent` has four
verbs over Docker or Podman through one adapter, tested against a fake runtime.
The owner may strike plan choices 5, 6 and 9: say so in the decision.

- **A `Runtime` trait** (`build`, `image_exists`, `volume_create`, `run`,
  `stop`, `rm`, `exec`, `inspect`) with `DockerCli` and `PodmanCli`, which
  differ in the binary and nothing else unless a test shows why, and a fake
  that records every argv.
- **`embarch agent up [<name>]`**: read the definition from umbrella's state
  (decision 65's registry); build the image when no image carries the
  Containerfile's hash; create the work volume once; compute Core's address
  with `core_addr_from_container` (the WSL gateway through
  `embarch_topology::software::parse_default_gateway`, the bridge gateway
  through `inspect`) and write it to `<definition>/start/core-addr`, which the
  container reads read-only; then `run` detached with decision 62's vector,
  passing `/etc/embarch-agent/entrypoint-agent.sh` as the root half's argument
  (decision 66's open line).
- **`down`**: stop and remove the container; the volume and the exchange
  folder stay.
- **`status`**: re-render the vector from the stored plan and compare its hash
  with the one `container.toml` records; compare `<definition>/core-fingerprint`
  with the host-side `core-fingerprint` beside the token file when both exist;
  through `exec`, check Core answers and an address off the allowlist does not.
  Each finding named. Keep the fingerprint read on the definition folder's
  read-only copy, never the agent's writable seed (the `umbrella/116`
  reviewer's note).
- **`shell [--claude]`**: `exec -it -u agent -w /work/<manifest path>` into
  `bash`, or into `claude`.
- **With no runtime binary**, every verb refuses and names the install the
  owner's first-container step describes.

## Where to look

- `src/main.rs` (`Command`), `src/agent.rs` (decisions 62 to 64, 66),
  `src/agent_init.rs` (65), `src/state.rs`
- `src/setup.rs` (`run`): the existing pattern for a child process
- `embarch-topology/src/software.rs` (`parse_default_gateway`)

## Where the doc goes

A new decision. `decisions/agent-container.md` is 10,150 B at filing, out of
reserve until 11,059 B, so a full decision there likely crosses into reserve:
prefer a new topic file (for example `decisions/agent-runtime.md`) with a
one-line pointer, per `DOC-COMPACTION.md` §2. **Do not edit 62**, already over
its per-decision limit. The CLI goes in `spec.md`. **`open.md` is in reserve**
(4,634 of 5,120 B, its compaction `umbrella/111` blocked): put this unit's open
items in the decision rather than in `open.md`. If you must write there,
compact it as part of this unit, keeping `umbrella/111`'s `Must not delete:`
list, and close only that item. If your work pushes any other file into
reserve, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit per
`tasks/README.md`.

## Done when

- [x] Against the fake runtime, each verb issues the expected argv, `up`
      building only when the image is missing.
- [x] `status` fails, naming it, on a hand-edited `container.toml`, on a
      fingerprint copy that differs from the host-side one, and on a fake
      `exec` that reaches an address off the list.
- [x] With no runtime on `PATH`, each verb refuses with the install pointer.
- [x] A hardware-verification debt is left for the owner's first container.
- [x] Gate green.

## Hardware-verification debt

Nothing ran against a container runtime. On the owner's first container (Docker or Podman installed; `embarch setup` and `embarch init --container` done in a repo): `embarch agent up`; `embarch agent status` (every line `ok`); `embarch agent shell` and `--claude`; `docker inspect embarch-agent-<name>` against the vector in `container.toml`; `embarch agent down` (the volume and exchange folder remain). Also check the from-memory items in decision 67 (`network inspect` JSON, `nc` as the agent user, the Podman network name). A definition folder written before this unit needs `entrypoint-root.sh` deleted and `init --container` run again.
