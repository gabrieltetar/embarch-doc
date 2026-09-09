# An unrecognised `EMBARCH_FLASH_BACKEND` tells the operator to install a tool that does not exist

**State:** done (leg 049)
**Source:** owner's repo survey, 2026-09-06 — the useful message exists and is unreachable
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`src/flash_backend.rs:270-272` — for `EMBARCH_FLASH_BACKEND=openocd`, a typo like `jlnk`, or an
empty value, `locate()` returns `None` because `env_override`/`on_path` only know four names, so
the bail reads "but no such tool was found — unknown tool 'openocd'". The genuinely useful message
at `:273-274` (`"{FLASH_BACKEND_ENV}='{forced}' is not a known backend"`) is **unreachable**:
`build()` is only called after `locate()` already succeeded. `flash_backend.rs:492-598` has no test
for the forced-backend path at all.

`discover` should validate the forced name against the four known backends *before* looking for a
binary. An unknown name fails naming the valid values; a known-but-absent tool keeps today's
install hint. The dead `with_context` arm is removed or made reachable — whichever leaves the code
honest.

## Why now

`spec.md` §5 lists `EMBARCH_FLASH_BACKEND` as the documented escape hatch for a bench the built-in
table is wrong about, and `flash_backend.rs:63-67` calls it "an escape hatch … so being wrong here
costs a config line rather than a Core release". A hatch whose typo message sends the operator to
install software is the opposite of that.

## Done when

- [x] `EMBARCH_FLASH_BACKEND=openocd`, `=""` and `=jlnk` each fail with a message naming
      `probe-rs`, `jlink`, `nrfutil`, `nrfjprog`.
- [x] A known-but-missing backend still gets its install hint unchanged.
- [x] `EMBARCH_FLASH_BACKEND=probe-rs` still forces probe-rs and still warns on a refused family,
      asserted by test.
- [x] Tests are serialised or scoped so the env var does not leak between parallel test threads.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Leg 049 — done

**Line-number drift found, as flagged.** `locate()` is at `:270-274` (task said `:270-272`), and
the unreachable `.is not a known backend` `with_context` arm is at `:308` (task said `:273-274`,
which is now the `discover` doc comment). `FLASH_BACKEND_ENV`'s doc comment (`:63-67`) and the
tests module boundary (roughly `:545-654` before this change) both matched as cited.

**Unreachable-arm decision: removed, not made reachable.** `discover` now validates `forced`
against `KNOWN_BACKEND_NAMES` (`probe-rs`, `jlink`, `nrfutil`, `nrfjprog`) before calling `locate`
at all. That makes `build()` infallible for every value that survives the check — there is no
longer a name reaching that point `build` does not recognise — so the old
`.with_context("...is not a known backend")` arm would be dead code with a `Result` shape
pretending it can still fail. Deleted it and replaced the call with
`.expect("forced backend name was validated above")`. Recorded as `embarch-core` decision 52
(`decisions/flashing.md`).

**Env-var test isolation:** this crate had no `serial_test`-style mechanism anywhere in its tree
(checked — no dependency, no existing pattern). Added a small in-module `ForcedBackendGuard`
(a `Mutex<()>` guard whose `Drop` always clears `FLASH_BACKEND_ENV`, even on panic) and used it in
every test that reads or sets that var, including the two pre-existing tests that relied on it
being unset. New tests also assert the forced-`probe-rs` warning via a minimal hand-rolled
`tracing::Subscriber` that captures event messages, since no test-capture crate was already a
dependency either.

No hardware touched. `cargo build`, `cargo test` (184 passed, 2 ignored — pre-existing, unrelated
to this change), and `cargo clippy --all-targets -- -D warnings` all clean. `check-docs.py` all 10
checks green; `check-client-names.py` and `check-ownership.py` (both worktrees) green.

## Supervisor notes — leg 049

**Doc-size reserve for `core`: nothing is in reserve.** `embarch-core/open.md` is the closest at
4478/5120 B (87.5%), which is outside the last 10%. Its compaction task `tasks/core/022` is
`blocked` and stays that way; you are not being asked to compact anything. If your work *does*
push a `embarch-core/` doc file into the last 10% of its cap, file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md` — your own scope's
directory, never `tasks/doc/`.

**Re-derive the line numbers before you act on them.** The task cites
`src/flash_backend.rs:270-272`, `:273-274`, `:63-67` and `:492-598` from a 2026-09-06 survey. Two
units in the previous leg found task-file line numbers that had aged out. Read the file, find the
construct the task is describing, and if what you find differs from what the task claims, write the
drift into this task file and act on what is actually there.

**The unreachable-arm question is the substance, and it has two honest answers.** The task says
"removed or made reachable — whichever leaves the code honest". Decide which, say why in one
sentence in the decisions/doc update, and do not do both. Validating the forced name in `discover`
before the binary lookup is the shape the task suggests; if that makes the `with_context` arm
genuinely dead, deleting it is honest and leaving it is not.

**Env-var test isolation is a real requirement, not boilerplate.** `EMBARCH_FLASH_BACKEND` is
process-global and `cargo test` runs threads in parallel. Use a serialising guard or a
`#[serial]`-style mechanism the repo already has — do not assume `--test-threads=1`, because the
gate does not pass it.

**Do not touch hardware.** No flash, no probe, no live Core. Everything here is unit-testable.
