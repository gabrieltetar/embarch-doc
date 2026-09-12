# 069 — `embarch-api/decisions/surface.md` is in reserve after decision 71

**State:** blocked
**Source:** `api/068`'s fix (decision 71, `validate`'s `kind`-branching wrapper) landed the
same commit that put this file into its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/decisions/surface.md
**Size debt due:** 2026-10-11
**In flux:** yes — this is the file every JSON/error-shape change to the tool/CLI surface
lands a decision in (decisions 16, 24, 50, 57, 67, and now 71, all here), so a shortening
pass now risks compacting prose a near-term surface-shaped unit will need to revise or add
to again. Unparked once a unit lands here without adding a new decision or materially
editing an existing one, or once a mission split is judged safe to do (this file's own
natural seam: "JSON shape and versioning" (16, 24, 50) vs "how a failure is reported and
attributed" (57, 67, 71)).
**Must not delete:** decision 50's argument for why `error_kind` was retired rather than
built (the Core-status-code-is-coarser-than-a-real-code-enum point — a future field named
`error_kind` must not silently repeat the mistake). Decision 67's scope note about
`tool-wrapping.md`'s own headroom, which is the reason this decision sits here rather than
there. Decision 71's three concrete facts: `kind` defaults to `"mismatch"` for an older
Core, `503` is dispatched through the same parse `409` already used, and both `tools.rs`
and `cli.rs` call `is_not_attached()` rather than re-deriving the condition from
`live_hardware_id.is_none()` — reverting any of the three is the regression `api/068`
exists to prevent.

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/decisions/surface.md` at 11258 B
against a 12288 B cap (91.6%) — inside the last 10% of its reserve, same mechanism
`api/057` already named for `zephyr.md`.

## Done when

- [ ] `embarch-api/decisions/surface.md` is back under its reserve band, its "must not
      delete" facts intact — a mission split (JSON shape/versioning vs failure-reporting)
      is one honest way to do it, not the only one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
