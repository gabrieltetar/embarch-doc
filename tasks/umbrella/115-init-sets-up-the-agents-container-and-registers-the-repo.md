# 115 — `init` sets up the agent's container and registers the repo

**State:** claimed by agent/umbrella/115-init-sets-up-the-agents-container-and-registers-the-repo, 2026-11-25 08:28
**Source:** EMB-447 — `embarch init` cannot set up the agent's container outside the repo
**Issue:** EMB-447
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

The design has `embarch init` set up the agent's container, with its
definition in a folder in the person's account, outside the repo, and has the
elevated install write `embarch/core-fingerprint` "in each firmware repo
`embarch init` registered" (`notes/hil/12-prevention.md`). Today `init` writes
only inside the repo (`src/init.rs`), and umbrella's state (`src/state.rs`,
`State`) holds no list of repos. When this is done:

- **`embarch init --container [--runtime docker|podman]`**, after today's
  steps, renders `umbrella/112` to `114`'s outputs (`src/agent.rs`: the run
  arguments, the firewall script, the Containerfile) into the definition folder
  `~/.config/embarch/agents/<name>/` (Windows `%APPDATA%\embarch\agents\<name>\`),
  `<name>` being the repo folder's name, with a suffix when that name is taken
  by another repo. It creates the exchange folder
  `~/.local/share/embarch/agents/<name>/` (Windows `%LOCALAPPDATA%`) holding a
  bare `exchange.git`, `outbox/` and `claude-config/`.
- **The clone's config template** in the definition folder:
  `[core] base_url = "auto"` (container mode overrides it later),
  `build_dir_root` under `/work/build`, `[publish] folder = "/outbox/publish"`.
- **Every `init` registers the repo** in umbrella's state:
  `registered_repos`, each with its path and, when there is one, the
  container's name and folders. A repo without a container is registered too,
  so it still gets its `core-fingerprint` later. The field defaults, so a state
  file without it loads.
- **It prints the person's fetch line**:
  `git fetch <exchange.git> '+refs/heads/*:refs/remotes/agent/*'`. The elevated
  fingerprint writer (the plan's C.8, not yet built) does not exist: print
  nothing for it, and say in the decision that it adds its own line.
- **`--uninstall`** removes the repo from state and, only after a typed yes,
  the definition and exchange folders, warning that the exchange may hold work
  not yet fetched. **`--dry-run`** names every folder and file and writes
  nothing.
- Nothing tracked in the repo changes, as today. Nothing builds or starts the
  image here (EMB-448).

Plan choices 1, 2, 4, 11 and 17 (folder locations, the name and its suffix,
the registry in umbrella's state, the fetch refspec, the uninstall prompt) are
the owner's to strike, and the decision says so.

## Why now

`umbrella/112`, `113` and `114` landed every pure renderer this writes out;
`init` is the first caller. EMB-451 (the agent's clone), EMB-448 (the image's
first build and start) and the elevated fingerprint writer start from the
folders and the registry written here. Decision 64's reviewer noted that the `NotWest` comment
says no workspace is mounted while `run_args` renders `west_workspace` mounts
independently of the toolchain: make the two agree where `init` builds the
plan, and say which way in the decision.

## Where to look

- `src/init.rs` (`init`, `print_plan`, `uninit`), `src/state.rs` (`State`,
  `STATE_SCHEMA_VERSION`), `src/agent.rs`
- `embarch-doc/embarch-umbrella/decisions/projects.md`,
  `decisions/agent-container.md` (62, 63, 64)
- `embarch-doc/notes/hil/12-prevention.md`

## Where the doc goes

A new decision in `decisions/projects.md`, as the issue asks; it says what it
extends in `agent-container.md`. **Decision 62 is 61 B over its per-decision
limit: do not edit its body.** **In reserve:** `embarch-umbrella/open.md`
(486 B left), filed against `tasks/umbrella/111-compact-umbrella.md`, `blocked`
with `In flux: yes`. Do not write into it; keep this unit's open items in the
new decision. If your work must touch it, compact that file as part of this
unit, keeping 111's `Must not delete:` list, and say so here. **Decisions near
their limit, do not grow:** `prune-policy.md` 26 (19 B left), `deploy.md` 32
(29 B), `mirrors.md` 20 (32 B), `probe-vendors.md` 49, `sticky-host.md` 48,
`budgets.md` 44. If your work pushes another file into reserve, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] On a temp repo with a temp home, `init --container` writes every listed
      file and folder, and `git status --porcelain` in the repo is empty after.
- [ ] State lists the repo with and without `--container`; a state file
      without the field loads.
- [ ] `--uninstall` removes the state entry and, only after a typed yes, the
      folders.
- [ ] `--dry-run` writes nothing and names every path.
- [ ] A new decision in `projects.md`.
- [ ] Gate green.
