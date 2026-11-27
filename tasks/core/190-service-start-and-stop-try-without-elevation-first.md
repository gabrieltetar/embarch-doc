# 190 — Service start and stop try without elevation first

**State:** done — start/stop try unelevated; classifier tested; hardware debt recorded
**Source:** EMB-342 — every switch between the service and a development Core needs elevation
**Issue:** EMB-342
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`service::start` and `service::stop` (`src/service.rs`) call
`elevate::ensure_elevated_or_fallback()` before doing anything, so every switch
between the service and a development Core raises a UAC prompt or needs `sudo`,
even where the elevated install has granted the engineer's account the right to
start and stop the service. `tasks/umbrella/124` adds that grant to
`install-core --agent-in-container` (a service-descriptor ACE on Windows, a
polkit rule on Linux). When this is done:

- `start` and `stop` first ask the service manager unelevated. Only a refusal
  for lack of rights (access denied on Windows, a polkit or permission refusal
  from `systemctl` on Linux) falls through to `ensure_elevated_or_fallback`,
  which behaves exactly as today. Any other failure is reported as today and
  does not elevate.
- The choice "was this a rights refusal?" is a pure function over the error the
  `service-manager` call returns, unit-tested per platform with the error
  shapes you can construct; say in the decision which shapes you could not
  construct and therefore matched by reading.
- `install`, `uninstall` and `install --service` still elevate first, always:
  the grant never covers changing the service.
- With no grant (every machine today), the unelevated attempt is refused and
  the user sees the same prompt as before, with no extra output beyond one
  debug-level log line.

**Not yours:** every other repo, including `embarch down`'s refusal under a
study, which is `tasks/umbrella/124`. You never touch hardware and never start
or stop a real service.

## Where to look

- `src/service.rs` (`start`, `stop`, `manager`), `src/elevate.rs`
  (`ensure_elevated_or_fallback`, `is_elevated`)
- the `service-manager` crate's error type for `start`/`stop` on the `sc` and
  `systemd` backends (read it in `~/.cargo/registry`)
- `embarch-doc/embarch-core/decisions/platform.md` (3, 157)

## Where the doc goes

**`decisions/platform.md` is 11,555 of 12,288 B, in reserve and filed against
`tasks/core/186`.** Do not grow it. Put the new decision in a new topic file
(for example `decisions/service-control.md`) with its index row; if decision 3
needs a pointer to it, keep the edit to 3 net-neutral or smaller. `spec.md` is
also in reserve under `core/186`: do not grow it. `open.md` is about 3,916 B,
just under its reserve line: net-neutral or smaller.

## Done when

- [x] `start` and `stop` try unelevated and elevate only on a rights refusal;
      the classifier is a tested pure function.
- [x] `install`, `uninstall` and `install --service` are unchanged.
- [x] A hardware-verification debt in this file: on Windows and on a systemd
      Linux, with and without `tasks/umbrella/124`'s grant, `embarch-core stop`
      and `start` as the engineer (no prompt with the grant, the usual prompt
      without it).
- [x] Gate green (`cargo build`, `cargo test`, `cargo clippy --all-targets --
      -D warnings`); the new decision and its index row; `changelog.d/`
      fragment. The Windows arm cannot be built under WSL (hidapi blocks the
      crate); type-check it in a throwaway crate as `core/185` did, and say so.

## Hardware-verification debt

Not run: no real service may be started or stopped here, and the Windows arm cannot be built under WSL. The code is platform-neutral (`cfg!(windows)` selects only the classifier branch), so the Windows arm was not type-checked in a throwaway crate; the shared path compiles and its tests run on Linux.

Needs running, on Windows and on a systemd Linux, with and without `tasks/umbrella/124`'s grant, as the engineer: `embarch-core stop` then `embarch-core start`. Expect no prompt with the grant and the usual prompt without it. Also confirm the Linux refusal text is one the classifier matches (decision 163 [assumed]).
