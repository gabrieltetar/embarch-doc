# 032 — Check 14's `WslHost` and `Remote` skip arms cannot be reached on a machine that has been set up

**State:** done, agent/umbrella/032-check-14-skip-arms, 2026-09-07
**Source:** supervisor bench unit `umbrella/027`, 2026-09-06 — live `embarch doctor` on the primary
`wsl-host` bench
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What was observed

Check 14 returned **`PASS every-family-covered`** with `nRF54L15=jlink, nRF52840=probe-rs,
esp32c5=probe-rs` — real output from the installed Windows service exe, run from WSL.

`embarch-umbrella/spec.md` and `decisions/doctor.md` treat check 14's `WslHost` and `Remote` arms as
states the check distinguishes. Reading `src/doctor.rs:2896-2915`, they are not verdicts about
flashing at all: **all three class arms sit inside a single `else` reached only when no
`embarch-core` binary is locatable**, and each just phrases the same skip differently. On a
`wsl-host` machine `setup` has run, so the locator finds the service exe under `/mnt/c/…`, the real
`flash-backend` arm runs, and the `WslHost` wording is unreachable by construction.

## Why this is worth recording rather than shrugging at

It is the third instance of one shape in this suite, and the pattern is what matters:

- `embarch-umbrella` decision 18's `probe-not-permitted` arm needs Core running natively on Linux;
  the primary topology has Core on Windows, so the scan is skipped and the arm is dead here.
- `embarch-topology` decision 18's branch is gated on `TopologyClass::Local` and is unreachable on
  the only topology this suite is actually used on (leg 022).
- Check 14's `WslHost` arm needs a `wsl-host` machine with **no locatable Core** — i.e. one where
  `embarch setup` has not completed, which is the state `doctor` exists to diagnose but not the
  state anyone runs `doctor` from twice.

Each is defensible on its own. Together they say that a check's *class-aware* arms are the ones
least likely to have ever run, and `spec.md`'s table gives no way to tell an exercised arm from a
worded one.

## Done when

- [x] Either the three skip arms collapse to one message plus the class name — they differ only in
      prose and none has been observed — or each keeps its wording with a note saying which are
      unreachable on a set-up machine, so nobody reads them as distinguished states.
      Kept distinct (each names a genuinely different next step for an operator), not collapsed —
      annotated in `src/doctor.rs` above the match and in `decisions/doctor.md` decision 31: all
      three fire only before *that class's own* `setup` finishes, which decision 38's real
      `wsl-host` run already demonstrates by hitting the real `flash-backend` arm instead.
- [x] `spec.md`'s check-14 row stops implying the class arms are flashing verdicts. They are
      "could not ask Core" phrased three ways.
      Row now reads "measured" for the real run and calls the unlocatable case "one skip worded
      per class, not a flashing verdict."
- [x] The general question gets an answer somewhere durable: **how does a reader of `spec.md`'s
      check table tell an arm that has run from an arm that has only been written?** This is now
      the third example; it is a table-shape question, not a check-14 question.
      Answered as an `embarch-umbrella`-local convention in `spec.md` itself (a `measured` marker
      cited to a decision recording a real run; unmarked prose is reasoned but not observed) —
      per supervisor direction, the suite-wide half (whether `DOC-CONVENTIONS.md` should adopt
      this) is left in `inbox/doc-check-table-exercised-vs-written-convention.md` rather than
      written here.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Supervisor direction, leg 041

**The third item is the one that will pull you out of scope, so read this before
you start it.** "How does a reader tell an arm that has run from an arm that has
only been written" is a real question and it is the reason this task is worth
more than a wording tidy — but the durable answer belongs in
`embarch-umbrella/spec.md`'s own check table first, as a convention *this*
sub-project adopts. If you conclude it should be a suite-wide documentation
convention, **that is `DOC-CONVENTIONS.md`, which no agent may write**: say so in
an `inbox/` drop and leave the suite-wide half there. Landing the umbrella half
is a complete unit; reaching for the other half is a refused branch.

**On the first item, prefer the answer you can defend over the tidier one.**
Collapsing three arms into one message is only right if nothing distinguishes
them *to a reader*; if the class name genuinely tells an operator something the
shared message would not, keep them and annotate. Do not collapse because three
into one looks like a simplification.

**`decisions/doctor.md` was split this morning** — `umbrella/037` moved check
13's mission out to `decisions/dev-bench-firmware.md` verbatim and filed its new
reasoning there. If you cite a doctor decision by number, resolve it against the
files as they are now rather than from memory of where things used to live.

## Doc-size reserve for `umbrella`

You are editing `spec.md`, and it is in reserve.

- `embarch-umbrella/spec.md` — 9430/10240 B, **810 B left**
- `embarch-umbrella/open.md` — 4270/5120 B, **850 B left**

Both are filed against `tasks/umbrella/038-compact-umbrella.md`, which is
**open, not blocked** — so the debt is already recorded and you do not need to
file another for these two. Plan your edit against that headroom rather than
discovering it: `spec.md`'s check-14 row is a table row, and a paragraph of new
prose beside it is what spends 810 bytes. Two other umbrella files
(`decisions/reporting.md`, `decisions/bind.md`) are in reserve behind **blocked**
compaction tasks; if your work lands in either of those, say so and apply
`DOC-COMPACTION.md` §2's ride-along rather than squeezing.
