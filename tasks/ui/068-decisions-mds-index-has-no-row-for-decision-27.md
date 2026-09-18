# 068 — `embarch-ui/decisions.md`'s index has no row for decision 27

**State:** open
**Source:** leg 144's refill sweep, 2026-09-17 — a mechanical check of every sub-project's
`decisions.md` index against the decision numbers actually present in its `decisions/` files.
**Scope:** ui
**Hardware:** none — one markdown table row.
**Owner:** no

## What

`embarch-ui/decisions/trace-view.md:45` carries:

```
### 27 — The decode-to-lanes pipeline stays duplicated with `embarch-core`'s `outpost_load.rs`, now
    for a checked reason rather than an open wait
```

It landed as `ui/064` and was amended by `ui/067`, both on 2026-09-17. **`embarch-ui/decisions.md`'s
group table never gained it.** The `decisions/trace-view.md` row reads `10 (trace)` in its
*Decisions* column, and decision 27 appears in no row of that table at all.

So a reader walking the index — which is the documented way into this sub-project's decisions — has
no route to the one decision that settles why two decoders exist. `check-decision-refs.py` does not
catch this: it resolves *references* to decision numbers, and nothing references a row that is not
there.

**Re-derive the coordinates before editing.** The line number and the `ui/064`/`ui/067` attribution
are the sweep's reading; "this does not hold" is a correct outcome to report.

## Done when

- [ ] The `decisions/trace-view.md` row's *Decisions* cell lists 27 alongside `10 (trace)`. Match the
      cell's existing convention for a file that holds a split decision number — do not invent a new
      spelling.
- [ ] That row's *What it settles* cell names the duplication boundary in the index's own voice —
      one clause, in the register of the rows around it ("What a trace renders, on which clock, and
      the load repartition" is the current text). A reader scanning the table should be able to tell
      that this is where the two-decoders question is answered without opening the file.
- [ ] Check the **whole** table the same way while you are in it: every decision number present in
      `embarch-ui/decisions/*.md` appears in exactly one row, and every number a row claims exists.
      Report the count either way — a clean sweep is a useful result and should be said plainly.
- [ ] If the index carries a size column, re-measure the rows you touch rather than trusting them.
- [ ] A `changelog.d/` fragment only if you judge the index fix reader-facing; a one-row index repair
      usually is not, and saying so is a fine answer.
- [ ] Gate green per `../../embarch-fleet/protocol.md` §10.

## Not yours

- **Do not amend decision 27 itself**, or any other decision's text. This is the index.
- **Do not touch `embarch-core`'s `outpost_load.rs` or `trace.rs`.** The duplication is settled; this
  task is about the pointer to where it is settled.
- **Do not renumber anything.** Decision numbers are permanent identifiers.
