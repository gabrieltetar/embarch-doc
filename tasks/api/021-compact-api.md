# 021 — Compact embarch-api's decision files, starting with shape.md at 7 bytes

**State:** blocked
**Source:** `scripts/check-doc-size.py` — `embarch-api/decisions/shape.md` 12281/12288 B, spent by `agent/api/020-bearer-sweep-exhaustive`
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/shape.md
**In flux:** yes — decision 46's account of how far the tests reach is still
moving, and it is the part of this file worth the most bytes. Two of its own
stated limits are open in [open.md](../../embarch-api/open.md): the smoke
harness (decision 30) is named and unwritten, and the end-to-end half is
`#[cfg(unix)]` with no Linux leg able to run a native Windows build
(`tasks/doc/012`). Both will rewrite the same paragraphs. **Unparks when the
smoke harness ships or is retired and the `#[cfg(unix)]` gap is closed or
accepted** — at which point the whole test-reach account can be written once
instead of three times.
**Must not delete:**
- Decision 46's "six mutations, one per criterion, each reverted" and decision
  54's mutation sentence. Both are the *evidence* that a test was watched to go
  red; shortened, they read as the boilerplate claim that everything is tested,
  which is what decision 54 exists because a comment did.
- Decision 54's "already fired twice — `post_study` and `open_study_events`".
  Without the two names the entry reads as speculative tidying rather than as a
  drift that had already happened.
- Decision 54's **Not covered** paragraph, and specifically the two lexical
  escapes asserted shut (one `reqwest::Client`; `http()` never bound to a
  local). Delete them and the mechanism reads as airtight, which it is not.
- Decision 46's reason the `CoreClient` tests live in `embarch-api/tests/` and
  not `crates/embarch-core-client/tests/` — the path dep is not a workspace
  member, so root `cargo test` would never run them there. A mechanical fact
  that reads as arbitrary placement once its reason goes.
- Decision 53's "why the gate did not catch it" paragraph. A failure signature.

## What

`embarch-api/decisions/shape.md` is 7 bytes from its cap. **Every other
`embarch-api` decision file is within a paragraph of the reserve line too** —
`zephyr.md` 11056, `config.md` 11008, `build.md` 10934, `surface.md` 10928,
`core-link.md` 10879, against a line of 11059 — so the next entry written
anywhere in this sub-project meets the same wall, and the wrong answer to it is
to put the entry in whichever topic file still has room. Leg 015 did exactly
that. So this is a sub-project-wide pass, one commit
([DOC-COMPACTION-PASS.md](../../DOC-COMPACTION-PASS.md)), not a shape.md fix —
but only `shape.md` is on the `Compacts:` line, because it is the only file
actually in reserve today and the others are not yet debts.

A mission split is the likely move for `shape.md`: it carries scope-and-
boundaries (1–10, 25, 53) and test reach (30, 46, 54), which are two subjects
under one heading, and the second is the half that is still growing.

## Why now

Filed by the commit that spent the reserve, per
[tasks/README.md](../README.md) and `DOC-COMPACTION.md` §2. It is not a wall
and nothing is blocked on it — the record is that the runway is nearly gone.

## Done when

- [ ] `embarch-api/decisions/shape.md` back under the reserve line, with the
      `Must not delete:` list above honoured item by item.
- [ ] The sibling decision files given the same pass, or a written reason each
      was left.
- [ ] `DOC-COMPACTION-PASS.md`'s question answered in the commit message, in
      the compactor's own words: *can `spec.md` alone answer what someone needs
      to work on this component today?*
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
