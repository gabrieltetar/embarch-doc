# 070 — Three `board_gate` migration sentences cite nothing, where a fourth cites decision 22

**State:** claimed — leg 131 unit 4, 2026-09-17, `agent/core/070-board-gate-migration-citations`
**Source:** leg 131 refill, 2026-09-17, generalising `tasks/topology/052`'s finding. That unit
found two sibling files in `embarch-topology` carrying the same *"formerly `embarch-core`'s own
X"* sentence with the same wrong attribution, and observed that **one was only inside a sweep's
scope because it happened to wrap across a line** — the class is a *migration-attribution* defect,
and a citation-number census can only reach it by accident. `tasks/topology/053` pays that finding
inside `embarch-topology`. This task pays the same class inside `embarch-core`, which is the repo
that **owns** the decision the migration is recorded under.
**Scope:** core
**Hardware:** none — Rust doc comments only. Nothing is built for a board, no probe, no flash, no
study, no live Core, no deploy. Host `cargo build`/`test`/`clippy` only.
**Owner:** no

**Doc-size reserve for `core`: one file, filed and blocked.**
`embarch-core/decisions/auth.md` (11,356/12,288 B, 932 B left) against `tasks/core/046`, which is
`blocked`. This unit is a doc-comment repair and **should not need to write any `embarch-core` doc
at all**; if it turns out you must, do not write `auth.md` — and if you spend reserve anywhere,
say so in your report and file `tasks/core/<next free NNN>-compact-core.md` in the same commit per
`tasks/README.md`. **`tasks/doc/` is not yours.**

## What

`embarch-core` moved its own `board_gate.rs` into `embarch-topology`. That move is recorded as
**`embarch-core` decision 22**, whose own text says *"Moved wholesale into `embarch-topology`"*
(`embarch-core/decisions/probes.md`). Four doc comments in this crate still describe the move.
**One of them cites decision 22. Three cite nothing for the migration claim.** Line numbers taken
at `b12ced1`; `main` moves, so locate them by their text, not by number:

| file:line | the sentence | what it cites for the migration |
|---|---|---|
| `src/api.rs:681` | ``embarch_topology::hardware::enroll`, formerly this crate's own `board_gate::enroll`` | **decision 22** — the model |
| `src/hardware.rs:76` | ``embarch_topology::hardware::validate_serial` (the board-identity gate, formerly this crate's own `board_gate.rs`)`` | nothing |
| `src/hardware.rs:107` | the same sentence again, in `open_probe`'s doc comment | nothing for the *migration*; the surrounding block cites **decision 61**, which is about the selection rule, not the move |
| `src/study.rs:873` | ``embarch_topology::hardware::validate_role` (formerly this crate's own `board_gate::enforce_for_role`)`` | nothing |

**`src/hardware.rs:107` is the one to read hardest.** A reader there sees a decision number in the
same paragraph and will take it as the citation for the whole thing. Decision 61 is real, current,
and correctly cited *for what it is attached to* — the selection logic no longer being this
crate's own copy. It is **not** the decision that moved `board_gate.rs`. That is exactly
`study-designer/059`'s and `ui/063`'s shape: on-topic, correctly labelled, wrong decision — except
here the wrong decision is *adjacent prose* rather than the number itself, which is why no census
in this suite has ever been able to see it.

## What to do

**Verify before you edit, and be willing to conclude "nothing to fix".** This task asserts a
defect; your job is to establish whether it is one, not to make the diff the task predicted.
`ui/063` wrote its task around three lines it expected to be wrong, all three were right, and the
real defect was on a line nobody had flagged — **a supervisor's guess at where the defect lives is
not evidence.**

1. **Read `embarch-core` decision 22's own body in full** (`decisions/probes.md`) and establish
   exactly what it claims was moved. If it names `board_gate::enroll` but not
   `board_gate::enforce_for_role`, then `study.rs:873` may need a *different* number, or none —
   say which and why.
2. **Read decision 61's own body in full** before you conclude it is the wrong citation at
   `hardware.rs:107`. If 61 turns out to cover the move as well, this item is not a defect and
   should be reported as a clean check, not edited.
3. **Check whether a nearer decision in this repo says it better.** `topology/052`,
   `study-designer/059` and `ui/063` all found the right answer one or three decisions away from
   the cited one, in the same file. Read decision 22's neighbours in `decisions/probes.md`.
4. **Add the citation where it is missing rather than rewriting the sentence.** `topology/052`
   reworded an illustration while repointing a number and the supervisor flagged that as the one
   change in its leg that could *introduce* a defect: **a comment citing the right decision while
   describing it slightly wrong is worse than a wrong number, because the number stops signalling
   anything.** If a sentence genuinely needs rewording, quote the decision's own words.
5. **Sweep for the class, do not stop at the four rows above.** Run
   `grep -rnIE "formerly|used to live|moved (in|out) of|moved wholesale|migrated from" src/` over
   `embarch-core` and report every hit, including the ones you conclude are fine. Report the count
   you actually got. The point of this unit is the class, not the four instances.

## Why this is worth a unit

The suite has run something like twenty citation sweeps and the standing doubt in the supervisor
log is whether a zero-defect sweep means a clean corpus or a blind census. `outpost/025` answered
that once — a sweep returning zero wrong *numbers* said nothing about the file's *completeness*.
This is the second answer from the same direction: **a migration claim with no number attached is
invisible to every grep this suite owns**, and the only reason `topology/052` caught its two was a
line wrap. Report whatever you find back into that argument explicitly, zero included.

## Done when

- [ ] All four sentences above adjudicated individually — fixed, or reported as correct with the
      decision body that makes them correct quoted.
- [ ] The class grep run fresh over `embarch-core/src`, its real count reported, and every hit
      adjudicated.
- [ ] No sentence reworded beyond what a cited decision's own text supports.
- [ ] Gate green (`../../../embarch-fleet/protocol.md` §10): `cargo build --all-targets`,
      `cargo test`, `cargo clippy --all-targets -- -D warnings`. **You do not have a native Windows
      toolchain and are not expected to run one** — say so in your report; the supervisor carries
      that as `core/015`'s standing debt.
- [ ] `changelog.d/core-*` fragment, reporting sentences checked, sentences fixed, and sentences
      found correct as three explicit numbers.
