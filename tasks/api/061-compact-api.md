# 061 — `embarch-api/decisions/core-link.md` is inside its reserve floor

**State:** blocked
**Source:** `api/039`, leg 073, 2026-09-10. Decision 66 (the shared client's home) landed in this
file — chosen over `decisions/shape.md` because it sits beside decisions 37/38, which already own
the extraction that put the crate here, and because it had more headroom (2.3 KB vs 1.3 KB) before
either received the new entry. The entry itself was trimmed six times during drafting to land
inside the 12,288 B cap at all; it now sits at 12,283 B, 5 B under cap and inside the reserve floor
(90% of cap = 11,059 B).
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/core-link.md
**Size debt due:** 2026-09-24
**In flux:** yes. This file just took a new decision (66) and the crate-home question it records is
live — `tasks/ui/013` (a different repo, not this worker's to touch) may add evidence either way
about whether the location actually causes a silent cross-repo break, which is decision 66's stated
reversal condition. Compact only prose, not the open question.
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

- [ ] `embarch-api/decisions/core-link.md` is clear of its reserve floor, **or** this task closes
      with a written argument that no safe cut or split remains (`DOC-COMPACTION.md` §2 prefers a
      split; this file already groups by decision number so a split by topic — addressing/transfer
      vs. the shared-client extraction vs. the auth funnel — has at least not been tried).
- [ ] Every `Must not delete:` item above is still readable in full.
- [ ] The commit message quotes the first dozen words of every deleted hunk verbatim
      (`DOC-COMPACTION-PASS.md`).
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
