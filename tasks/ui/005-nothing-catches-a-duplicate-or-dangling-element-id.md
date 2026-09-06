# Add a static guard that every `getElementById` target exists and no element id is defined twice

**State:** open
**Source:** `embarch-ui/decisions/trace-chart.md` decision 10 — the defect this would have caught, which shipped
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A Rust test over the two `include_str!`-embedded assets asserts that **no id is declared twice**
across `assets/index.html` and the markup `assets/app.js` emits, and that **every id `app.js` looks
up is declared somewhere**. The surface is 142 ids in `index.html` and 42 `getElementById` sites
plus the `sdEl`/`trEl` wrappers.

This finds no live defect today — it is a regression guard, and it should be filed as one. What
earns it is the defect it would have caught: decision 10 records that "The Load button and the load
table's body carried **the same element id**, so every summary row had been rendering into the
button: the table had never once displayed, and its Rust tests all passed."

## Why now

`spec.md`'s Verification technique section says "tested in Rust, never looked at" is how this UI's
worst defects hid, and decisions 10, 17 and 18 each record one found only by rendering. This is the
one shape of that class a Rust test *can* catch.

## Done when

- [ ] The test parses both assets and fails on a duplicate id and on a dangling lookup.
- [ ] It is shown to fail when a duplicate id is introduced deliberately (revert, confirm, restore).
- [ ] It passes on the tree as it stands.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
