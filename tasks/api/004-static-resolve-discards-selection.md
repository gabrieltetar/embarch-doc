# 004 — A static project silently discards everything the caller selected

**State:** claimed by agent/api/004-static-resolve-discards-selection, 2026-09-03 12:10
**Source:** embarch-api/open.md — "**`snippets` is accepted, silently discarded, and reported as success** for a project with an explicit build command"
**Scope:** api
**Hardware:** none

## What

`resolve::resolve` dispatches on `project.discovery`. The `ZephyrWest` arm
consumes the whole `Selection`; the `Static` arm takes `&ProjectConfig` only and
**never looks at `selection` at all** — `resolve_static(project)` builds its
`Resolved` entirely from config. So for a project with an explicit
`build_command`, every one of `board`, `variant`, `revision`, `app`, `snippets`
and `extra_args` is accepted, dropped on the floor, and the build reports
success. `open.md` records the observed cost: a build with two snippets returned
success having produced an image whose config said the option was unset.

Note that `open.md` names only `snippets`, and the source says the problem is
wider than the bullet does — **verify that for yourself before you widen the
fix**, and if the other five turn out to be honoured somewhere upstream of
`resolve`, fix what is actually broken and say so rather than following this
paragraph.

`open.md` states the fork: **reject them, or splice them in.** Splicing a
snippet into an opaque, caller-supplied `build_command` is not something this
crate can do correctly — there is no `-S` to add to a command it did not
assemble. So the expected answer is **reject**, with an error naming which
fields were given and that this project's `discovery = "static"` cannot honour
them. Reach the other conclusion if the code says otherwise, but say why.

The help text claiming snippets are Zephyr-discovery-only is documentation, not
a gate; this task turns that sentence into the gate.

## Why now

It is the first item under `embarch-api/open.md`'s **"Known wrong, not fixed"**,
it has a recorded real-world cost, and it violates the surface's own contract
that a success means what was asked for is what was built. It is entirely
host-side: config in, error or plan out.

## Done when

- [ ] A static-discovery project given a selection field it cannot honour fails
      with an error that names the fields and the reason, rather than succeeding.
- [ ] The empty/default case is unchanged: a static project resolved with no
      selection still resolves exactly as it does today. Confirm this against
      the existing `resolve_static_*` tests rather than by reading.
- [ ] Whatever the CLI and MCP surfaces do with the new error is coherent — a
      caller sees the reason, not a panic and not a bare `anyhow` chain.
- [ ] Unit tests at the `resolve` boundary for both the rejected and the
      unaffected case.
- [ ] `embarch-api/spec.md` says what a static project does with a selection,
      and `open.md`'s first "Known wrong" bullet is rewritten to whatever is
      still open (or removed if nothing is).
- [ ] Gate green (`embarch-parallel-agents.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Not in scope

The other two bullets under "Known wrong, not fixed" — the inferred `board`
field and the build-log head/tail cap — are separate and are not to be touched
here. The board one is not even this repo's `init`.
