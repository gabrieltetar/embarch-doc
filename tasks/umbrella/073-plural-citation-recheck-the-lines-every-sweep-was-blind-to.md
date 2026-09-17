# 073 — Plural-citation re-check: the 13 lines every `umbrella` sweep was structurally blind to

**State:** done — worker agent/umbrella/073-plural-citation-recheck, 2026-09-16. Re-census matched
the floor exactly (13 lines); existence-and-truth pass on all 30 instances found 0 wrong numbers
and 0 false sentences. No code change landed in `embarch-umbrella` — see "Result" below.
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-umbrella` was declared **completely** citation-swept after `umbrella/066` and `umbrella/072`.
**Every one of those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match
`decisions 2, 3` or `decisions 53/13`** — so these lines were never in any sweep's input at all.
This is not a re-read of checked work; it is the first read, and "completely swept" was measured
with an instrument that could not see this form.
**Scope:** umbrella
**Hardware:** none — doc comments, two `Cargo.toml` comments and one workflow comment. `doctor` is
not executed; nothing is built for a board, no probe, no live Core, no deploy, no study. Classified
fresh at filing.
**Owner:** no

**Doc-size reserve for `umbrella`:** one file, `embarch-umbrella/decisions/bind.md` at
**11,533/12,288 B (755 B left)**, filed as `tasks/umbrella/009` and **blocked**. Nothing else in
scope is in reserve. A source-comment sweep should not need to write it; if it does, say why. If
your work leaves an `umbrella` doc inside the last 10% of its cap with nothing filed against it,
file `tasks/umbrella/<next free NNN>-compact-docs.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Thirteen lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git` and `target`:

```
src/config.rs:21                  `embarch-api` decisions 53/13
src/state.rs:32                   (decisions 48 and 51, `embarch-umbrella/decisions/sticky-host.md`)
src/main.rs:306                   embarch-topology decisions 2, 3
.github/workflows/release.yml:23  embarch-umbrella decisions 27/29
Cargo.toml:24                     `embarch-topology` decisions 2, 3, 4, 6
Cargo.toml:52                     embarch-umbrella decisions 32/50 (deploy.md)
src/env.rs:6                      decisions 2, 3           — check whose; the line wraps
src/setup.rs:5                    decisions 3, 4, 7        bare — own repo
src/setup.rs:76                   `embarch-topology` decisions 2, 3
src/init.rs:3                     Decisions 10, 12, 13     CAPITALIZED — own repo
src/doctor.rs:141                 `embarch-topology` decisions 2, 3
src/doctor.rs:1977                (decisions 33, 35)
src/doctor.rs:4329                check 11 ... (decisions 35, 36)
```

**Thirteen lines, roughly 31 distinct decision instances** — every line cites two to four numbers and
each number is its own claim. Treat the line count as a floor and report the instance count you
actually checked.

Two things to notice before you start:

- **`src/init.rs:3` spells it `Decisions`, capitalized.** That is the *second* blind spot in the
  canonical census instruction — `tasks/doc/065` records the case-sensitivity one and
  `tasks/doc/069` records this plural one — and this line is invisible to both defects at once.
  Grep case-insensitively.
- **`src/env.rs:6` reads `decisions 2, 3), so this file shrank to just this`** — the line wraps and
  the repo prefix, if any, is on the line above. Read the whole comment, not the grep hit. The same
  caution applies to `Cargo.toml:24`, which continues onto the next line.

## How

Same pass the chain has run eleven times, unchanged except for the census pattern:

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** Report your number against the
   thirteen above.
2. **For each cited number, check the decision exists in the file the citation points at**, and
   remember a bare `decision NN` in another sub-project's file means *that* sub-project's NN. This
   repo cites `embarch-topology` and `embarch-api` heavily, so the prefix is load-bearing.
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** This is the half that finds real defects: `api/102` found a comment citing a
   real, existing, topically wrong decision, and `study-designer/054` found a citation that was
   correct when written and went false when another repo amended the decision it cited. A number
   that resolves is not the same as a sentence that holds. The three `embarch-topology decisions
   2, 3` sites all assert *"live, in-process, every call"* as present-tense behaviour — check that
   against the decisions' current text, not just against each other.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation is a finding for `inbox/`, not an edit.

## Done when

Every plural-form citation line in `embarch-umbrella` has had the existence-and-truth pass, the
report states the instance count checked against the thirteen-line floor, and each defect found is
either fixed here or filed with its reason for not being fixed here.

## Result, worker (umbrella/073), 2026-09-16

**Re-census:** `grep -rInE '[Dd]ecisions? [0-9]'` over the repo (excluding `.git`/`target`),
filtered to the plural form, returned exactly the same 13 lines listed above — no fourteenth line,
no dropped one.

**Instance count:** 30, not the ~31 estimated as a floor (`config.rs:21` is 2, `state.rs:32` is 2,
`main.rs:306` is 2, `release.yml:23` is 2, `Cargo.toml:24` is 4, `Cargo.toml:52` is 2, `env.rs:6` is
2, `setup.rs:5` is 3, `setup.rs:76` is 2, `init.rs:3` is 3, `doctor.rs:141` is 2, `doctor.rs:1977`
is 2, `doctor.rs:4329` is 2 — sum 30). All 30 got the full existence-and-truth pass: number resolved
in the file the citation names (own-repo bare, or the stated cross-repo prefix), then the cited
decision's current body read against the sentence around the citation.

**Findings: 0 wrong numbers, 0 false sentences.** Notable checks:

- The three `` `embarch-topology` decisions 2, 3 `` sites (`main.rs:306`, `setup.rs:76`,
  `doctor.rs:141`, plus `env.rs:6` bare) all assert present-tense "live, in-process, every call" —
  checked against `embarch-topology/decisions/crate.md`'s decisions 2 and 3 (unreversed, unamended)
  and against the actual code: all three call sites do call
  `embarch_topology::software::resolve_software_topology`/`topology::resolve_software_topology`
  live, per call. Holds.
- `Cargo.toml:24`'s `` `embarch-topology` decisions 2, 3, 4, 6 `` (the line that wraps) — all four
  exist (2/3 in `crate.md`, 4 in `consumer-boundary.md`, 6 in `crate.md`) and the sentence
  ("software-topology detection... now calls this shared crate live, in-process", no `hardware`
  feature) matches all four bodies, including decision 4's "both software and hardware topology, in
  one pass."
- `Cargo.toml:52`/`state.rs:32`'s decisions 32/50 and 48/51 (`embarch-umbrella/decisions/deploy.md`,
  `sticky-host.md`) checked against both the decision bodies and the current
  `src/deploy.rs::landed`/`src/setup.rs::apply_plan` implementations — both still hash-based (not
  length) and still clear `saved.host` on a non-`remote` conclusion, exactly as the comments claim.
- `release.yml:23`'s `27/29` is one decision recorded under two numbers
  (`decisions/release.md`'s own "renumbered... recorded rather than renumbered again" note) — a
  plural citation of a single entry, not two separate ones; both resolve to the same heading and
  the sentence (mismatch fails the release outright, gates the build matrix) matches, and the repo's
  `verify-version` job still `needs:`-gates the build matrix.
- `config.rs:21`'s `` `embarch-api` decisions 53/13 `` (targets/soc_chip_overrides retirement) still
  matches the two structural refusals in `Config::validate`.
- `setup.rs:5`'s bare `decisions 3, 4, 7` and `init.rs:3`'s bare (capitalized) `Decisions 10, 12, 13`
  — both own-repo, both resolved to `install.md`/`topology.md` and `integration.md`/`projects.md`
  respectively, and both module-doc summaries still match the decision bodies' current text.
- `doctor.rs:1977`/`doctor.rs:4329`'s decisions 33/35/36 (own repo, `decisions/schema-skew.md`) —
  match the `SchemaVersions` struct fields and the check-11 test names/bodies exactly.

**Doc-size reserve:** untouched. No prose written to `spec.md`, `open.md`, or any decisions file;
`decisions/bind.md` stays at its filed, blocked `tasks/umbrella/009` reserve. No new compaction task
needed.

**No `inbox/` drop filed** — no finding here fell outside this task's scope (no wrong number that
wasn't a decision citation, no second-repo issue).
