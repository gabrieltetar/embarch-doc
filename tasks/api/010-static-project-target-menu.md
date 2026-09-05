# 010 — A static project declares a `[[projects.targets]]` menu nothing can pick from

**State:** done, agent/api/010-static-project-target-menu, 2026-09-05
**Source:** [embarch-api/open.md](../../embarch-api/open.md) — "A `static` project's `[[projects.targets]]` menu cannot be picked from. Nothing reads the rows `list_targets` returns; a build runs the project-level `build_command`. **A `target` param, or drop them.**"
**Scope:** api
**Hardware:** none

**Doc-size reserve (supervisor, 2026-09-05):** four `api` files are already in the
last 10% of their caps and **all four are already filed against
`tasks/api/012-compact-api.md`** — `decisions/zephyr.md` 99.2% (96 B left),
`open.md` 97.3% (139 B), `spec.md` 96.5% (357 B), `interfaces/config.md` 92.6%
(914 B). Plan your edits around that headroom; prefer replacing text to appending
it. You owe **no new compaction task** — 012 already covers every one of them —
but say in your report if you spent so much of a reserve that 012 is now urgent.

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

- [x] Either a static project accepts a target selection and honours it, or it no
      longer advertises `[[projects.targets]]` rows at all.
- [x] `list_targets`' behaviour for a static project matches whichever was chosen,
      covered by a test.
- [x] `interfaces/config.md` and the owning decision updated to match.
- [x] The `embarch-api/open.md` bullet answered and removed.
- [x] `changelog.d/` fragment dropped; `status.d/` fragment for anything suite-level
      made false; `features.d/api-*` row if the surface changed.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Answer

**Dropped the rows** (`embarch-api` decision 53, in `decisions/shape.md` — not
`decisions/zephyr.md`, which has 96 B of headroom and could not take an entry).

*Rejected: a `target` param.* It is buildable and does **not** contradict
decision 51 — a row replaces the whole argv rather than splicing into one — but
it would add a second, differently-shaped selection grammar to
`build`/`flash`/`build_and_flash`/`reset`/`run_study` and the CLI for a feature
**no config in this suite uses**: the rows are absent from
`config.example.toml`, from `/home/gabriel/.config/embarch/`, and from every
other repo's docs and source, and every field a row can carry is already
expressible as one more `[[projects]]` entry.

Two things make the removal lossless rather than merely smaller:

- `list_targets` for a `static` project **no longer errors** demanding a menu.
  It returns exactly one row — the project itself, with its configured
  `build_command`, `chip` and *resolved* `artifact_path` — so the tool answers
  "what can I build?" for every project kind, and the row it names is the build
  a bare `build` actually runs. Covered by
  `list_targets_reports_a_static_project_as_its_own_single_target` in
  `src/resolve.rs`.
- A config still carrying `[[projects.targets]]` **fails at load naming the
  retirement** rather than parsing into a field nothing reads — decision 51's
  reject-rather-than-ignore posture applied to config. Covered for both
  discovery kinds in `src/config.rs`.

**No hardware-verification debt**: every path here is config and JSON shape,
exercised host-side, and `tests/json_surface.rs` drives the real binary.

**Doc-size:** `spec.md` spent ~220 B of its reserve (357 B → 135 B left);
`interfaces/config.md` net +41 B (873 B left); `open.md` shrank by 209 B.
`tasks/api/012-compact-api.md` already covers all three. Nothing new filed.
