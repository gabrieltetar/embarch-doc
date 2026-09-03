# 006 — Expose `embarch-api`'s compiled `HOST_TYPE_SCHEMA_VERSION`, so `doctor` can read it

**State:** open
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

- [ ] `embarch-api` exposes its compiled `HOST_TYPE_SCHEMA_VERSION` on a
      machine-readable surface, documented in `embarch-api/interfaces/`.
- [ ] `embarch-api/decisions/` records which surface and why.
- [ ] A follow-up task (or this one's second half, if `suite`) points
      `embarch-umbrella`'s check 11 at it and closes that `open.md` bullet.
- [ ] Gate green (`embarch-parallel-agents.md` §10).
