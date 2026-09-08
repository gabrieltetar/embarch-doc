# `validate`'s response mirror and MCP tool should show `validated_at_utc_ms` when Core sends it

**State:** claimed — leg 043, 2026-09-07
**Source:** `tasks/topology/009` (embarch-doc), topology decision 26
**Scope:** api
**Hardware:** none
**Was blocked on:** `tasks/core/026-validate-handler-wires-validated-at.md`,
which landed in leg 042 (`embarch-core` `b0bf60d`, decision 50). `POST
/validate` now serves the field, so both mirrors here have something real to
carry. This is the head of the chain: `tasks/umbrella/041` and `tasks/ui/020`
are blocked on *this* task where they read Core through `embarch-api`'s mirror.

## What

`embarch-topology` decision 26 adds a second `validate` timestamp,
`validated_at_utc_ms` — when the live hardware-ID check ran — additive
alongside the existing `confirmed_at_utc_ms`, which is enrolment time and does
not move on a successful re-check. Once `embarch-core`'s `POST /validate`
picks the new field up (a separate inbox drop, `core-validate-handler-wires-
validated-at.md`), this repo has two hand-maintained mirrors of that response
shape to update: `crates/embarch-core-client`'s response struct, and the MCP
`validate` tool's output.

**This is additive, and nothing here is urgent on its own** — the existing
field name and shape are unchanged, so both mirrors keep deserializing with no
edit at all. This drop exists so the new field is enumerated as a consumer
before anyone reaches for `confirmed_at_utc_ms` expecting it to answer "how
stale is this check," which is exactly the defect `topology/009` observed.

## Why now

Not urgent — filed so the fix is visible once Core sends the field, per the
`topology/009` supervisor direction to enumerate every consumer of this
response shape before it changes.

## Done when

- [ ] `crates/embarch-core-client`'s `validate` response type gains
      `validated_at_utc_ms` once Core's own response carries it.
- [ ] The MCP `validate` tool surfaces it (both timestamps, distinctly
      labelled — not one replacing the other).

## Supervisor direction (leg 043)

**1. The wire is flat; the crate is not, and mirroring the wrong one is the
one way to get this wrong.** `embarch-topology` returns a `Validation { board,
validated_at_utc_ms }`, so in *that* crate the field sits beside a nested
board. `embarch-core`'s `POST /validate` does **not** serve that shape: read
`ValidateOkResponse` in `embarch-core/src/api.rs` (~line 864) and mirror it
literally — `ok`, `role`, `probe_serial`, `chip`, `hardware_id`,
`confirmed_at_utc_ms`, `validated_at_utc_ms`, all **flat, top level**. Do not
infer the wire from the topology crate; read Core's serialized struct. Core is
another sub-project's repo — **read it, never edit it.**

**2. Only the validate response type gains the field.** `confirmed_at_utc_ms`
appears in three structs in `crates/embarch-core-client/src/client.rs` (~208,
~226, ~299) because several endpoints echo an enrolled board. Exactly one of
them is `POST /validate`'s response. Adding the field to the other two would
be a mirror of a wire that does not carry it — a fabricated contract that
compiles and passes tests. Identify which by the method that calls it, not by
proximity.

**3. Both surfaces, and there are more of them than the Done-when list says.**
`grep -n confirmed_at_utc_ms` finds two sites in `src/tools.rs` (the MCP tool)
and two in `src/cli.rs`. The task file names the MCP tool; the CLI is the same
mirror by hand and should move with it — a CLI that prints one timestamp and an
MCP tool that prints two is the drift this whole chain exists to close. If you
find a reason the CLI should *not* change, say so in the task file rather than
silently leaving it.

**4. Label them so a reader cannot confuse them.** The defect `topology/009`
found is that a caller read `confirmed_at_utc_ms` as freshness and got a
plausible wrong answer. A JSON key pair alone does not fix that for a human
reading MCP or CLI output; whatever the surrounding output style is, the two
must be distinguishable without knowing the history. Follow the existing
style — do not invent a new one.

**5. Prefer citing the upstream decisions to writing a new one.** The design
was decided twice already: `embarch-topology` decision 26 and `embarch-core`
decision 50. A mirror that faithfully carries an upstream decision usually
needs no decision of its own. **If you conclude one is genuinely needed, stop
and read this first:** `embarch-api/decisions/core-link.md` has **22 bytes**
of headroom and `decisions/surface.md` has **415**; both are in reserve and
both have a compaction task parked `In flux: yes` (`tasks/api/026`,
`tasks/api/043`). Under `DOC-COMPACTION.md` §2 that means **you compact the
file you are writing into, as part of this unit** — carrying that parked
task's `Must not delete:` list verbatim and closing only that one file's item,
leaving the rest of the task parked. Do not file fresh compaction debt for a
paragraph, and do not put an `api` decision in a file it does not belong in
because that file has room. `embarch-api/spec.md` (9087/10240) and
`interfaces.md` are the likelier homes for a mirror-shape fact anyway.

**6. Decision numbers are global across `decisions/*.md`, not per file.** If
you do write one, take the next number after the maximum across the whole
directory.

**7. Out of scope, deliberately.** `tasks/api/044` covers the `hardware_id`
spelling in this same client. Do not touch it here; two wire-shape changes in
one diff is how a revert stops being possible.

**Reserve for `api` (headroom at dispatch):** `decisions/core-link.md` 22 B,
`decisions/surface.md` 415 B, `open.md` 386 B, `spec.md` 1153 B. If your work
pushes any file into reserve, or leaves one there with nothing filed, file
`tasks/api/<NNN>-compact-api.md` in the same commit.
