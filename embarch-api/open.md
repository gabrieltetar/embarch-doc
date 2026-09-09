# embarch-api: open questions

**Status:** active, 2026-09-09.

Current truth: [spec.md](spec.md). Rationale: [decisions.md](decisions.md).

## Known wrong, not fixed

- **A `[[projects]]` `board` is a hardware fact nothing compares against the hardware.** Derived from `build_info.yml`, it names the last build, not the board on the desk — a mismatched revision costs a day of bring-up. Violates [spec.md](spec.md) §2's no-inference-as-fact invariant. `init` stopped writing one unconfirmed (`embarch-umbrella` decision 41), but every older config still asserts one, and comparing it to real hardware is unbuilt.

## Unfinished couplings

- **The alert/enrolled-board response types were unpinned mirrors, and it fired**: `link_port_interface` (`embarch-topology` decision 20) reached Core's wire body and the client mirror silently dropped it. `api`'s half is now pinned against a JSON literal (task `032`). **Core's half is not** — filed to `embarch-core`'s inbox.
- **The smoke harness ([decisions](decisions/tests.md) 30) is named and unwritten.** Its six mocked criteria live in `tests/` ([decisions](decisions/tests.md) 46); end-to-end is `#[cfg(unix)]`, so Windows runs direct tests only.
- **The study event stream has never met a real embarch-core.** `study-status --follow`/`study_watch` ([decisions](decisions/core-link.md) 48, 49) run only against a mock that copies the wire format. Debt: `tasks/api/001-sse-client.md`.
- **Nothing gives a scripted caller a failure *kind*.** `error_kind` is retired unbuilt ([decisions](decisions/surface.md) 16, 50); branching on a cause means matching prose. **Not this repo's to fix**: Core's `{code, message, cause}` body (`embarch-core` decision 12) is deferred; Core emits codes, the shared client carries one typed, this crate passes it on. **Do not derive a kind from the HTTP status.**
- **`embarch-umbrella` still scaffolds `artifact_path_for_core`**, a field this crate no longer reads — a different repo's fix. **Deliberately no by-name load refusal for it** (unlike `[[projects.targets]]`/`soc_chip_overrides`): every umbrella-scaffolded config still carries it, so refusing it by name would break real machines this task never saw. It just loads, silently unread.

## Owed decisions

- **`list_serial_ports`/`list-serial-ports` (task `041`) shipped with no numbered
  decision**, under the burndown rule of no new numbered decisions this leg.
  What it would record if written: surfacing `GET /serial-ports` as a bare
  no-param tool/subcommand pair mirroring `status`'s shape, why `serial_log`
  gets no automatic fallback onto it (a caller must read the list and choose,
  since a machine can enumerate several ports and only a human or the caller's
  own knowledge says which one is the DUT's console), and the correction to
  `interfaces/tools.md:28`'s claim of a `GET /dev-bench/port` fallback that
  never existed in this crate. File as a `decisions/tool-wrapping.md` entry
  once it is out of reserve (`tasks/api/047`) — or, if a split lands first, in
  whichever successor file gets the tool-wrapping mission. Still open, also
  not this crate's to fix: `embarch init` never writes `serial_port` at all
  (`embarch-umbrella`), so the newcomer path this task partially closes still
  starts from an unconfigured project either way.

## Structural limits

- **Nothing can read a firmware version off a DUT** — a declared version describes the tree built, weaker than a measurement.
- **The inbound trust boundary is "whoever can spawn the process"** ([spec.md](spec.md) §6) — fine while an interactive client spawns it; revisit if one does not.
- **The artifact-transfer gap reaches the manifest too** ([decisions](decisions/studies.md) 39): a remote Core cannot see a local path.

## Settled-deferred

Re-read suite-wide; none acquired a new argument.

- **PATH/toolchain preflight** — a build failure surfaces naturally; preflighting costs the common case for an uncommon message. Expected as a `doctor` check.
- **Config fragments / `include`**, so `[core]` is not duplicated per repo. Tolerable: `[core]` is three lines.
- **Config hot-reload** — config loads once; picking up an edit means a reconnect.
- **`serial_log` stays one-shot** — Core's endpoint is itself a bounded capture; streaming needs Core to grow one first, **not this crate's to decide**.
- **Adding projects stays manual TOML editing** — no mutation tool; the list barely churns. `zephyr-west` needs no edit to add a board, variant, revision or app.
- **The decision corpus runs narrow across `api`.** Several `decisions/*.md` sit within a paragraph of the reserve line, invisible to `check-doc-size.py` until they cross — the wrong answer to the next entry is whichever file has room, not the one whose topic it is (leg 015, 96 B left). `tasks/api/*-compact-api.md` tracks which have crossed.
