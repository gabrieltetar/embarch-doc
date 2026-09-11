# 060 — `embarch-api/open.md` is 221 bytes inside its reserve floor

**State:** open
**Source:** `api/026`'s fold, leg 073, 2026-09-10. `api/026` squeezed this file to 3,914 B — six
bytes under a 3,920 B floor — and its reviewer then found that the squeeze had **deleted a fact
recorded nowhere else in the suite** (`inbox/api-026-squeeze-quoting-and-lost-fact.md`, resolved at
the fold rather than filed as its own task). Restoring that fact cost 227 B and put the file back
inside reserve. `DOC-COMPACTION.md` §2 — the commit that spends the reserve is the one that files
the debt, and this is that filing.
**Scope:** api
**Hardware:** none
**Owner:** no

**Compacts:** embarch-api/open.md
**Size debt due:** 2026-09-24
**In flux:** no. `api/026` established this for both its files and its reasoning holds: the
event-stream flux that parked the old `api/026` moved out into `decisions/study-events.md` and was
settled by `api/035` against a real Core.
**Must not delete:** the restored sentence itself — **"`embarch init` never writes `serial_port` at
all"**, with its pointer to `embarch-umbrella` decision 17's minimal discovery schema. The reviewer
swept `embarch-umbrella/spec.md`, `decisions/projects.md`, `decisions/integration.md`,
`embarch-api/interfaces/config.md`, `interfaces/tools.md`, `decisions/core-link.md`,
`history/api.md`, `suite/features.md` and `features.d/*` at merge `04929b8` and found the claim
stated **nowhere else** — umbrella decision 17 describes the minimal schema without ever naming
`serial_port`. It was deleted, not moved, and it is back only because a reviewer caught it. Also
inherited from `api/026`: decision 15's failure signature, decision 36's rejected
`Builder::thread_stack_size` and its 64 MiB/512 MiB pair, decision 26's correction, and decision
55's corrected `default_headers` rejection — all of which live in `decisions/core-link.md` and were
untouched.

## What

`embarch-api/open.md` is **4,141 B against a 5,120 B cap, 979 B left against a 1,200 B floor** —
221 B inside reserve.

## Why this one should probably not be paid by squeezing

**This file has now been squeezed twice in three days and both passes ended with a reviewer putting
a fact back.** `api/031` cut it 4,802 → 3,782 B; `api/026` cut it again to 3,914 B, six bytes under
the floor, and lost the `serial_port` aside doing it. The same thing happened to
`embarch-core/open.md` in the same leg (`tasks/core/036`). Two independent passes tuned to within
single-digit bytes of a floor, each losing one real claim, is evidence about the floor rather than
about the compactors.

So the outcome this task should be willing to reach is **"no safe cut remains, and the cap is wrong
for what this file holds"** — written down as an argument, with what was considered. That is a real
finding, not a failure to complete. `DOC-COMPACTION.md` §2 prefers a split, and this file has six
named sections, so a split has at least not been tried.

**Changing the cap is not this task's to do** — `DOC-BUDGET.md` carries it. If the conclusion is
that the cap is wrong, say so here and file it for the owner.

## Done when

- [ ] `embarch-api/open.md` is clear of its reserve floor (≤ 3,920 B), **or** this task closes with
      a written argument that no safe cut or split remains, naming what was considered and whether
      the cap is the thing that should move.
- [ ] The restored `serial_port` sentence and every other `Must not delete:` item is still readable
      in full.
- [ ] The commit message quotes the **first dozen words of every deleted hunk verbatim**
      (`DOC-COMPACTION-PASS.md`). `api/026` paraphrased its one real cut instead of quoting it,
      which is why the loss was only findable by a reviewer reading the whole diff.
- [ ] The commit message answers the human question in the compactor's own words: can
      `embarch-api/spec.md` alone answer what someone needs to work on `embarch-api` today?
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
