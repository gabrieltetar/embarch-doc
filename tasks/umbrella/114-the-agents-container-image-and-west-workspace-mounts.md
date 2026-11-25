# 114 — The agent's container image and its west workspace mounts

**State:** open
**Source:** EMB-446 — the agent's container has no toolchain image and no view of the west workspace
**Issue:** EMB-446
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

Firmware builds run inside the agent's container, through EmbArch's build, so
the container needs the toolchain and the west workspace the repo builds in
(`notes/hil/12-prevention.md`, the boundary's costs and "Open"). Nothing
renders an image or says which workspace projects to mount. When this is done,
`src/agent.rs` (`umbrella/112`, `umbrella/113`) gains, pure:

- **`render_containerfile(&plan) -> String`**: a Debian or Ubuntu base; the
  Zephyr SDK at the version the person's workspace pins (`zephyr/SDK_VERSION`,
  read on the host by `init`); west and the workspace's Python requirements
  (`zephyr/scripts/requirements*.txt`); `git`; **every binary decision 63's
  root script calls** — `iptables`, `ip6tables`, `ipset`, `nc`, `getent`,
  `timeout`, `setpriv` — with the package that provides each; Claude Code
  installed as its documentation says (from memory, marked so); a user `agent`,
  uid 1000, with no `sudo`. The image tag is the SHA-256 of the rendered text,
  so a changed Containerfile is a new image and an unchanged one is not.
- **`west_mounts(west_list: &str, manifest_path: &str) -> Vec<Mount>`**: parses
  `west list -f "{path} {abspath}"` as run on the host by `init` (the format
  string from memory; say so, to be checked against the installed west). Every
  project but the manifest repo becomes a read-only bind at `/work/<path>`; the
  manifest repo's path is left for the agent's own clone (EMB-451). `zephyr/`
  and the modules are third-party code the container reads and never writes.
- **A repo that is not Zephyr and west** gets no workspace mounts and a
  Containerfile comment where its toolchain lines go; that case is otherwise
  out of this pass.
- EmbArch's own Linux binaries are not in the image: decision 62 already mounts
  the canonical bin dir read-only.

Reuse the existing Zephyr and west detection (`src/zephyr.rs`,
`looks_zephyr_west_shaped`; `src/init.rs`, `parse_west_command`, `split_argv`;
umbrella decisions 17 and 41) rather than a second one. Plan choice 10 (the
image's shape) is the owner's to strike, and the decision says so. Nothing
builds or runs the image here; that is EMB-448's.

## Why now

`umbrella/112` and `umbrella/113` landed the renderer and the firewall script
this extends; `umbrella/113`'s decision 63 assumes the image carries the
firewall's binaries, and this is where that assumption is met. EMB-447,
EMB-451, EMB-448 and EMB-461 wait on it in that order.

## Where to look

- `src/agent.rs`, `src/zephyr.rs`, `src/init.rs`
- `embarch-doc/embarch-umbrella/decisions/agent-container.md` (62, 63),
  `decisions/projects.md` (17, 41)
- `embarch-doc/notes/hil/12-prevention.md`

## Where the doc goes

A new decision 64 in `decisions/agent-container.md`. **Decision 62 is 61 B over
its per-decision limit: do not edit its body**; 64 says what it extends, as 63
did. Keep the open items in 64, as 62 and 63 did. **In reserve:**
`embarch-umbrella/open.md` (486 B left), filed against
`tasks/umbrella/111-compact-umbrella.md`, `blocked` with `In flux: yes`. Do not
write into it; if your work must, compact that file as part of this unit,
keeping 111's `Must not delete:` list, and say so in this file. **Decisions
near their per-decision limit:** `prune-policy.md` 26 (19 B left),
`deploy.md` 32 (29 B left), `mirrors.md` 20 (32 B left); do not grow them. If
your work pushes another file into reserve, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] The Containerfile is golden-tested, with the SDK version read from a
      fixture workspace, and installs every binary decision 63's script calls.
- [ ] A fixture `west list` output gives the expected read-only mounts, the
      manifest repo absent from them.
- [ ] A non-west fixture gives no mounts and the toolchain comment.
- [ ] The image tag changes when the rendered text changes, and only then.
- [ ] Decision 64 records it.
- [ ] Gate green.
