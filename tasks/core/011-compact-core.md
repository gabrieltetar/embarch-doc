# 011 — `embarch-core/open.md` crossed into reserve

**State:** done, agent/core/011-compact-core, 2026-09-06
**Source:** `core/005` spent the last of this file's headroom adding a structural-limits bullet; `DOC-COMPACTION.md` §2
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/open.md
**In flux:** **No, for the file as a whole.** Every subsystem it describes is
shipped and deployed; nothing here is a design mid-rewrite, and `core/005` — the
change that spent the reserve — touched only test-side evidence for an invariant
that has not moved since decision 5.

**But three bullets are live measurements, not prose, and must be re-measured
rather than restated from memory:** the signal-tap bullet's "no real port has
ever been resolved or read", decision 35's "the Espressif relation is verified
only by construction", and the Windows-registry bullet's "has never executed on
real hardware". Each is true only until someone plugs something in, and a
compactor who paraphrases one is asserting a hardware fact it did not check
(`embarch.md` §5's rule, and this suite's most expensive failure mode).

**Also note the queue:** `core/006`–`core/010` are open against this
sub-project, and at least `008` and `009` will add or remove individual bullets
here. That is a merge nuisance, not a reason to park — they edit bullets, not
the file's shape.

**Must not delete:**
- The **`validate_signal` has no caller anywhere, deliberately** reasoning.
  Without the "resolving a route at the moment of use *is* the validation"
  sentence it reads as an oversight and someone wires up a second check.
- Decision 36's **counterfactual is not established** — evidence, not proof.
  Shortened, it becomes proof, which is the exact claim it refuses to make.
- The **18 stale records** finding and *why* the purge does not reach them
  (they are inside the USB-UART bridge). It is the only place that is written,
  and it is what makes the clear correct-and-free rather than broken.
- The SSE bullet's **reason** the missing `Last-Event-ID` is closed rather than
  owed: both consumers fall back to polling on a drop instead of pretending to
  resume. Cut the reason and the bullet reads as an unaddressed gap.
- In the **route sweep proves rejection, not reach** bullet (decision 42), the
  rejection-versus-reach distinction itself. The bullet may be shortened; that
  distinction is the whole of it, and losing it makes the sweep read as a
  guarantee that each route is wired to the right handler, which it is not.

## What

`open.md` is **4,885 B against a 5,120 B cap**; the reserve line is 4,608. It
was 4,422 B before `core/005`, so it had 186 B of clearance — any bullet at all
was going to cross it.

The cheapest real reduction is **Structural limits**, six bullets that are
mostly pointers to a doc that already carries the full account
(`embarch-token.md`, `embarch-api/decisions/core-link.md`); several restate what
they point at. **Never exercised** should be touched last and least — it is the
honest ledger of what this sub-project has *not* proven, which is the thing this
file exists for.

## Why now

`check-doc-size.py` fails on a file in reserve with no task naming it, and the
commit that spends the reserve is the one that files it (`DOC-COMPACTION.md`
§2). This task is that filing. Nothing else in `embarch-core` is in reserve —
`spec.md` is at 82% and `decisions/platform.md` at 48%.

## Done when

- [x] `open.md` is clear of its reserve line (under 4,608 B).
- [x] Every `Must not delete:` item above is still readable.
- [x] No live measurement above is restated from memory rather than re-measured
      or left alone.
- [x] The commit message answers `DOC-COMPACTION-PASS.md`'s question in the
      compactor's own words: *what does someone starting on `embarch-core`
      tomorrow lose if this paragraph is gone?*
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Outcome

`open.md` **4,885 -> 4,488 B** (87.7% of the 5,120 cap, 120 B below the 4,608
reserve line). Only the **Structural limits** section and one cross-reference
were touched; `Never exercised`, `Unverified diagnoses` and `Moved elsewhere` —
which hold all three live hardware measurements and three of the five
`Must not delete:` items — are byte-for-byte unchanged, so **no measurement was
re-measured and none was restated.**

Two bullets deleted, both nameable as answered rather than dropped:

- The `EMBARCH_TOKEN`/no-TLS bullet. `spec.md` §2's auth invariant already says
  "No per-caller identity and no TLS" and points at `embarch-token.md`, whose §8
  is the threat model. A claim held in two of the four files is the §3 error
  `check-duplication.py` exists to find, not an open question.
- `FlashedThisRun is unreachable from Core alone`. Decision 31 states it with
  its reason ("that needs a build, which is `embarch-api`'s job"), and
  `embarch-study-designer/interfaces/types.md` states it for the field itself.

Two shortened, each keeping the clause its `Must not delete:` entry names: the
route sweep keeps **rejection, not reach** and what that fails to catch; the SSE
bullet keeps **why the missing `Last-Event-ID` is closed rather than owed** —
both consumers fall back to polling instead of pretending to resume.

`collect-open-questions.py`: 104 -> 102, exactly the two above.

Nothing in `embarch-core` remains in reserve, so no follow-on compaction task is
filed. No code change: this task is doc-only, and the code branch is unmodified.

