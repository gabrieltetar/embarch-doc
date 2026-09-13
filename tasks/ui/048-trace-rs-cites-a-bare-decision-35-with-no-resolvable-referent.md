# 048 — `src/trace.rs:132` cites a bare "decision 35" and no decision 35 anywhere is about what the comment describes

**State:** done
**Source:** `inbox/ui-src-trace-rs-132-bare-decision-35-no-referent.md`, dropped by `ui/047`'s
worker, which named this site as real but outside its own `Done when`. Filed by the leg of 2026-09-13 16:20 (the
leg-number field is self-assigned and has collided twice today; the timestamp is the handle).
**Scope:** ui
**Hardware:** none — a source doc comment.
**Owner:** no

## What

`embarch-ui/src/trace.rs:132`, on `TraceSubject.unnamed`:

```rust
/// True when the manifest did not name this subject, so `label` is a raw
/// number. Rendered visibly differently — a pointer that looks like a name
/// is the defect decision 35 exists to prevent.
```

The citation carries **no repo prefix**, so under this suite's conventions it reads as an
`embarch-ui` decision, and `embarch-ui` has no decision 35. The drop also checked five sibling
repos' `### 35` entries and found none whose subject is about naming, identity, or a pointer that
looks like a label.

**Re-derive all of that yourself rather than inheriting it.** Check `embarch-ui/decisions.md` and
every `embarch-ui/decisions/*.md` for a 35, and check each sibling repo's 35 against its own body,
not its index line. Two consecutive legs have had a reviewer catch a citation repair that got the
number right and the surrounding sentence wrong, so the derivation is the work here; the edit is
small.

Then take **exactly one** of these three outcomes, and say in your report which and why:

1. **A referent exists** — an `embarch-ui` decision that was renumbered, or a sibling-repo decision
   the drop's sweep missed. Write the correct number, with a repo prefix if it is foreign, and quote
   the clause of its body that supports the comment's claim.
2. **No referent exists and the claim is still true** — `unnamed` really is rendered differently so a
   raw pointer cannot masquerade as a label. Then **drop the citation** and keep the sentence as a
   plain statement of the behaviour, verified against the rendering code rather than assumed.
3. **No referent exists and the claim is not verifiable** — the rendering does not in fact
   distinguish them. Then say so plainly in the comment or delete the clause, and file an
   `inbox/` drop describing the gap.

## What is NOT in scope

**Authoring a new `embarch-ui` decision.** The drop's own suggested step (b) offers "decide whether
`unnamed`'s behavior is worth a new decision" — that is a judgement with a number and an index
behind it, and a new numbered decision is not what this unit is for. If you conclude one is owed,
**file an `inbox/` drop for it** at the absolute path
`/home/gabriel/Github/embarch/embarch-doc/inbox/`, in full task format, and say so in your report.

Also not in scope: the other bare or foreign decision citations in `embarch-ui`. `ui/047` already
established that nine `decision 40` sites in this repo are correct and must not be swept; do not
sweep anything.

## Why now

A citation with no referent is worse than no citation: it tells the next reader that a decision
settled this, and sends them looking for a decision that does not exist. `ui/047` found this site
while fixing three neighbouring miscitations and deliberately queued it rather than guessing, which
is the right call and is why it is a task rather than a ride-along.

## Doc-size reserve for `ui`

Nothing in `embarch-ui`'s doc tree is in reserve. If your work pushes any `embarch-ui` doc file into
its last 10%, file `tasks/ui/<next>-compact-ui.md` in the same commit
(`scripts/check-task-numbers.py --next ui` for the number).

## Done when

- [x] `src/trace.rs:132`'s comment either cites a decision whose body you have read and quoted, or
      cites none at all.
- [x] Your report names every decision index you checked and what each 35 actually is.
- [x] No other citation in `embarch-ui` was changed.
- [x] `cargo build` / `cargo test` / `cargo clippy --all-targets -- -D warnings` green in
      `embarch-ui`.
- [x] `changelog.d/` fragment in `embarch-doc`.
- [x] `python3 scripts/check-docs.py` green in `embarch-doc`.

## Outcome taken

**Outcome 2** — no referent exists, and the claim is still true. `embarch-ui`'s own
`decisions.md`/`decisions/*.md` top out at decision 26 (no 35 exists or ever existed under that
number — `DOC-CONVENTIONS.md` states numbers are never renumbered or reused, which forecloses
outcome 1's "renumbered" branch outright). All six sibling repos with an actual decision 35
(`embarch-dev-bench`, `embarch-core`, `embarch-api`, `embarch-umbrella`, `embarch-study-designer`;
`embarch-outpost` and `embarch-topology` have none) were read in full body, not by index line —
none is about naming, identity, or a pointer rendered as a label (see report). `embarch-ui`
decision 10 (`trace-view.md`) covers closely related ground — "'unnamed' is a first-class state
here, not an error path, drawn italic and dotted with the number as the label" — and is already
this module's umbrella citation (`trace.rs`'s top-of-file doc comment: "decision 10's second
half"), but it was never numbered 35 under any theory, so it does not satisfy outcome 1 for *this*
citation.

The claim itself checked out against the rendering code: `assets/app.js` renders `unnamed`
lanes/subjects muted, italic, with a dashed underline and an explanatory tooltip, in both the load
table (`nameCell`, ~line 3692) and the lane chart (~lines 4269–4280, 4690). Dropped the dead
citation in `embarch-ui/src/trace.rs:130-133` and restated the sentence as a plain, verified fact.
No new decision authored; no `inbox/` drop needed since the claim held and nothing else in scope
was left unresolved.
