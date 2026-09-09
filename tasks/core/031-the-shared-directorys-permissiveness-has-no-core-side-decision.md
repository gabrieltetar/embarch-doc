# The shared directory's permissiveness is load-bearing for embarch-topology and no embarch-core decision records it

**State:** claimed — leg 061, worker on `agent/core/031-shared-dir-decision`

**Dispatch note (supervisor, leg 061):** this is a normal leg, not burndown, so authoring the
numbered decision is in scope — that is the whole task. Write it in `embarch-core/decisions.md`
(or the `decisions/` topic file whose subject it actually belongs to), which is **not** in reserve.
**Doc-size reserve for `core`:** `embarch-core/open.md` 4,813/5,120 B (307 B left) filed against
`tasks/core/022-compact-core.md`, and `embarch-core/spec.md` 9,148/10,240 B filed against
`tasks/core/030-compact-core-spec.md` — both already filed, neither blocked. If your edit pushes a
file further into reserve or leaves one there unfiled, file `tasks/core/<NNN>-compact-core.md` in
the same commit. Prefer replacing `open.md` prose with a citation to the new decision over adding
to it; that is a net saving and it is what the task asks for.
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
