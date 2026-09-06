# 028 — `embarch-api/open.md` and `spec.md` both crossed into reserve on the same commit

**State:** claimed by agent/api/028-compact-api, 2026-09-06 16:25
**Source:** `api/024` spent the last 3 and 6 bytes of these two files' headroom writing decision 56; `DOC-COMPACTION.md` §2
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md, embarch-api/spec.md
**In flux:** no, for `spec.md`. It describes what this binary is today, and
nothing about the surface it documents is mid-change: `api/022` closed the auth
funnel, `api/024` closed the gate-reach question, and the two `open.md` items
that could rewrite it (`api/001`'s live SSE run, `api/025`'s `init` refusal) are
scoped to `open.md`'s own bullets rather than to `spec.md`'s prose.
**Yes, for `open.md`'s last bullet only** — "The decision corpus has no headroom
left" is a live measurement of five files that `api/026` is actively moving. Do
not restate that bullet's numbers from memory; re-measure or leave it alone.
**Must not delete:** `open.md`'s **Known wrong, not fixed** bullet — the derived
`board` and the day of bring-up it cost — until `api/025` lands; it is the only
place the cost is written. The `error_kind` bullet's **ordering** (Core emits
codes, then the shared client carries one typed, then this crate passes it on)
and its "do not derive a kind from the HTTP status" warning: the ordering is the
whole content and the warning is a trap someone will otherwise re-enter.
In `spec.md`, §2's no-inference-as-fact invariant, and §6's statement that the
inbound trust boundary is "whoever can spawn the process" — both are cited from
elsewhere by name.

## What

`open.md` is **4,886 B against a 5,120 B cap** and `spec.md` is **9,333 B against
10,240 B**; the reserve lines are 4,608 and 9,216. Both were 3 and 6 bytes clear
of reserve before this commit, which is not headroom — it is the wall with a
rounding error in front of it.

**`open.md` is the one that actually needs work.** It is a 5 KB cap holding four
sections, and its **Settled-deferred** section is six bullets of things
deliberately not being done — the cheapest real reduction in the file, and the
one least likely to lose a fact somebody needs. `spec.md` has 907 B and can wait
behind it if a pass runs short.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md` §2).
This task is that filing. `api/026` already carries the decision corpus; this is
the other half of the same squeeze and is deliberately a separate task because
`026` is blocked on `api/001` and this is not.

## Done when

- [ ] `open.md` and `spec.md` are both clear of their reserve lines.
- [ ] Every `Must not delete:` item above is still readable.
- [ ] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *what does someone starting on `embarch-api`
      tomorrow lose if this paragraph is gone?*
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
