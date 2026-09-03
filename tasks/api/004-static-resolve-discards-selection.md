# 004 — A static project silently discards everything the caller selected

**State:** done, 2026-09-03 — branch `agent/api/004-static-resolve-discards-selection` in `embarch-api` and `embarch-doc`, pushed, not merged.
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

- [x] A static-discovery project given a selection field it cannot honour fails
      with an error that names the fields and the reason, rather than succeeding.
- [x] The empty/default case is unchanged: a static project resolved with no
      selection still resolves exactly as it does today. Confirm this against
      the existing `resolve_static_*` tests rather than by reading.
- [x] Whatever the CLI and MCP surfaces do with the new error is coherent — a
      caller sees the reason, not a panic and not a bare `anyhow` chain.
- [x] Unit tests at the `resolve` boundary for both the rejected and the
      unaffected case.
- [x] `embarch-api/spec.md` says what a static project does with a selection,
      and `open.md`'s first "Known wrong" bullet is rewritten to whatever is
      still open (or removed if nothing is).
- [x] Gate green (`embarch-parallel-agents.md` §10).
- [x] `changelog.d/` fragment dropped.

## Not in scope

The other two bullets under "Known wrong, not fixed" — the inferred `board`
field and the build-log head/tail cap — are separate and are not to be touched
here. The board one is not even this repo's `init`.

## What was done

**The premise was checked and is true, and it is wider than `open.md` said.** Both
front-ends do nothing with these params except hand them to `resolve` —
`TargetSelection::selection` (CLI), `TargetParams`/`FlashParams`/`RunStudyParams`
`::selection` (MCP) are the only construction sites, and `reflash.rs` passes its
`Selection` straight through. So all six fields were discarded identically; none
was honoured upstream. All six are now refused together, in `resolve_static`.

**Reject, as expected** — reasoning in `embarch-api` decision 51. The empty case
is asserted unchanged over the whole `Resolved`, not just the error path.

Surface text moved with it: MCP tool descriptions (`build`, `flash`,
`build_and_flash`, `reset`, `run_study`), every selection param's description,
CLI help, and `config.example.toml` now say *refused*, not *ignored*.
`interfaces/tools.md` was **not** edited — it was 3 bytes under its 12 KB cap and
already points at `interfaces/config.md` for selection semantics, which carries
the new rule.

## Found on the way, not fixed (now in `embarch-api/open.md`)

- `[[projects.targets]]` rows are advertised by `list_targets` and read by
  nothing else, so a `static` project's menu cannot be picked from at all.
- Decisions 20 (`default_target`) and 21 (the `["none"]` snippet sentinel) are
  documented in `interfaces/config.md` as truth and exist nowhere in the crate.
  `suite/user-guide.md` §5.2 repeats the sentinel claim — `status.d/api-user-guide-snippet-none.md`
  carries that one, since a worker does not edit a suite-level doc.

## Hardware-verification debt

None. The change is config in, error or plan out; every claim here is covered by
host unit tests.
