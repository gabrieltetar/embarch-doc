# 068 — Plural-citation re-check: the 11 lines every `core` sweep was structurally blind to

**State:** claimed by agent/core/068-plural-citation-recheck, 2026-09-16 20:35
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-core` was declared citation-swept after `core/058`, `core/066` and `core/067`. **Every one
of those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match `decisions 17, 18`
or `decisions 31/32`** — so these lines were never in any sweep's input at all. This is not a
re-read of checked work; it is the first read.
**Scope:** core
**Hardware:** none — doc comments, one `Cargo.toml` comment and one workflow comment. Nothing is
built for a board, no probe, no live Core, no deploy, no study. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `core`:** one file, `embarch-core/decisions/auth.md` at
**11,356/12,288 B (932 B left)**, filed as `tasks/core/046` and **blocked**. Nothing else in scope
is in reserve. A source-comment sweep should not need to write it; if it does, say why. If your work
leaves a `core` doc inside the last 10% of its cap with nothing filed against it, file
`tasks/core/<next free NNN>-compact-core.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Eleven lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git` and `target`:

```
src/logs.rs:4                     `embarch-topology` decisions 2/8/14
src/stream_store.rs:178           `embarch-outpost` decisions 17 and 18
src/outpost_manifest.rs:198       `embarch-outpost` decisions 17, 18
.github/workflows/release.yml:24  embarch-umbrella decisions 27/29
Cargo.toml:26                     embarch-topology decisions 2, 4, 8
src/service.rs:107                decisions 4/7            (bare — own repo)
src/study.rs:1255                 `decisions 30/31`        (bare — own repo)
src/study.rs:1916                 `embarch-outpost` decisions 4, 17, 18
src/study.rs:2910                 `embarch-outpost` decisions 17, 18
src/study.rs:4259                 `embarch-study-designer` decisions 31/32
src/main.rs:165                   decisions 31/32's        (bare — own repo)
```

**Eleven lines, roughly 28 distinct decision instances** — each line cites two to three numbers and
every number is its own claim. Treat the line count as a floor and report the instance count you
actually checked.

`.github/workflows/release.yml:24` is the exact line `core/067`'s re-census found by accident and
which its reviewer confirmed the filing census had missed; it is listed here for completeness, and
if `core/067` already checked it, say so and move on rather than re-deriving it.

## How

Same pass the chain has run eleven times, unchanged except for the census pattern:

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** `ui/054` found two sites spelled
   `Decision` at the start of a sentence that a case-sensitive grep skipped. Report your number
   against the eleven above.
2. **For each cited number, check the decision exists in the file the citation points at**, and
   remember a bare `decision NN` in another sub-project's file means *that* sub-project's NN. Three
   of the lines above are bare and are `embarch-core`'s own.
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** This is the half that finds real defects: `api/102` found a comment citing a
   real, existing, topically wrong decision, and `study-designer/054` found a citation that was
   correct when written and went false when another repo amended the decision it cited. A number
   that resolves is not the same as a sentence that holds.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation — a stale path, a count, a constant — is a finding for `inbox/`, not an edit; `api/102`
   did exactly that and `tasks/api/103` came out of it.

## Done when

Every plural-form citation line in `embarch-core` has had the existence-and-truth pass, the report
states the instance count checked against the eleven-line floor, and each defect found is either
fixed here or filed with its reason for not being fixed here.
