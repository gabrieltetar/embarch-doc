# 063 — The bare decision citations in `locate.rs`, `init.rs` and `config.rs` have never been checked against their bodies

**State:** claimed by agent/umbrella/063-bare-decision-citations-locate-init-config, 2026-09-13 17:20
**Source:** the leg of 2026-09-13 17:0x, refill sweep. `supervisor-log.md`'s 2026-09-12
carry-forward says **no sweep has been filed yet for `embarch-umbrella`'s own source**, and that
`check-decision-refs.py` resolves numbers only inside `*.md` — a wrong number in a `.rs` comment
that happens to resolve fails nothing.
**Scope:** umbrella
**Hardware:** none — comments and, where a claim has gone false, the prose around them.
**Owner:** no

## What

Three files carry **~37 bare `decision N` citations** between them — `locate.rs` (~20), `init.rs`
(~10), `config.rs` (~7) — with no repo qualifier, so each resolves by convention to
`embarch-umbrella`'s own decision N. `embarch-umbrella` has 52 decisions and every one of these
numbers is in range, **which is what makes this worth a unit**: all of them resolve, so nothing
fails, and the only way to know whether they are right is to read the bodies.

`doctor.rs` carries roughly another 100 and is deliberately out of scope — it is a separate unit,
and one file that size is not a twenty-minute pass.

## The method, which is the whole task

For each bare citation: resolve it in `embarch-doc/embarch-umbrella/decisions/*.md`, **read the
body**, and ask whether the comment's claim is what that decision actually says.

- **Right number, claim holds** → leave it. Most will be this.
- **Wrong repo** → prefix the owning repo, and **re-derive the number in that repo** rather than
  assuming it is the same number. `ui/040`'s reviewer caught two citations prefixed without being
  re-derived; that is this fix's own characteristic failure.
- **Right number, claim has gone false** → the finding that matters. Four consecutive units have
  hit exactly this, twice in this repo: `umbrella/062` corrected a link's depth while its target
  `spec.md` section had been dead four days, and `core/053` corrected a filename while the sentence
  around it had also gone false. **A citation repair that leaves a false claim intact is the defect
  this suite keeps paying for.** Reword to what is true and say so in the commit message.
- **Number resolves nowhere** → say so; do not guess a replacement.

Note two citations already carry a qualifier of a different kind — `config.rs:94` says *"this
repo's decision 16"* — and those are fine as they are; the task is the unqualified ones.

## Constraints

- **Comments and prose only.** No behavioural change, no refactor. A real code defect is a drop in
  `/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path), not a change here.
- **Do not renumber or edit any decision body.**
- **Do not touch citation *form*.** Whether a cross-repo `embarch-doc` path is written
  `../../embarch-doc/...` or `embarch-doc/...` is an open, owner-reserved question
  (`tasks/doc/055`). Leave every path exactly as long as you found it.
- **In reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` at 11533/12288 B (755 B
  left), filed against blocked `tasks/umbrella/009`. If your work spends that reserve, file
  `tasks/umbrella/<NNN>-compact-docs.md` in the same commit.

## Done when

- [ ] Every bare `decision N` in `locate.rs`, `init.rs` and `config.rs` has been resolved against
      its body and either left, attributed, or corrected — and the commit message says how many of
      each.
- [ ] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/umbrella-*` fragment.
