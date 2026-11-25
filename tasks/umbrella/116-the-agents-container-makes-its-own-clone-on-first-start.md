# 116 — The agent's container makes its own clone on first start

**State:** claimed by agent/umbrella/116-the-agents-container-makes-its-own-clone-on-first-start, 2026-11-25 09:19
**Source:** EMB-451 — the agent's container has no clone of its own on first start
**Issue:** EMB-451
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

The agent works in its own clone inside the container, reads the person's
`embarch/` but writes only its own copy, and pushes its work where the person
can fetch it (`notes/hil/12-prevention.md`, "The repo is the boundary's one
door"). Nothing makes that clone, and `embarch init` installs the skill and
registers the MCP server with the host's `claude`, which does not reach a
container (`src/init.rs`, `skill_step`, `register_mcp`). When this is done,
umbrella renders the agent half of the container's entrypoint:
`render_entrypoint_agent(&plan) -> String`, run as uid 1000 after the root
half (decision 63's firewall). When `/work/.embarch-seeded` is absent:

1. `git -c safe.directory=/person/repo clone --no-local /person/repo
   /work/<manifest path>` (from memory: git refuses a repo another user owns
   unless named in `safe.directory`, and `--no-local` avoids hard links into a
   read-only source; mark it so in the decision);
2. `git remote add person /exchange.git`, the only remote;
3. `/work/.west/config` naming the manifest path, so decision 64's read-only
   projects form the workspace;
4. the clone's `embarch` as a link to `/outbox/embarch`, git already ignoring
   `embarch/` through the clone's own exclude; `/outbox/embarch` seeded by
   copying the person's `/person/repo/embarch/`, leaving out `embarch.toml`
   and `build/`; `embarch.toml` from the template `umbrella/115` wrote;
5. the `embarch-hil` skill from the definition folder into the clone's
   `.claude/skills/`, excluded as `init` does;
6. `claude mcp add embarch -- /opt/embarch/bin/embarch-api --config
   /work/<manifest path>/embarch/embarch.toml`, inside the container's own
   Claude config;
7. touch the marker.

**Every later start** copies any file the person's `embarch/` holds that the
agent's copy lacks, and leaves a file present in both as the agent's. The
script runs nothing from the person's repo: no hook, no `west update`, no
build. Plan choices 1, 2 and 10 are the owner's to strike; say so in the
decision. Decision 65 (`umbrella/115`) put the clone at `/work/<repo folder>`
and left it to this unit.

## Where to look

- `src/agent.rs` (decisions 62 to 64), `src/agent_init.rs` (65), `src/init.rs`
  (`SKILL_TEXT`, `add_exclude_entry`)
- `embarch-doc/notes/hil/12-prevention.md`, the boundary's rules
- `embarch-doc/embarch-umbrella/decisions/agent-container.md`

## Where the doc goes

A new decision extending 62 to 65 in `decisions/agent-container.md` (10,150 B
at dispatch, out of reserve until 11,059 B). **Do not edit 62**, which is
already over its per-decision limit. **`open.md` is in reserve** (4,634 of
5,120 B, its compaction `umbrella/111` blocked): put this unit's open items in
the decision rather than in `open.md`. If you must write there, compact it as
part of this unit, keeping `umbrella/111`'s `Must not delete:` list, and close
only that item. If your work pushes any other file into reserve, file
`tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit per
`tasks/README.md`.

## Done when

- [ ] The agent half is golden-tested.
- [ ] Run by a shell test against temp folders, with stub `git` and `claude`
      first on `PATH`, the first start makes the clone, the remote, the west
      config, the link and the seed; a second start seeds nothing but a new
      file.
- [ ] A file the agent changed in its copy is left alone on a later start.
- [ ] A hardware-verification debt is left for the owner's first container.
- [ ] Gate green.
