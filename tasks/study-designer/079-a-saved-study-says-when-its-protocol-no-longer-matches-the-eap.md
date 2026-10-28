# 079 — A saved study can be told that its protocol no longer matches the `.eap` it names

**State:** open
**Source:** the 2026-10-28 leg's refill sweep of `embarch-study-designer/open.md`: the bullet "A saved study is never checked against the `.eap` file it was built from", opened by the owner's `suite/045` commit (`685b691c`). `embarch-ui/open.md` carries the same bullet and says the check is this crate's, the UI's half only being where a divergence is shown.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## What

A saved study carries a *resolved* `ProtocolDef` (decision 58) and a protocol **name**, never a filename (decisions/protocols.md, the `defs()` paragraph). That is what makes it replay identically on another machine, and it is also silent: once the author edits the `.eap`, the study still runs the old definition and nothing says the two differ.

Give this crate the comparison and leave the showing to `embarch-ui`. When this is done, a caller holding a saved study and the repo's current protocol set can ask, per protocol the study carries, whether the current manifest still resolves that name to the same definition, and gets back one of: **unchanged**, **changed** (naming what differs at least to the level of which messages or fields), or **gone** (the name no longer resolves). The study itself is not modified and nothing is refused: a diverged study still runs what it carries, because that is decision 58's point.

**Do not pin a CRC or hash of the manifest text into the study.** `decisions/protocols.md` rejected exactly that ("a saved study's pinned CRC would go stale on the author's next edit"). Compare the resolved definitions instead: re-resolve the named protocol from the current manifest and compare it structurally with what the study carries. If that comparison needs a type to derive `PartialEq`, that is fine; **adding a `pub` field to a struct other repos build by literal is not** (it breaks their compile, and this task owns one repo). If you find you need one, stop and say so in this file.

Record it as a new decision in the topic file it belongs to (likely `decisions/protocols.md`; check its size first). Replace the `open.md` bullet with a one-line pointer to the decision, or remove it, and say in your report which.

## Why now

`embarch-study-designer/open.md` is in the size reserve and its compaction task (`tasks/study-designer/026`) is overdue and parked because every bullet is a live question. Answering this one is the only payment that does not delete a live question.

## Done when

- [ ] A public function (or method) answers unchanged / changed / gone per protocol for a saved study against a current protocol set, with unit tests for all three and for a study carrying no protocol.
- [ ] Nothing stored in a study changes shape; every existing fixture and saved study still loads.
- [ ] A numbered decision records the comparison and why it is structural rather than a pinned digest.
- [ ] `open.md`'s bullet answered (pointer or removal); `embarch-ui/open.md` is the UI's and stays as it is.
- [ ] Gate green (`../../embarch-fleet/gate.md`), including `--features` cells the crate's CI runs.
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
