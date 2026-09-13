# 083 — `embarch-api/spec.md` is in reserve after the dev-bench-config index fix

**State:** blocked
**Source:** `api/082`'s `Config:` pointer edit (adding `interfaces/dev-bench-config.md` alongside
`interfaces/config.md`) put this file into its reserve band; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/spec.md
**Size debt due:** 2026-09-27
**In flux:** yes — this is the sub-project's "what is true now" doc, and nearly every `api` unit
that lands a behaviour change touches it (most recently `api/080`, `api/082`); a compaction pass
run now risks shortening prose the next such unit will need to revise or add to within days.
Unparked once a unit lands here without adding a new invariant, constant row or module note, or
once the file is judged safe to split (its own natural seam: §§1-2 "what it is and what must
always hold" vs §§3-7 "how it does it" — build orchestration, deployment, modules, security,
constants).
**Must not delete:**
- Every bullet in §2 Invariants — each is a load-bearing rule an agent must not invert, several
  citing the specific incident that established it (the artifact-freshness race, the tree-mutating
  `git` ban, the `lagged`-frame-is-a-fact rule).
- The Session-0/UNC failure signature in §4 ("the network name cannot be found") — the concrete
  symptom that tells a future reader this is not an account problem.
- The `base_url = "auto"` resolution order and its "a `401` counts as an answer" line in §4 — easy
  to silently simplify away, hard to rediscover.
- Every row and Provenance column in §7's constants table, especially the `[measured]`/`[assumed]`
  tags — losing the tag turns an assumption into an unstated fact.

## Why now

`python3 scripts/check-doc-size.py` names `embarch-api/spec.md` at 9090/10240 B (88.8%, 1150 B
left) — inside the last 10% reserve band (`RESERVE_FLOOR` = 1200 B), crossed by `api/082`'s
pointer-line edit.

## Done when

- [ ] `embarch-api/spec.md` is back under its reserve band, its "must not delete" facts intact —
      a mission split (§§1-2 vs §§3-7) is one honest way to do it, not the only one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
