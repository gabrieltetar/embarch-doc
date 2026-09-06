# 028 — `embarch-api/open.md` and `spec.md` both crossed into reserve on the same commit

**State:** done on agent/api/028-compact-api, 2026-09-06
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

- [x] `open.md` and `spec.md` are both clear of their reserve lines. `open.md`
      4,711 -> **4,385 B** (85.6%), `spec.md` 9,333 -> **9,087 B** (88.7%);
      `check-doc-size.py --pressure` reports both PAID.
- [x] Every `Must not delete:` item above is still readable. The `board` bullet
      keeps the derived-from-`build_info.yml` claim, the day of bring-up and the
      unbuilt `validate`/`status` comparison; the `error_kind` bullet is
      untouched, ordering and HTTP-status warning intact; `spec.md` §2's
      no-inference-as-fact invariant and §6's trust-boundary sentence are
      untouched.
- [x] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *what does someone starting on `embarch-api`
      tomorrow lose if this paragraph is gone?*
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What went, and what did not

**`open.md`.** The smoke-harness bullet's two *closed* halves — the shared
client's own tests, and the bearer sweep — were history, and decisions 54, 55
and 56 hold them; what survives is the live residual, that the gate reports no
blind spot of its own. Two dates and one flourish went from the `board` bullet.
The **Settled-deferred** bullets kept every "why not" clause and lost only
wording.

**The last bullet was left in place, as `In flux:` requires** — its numbers were
re-measured rather than restated, and one had drifted: `surface.md` is 10,946 B,
not the 10,928 written there. Only that figure changed (and the four files
re-sorted descending to stay sorted). `core-link.md` at 12,266/12,288 is still
true and still filed under `tasks/api/026`.

**`spec.md`.** §3's opening paragraph restated `interfaces/config.md` rows 37,
39, 50, 54, 56 and 60 nearly verbatim — a §3 duplication. It now points there
for `default_target` narrowing, the `snippets` literal and build-dir naming, and
keeps only the two rules an agent would otherwise invert (`static` **refuses**
rather than accepts-and-drops; it has exactly one target, itself, the
`[[projects.targets]]` menu retired). §7's capture-cap row keeps its
`[assumed]` flag and points at decision 18, which says in its own text that the
provenance is the load-bearing part and owns the reasoning. "neither
privileged" went from §5, being already stated in §1.

No fact moved to a doc outside `embarch-api/`.
