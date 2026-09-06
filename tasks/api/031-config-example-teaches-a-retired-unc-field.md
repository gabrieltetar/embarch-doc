# `config.example.toml` teaches a retired UNC field and omits five live ones

**State:** open
**Source:** owner's repo survey, 2026-09-06 — `embarch-api/spec.md:42` says the opposite of what the example teaches
**Scope:** api
**Hardware:** none
**Owner:** no

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

- [ ] `grep -c artifact_path_for_core config.example.toml` is `0`.
- [ ] `serial_port`, `serial_baud`, `probe_serial`, `version_command` and `[projects.env]` each
      appear with a comment consistent with `interfaces/config.md`.
- [ ] A test loads `config.example.toml` through the real `Config` loader and asserts it parses.
- [ ] `embarch-doc/embarch-api/open.md` names the silently-dropped-key gap explicitly.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
