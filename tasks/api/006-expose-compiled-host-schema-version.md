# 006 — Expose `embarch-api`'s compiled `HOST_TYPE_SCHEMA_VERSION`, so `doctor` can read it

**State:** done on agent/api/006-expose-compiled-host-schema-version, 2026-09-03
**Source:** embarch-umbrella/open.md — "Check 11 compares *this* `embarch` binary's compiled host schema version, not the located `embarch-api`'s"
**Scope:** api
**Hardware:** none

## What

`embarch-api` compiles in `embarch_study_designer::HOST_TYPE_SCHEMA_VERSION`
and compares it against Core's served one before every submit
(`crates/embarch-core-client/src/client.rs`). **That number is readable from
nowhere outside the process** — `--version` prints only the crate version, and
`status --json` returns Core's probes without it.

`embarch doctor`'s check 11 (embarch-umbrella decision 33, built 2026-09-03)
wants exactly that number: its job is to say whether the deployed Core and the
installed `embarch-api` agree on the host schema, unasked. Unable to read it,
it substitutes the `embarch` binary's own compiled copy — exact whenever all
three binaries came from one suite archive, and **wrong precisely in the case
that matters most: a hand-built mixed install, which is how this suite is
actually developed.**

Cheapest shape that closes it: add the field to `status --json`'s object
(it is already stamped by `json_out`, so this is one key), or a bare
`embarch-api schema-version` that prints it. A `--json` field is probably
better — `doctor` would then get it from a surface it can also read when
`embarch-api` is on another machine — but that is `api`'s call, not umbrella's.
Whichever it is, `doctor`'s check 11 then reads the located binary's real
number and `embarch-umbrella/open.md`'s stand-in bullet closes.

## Why now

Check 11 was a hardcoded stub for months while the exact failure it exists to
catch happened undetected (Core wire v13 against a bench flashed to v14,
2026-08-26). It is now real, and this is the one remaining thing that makes it
approximate rather than exact.

## Done when

- [x] `embarch-api` exposes its compiled `HOST_TYPE_SCHEMA_VERSION` on a
      machine-readable surface, documented in `embarch-api/interfaces/`.
      `embarch-api versions [--json]`, key `host_type_schema_version`; row in
      `interfaces/tools.md`.
- [x] `embarch-api/decisions/` records which surface and why — decision 52 in
      `decisions/surface.md`, including why the suggested `status --json` field
      was rejected.
- [x] A follow-up task points `embarch-umbrella`'s check 11 at it:
      `inbox/umbrella-check-11-reads-embarch-api-versions.md` (scope `umbrella`,
      unnumbered per `inbox/README.md`). **The `open.md` bullet is not closed
      yet** — that closes when the umbrella task lands, and `embarch-api/open.md`
      carries a matching "nothing reads `versions` yet" bullet until then.
- [x] Gate green (`embarch-parallel-agents.md` §10) — build/test/clippy in
      `embarch-api`, all six doc checks, both ownership scopes. No native
      Windows build: this is not `embarch-core`.

## Verification debt

**No live consumer has read this surface.** The number is pinned against the
constant by `tests/json_surface.rs` and printed by the real binary, but nothing
outside the process has consumed it yet, and no MCP round trip or live Core was
available. `embarch doctor` reading it is the first real exercise, and that is
the follow-up above. No hardware is involved either way.

## Added by the supervisor when dispatching (2026-09-03)

**`embarch-api`'s docs are at their size cap.** As of `api/004` landing,
`spec.md` is at exactly 10240 bytes — **zero headroom** — `interfaces/tools.md`
has 3 and `open.md` has 9. `check-doc-size.py` is part of the gate, so budget for
compressing adjacent prose *before* you add a sentence, not after the check goes
red. `api/004` did exactly this and it worked; the same trick is available.

**There is a live consumer, and this one is real** — unlike `core/002`'s stated
premise last leg, which was not. `embarch-umbrella`'s `doctor` check 11 shipped
2026-09-03 comparing Core's served `study_designer_schema_version` against the
**`embarch` binary's own** compiled constant, because yours is unreadable. Pointing
it at the real number is a follow-up in `umbrella`, not yours — but it means the
surface you choose has to be readable by a *different process*, so a value only
reachable inside this crate does not close it.
