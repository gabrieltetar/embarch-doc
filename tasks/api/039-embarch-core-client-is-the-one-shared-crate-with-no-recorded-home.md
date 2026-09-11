# 039 — `embarch-core-client` is the one shared crate in the suite with no recorded home, and its module-map row is wrong about its own dependency shape

**State:** done — leg 073, 2026-09-10.

**Supervisor's dispatch note, leg 073.** Two things settled before dispatch so the worker does not
have to guess them:

- **The reserve objection in the fourth `Done when` box is discharged.** It says the decision must
  not land in `decisions/core-link.md` unless that file's reserve has been spent first, and names
  `tasks/api/026` as the thing that would spend it. `api/026` landed earlier in this leg: it took
  `open.md` and `spec.md` clear, and `core-link.md` itself came out of reserve back on 2026-09-07
  when `api/046` split `decisions/study-events.md` out of it. **`core-link.md` is 9,955 B against a
  12,288 B cap today — out of reserve, 2.3 KB of headroom.** So that box is satisfiable either way
  and is no longer a constraint on where the decision goes.
- **Where it should go is still the worker's call, and both candidates are healthy.**
  `decisions/core-link.md` 9,955 B and `decisions/shape.md` 10,969 B; `decisions/zephyr.md` is
  **1,981 B over cap** and filed against the blocked `tasks/api/057`, so nothing new goes there.
  Argue the choice in the commit message rather than defaulting.

This is documentation-only: everything it touches is in `embarch-doc`, and `embarch-api` has no
diff. Do not create a code worktree.
**Source:** suite review pass 2026-09-06, dimensions 1 and 4 (two hunters, one finding). Code-confirmed.
**Scope:** api
**Hardware:** none
**Owner:** no

## What

The suite has three shared crates. Two had this exact question reasoned in writing:

- `embarch-study-designer/decisions/crate.md` decision 8 — *"standalone rather than a workspace
  member of an existing repo — three independently-versioned consumers … is the case a shared
  standalone crate is for."*
- `embarch-topology/decisions/crate.md` decision 13 followed it — *"a plain path dependency —
  exactly `embarch-study-designer`'s precedent."*

The third — the one implementation of how anything reaches Core — lives **inside one of its
consumers**, at `embarch-api/crates/embarch-core-client`, and `embarch-ui/Cargo.toml` path-depends
on it as `path = "../embarch-api/crates/embarch-core-client"`. `embarch-api/decisions/core-link.md`
decisions 37/38 settle the dependency *kind* (*"A plain path dependency, not a Cargo
workspace"*) and never the *location*.

**The consequences are documented and unmitigated.** `embarch-api/spec.md:48` — *"`embarch-ui`
path-depends on it from outside that workspace — **a change there reaches a repo this one does not
own**."* `suite/decisions.md` 1 spends a paragraph on the gate spellings this nesting creates (`--all`
reaching 33 files outside the repo, `embarch-topology` reached *transitively* through it).
`check-ownership.py` treats `embarch-api` as one worker's whole tree, so nothing refuses the move
that would break `embarch-ui`.

**And its own module-map row is now wrong.** `embarch-api/interfaces/modules.md`'s last row says
*"**A path dependency, not a workspace member**, and `embarch-ui` path-depends on it too, so a
change here reaches a repo this one does not own."* The first clause was reversed by decision 56
on 2026-09-06 — the manifest now declares it both a `member` and a `default-member`
(`embarch-api/Cargo.toml:12-14`). The second clause is the hazard, correctly named, in a row that
is otherwise false.

Candidate direction: not necessarily a ninth repo. The minimum property is that the crate has one
recorded home and owner, so a task about it has a scope, and the module-map row states its current
dependency shape. Whether that means its own sub-project docs, a named section in an existing one,
or a move, is a judgement worth writing down either way.

## Why now

The cost is landing on the queue rather than on the code. `tasks/api/032`'s own text: *"Pinning
both mirrors 'from each side' needs a matching test in `embarch-core` … that is a second task in a
second repo, and a worker must not reach across."* The crate's decisions are spread across six
doc locations in three sub-projects, and the file carrying most of them
(`embarch-api/decisions/core-link.md`) is **22 bytes from its cap** with `tasks/api/026` blocked on
it — so whoever takes this must not plan to write the decision there. And
`embarch-fleet/protocol.md` §5 rule 2 forbids a worker reaching across repos, while half this
crate's consumers are across one.

## Done when

- [x] `embarch-api/interfaces/modules.md`'s core-client row states its actual dependency shape
      post-decision-56.
- [x] There is one place that records why the shared Core client lives inside a consumer's repo,
      what that costs, and what would reverse it. Decision 66, `decisions/core-link.md`.
- [x] A future task about this crate has an unambiguous scope: `embarch-api` owns the crate and its
      decision; `tasks/ui/013` is the adjacent, separate stale-claim fix in `embarch-ui`.
- [x] The decision does not land in `decisions/core-link.md` unless its reserve has been spent
      first (`DOC-COMPACTION.md` §2, `tasks/api/026`) — discharged per this leg's dispatch note;
      landing decision 66 there pushed the file 5 B under cap and into its own reserve, filed as
      `tasks/api/061-compact-api.md` (blocked, in flux).
- [x] Gate green; `changelog.d/api-core-client-home.decided.md`.

**Adjacent, not the same:** `tasks/ui/013` fixes a stale topology claim in `embarch-ui/Cargo.toml`.
