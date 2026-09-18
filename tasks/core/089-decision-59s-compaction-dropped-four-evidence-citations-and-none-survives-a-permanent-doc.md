# 089 — Decision 59's compaction dropped four evidence citations, and none of them survives in a permanent doc

**State:** open
**Source:** leg 141, 2026-09-17. **Found by the supervisor reading `core/078`'s diff before merging
it** — the merge gate's one judgement call, applied because that diff retires and rewrites decision
prose — and then **confirmed and extended by `core/078`'s reviewer**, which token-diffed decisions 55
and 59 in full at merge `embarch-doc@00f9d79d` and found two more than the supervisor had. The
reviewer declined to file, on the honest ground that it was *"additional damage inside the wound you
already found, not a separate one."* That judgement was right about the wound and wrong about the
filing, which is why this exists: four is a different fact from two.
**Scope:** core
**Hardware:** none — one decision's prose, and a grep over the doc corpus to say what is reachable.
Nothing built, no board, no probe, no live Core.
**Owner:** no

## What

`core/078` had to write decision 67 into `embarch-core/decisions/surfaces.md` while that file was in
reserve at 91.6% with its compaction task (`tasks/core/079`) blocked on `In flux: yes`, so
`.claude/leg.md`'s ride-along rule applied: it compacted the file inside its own unit, carrying
`079`'s `Must not delete:` list. **It did that correctly — every protected item survives in
substance and the file came back to 88.7%.** What the protected list did not cover, and what the
squeeze took, is the **evidence** behind two of the protected findings:

1. **`validate_handler`** — the handler whose final `Err(internal_err(e))` is the reason `/validate`
   answers `500` for the whole un-downcastable failure class.
2. **`embarch-topology/src/hardware/validate.rs`** — the path holding `validate_known_timed`.
3. **The confirmation trail itself**: *"confirmed by reading `describe_topology_error`'s and
   `describe_gate_error`'s `None` arms and `validate_handler`'s final `Err(internal_err(e))`
   (`src/api.rs`, `src/study.rs`)"* — how `core/074` established its claim, as distinct from the
   claim.
4. **The grep receipt in the `core/077` paragraph**: *"(`embarch-ui`, the user guide: no hits on
   `kind`/`not_attached`)"*. The conclusion it supports — *"No consumer today reads `kind` needing
   that distinction"* — survives verbatim; the evidence for it does not.

**None of the four survives anywhere permanent.** `validate_handler` appears only in
`tasks/core/072`, `074`, `077` and `tasks/topology/056`, **all four `done` and slated for removal**;
`internal_err` survives as a general claim in `embarch-core/interfaces.md` but not as the citation
for this one; the `validate.rs` path survives nowhere, though the function name
`validate_known_timed` does, inside decision 59.

**Everything else the squeeze touched is intact**, and that is worth stating so nobody re-audits it:
status codes `500`/`502`/`503`/`409`, field names `kind`/`fix_it_url`/`live_hardware_id`, and
`raise()`, `classify_topology_mismatch`, `describe_topology_error`, `describe_gate_error`,
`validate_known_timed`, decisions 20, 28 and 34, and `topology/058` all survive.

## Why it matters, and why it is small

**It is the `core/086` failure shape from the leg before, one notch milder** — a squeeze taking
named identifiers out of the corpus — and it is worth fixing for the reason `core/086` was: this
suite's decisions are read later by someone re-deriving a claim, and a claim whose evidence has been
compacted away can only be re-established by reading the whole source again. A `Must not delete:`
list that protects findings but not the citations *behind* findings is a list with a gap, and this
is the first clean instance of it.

**It is small because the findings themselves all survive.** Nothing in decision 59 now asserts
something unsupported; it asserts supported things without saying where the support was found.

## Done when

- [ ] Each of the four is either **restored** to decision 59 in the shortest form that still names
      the symbol (a parenthetical, not the original sentence), or **deliberately dropped** with one
      line in the body saying so and why — `surfaces.md` has ~1.4 KB of headroom at 88.7%, so
      restoring all four is affordable; do not spend more than a few hundred bytes on it.
- [ ] `validate_handler`'s survival is checked against the four `done` task files that currently
      carry it (`tasks/core/072`, `074`, `077`, `tasks/topology/056`) — **those are retired on
      close**, so "it is written down over there" is not an answer.
- [ ] Say in the report whether `tasks/core/079`'s `Must not delete:` list should have covered
      citations as well as findings. If yes, that is a general lesson about how those lists are
      written and belongs in `inbox/` as a `doc` task, not fixed here —
      `DOC-COMPACTION-PASS.md` is owner-reserved.
- [ ] `check-doc-size.py` clean and `surfaces.md` still under 90% afterwards.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
