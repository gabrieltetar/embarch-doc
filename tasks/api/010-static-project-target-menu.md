# 010 — A static project declares a `[[projects.targets]]` menu nothing can pick from

**State:** open
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "A `static` project's `[[projects.targets]]` menu cannot be picked from. Nothing reads the rows `list_targets` returns; a build runs the project-level `build_command`. **A `target` param, or drop them.**"
**Scope:** api
**Hardware:** none

## What

`list_targets` returns a static project's `[[projects.targets]]` rows, and nothing
consumes them: a build runs the project-level `build_command` regardless. Task 004
already made the honest half of this true — a static project now **refuses** a
selection it cannot honour rather than accepting and discarding it (`api/004`,
reversals shape 3) — which sharpens rather than closes the question: the config
still advertises a menu, and every choice on it is now explicitly rejected.

Two defensible answers, and it is yours to pick within `api`:

- **A `target` param**, so a static project's rows mean something and a build can
  select one.
- **Drop the rows** for static projects, so the config stops advertising a choice
  that does not exist, with `list_targets` and `interfaces/config.md` following.

## Why now

A menu whose every entry is refused is worse than no menu — it reads as a bug in the
caller. This is also the shape `embarch-decision-reversals.md` catalogues most
often, and task 004 fixed the silent-discard half of it while leaving the advertised
choice standing.

**Sequencing:** if task 009 (`default_target` and the `["none"]` snippet, built or
retired) is still open, work 009 first — the two answers must agree, and 009 owns
the same interface doc.

## Done when

- [ ] Either a static project accepts a target selection and honours it, or it no
      longer advertises `[[projects.targets]]` rows at all.
- [ ] `list_targets`' behaviour for a static project matches whichever was chosen,
      covered by a test.
- [ ] `interfaces/config.md` and the owning decision updated to match.
- [ ] The `embarch-api/open.md` bullet answered and removed.
- [ ] `changelog.d/` fragment dropped; `status.d/` fragment for anything suite-level
      made false; `features.d/api-*` row if the surface changed.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
