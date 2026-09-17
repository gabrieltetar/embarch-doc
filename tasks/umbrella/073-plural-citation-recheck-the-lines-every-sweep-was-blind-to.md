# 073 — Plural-citation re-check: the 13 lines every `umbrella` sweep was structurally blind to

**State:** open
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
