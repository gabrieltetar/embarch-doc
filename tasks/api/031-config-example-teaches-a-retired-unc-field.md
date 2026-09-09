# `config.example.toml` teaches a retired UNC field and omits five live ones

**State:** done — leg 059, 2026-09-09, burndown
**Source:** owner's repo survey, 2026-09-06 — `embarch-api/spec.md:42` says the opposite of what the example teaches
**Scope:** api
**Hardware:** none
**Owner:** no

## Supervisor note — leg 059, doc-size reserve in `api`

**In reserve right now** (`check-doc-size.py --pressure`), headroom in bytes:
`decisions/tool-wrapping.md` **66**, `decisions/core-link.md` **212**, `open.md` **318**,
`spec.md` **815**, `decisions/build.md` **1154**. Plan your edits against those numbers rather
than discovering a cap mid-write. If your work pushes a file into reserve or leaves one there
that nothing has filed, file `tasks/api/<NNN>-compact-api.md` in the same commit
(`tasks/README.md` has the shape) — recording the debt, not paying it.

**One exception, and it is the file this task writes into.** `open.md` has 318 B left and its
compaction task `tasks/api/026-compact-api.md` is **blocked on `In flux: yes`** — so nobody else
can shorten it. Per `.claude/leg.md` and `DOC-COMPACTION.md` §2: **compact `open.md` as part of
this unit**, carrying `026`'s `Must not delete:` list forward and closing only `open.md`'s item
there (leave `spec.md` and `decisions/core-link.md` parked). Prefer a split or a genuine
duplicate deletion over a squeeze; you are the actor making the flux, so you are the only one who
can shorten it without writing a clean statement of something about to be wrong.

## What

`config.example.toml:69-73` documents `artifact_path_for_core` with a `\\wsl.localhost\…` example.
Nothing in `src/` or `crates/` reads that key — only two retrospective comments mention it
(`src/config.rs:278`, `:287`) — and `embarch-doc/embarch-api/spec.md:42` states "**No UNC path is
computed anywhere any more**." The same file documents none of `serial_port`, `serial_baud`,
`probe_serial`, `version_command` or `[projects.env]`, all live fields that
`embarch-doc/embarch-api/interfaces/config.md` does document, while `README.md:55` calls the
example "the full configuration schema".

The retired key and its UNC prose go. The five undocumented live fields appear as commented
examples, worded from `interfaces/config.md` so the two agree.

**Do not add a by-name load refusal for `artifact_path_for_core`.** Unlike `[[projects.targets]]`
and `soc_chip_overrides` it has none, and umbrella-scaffolded configs in the field still carry it —
refusing it would break a machine this task never saw. Record that gap in `open.md` beside the
existing umbrella bullet instead.

## Why now

`open.md`'s "Unfinished couplings" already names `artifact_path_for_core` as scaffolded-but-unread
and calls the umbrella half "a different repo's fix". The half in *this* repo's own example file is
nobody's yet, and it is the file a new engineer copies.

## Done when

- [x] `grep -c artifact_path_for_core config.example.toml` is `0`.
- [x] `serial_port`, `serial_baud`, `probe_serial`, `version_command` and `[projects.env]` each
      appear with a comment consistent with `interfaces/config.md`. (Written as `env = {...}`,
      matching that doc's own field name.)
- [x] A test loads `config.example.toml` through the real `Config` loader and asserts it parses
      (`src/config.rs::tests::config_example_toml_loads_through_the_real_loader` — its three
      `[[projects]]` placeholder `source_path`s are rewritten to a real tempdir before load,
      since `validate()` requires each to exist).
- [x] `embarch-doc/embarch-api/open.md` names the silently-dropped-key gap explicitly (the
      `artifact_path_for_core` bullet under "Unfinished couplings" now also states there is
      deliberately no by-name load refusal for it, and why).
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`/`test`/`clippy` clean in
      `embarch-api`, `check-docs.py` all green in `embarch-doc`.
- [x] `spec.md`/`decisions.md`/`open.md` updated (`spec.md` already said the correct thing —
      the bug was only in the example file — so no change there; no new decision, per this leg's
      burndown constraint; `open.md` updated and, per the supervisor note, compacted from
      4,802 B to 3,782 B, clearing the reserve line), `changelog.d/` fragment dropped
      (`api-config-example-drops-unc-field.fixed.md`). No suite-level fact changed, so no
      `status.d/` fragment.
- [x] `open.md`'s compaction recorded in `tasks/api/026-compact-api.md` (its own item closed;
      `spec.md`/`decisions/core-link.md` left parked, per the supervisor note's scope).
