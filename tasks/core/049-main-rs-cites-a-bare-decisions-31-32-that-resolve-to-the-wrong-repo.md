# 049 — `main.rs` cites a bare `decisions 31/32` for the GATT result fields; those numbers are another repo's

**State:** open
**Source:** leg 101's refill sweep, 2026-09-12. Verified by reading all four decision bodies.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/src/main.rs:163-164`, inside `build_runtime`'s doc comment:

> the first real `run_study` POST against this milestone's GATT-extended `StepResult` (decisions
> 31/32's `gatt_services`/`gatt_activity`, larger than anything sized when that finding was written)

A **bare** `decision N` means this repo's decision N (`DOC-CONVENTIONS.md:21`, restated for code and
tool text as `embarch-api` decision 57). `embarch-core`'s own 31 and 32 are unrelated:

- `embarch-core/decisions/handshake.md:12` — *31 — Core enforces exactly what Core can verify*
- `embarch-core/decisions/flashing.md:20` — *32 — `erase` must not be EmbArch's own guess: it
  bricked a real board*

The decisions that actually introduce those two fields are `embarch-study-designer`'s:

- `embarch-study-designer/decisions/gatt.md:9` — *31 — `Action::GattDiscover`*
- `embarch-study-designer/decisions/gatt.md:15` — *32 — `Action::GattMonitorAll`*

and `embarch-study-designer/interfaces/limits.md:28` attributes `StepResult.gatt_services` to
"(decisions 31/32, §4.3a)" from inside that repo, where the bare form is correct.

**The same comment gets it right twice.** Lines 158–159 and 169 both write
`` `embarch-study-designer` decision 63 ``. So one unqualified citation sits between two qualified
ones, about the same repo.

## Why now

Third instance of this exact class this week — `core/008`, `topology/034`, and now this — and it is
the worst-behaved member of it, because a bare number that *resolves* is invisible in a way a broken
link is not: `embarch-core` really does have a decision 31 and a decision 32, so a reader who follows
the citation lands on a version gate and an `erase` footgun, finds no mention of GATT, and concludes
the comment is stale rather than misrouted.

## Done when

- [ ] `main.rs:163` reads `` `embarch-study-designer` decisions 31/32's ``, matching the form used
      six lines below it.
- [ ] **Sweep the rest of the repo, because one line is not the defect — the class is.** Every bare
      `decision N` in `embarch-core`'s `src/` and `bin/` either resolves to a real `embarch-core`
      decision of that number *whose body is about the thing the comment claims*, or gets qualified.
      Reading the number is not enough; `core/008` and `topology/034` both found citations that
      resolved to the wrong body. A starting grep:
      `grep -rn "decision" embarch-core/src embarch-core/bin | grep -vE '\`embarch-[a-z-]+\` decisions?'`
      Report the count you checked and the count you changed — they will differ, and the difference
      is the useful number.
- [ ] `embarch-core` `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.

**Native Windows build:** `embarch-core` normally also needs one. This is expected to be a
comment-only change, which cannot reach the running service — **`core/015`'s native Windows build is
an outstanding debt of the owner's and already carries seven other landed `embarch-core` changes**;
say in your report that this adds an eighth rather than treating it as something you can clear.

**Doc-size note:** `embarch-core/decisions/auth.md` is in reserve (92.4%) and filed against blocked
`tasks/core/046-compact-core.md`. A comment repoint should need no doc edit at all beyond the
changelog fragment; if it does, stay out of `auth.md`, and if your work leaves any `embarch-core` doc
in reserve unfiled, file `tasks/core/NNN-compact-core.md` in the same commit. Your own scope only,
never `tasks/doc/`.
