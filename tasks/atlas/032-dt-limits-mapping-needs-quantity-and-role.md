# 032 — a DT-limits mapping by name needs a matching quantity and role

**State:** claimed by agent/atlas/032-dt-limits-mapping-needs-quantity-and-role, 2026-11-06 13:14
**Source:** a worker's finding, filed to Fleet Ready
**Issue:** EMB-53
**Scope:** atlas
**Hardware:** none — `score` and `Analysis.proposed` run on a node's properties and a list of limit records, both of which a test can build.
**Owner:** no

## What

The DT-limits check (`src/embarch_atlas/limits.py`) proposes property-to-limit mappings by name, and some of them compare unrelated quantities. On a BQ25188 charger node, `battery-discharge-current-limit-milliamp = 500` is compared with `IBAT_SHIP` (ship-mode battery current, max 5 µA), and `re-charge-threshold-millivolt = 100` (an offset below VBATREG) is compared with `VREG_RANGE` (3.5 to 4.65 V). Both come out as `dt-limit-outside-ec`, a candidate that means nothing. A proposed mapping is accepted when the property's words overlap the record's `sym` or `param` at score 1 or more (`THRESHOLD`), so a shared word and the same dimension are enough (`score`, `Analysis.proposed`, `Analysis._skip_reason`).

When this is done, a proposed mapping needs a matching quantity and a matching role — a discharge limit against a discharge or OCP setting, an offset against an offset — and one that fails either test is listed as "mapping uncertain", not as a candidate outside the limit. A declared mapping in `boards/bindings.json` `prop_limits` is still compared as before. The module docstring's "proposed, by name" description says the new rule.

## Why now

A `dt-limit-outside-ec` reads as "this board is configured outside the part's ratings", the most alarming thing the check can say; it should never say it about two quantities that only share a word.

## Done when

- [ ] `battery-discharge-current-limit-milliamp` is not compared with `IBAT_SHIP`, and `re-charge-threshold-millivolt` is not compared with `VREG_RANGE` (unit test with both records).
- [ ] A mapping that fails the quantity or role test is shown as "mapping uncertain", not as `dt-limit-outside-ec`.
- [ ] A declared mapping in `boards/bindings.json` `prop_limits` is still compared as before.
- [ ] The module docstring and any design doc that states the mapping rule say the new one.
- [ ] Gate green (`../../../embarch-fleet/gate.md`, the Python bullet).
- [ ] `changelog.d/` fragment dropped.
