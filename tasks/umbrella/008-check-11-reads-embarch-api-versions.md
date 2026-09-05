# 008 — Point `doctor` check 11 at `embarch-api versions`, not at `embarch`'s own constant

**State:** done on agent/umbrella/008-check-11-reads-embarch-api-versions, 2026-09-04 — pushed, not merged
**Source:** embarch-api/006 (decision 52) — the surface check 11 was missing now exists
**Scope:** umbrella
**Hardware:** none
**In reserve for this sub-project (supervisor, leg 007):** `embarch-umbrella/open.md` 4795/5120 B — **325 B left**; `embarch-umbrella/spec.md` 9527/10240 B — **713 B left**. Both are already filed against `tasks/umbrella/009-compact-docs.md`, which is deliberately `blocked`. So plan your `open.md` edit inside ~325 bytes — closing the stand-in bullet should *free* bytes, not spend them. **You do not need to file a new compaction debt** unless your work pushes a third umbrella doc into reserve, or you leave one there that `tasks/umbrella/009` does not name; then file `tasks/doc/<NNN>-compact-umbrella.md` in the same commit, per `tasks/README.md` § "Compaction tasks". Do not unblock `umbrella/009`.

## What

`embarch-api` now exposes its compiled `embarch_study_designer::HOST_TYPE_SCHEMA_VERSION`
on a machine-readable surface:

    embarch-api versions --json
    { "schema_version": 1, "success": true, "api_version": "0.1.0",
      "host_type_schema_version": 17 }

It loads **no config** and contacts **no Core**, is dispatched before config
resolution, and always exits 0 — chosen over a `status --json` field precisely
so it answers on a machine whose config or Core is the thing being diagnosed
(`embarch-doc/embarch-api/decisions/surface.md` 52).

`doctor` check 11's `SchemaVersions.local_host` is currently the `embarch`
binary's *own* compiled constant, which is exact only when all three binaries
came from one suite archive and wrong for a hand-built mixed install. Run the
**located** `embarch-api` and read `host_type_schema_version` from its `--json`
object instead.

Two things to settle, both umbrella's call:

- **`local_host` becomes fallible.** Today it is a plain `u32` "always
  available". The located binary may be missing, too old to know `versions`
  (clap exits 2 on an unknown subcommand), or unreadable. That is a third
  `Result<u32, &str>` beside `core_host`/`bench_wire`, not a silent fallback —
  and "could not ask embarch-api" is a different verdict from "they disagree".
- **Whether to keep the local constant as a fourth number.** `embarch`'s own
  copy is still a real fact about the installed suite, and an `embarch` that
  disagrees with the `embarch-api` it just located is itself a mixed install
  worth naming. Report it, or drop it deliberately.

## Why now

Check 11 shipped 2026-09-03 approximating the number it wanted, and
`embarch-umbrella/open.md` carries a stand-in bullet for exactly this. The
approximation is wrong in the one case the check exists for. The blocking half
is built and landed; this is the half that closes the bullet.

## Done when

- [x] Check 11 reads the located `embarch-api`'s `versions --json`
      `host_type_schema_version`, with a distinct verdict when it cannot be asked.
- [x] `embarch-umbrella/open.md`'s stand-in bullet closes; `decisions/` records
      what happened to the local constant.
- [x] `embarch-api/open.md`'s "Nothing reads `versions` yet" bullet is named as
      closable in the report (a different repo — do not edit it), and in
      `status.d/umbrella-api-versions-has-a-consumer.md`.
- [x] Gate green. `cargo build`/`test`/`clippy --all-targets -D warnings` clean;
      `check-docs.py` green on all six doc checks. The one red is
      `install.py --check`, which the supervisor pre-declared as a worktree-depth
      artefact and not this task's.

## Both judgements, decided

- **`local_host` is now `api_host: Result<u32, String>`** — the located
  `embarch-api`'s own number, and a `Warn` naming which failure when it cannot be
  had (not located / clap-exit-2 too old / not executable / no field). Never a
  fall back to the local constant; a test pins that "could not ask" and "they
  disagree" reach different verdicts on the same numbers. Decision 35.
- **`embarch`'s own constant stays, as a fourth number that can only warn.** It
  is free, and an `embarch` disagreeing with the `embarch-api` it just located is
  a mixed install nothing else notices without a suite manifest — but it blocks
  no study, because `embarch` submits none. Decision 36.

## Two things found on the way

- **The invocation in this task file is wrong.** `--json` is a top-level flag on
  `embarch-api`'s parser and is not `global`, so `embarch-api versions --json`
  exits **2** with `unexpected argument '--json' found`. It has to be
  `embarch-api --json versions` [verified 2026-09-04 against a local build].
  Nothing in `embarch-api`'s own docs states the wrong order; only this task did.
- **`embarch-umbrella/decisions/doctor.md` could not hold two more entries** —
  it was 4 B under its reserve and 1233 B under its 12 KB cap, with five more
  open umbrella tasks queued to write there. Decisions 24, 33, 34 and the two new
  ones moved into `decisions/schema-skew.md`; `doctor.md` is now 6.5 KB and the
  new group 7.0 KB. No compaction debt filed: nothing was left in reserve that
  `tasks/umbrella/009` does not already name, and `open.md` came *out* of reserve
  when the stand-in bullet closed (4795 -> 4512 B). `009` is untouched and stays
  blocked.

## Verification debt (not hardware)

Everything here is host-side: the check is exercised against fabricated
`embarch-api` binaries (a good one, one exiting 2, one with no execute bit) and
a local debug build. **What has not happened is one `embarch doctor` against the
installed suite**, which would confirm the installed `embarch-api` answers
`--json versions` with the field. Carried in `embarch-umbrella/open.md`'s first
bullet alongside the live-Core debt that was already there.
