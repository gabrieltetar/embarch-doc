# 017 — A fourth flashing backend, for a vendor-deprecated tool at third preference, that no document in the suite mentions

**State:** done
**Source:** suite review pass 2026-09-06, dimension 6 (deletion candidates). Code-confirmed, with a whole-corpus grep.
**Scope:** core
**Hardware:** none. Either a deletion or a doc row; both are host-side. No claim is made here about what this tool does to any part — that is engineer-declared.
**Owner:** no

## What

`embarch-core/src/flash_backend.rs` carries a `Backend::NrfJprog` variant whose own comment says
(`:79-82`): *"Nordic's legacy nRF Command Line Tools. **Deprecated upstream**; supported because a
bench that already has it working should not be forced to migrate to close this bug."* At `:119`,
`preferred_for("nrf")` returns `&["nrfutil", "jlink", "nrfjprog"]` — it is tried **third**. And
`:42-44`, the module's own doc: *"`nrfjprog` is Nordic-proprietary **and links SEGGER's `JLinkARM`
library**, so it inherits that restriction (Nordic has also deprecated it in favour of nRF Util)."*

So it is selectable only on a machine that has the deprecated wrapper and neither the tool it
wraps nor the tool that supersedes it.

**It appears in no document.** Grepped all nine repos plus the ~3 MB doc corpus for
`nrfjprog|NrfJprog|NRFJPROG|nRF Command Line`. In the whole corpus there is exactly **one** hit:
`tasks/core/010:33`, inside an open task's quoted list of accepted values. It is in no `spec.md`,
no `decisions/flashing.md`, no `interfaces.md`, no `suite/features.md` row, no roadmap entry and
no `open.md`. `EMBARCH_NRFJPROG_EXE` has one use outside its own declaration.

Retiring it removes, counted: the variant, its `name()` arm, its entry in `preferred_for`, its
`extra_candidates` arm (four hardcoded install paths), `NRFJPROG_EXE_ENV`
(`EMBARCH_NRFJPROG_EXE`) plus its `env_for` arm, its `exe_names` arm, its `from_name` arm, its
`install_hint` arm, its line in the not-found error message, and its `Command` construction arm in
`flash` — **about ten sites and one environment variable**, plus one of the four accepted values of
`EMBARCH_FLASH_BACKEND` that `tasks/core/010` is already editing the error path of.

Candidate direction: settle whether this bench's Core has ever selected `nrfjprog`. The
disambiguating read is `doctor` check 14, which reports the choice
(`embarch-umbrella` decision 38) — that needs the owner's machine, so a worker should instead
settle it from the record: the keep-reason's premise is *"a bench that already has it working"*,
and no recorded bench in this suite has ever had it. If nothing names it, retire the variant and
its env var. If something does, the finding **inverts** into a doc gap and the backend needs a
`features.md` row and a `spec.md` mention rather than deletion.

## Why now

`suite/features.md` asserts, with `Verified: hw`, *"Erase on flash | Shipped — **the brick hazard
is closed: no backend maps it to a chip erase**"* — a claim over four backends, one of which
appears in no document and has no recorded run, so the claim is unfalsifiable from the docs alone.
`embarch-core/decisions/flashing.md` (decisions 32, 36, 49) does not name `nrfjprog` at all, so
there is no recorded decision to add it and none to keep it. Either outcome makes the suite
smaller or more honest; the current state is neither.

## Done when

- [x] `Backend::NrfJprog` is gone. Deleted (no bench in this suite ever recorded selecting it):
      the variant, `name()` arm, `preferred_for` slot, `extra_candidates` arm, `NRFJPROG_EXE_ENV`
      + `env_for` arm, `exe_names` arm, `build` arm, `install_hint` arm, its line in the refusal
      message, and its `run()` `Command` arm. Recorded as `embarch-core` decision 54.
- [x] `EMBARCH_FLASH_BACKEND`'s accepted values are the same in the code (`KNOWN_BACKEND_NAMES`,
      now 3), `interfaces/constants.md`, and the error message.
- [x] The erase-on-flash claim (`features.d/core-150-erase-on-flash.md`) is true of every backend
      that still exists (`probe-rs`, `jlink`, `nrfutil`).
- [x] Gate green; `changelog.d/core-nrfjprog-backend.removed.md` filed.

`embarch-core/decisions/flashing.md` crossed into doc-size reserve as a result
(93.5%); filed `tasks/core/035-compact-core.md`, `blocked` on `In flux: yes`
with a size-debt-due date, per protocol.

**Adjacent, not the same:** `tasks/core/010` fixes the *message* an unrecognised backend name
prints. It does not touch which backends exist.
