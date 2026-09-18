# 085 — Check 15's open question still says a content hash is "`embarch-core`'s call", and the call was made

**State:** done 2026-09-17 leg 142 unit 3 — `agent/umbrella/085-check-15-hash-call-made`
**Doc-size reserve for `umbrella`** (leg 142, before dispatch): `decisions/install.md` 217 B left,
`decisions/bind.md` 755 B left, `decisions/projects.md` 1125 B left, `open.md` 851 B left — all four
filed against blocked compaction tasks. **`open.md` is the file this unit edits**; see the fourth
`Done when` box. If this unit pushes any file into the last 10% of its cap, file
`tasks/umbrella/<NNN>-compact-docs.md` in the same commit.
**Source:** leg 142's refill sweep of every `open.md` via `scripts/collect-open-questions.py`,
2026-09-17. Not a worker report and not a reviewer finding — the supervisor found it by reading
`embarch-umbrella/open.md` against `embarch-core/open.md` at the same moment.
**Scope:** umbrella
**Hardware:** none — one clause in one bullet of one markdown file, settled by reading two `open.md`
files and one decision against each other.
**Owner:** no

## What

`embarch-umbrella/open.md` line 9 reads:

> **Check 15 is not a hash comparison and must not be read as one.** It catches a *cross-version*
> stale deploy and is blind to a same-version one: `core_version` is `CARGO_PKG_VERSION`, so a
> rebuild and failed deploy at one version reads as a match ([decision 34](../../embarch-umbrella/decisions/schema-skew.md)).
> *(The link is written relative to `tasks/umbrella/` here; in the file itself it is
> `decisions/schema-skew.md`, relative to `embarch-umbrella/`. Keep the file's own spelling.)*
> **A content hash on `/status` would close it, `embarch-core`'s call.**

That last clause was true when written and is now stale. **`embarch-core` made the call on
2026-09-17**: `embarch-core/decisions/surfaces.md` **decision 67** settles that `/status` should
carry a self-hash of the running binary's own bytes, and settles *why* a git SHA or a build
timestamp will not do. `embarch-core/open.md` already carries the matching bullet in the right
tense — *"decided yes, not yet built… Filed as `tasks/core/088`, a wire-schema bump the supervisor
announces before landing"* — so the two `open.md` files now disagree about whether anyone has
decided anything.

**The cost of leaving it is specific, not cosmetic.** `embarch-core` decision 34's own history is
that this question sat in `embarch-umbrella/open.md` phrased as another repo's call, and nothing was
ever filed in that other repo, so the sentence was *true and unactioned for as long as it existed* —
which is the reason leg 141 had to go and file it. A reader arriving at this bullet today concludes
the same thing a second time and re-derives a decision that is already written down.

## Why now

Cheap, and it is the deferral-pointer class this suite treats as load-bearing: a bullet that names
another repo as the decider is worth exactly as much as its statement of whether that repo has
decided. It also gets *less* recoverable as `tasks/core/088` lands — once `/status` actually serves
the field, this bullet will read as though the fix is still unowned.

## Do not

- **Do not delete the bullet, and do not delete its first sentence.** `tasks/umbrella/077`'s
  `Must not delete:` list names *"`open.md`'s note that check 15 is not a hash comparison and must
  not be read as one"* explicitly. The bullet's whole job — check 15 is a version comparison, not a
  content one — is still true and still the thing a reader needs. **Only the final clause is stale.**
- **Do not say the field ships.** It does not. Decision 67 is a decision; `tasks/core/088` is the
  build and has not run. The honest tense is *decided, not yet built*, which is the tense
  `embarch-core/open.md` already uses.
- **Do not edit anything under `embarch-core/`.** That is another sub-project's row
  (`../embarch-fleet/protocol.md` §3) and its half is already correct anyway.
- **Do not restate decision 67's reasoning here.** One pointer, not a summary — `DOC-PROTOCOL.md`'s
  whole posture is that the decision lives in one place.

## Done when

- [x] The check-15 bullet's closing clause names `embarch-core` decision 67 as the call that was
      made, in the *decided-not-built* tense, and points at where the build is tracked
      (`tasks/core/088`) rather than at an unnamed future decider.
- [x] The bullet's first sentence — check 15 is not a hash comparison and must not be read as one —
      survives verbatim, and the `decision 34` link still resolves.
- [x] `embarch-core/open.md` is read and **not edited**, and the two bullets are confirmed to agree
      in tense afterwards.
- [x] `embarch-umbrella/open.md` is still inside its cap with room to spare. It was **4,269/5,120 B
      (83.4%)** at filing, filed against blocked `tasks/umbrella/077-compact-docs.md`
      (`In flux: yes`). This edit should be roughly net-neutral; if it is not, and the file crosses
      into the last 10%, say so in the report rather than silently spending the headroom.
      **Landed at 4,350/5,120 B (85.0%)** — +81 B, still 15.0% of cap free, not in the last 10%.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment: **not expected.** Nothing a reader of `history/umbrella.md` acts on
      changes — this is an open question's pointer, not shipped behaviour. If you disagree, say why
      rather than adding one by reflex.
