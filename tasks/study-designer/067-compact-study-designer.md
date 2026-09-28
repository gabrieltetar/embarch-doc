# 067 — `interfaces/limits.md` and `decisions/protocols.md` are in reserve

**State:** done
**Dispatch note (supervisor, 2026-09-28):** overdue since 2026-09-24. The numbers below still hold
(14 B and 75 B left); re-derive them, and re-check `git log` on both — last touched 2026-09-17
(`685b691c`, the owner's "Study Designer authors every field" pass). **`interfaces/eap.md` already
exists (8,368 B)**, so before creating a new file for the `.eap` constants check whether they belong
there — a split into the file that already owns the `.eap` interface is cheaper than a new one, but
not if it pushes `eap.md` past 90% of 12,288 B (11,059 B). Also in reserve in this sub-project and
**not yours**: `decisions/gatt-extract.md` (36 B left, `069`), `decisions/declares.md` (88 B left,
`068`), `spec.md` (840 B left, `032`, blocked) and `open.md` (over its 5,120 B cap, `026`, blocked)
— push none of them further in; if a moved decision's citation lives in one of them, repoint it
only if the repoint does not grow the file. A citation **outside `study-designer`** you do not
edit: drop an inbox file by absolute path (`/home/gabriel/Github/embarch/embarch-doc/inbox/`) with
the exact fix and say so in your report; the supervisor repoints it at landing.
**Source:** `scripts/check-doc-size.py`'s reserve floor, crossed by `tasks/suite/045` — decision 75's `eap_repo` and the three advisory dev-bench caps
**Scope:** study-designer
**Hardware:** none
**Owner:** no
**Compacts:** embarch-study-designer/interfaces/limits.md, embarch-study-designer/decisions/protocols.md
**Size debt due:** 2026-09-24
**In flux:** no — `suite/045` closed the authoring gap `open.md` had carried since 2026-08-27, and nothing queued against this sub-project targets either file.

## What

`interfaces/limits.md` is **12,274 / 12,288 B (99.9%), 14 B left** and
`decisions/protocols.md` is **12,213 / 12,288 B (99.4%), 75 B left**. Both are
out of reserve when this closes, or the task says why not and what was deleted
instead.

The reserve was already half spent before this: decision 76 was written into
`decisions/protocols.md` and moved to `decisions/limits.md` in the same pass,
which is where a limits decision belongs and bought protocols.md ~1.4 KB. The
advisory-cap section in `interfaces/limits.md` was written twice and cut to the
table plus one line of posture, the argument living in decision 76. **Both easy
moves are already taken**, so this one is a real squeeze or a real split.

`interfaces/limits.md` is one long table plus the `.eap` block plus the new
advisory block. `DOC-COMPACTION.md` §2 prefers a split, and the seam is visible:
the `.eap` constants (decisions 58-62) are a self-contained group of eighteen
rows that nothing outside protocol work reads.

## Why now

14 bytes left means the next correction to any constant in that file cannot land
without paying first. Recording the debt is the mechanism; an unfiled file in
reserve is what `check-doc-size.py` fails on.

## Done when

- [x] Both files out of reserve, or the task says why not.
- [x] A split was preferred over deleting live reasoning per `DOC-COMPACTION.md`
      §2, or the report says why the seam was rejected.
- [x] If it split: every inbound citation still resolves and the group table
      gained its row.
- [x] Every `[measured]`/`[assumed]` marker and every provenance sentence
      survives — that column is the whole point of the file, and a constant
      whose sizing is deleted becomes a number nobody can revisit.
- [x] Decision 75's three load-bearing properties survive in full: `scan` never
      fails on a bad file, `defs()` is the only place a duplicate name is
      refused, `save` parses before it writes.
- [x] Byte numbers before and after, for every file touched.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/` fragment.

## Done

Two splits, both verbatim moves, no reasoning shortened.

**`interfaces/limits.md`** (12,274 → 8,951 B): the `.eap` protocol manifest
constants table (decisions 58–62, `MAX_PROTOCOLS_PER_STUDY` through
`MAX_WRITE_FIELDS`, 18 rows) moved verbatim to a new sibling file,
**`interfaces/eap-limits.md`** (0 → 4,251 B), replaced in `limits.md` by a two-
sentence pointer. Checked merging into the existing `interfaces/eap.md` first,
per the dispatch note — it doesn't fit: `eap.md` is 8,368 B and the block is
~3.8 KB, which would have landed it at 12,173 B, past its own 11,059 B reserve
floor (99% full, 115 B left) and simply moved the debt sideways. A new sibling
file was the alternative `DOC-BUDGET.md` names for that case, and one already
existed for the model: `interfaces/decoders.md`/`gatt-types.md`/`taps.md`/
`result-types.md` are all siblings of `types.md` for exactly this reason. Every
row's `[measured]`/`[assumed]` marker and provenance sentence is unchanged;
`eap-limits.md` cross-links back to `limits.md` and `eap.md` (which still holds
the `.eap` types, grammar and worked protocols — untouched) and cites
`../decisions/protocols.md` for why. No inbound citation broke: grepped the
whole doc repo and the code repo for every constant name in the moved table —
the only file-path citations to `interfaces/limits.md` are to the *retired*
constants section (`src/gatt.rs:52`, `src/result.rs:185`), which stayed put and
is unaffected. Code comments already citing `interfaces/eap.md` for this block
(`src/limits.rs:148,172`) only ever cited the worked-protocols narrative for
sizing rationale, which is still there, so no code repo change was needed —
made no commit in `embarch-study-designer`.

**`decisions/protocols.md`** (12,213 → 10,876 B): decision 71 (`A host-side
primitive still parsed but not rendered refuses loudly, by name`) moved
verbatim to **`decisions/payload-meaning.md`** (8,650 → 9,987 B). Decision 71 is
about `ResolvedProtocol::render_layout` producing a decision-52 `StructLayout`
— "where a byte payload acquires a meaning" is payload-meaning.md's own mission
statement, and the decision's own text cites decision 52 twice, a stronger
mission fit than `protocol-exec.md`'s "what a run does" (60, 62), which is
about the bench-side state machine, not host-side rendering. `decisions.md`'s
routing table updated to match (71 moved from the `protocols.md` row to the
`payload-meaning.md` row). Decision 71 is cited elsewhere only by number
(`src/crc.rs:180`, `decisions.md`), never by file path, so `check-decision-refs.py`
(which resolves by number per sub-project, not by file) sees no break, and no
code repo change was needed for this move either — confirmed a clean code
worktree (`git status`, 0 changed paths) rather than assuming it.

Decision 75's three properties (`scan` never fails on a bad file, `defs()` is
the only place a duplicate name is refused, `save` parses before it writes) are
untouched, still in `decisions/protocols.md`.

Gate: `check-docs.py` 11/11 green, `check-doc-size.py --pressure` shows both
files `PAID`/out of reserve, `check-ownership.py` clean on both worktrees,
`check-client-names.py` clean. `changelog.d/study-designer-eap-limits-split.changed.md`
filed. Zero commits in `embarch-study-designer` — nothing there needed changing.

Not touched, per the dispatch note: `decisions/gatt-extract.md`, `decisions/declares.md`,
`spec.md`, `open.md` — all separately filed and none pushed further in.
