# 190 — The HIL guide's Words point at the glossary

**State:** open — `doc/102`'s glossary rows landed; the glossary now defines Study, and Bench, Test, Run, Measurement and Verdict have no glossary row of their own, so gloss those in place and point only where a row exists
**Source:** EMB-317 — hil-guide's "Words" section redefines Bench, Study, Test, Run, Measurement and Verdict
**Issue:** EMB-317
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`suite/hil-guide.md`'s "Words" section defines Bench, Study, Test, Run,
Measurement and Verdict itself, and `embarch-api` embeds that guide as a
pinned copy (`guide/hil-guide.md`, checked by `tests/guide_cli.rs`). When this
is done, each Words entry the glossary now covers keeps a one-line gloss and
names the glossary row as the definition, so a term is defined once.

**How it lands:** edit the api's pinned copy and quote the old and new section
in a `status.d/` fragment; the supervisor applies the same bytes to
`suite/hil-guide.md` at the fold, as `api/189` did. The guide is read from the
binary, so a reader may have no repo: keep each gloss readable on its own.

## Why now

EMB-317, after `doc/102` adds the glossary rows.

**Burndown leg: no new numbered decision.**

## Done when

- [ ] The pinned copy's Words entries name the glossary as the definition.
- [ ] Gate green (`../../embarch-fleet/gate.md`), drift guard green against a
      sibling `embarch-doc` carrying the same edit, `changelog.d/` fragment
      dropped.
