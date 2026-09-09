# The shared directory's permissiveness is load-bearing for embarch-topology and no embarch-core decision records it

**State:** open
**Source:** `embarch-fleet/supervisor-log.md`, unit `core/023` (doc `2d070a8`, fold `e5fa115`), leg 059 — an owed decision the burndown constraint forbade that unit from authoring
**Scope:** core
**Hardware:** none
**Owner:** no

## What

Nothing on `embarch-core`'s own decision log records that `%ProgramData%\embarch`'s permissive ACL
is **deliberately** preserved. The unit's reviewer checked `embarch-core/decisions.md`,
`decisions/handshake.md` and `decisions/surfaces.md` and found it stated in none of them.
`embarch-topology` records the dependency, but only from topology's side.

The consequence is one-directional and specific: **a future core-side change tightening that
directory's ACL would silently break the cross-repo sharing, with nothing in this repo to catch
it.** A core author reading only core's decisions would have no reason to know the permissiveness
is a contract rather than a default nobody got around to hardening — and "we lock the token file,
not the directory" reads, to that author, exactly like an oversight worth fixing.

## Why now

`core/023` landed under leg 059's burndown constraint, which forbids a unit from authoring a new
numbered decision. That constraint is right — a decision is the most expensive thing in this suite
to reverse and burndown optimises for volume — but the cost here is a cross-repo invariant that
currently exists in one repo's head only.

**It is filed now because of where it was living.** The supervisor recorded it in
`supervisor-log.md` and nowhere else, calling it "the owner's to author". Two of that burndown's
five owed decisions went into an `open.md` "Owed decisions" section and one became
`tasks/outpost/015`; this one and `api/031`'s did not. `supervisor-log.md` folds daily and rolls
into `log-archive/` past 40 KB, so an owed decision recorded only there is on a timer. That is the
tracking gap, not just this one item: **three mechanisms for one class of debt, and the weakest is
the default.**

## Done when

- [ ] A numbered `embarch-core` decision states that the shared directory's permissiveness is
      deliberate, what depends on it, and what a future author must do instead of tightening it.
- [ ] It names the topology-side dependency explicitly, so the invariant is discoverable from
      core's decisions alone — that is the whole point, and a decision that only says "keep it
      permissive" without saying who breaks does not close this.
- [ ] `embarch-topology`'s side is consistent with it afterwards: still correct, and citing the new
      decision rather than asserting the core-side behaviour on its own authority.
- [ ] **No code change.** The ACL behaviour as shipped is correct and `embarch-token.md` already
      describes it accurately since `2d070a8`. This is a decision-record gap only.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

## Doc-size note for whoever takes this

`embarch-core/decisions.md` was **not** in reserve as of 2026-09-09, so there is room to write.
`embarch-core/open.md` is at **4,813/5,120 B (94.0%, 307 B left)**, filed against
`tasks/core/022-compact-core.md` — which leg 060 reopened after a worker closed it with its
`open.md` item still unpaid. If this decision also needs an `open.md` edit, check that file first;
it is 307 bytes from its cap and already owes ~750 B.
