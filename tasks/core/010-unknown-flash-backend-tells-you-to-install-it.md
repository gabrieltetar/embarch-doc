# An unrecognised `EMBARCH_FLASH_BACKEND` tells the operator to install a tool that does not exist

**State:** open
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

- [ ] `EMBARCH_FLASH_BACKEND=openocd`, `=""` and `=jlnk` each fail with a message naming
      `probe-rs`, `jlink`, `nrfutil`, `nrfjprog`.
- [ ] A known-but-missing backend still gets its install hint unchanged.
- [ ] `EMBARCH_FLASH_BACKEND=probe-rs` still forces probe-rs and still warns on a refused family,
      asserted by test.
- [ ] Tests are serialised or scoped so the env var does not leak between parallel test threads.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
