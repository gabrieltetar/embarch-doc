# `crate.md` decisions 4 and 8 claim a uniqueness the crate cannot enforce

**State:** open
**Source:** `api/038`, leg 049, 2026-09-08 — filed as a `status.d/` fragment by that unit and
converted to a task by the supervisor, because `status.d/` is only for the five shared suite-level
docs and `embarch-topology/decisions/crate.md` is a sub-project doc this scope owns
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/decisions/crate.md` decisions 4 and 8 assert a consolidation that had not
happened and a property the crate cannot provide.

**Decision 4** says the software-class detection "mirrored between `embarch-api` and
`embarch-umbrella` all move here as the sole implementation. The mirrored-copy CI diff job becomes
obsolete: there is nothing left to mirror once everyone links the same crate."

**Decision 8** says "there is no way for the two to disagree, since there is only one of them."

**Both were false as written, and `api/038` proved it by fixing one half.**
`embarch-api/crates/embarch-core-client` **already linked `embarch-topology`** and still ran its own
second, narrower WSL2 predicate (`token_discovery::is_wsl2`) beside `detect_wsl2` — the same binary
carrying two rules that could disagree, each unit-tested only against its own expectations, so
nothing compared them. `api/038` (`embarch-api` decision 62, code `861f30f`) made
`token_discovery::is_wsl2` delegate, which closes that instance.

**The general claim still needs qualifying, and that is what this task is for.** Linking the crate
stops a mirrored *copy* of the crate's own logic; it cannot stop a caller writing a second,
unrelated predicate next to the call it never makes. Decision 8's "there is no way for the two to
disagree, since there is only one of them" is true **only inside the crate's own boundary** — it is a
statement about the crate, not about its callers, and it currently reads as the latter.

**A third copy is still live and is not yours:** `embarch-umbrella/src/token.rs` carries a verbatim
copy of the old narrow rule. That is `umbrella/036`'s to remove. Do not touch it; do not claim in
`crate.md` that it is gone until it is.

## Why now

The claim is load-bearing in the wrong direction: it is the reason nobody went looking for a second
predicate, and it read as an audit result rather than an intention. It also matters for what happens
next — if `crate.md` says callers cannot disagree, the natural conclusion is that no check comparing
them is needed, and no such check exists.

## Done when

- [ ] Decisions 4 and 8 are corrected in place, **without rewriting the history of what was decided**
      — the reversal convention, not a silent edit. What the crate guarantees (one implementation of
      the predicate, inside the crate) is separated from what it cannot (a caller declining to call
      it).
- [ ] The correction names `api/038`'s fix as the instance that disproved the general claim, and does
      **not** assert that every mirror is gone — `embarch-umbrella/src/token.rs` still has one.
- [ ] Whether anything should *detect* a second predicate beside a live call is answered one way or
      the other. If the answer is "nothing can cheaply", that goes in `open.md` as an open question
      rather than being left implied.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment if anything shipped; a doc-only correction likely owes none.

## Supervisor note — leg 049

**Check the doc-size reserve before you write.** `embarch-topology/spec.md` had 279 B of headroom,
`decisions/validation.md` 1110 B and `decisions/enrollment.md` 942 B at the start of this leg, all
filed against `tasks/topology/017` and `019`. `crate.md` itself was not in reserve. Re-read
`check-doc-size.py --pressure` rather than trusting these numbers; three units landed after they were
taken.

**`embarch-api` decision 62 cites this task file by path.** If you renumber or rename this task,
that citation dies silently — it is backticked prose, not a markdown link, so `check-links.py` will
not catch it. That exact defect class was two separate units in this leg and the one before it.
