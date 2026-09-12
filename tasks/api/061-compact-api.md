# 061 — `embarch-api/decisions/core-link.md` is inside its reserve floor

**State:** done — leg 085, `api/067`, 2026-09-11. The file went from inside-the-reserve-floor to
**over cap** in the interim (`api/039`'s decision 66 correction, then `api/067`'s own one-clause fix
to decision 37/38), so this task's item is closed by the split its own `Done when` box named as
untried: decisions 36, 37/38, 55, 58, 62, 66 (the shared client crate's own lifecycle) moved,
byte-for-byte, into a new `decisions/client-crate.md`; decisions 11, 14, 15, 17, 26 (address
resolution and artifact transfer) stayed in `core-link.md`. Nothing was deleted or trimmed — every
`Must not delete:` item below is present in full, just in a different file — so there is no deleted
hunk to quote. `core-link.md` is now 3,963 B; `client-crate.md` is 10,817 B; both clear of the
11,059 B reserve floor. `decisions.md`'s index row split to match, and the two `spec.md` pointers
into decisions 36 and 55 were retargeted to `client-crate.md`.
**Source:** `api/039`, leg 073, 2026-09-10. Decision 66 (the shared client's home) landed in this
file — chosen over `decisions/shape.md` because it sits beside decisions 37/38, which already own
the extraction that put the crate here, and because it had more headroom (2.3 KB vs 1.3 KB) before
either received the new entry. The entry itself was trimmed six times during drafting to land
inside the 12,288 B cap at all; it now sits at 12,283 B, 5 B under cap and inside the reserve floor
(90% of cap = 11,059 B).
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** (closed — was `embarch-api/decisions/core-link.md`; split into `core-link.md` +
`decisions/client-crate.md`, see State above)
**Size debt due:** 2026-09-24 — met
**In flux:** no — the `Compacts:` line is now empty (closed above), so there is no file left for
this task to be in flux about. Decision 66's own reversal condition is still live, but it now lives
in `decisions/client-crate.md`, unparked and not blocking anything.
**Must not delete:** any of decisions 11, 14, 15, 17, 26, 36, 37, 38, 55, 58, 62, 66 — in particular
decision 36's 64 MiB/512 MiB thread-stack pair and the rejected `Builder::thread_stack_size` API,
decision 55's rejected `default_headers` alternative, decision 58's "thirteen existing fields"
count, decision 62's WSL2 predicate delegation, and decision 66's stated reversal condition (a
third Cargo consumer with independent release cadence, or an `api`-only change silently breaking
`embarch-ui`).

## What

`embarch-api/decisions/core-link.md` is 12,283 B against a 12,288 B cap — 5 B of headroom, well
inside the 1,229 B reserve floor (10% of cap).

## Done when

- [x] `embarch-api/decisions/core-link.md` is clear of its reserve floor via the topic split named
      as untried (addressing/transfer stayed; the shared-client extraction, auth funnel,
      older-Core parsing, WSL2 predicate and crate-home question moved to `client-crate.md`).
- [x] Every `Must not delete:` item above is still readable in full (moved, not cut).
- [x] No hunk was deleted, so there is nothing to quote — the commit message says so and lists what
      moved where.
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
