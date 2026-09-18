# 088 — `open.md`'s check-15 bullet still says the self-hash is "not yet built"; it landed as `core/088`

**State:** open
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

## Done when

- [ ] `embarch-umbrella/open.md` line 9's bullet reflects that the field is
      built and served, not "not yet built."
- [ ] Either check 15 gains a content-hash comparison against `binary_sha256`
      (a real behavior change, its own task) or the bullet is retired with a
      one-line note on why comparing it is left undone — `embarch-umbrella`'s
      call, not asserted here.
- [ ] Gate green.
