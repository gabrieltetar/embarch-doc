# 050 — Plural-citation re-check: the 12 lines every `topology` sweep was structurally blind to

**State:** open
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-topology` was declared **completely** citation-swept after `topology/040`, `046` and `049`.
**Every one of those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match
`decisions 3, 9` or `decisions 10/11`** — so these lines were never in any sweep's input at all.
This is not a re-read of checked work; it is the first read, and "completely swept" was measured
with an instrument that could not see this form.
**Scope:** topology
**Hardware:** none — doc comments and one workflow comment. Nothing is built for a board, no probe,
no live Core, no deploy, no study. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `topology`: nothing in reserve.** `embarch-topology`'s files are all clear
after `topology/043`, `044` and `048`. If your work pushes a `topology` doc into the last 10% of its
cap, file `tasks/topology/<next free NNN>-compact-topology.md` in the same commit per
`tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Twelve lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git` and `target`:

```
src/lib.rs:11                     (decisions 5, 8)         bare — own repo
src/software.rs:3                 decisions 3, 4, 11       bare — own repo
src/hardware/mod.rs:131           (decisions 17, 18)       bare — own repo
src/hardware/mod.rs:148           (decisions 3, 9 — no env var overrides any more)
src/hardware/mod.rs:227           (decisions 8, ...)       check the full line, it wraps
src/hardware/signal.rs:29         matching decisions 10/11
src/hardware/signal.rs:199        (decisions 3, 9)
src/hardware/hardware_id.rs:6     (decisions 2, 4)
.github/workflows/release.yml:22  embarch-umbrella decisions 27/29
src/hardware/port.rs:3            (decisions 2, 4)
src/hardware/port.rs:590          (decisions 3, 9)
src/hardware/validate.rs:2        (decisions 2, 8)
```

**Twelve lines, roughly 25 distinct decision instances** — every line cites two or three numbers and
each number is its own claim. Treat the line count as a floor and report the instance count you
actually checked. `src/hardware/mod.rs:227` wraps; read the whole comment, not the grep hit.

**Eleven of the twelve are bare** — no repo prefix — and this repo is the one where that is most
likely to be right, since these sit in `embarch-topology`'s own source citing its own decisions.
Confirm rather than assume: the chain's standing rule is that a bare `decision NN` in another
sub-project's file means *that* sub-project's NN, and this repo is cited by four others.

## How

Same pass the chain has run eleven times, unchanged except for the census pattern:

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** `ui/054` found two sites spelled
   `Decision` at the start of a sentence that a case-sensitive grep skipped. Report your number
   against the twelve above.
2. **For each cited number, check the decision exists in the file the citation points at.**
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** This is the half that finds real defects: `api/102` found a comment citing a
   real, existing, topically wrong decision, and `study-designer/054` found a citation that was
   correct when written and went false when another repo amended the decision it cited. A number
   that resolves is not the same as a sentence that holds. `src/hardware/mod.rs:148`'s parenthetical
   — *"no env var overrides any more"* — is a factual claim about current behaviour as well as a
   citation, so check it against the code too.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation is a finding for `inbox/`, not an edit.

## Done when

Every plural-form citation line in `embarch-topology` has had the existence-and-truth pass, the
report states the instance count checked against the twelve-line floor, and each defect found is
either fixed here or filed with its reason for not being fixed here.
