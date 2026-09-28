# 088 — `open.md`'s check-15 bullet still says the self-hash is "not yet built"; it landed as `core/088`

**State:** claimed by agent/umbrella/088-check-15-self-hash-bullet, 2026-09-28 17:02
**Source:** `embarch-core` task `088` (`tasks/core/088-serve-a-self-hash-of-the-running-binary-on-status.md`),
landed on `agent/core/088-status-self-hash`. `embarch-umbrella/open.md` line 9
reads: *"Check 15 is not a hash comparison and must not be read as one. It
catches a cross-version stale deploy and is blind to a same-version one:
`core_version` is `CARGO_PKG_VERSION`, so a rebuild and failed deploy at one
version reads as a match (decision 34). A content hash on `/status` would
close it — `embarch-core` decided yes, not yet built (`embarch-core` decision
67), tracked as `tasks/core/088`."*
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`GET /status` now serves `binary_sha256` (`Option<String>`, lowercase hex
SHA-256 of the running Core binary's own bytes, cached once at first request
via `std::sync::OnceLock`, `null` if the self-read fails). Implementation is
`embarch-core` decision 68, citing decision 67. `embarch-core/interfaces/hardware.md`'s
`/status` row and `embarch-core/decisions/surfaces.md` both document the field
now.

The bullet quoted above is stale on two counts: it still says "not yet built"
and it still cites `tasks/core/088` as the tracking task rather than the
landed decision. Whether check 15 itself should be extended to compare
`binary_sha256` (not just `core_version`) is `embarch-umbrella`'s own call —
this drop is only "the field exists now," not "go consume it."

## Why now

This worker is `core`-scoped and `embarch-umbrella/open.md` is out of its
ownership row (protocol.md §3) — cross-repo, not a shared suite-level doc
either, so `status.d/` isn't the right mechanism (that fragment type is for
`embarch.md`/`suite/roadmap.md`/`suite/features.md`/`embarch-decision-reversals.md`/
`embarch-glossary.md`/`suite/user-guide.md` only, per `status.d/README.md`
and `DOC-PROTOCOL.md` §2). This drop is how the fact reaches `embarch-umbrella`'s
own queue instead.

## Dispatch note (supervisor, 2026-09-28)

**Reconciled at claim: still true.** `embarch-umbrella/open.md` line 9 still says "not yet built",
and nothing under `embarch-umbrella/src/` reads `binary_sha256`.

**The file you are editing is in reserve and its compaction is parked on flux**, so per
`.claude/leg.md` the compaction rides in this unit. `embarch-umbrella/open.md` is **4,372 / 5,120
B, 748 B left**, filed against `tasks/umbrella/077` (`blocked`, `In flux: yes`). Compact it as part
of this unit, **carrying 077's whole `Must not delete:` list** — and note that its first item is
*the check-15 bullet you are rewriting*: "check 15 is not a hash comparison and must not be read as
one" has to survive whatever you do to the "not yet built" half. Close only that file's item: 077
has one file, so if `open.md` leaves reserve, record the before/after bytes in 077 and set it
`done`; if it does not, say in 077 what you paid and why it was not enough, and leave it `blocked`.

**The Done-when's second box is `embarch-umbrella`'s call, as the task says.** Consuming
`binary_sha256` in check 15 is a real behavior change with its own decision; retiring the bullet
with a one-line reason is the other legal answer. Either is in scope.

**Also in reserve in `umbrella`, not yours to write:** `decisions/install.md` 217 B left
(`tasks/umbrella/079`), `decisions/bind.md` 733 B left (`tasks/umbrella/009`),
`decisions/projects.md` 1,172 B left (`tasks/umbrella/084`) — all blocked. A new decision, if you
make one, goes in the topic file whose mission fits and has room; if that pushes a file into
reserve, file `tasks/umbrella/<NNN>-compact-docs.md` in the same commit.

## Done when

- [ ] `embarch-umbrella/open.md` line 9's bullet reflects that the field is
      built and served, not "not yet built."
- [ ] Either check 15 gains a content-hash comparison against `binary_sha256`
      (a real behavior change, its own task) or the bullet is retired with a
      one-line note on why comparing it is left undone — `embarch-umbrella`'s
      call, not asserted here.
- [ ] Gate green.
