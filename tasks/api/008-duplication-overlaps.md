# 008 — `embarch-api` holds fifteen claims in two files each

**State:** done
**Source:** tasks/api/007-compact-docs.md, closed 2026-09-04 when its reserve debt was paid — this is the half of it that was never about size
**Scope:** api
**Hardware:** none
**In reserve for this sub-project:** none. `open.md` (89.1%) and
`decisions/surface.md` (88.9%) both came **out** of reserve under `api/005`, and
`spec.md` came out under the 2026-09-04 compaction pass. This task has room.

## What

`scripts/check-duplication.py embarch-api` reports **15 overlaps of 12+ words**.
The two worth naming, because they are the largest and the most load-bearing:

- A **37-word run** between `interfaces/modules.md` and `spec.md` §5 — the
  512 MiB runtime-thread-stack paragraph, kept in both when the module map was
  split out of `spec.md`.
- **Four** between `decisions/surface.md` and `interfaces/tools.md`, all about
  `erase`.

**Every one of these is a `DOC-PROTOCOL.md` §3 question — which file owns the
claim — and not a `DOC-COMPACTION.md` §9 hot/cold one.** That distinction is why
this is filed separately rather than folded into a compaction pass: a §9 pass
asks whether a sentence still earns its place, and answering it about a sentence
that exists twice will delete the wrong copy about half the time.

## Why now

Not urgent, and deliberately not a size task. It was discovered while `api/007`
was looking for bytes, and it survived that task's closure because the bytes
turned out not to be needed — `api/005` freed both files by closing an `open.md`
bullet and moving decision 18 out of `surface.md`. The finding is real
independently of whether anything is in reserve, and `check-duplication.py` is
advisory and in nobody's gate, so nothing else will re-surface it.

`api/007`'s original `Must not delete:` still applies to any pass over these
files and is carried here verbatim rather than lost:

> `open.md`'s *do not derive a kind from the HTTP status* clause and its
> ordering (Core emits codes, the shared client carries one typed, this crate
> passes it on) — decision 50 exists because that shortcut was proposed and it
> is coarser than `embarch-core` decision 12's enum; decision 52's rejection of
> a `status --json` field, whose reason is that a diagnostic's input has to
> survive a broken machine.

## Done when

- [x] Each of the 15 overlaps is either resolved by assigning the claim to one
      file per `DOC-PROTOCOL.md` §3, or named here as a deliberate restatement
      with the reason. **Both are real answers**; a pointer in the losing file
      is usually better than silence where the claim used to be.
- [x] `check-duplication.py embarch-api` reports what you intended, and the
      commit message says which overlaps were kept on purpose.
- [x] No file pushed into reserve; if one is, file the debt in the same commit
      per `tasks/README.md` § "Compaction tasks".
- [x] Gate green, `changelog.d/api-*` fragment dropped.

## What shipped

`check-duplication.py embarch-api` reported **17**, not the 15 this task was
filed against: `interfaces/modules.md` was split out of `spec.md` §5 the same
day the task was written and carried two more claims with it. **Sixteen are
resolved by assignment, one is kept deliberately.** The report now reads 1.

**The rule the sixteen were decided under**, since two plausible ones disagree:
a `decisions/` entry may state its own claim — [DOC-COMPACTION.md](../../DOC-COMPACTION.md)
§5 says an entry *is* a heading stating the claim, and one that cannot state it
is not readable alone. What an entry must **not** carry is the *reference
detail* (a schema row, a table cell, a wire shape) or the *status* of a gap;
those belong to `interfaces/` and `open.md`. Applied the other way: an
`interfaces/` file carries the rule a caller obeys, never the argument for it.

| Claim | Was in | Now owned by | The other file now says |
|---|---|---|---|
| The 512 MiB runtime thread stack (37 w) | `interfaces/modules.md`, `spec.md` | `spec.md` §5 — the constant with its provenance sits in §7 beside it, and this is the one file an agent loads | a pointer from the module map |
| `erase`'s description: destructive, un-undoable, not needed by a normal reflash (32 w + 18 w + 15 w + 14 w — four of the report's rows) | `decisions/surface.md` 41, `interfaces/tools.md` | `decisions/surface.md` 41 — the *wording* is the design point, so changing it is a decision | `tools.md` keeps what a caller obeys (`false` by default, Core performs it, a refusal is relayed) and points at 41 |
| A dev-bench default would build the wrong image and flash it through the wrong interface at the wrong chip (25 w + 12 w) | `decisions/dev-bench.md` 45, `interfaces/config.md` | `decisions/dev-bench.md` 45 | `config.md` keeps the schema fact — every field required, a missing one a startup error naming it |
| NCS turns sysbuild on and vanilla Zephyr does not, so the image sits a directory deeper (12 w) | same pair | `decisions/dev-bench.md` 45 — it is the *evidence* for declaring `artifact_path`, read off a real build | `config.md`'s row says it varies with which SDK the workspace pulls, cited |
| Decisions 31 and 33 are one entry, and how the renumber happened (22 w) | `decisions.md`, `decisions/studies.md` | `decisions.md` — the index is where the permanent-numbers rule is argued from this breakage | the entry keeps only "both resolve here, neither is reused" |
| Truncation's marker and the 16/48 split (22 w) | `decisions/zephyr.md` 18, `spec.md` | `spec.md` §3 and §7 | decision 18 keeps the *why* — the first compiler error is the actionable one — and the `[assumed]` provenance |
| The cap bounds the retained bytes, not each half (13 w) | same pair | `spec.md` §3 | decision 18 keeps the heading as its own claim plus the rejected per-half cap; the restating sentence is gone |
| `1` means the shape as of 2026-09-03, not "unchanged since the beginning" (20 w) | `decisions/surface.md` 24, `interfaces/tools.md` | `decisions/surface.md` 24 | `tools.md` states the counter's scope and bump rule and cites 24 for its origin |
| A list mixing `"none"` with real snippet names is a call-time error (13 w) | `decisions/zephyr.md` 21, `interfaces/config.md` | `interfaces/config.md` — a caller reads the reference in order to obey it | decision 21 keeps the sentinel *choice* and the rejected silent interpretation |
| `build.rs` is the only module behind the `lib` target (12 w) | `interfaces/modules.md`, `spec.md` | `spec.md` §5 keeps the reason | the map row keeps the fact and the citation |
| Decision 27's capacity error is only half built (12 w) | `decisions/studies.md`, `open.md` | `open.md` — a gap's *status* is `open.md`'s | decision 27 says it is partially realised and points |
| The manifest inherits the artifact-transfer gap (12 w) | `decisions/studies.md` 39, `open.md` | `open.md` | 39 names the inheritance and points for the tracking |

**Kept on purpose — one, and the report still shows it.** *"Reflash means build
and flash the tree as it stands, then verify"* (12 w) is in `spec.md` §2 as an
invariant and in `decisions/studies.md` 40 as that decision's own claim. Neither
copy can go: an agent that loads only `spec.md` — the documented common case —
has to hit the no-`git checkout` rule *there*, and decision 40 stating its claim
is §5 working rather than failing. **Decision 40 now says so inline**, so the
next reader of the report finds the answer in the doc instead of in a task file
that will have been deleted. Twelve words is also the script's own idiom floor.

**Nothing in `embarch-api` is in reserve.** `spec.md` is the closest at 89%, and
this pass did not grow it — it won most of these arguments and gained nothing.
Four files shrank. No compaction debt filed, none owed.

**Doc-only.** No Rust touched, no hardware, and no suite-level fact made false,
so no `status.d/` fragment. The `Must not delete:` clauses above are untouched:
`open.md` was not edited at all, and decision 52 was not either.

**One honest red, and it is not this branch's:** `check-ownership.py --scope api`
against *local* `main` reports `tasks/umbrella/003-setup-dry-run.md` outside
scope. That path comes from the leg's own claim commit `61b5cd0`, which is
already on `origin/main`; against `origin/main` the check reads `OK: all 0
changed path(s) owned by the 'api' worker`. Local `main` is stale at `744419e`.
