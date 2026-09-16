# 037 — Comments in `embarch-topology`'s enrolment trio that state an invariant the code may not implement

**State:** claimed — `agent/topology/037-comments-vs-code-in-enrolment-trio`, leg 116, 2026-09-16
**Source:** refill sweep, leg 116, 2026-09-16 — from
[`embarch-decision-reversals.md`](../../embarch-decision-reversals.md)'s **shape 8, "the comment
names the right invariant; the code does not implement it"** (rows 100, 101, 102, 104). That shape is
the page's own statement of an unclosed pattern: **three of its four instances were found in a single
pass**, one had a test *asserting the loss as intended behaviour*, and the page's own diagnosis of why
they survive is the line to carry into this sweep — *"it names a class it does prevent, which reads as
though it had considered the space."* Nothing has run that pass over `embarch-topology`.
**Scope:** topology
**Hardware:** none — this is reading Rust source and its comments against each other, plus `cargo
test`. **No board, no probe, no live Core, no `validate`, no enrolment performed.** Do not run
`embarch-topology validate` or any CLI subcommand that touches hardware; if a question can only be
settled by attaching a board, that is a finding to report, not a thing to do.
**Owner:** no

**Doc-size reserve for `topology`: nothing.** No `embarch-topology/` doc is in reserve — you have
full headroom in all of them. (For contrast, five other sub-projects are in reserve right now.) If
your work somehow pushes one *into* reserve, file
`tasks/topology/038-compact-topology.md` in the same commit per `tasks/README.md`.

## Why this repo, and why these three files

`embarch-topology` is a **shared crate**: `embarch-api`, `embarch-core`, `embarch-ui` and
`embarch-umbrella` all path-depend on it. A comment here that promises a guarantee the code does not
keep is read by four repos' worth of callers, and this repo has already produced exactly this defect
once — `tasks/topology/020`, *"crate.md decisions 4 and 8 claim a uniqueness the crate cannot
enforce"*, now closed. So the class is proven present here, not hypothesised.

**Read these three files, in this order, and nothing else:**

| file | lines | why it is first |
|---|---|---|
| `src/hardware/hardware_id.rs` | ~555 | identity — the thing enrolment exists to pin |
| `src/hardware/enrollment.rs` | ~515 | the write side of that pin |
| `src/hardware/validate.rs` | ~570 | the read side that is supposed to refuse a mismatch |

~1,640 lines. **That bound is deliberate** — `src/` is 4,612 lines and a sweep that skims all of it
finds less than one that reads a third of it properly. The trio is chosen because the suite's single
most expensive documented hardware failure mode is *"a bench that flashed, booted, ran, and timed
out"* after a mismatch was papered over, and these three files are where that is meant to be
impossible.

## What you are looking for — and what you are NOT

**Looking for:** a comment (`//`, `///`, `//!`, or a `#[doc]`) that states something the code around
it is supposed to guarantee, where reading the code shows it does not. Concretely:

- A comment naming a class of input it rejects, where the rejection sits on only one arm of a `match`,
  behind an `if` that the other path skips, or after an early return.
- A comment saying two things "must" or "always" agree — a constant mirrored elsewhere, a field and
  its serialized name, an ID and its source — where **nothing in the code compares them**
  (reversals shape 4: *"a note describing a gap is not a mechanism for closing one"*).
- A `///` on a public function whose stated contract is stronger than what the body enforces —
  especially a claimed uniqueness, a claimed non-empty, or a claimed "never `None` here".
- A comment describing behaviour that was **true when written and was later moved or retired**
  (reversals shape 9). `git log -L` or `git blame` on the surrounding lines settles this cheaply.
- **A test that asserts the wrong behaviour as intended.** Row 102 is exactly this, and it is the
  hardest one to see, because a green test reads as evidence.

**NOT looking for:** citation numbers. `tasks/topology/036` already swept this repo's source comments
for dead decision references and closed. **Do not re-run that sweep**, do not "fix" a citation you
happen to pass, and if a citation looks wrong, note it in your report as a by-catch for a future task
rather than changing it — a citation fix inside this diff makes the shape-8 findings harder to review.

## How to report, and the discipline that matters most here

**Report a number, and report it red if it is red.** The immediately preceding legs have produced
several zero-defect sweeps, and the honest open question — raised independently by `ui/049` and
`umbrella/066` — is whether that means the corpus is clean or whether sweeps have converged on easy
files. **This sweep's value is the same whether it finds four defects or zero, but only if the zero is
trustworthy.** So:

- State **how many comments you read that make a checkable claim**, and how many of those you actually
  traced into the code. Those are two different numbers and the second is the real one.
- A comment you could not settle is **`unsettled`, named with its line number** — never rounded to
  "clean". `umbrella/066` reported 114/0 where the honest answer was 113/1, and `api/095` is the
  counter-example worth copying: it refused to resolve one citation either way and said so.
- If you find nothing, say **"0 findings in N traced claims"** and list the N. Do not pad the diff.

## Fix what you find, within scope

For each real finding, **change the side that is wrong**, and say in the commit message which side you
chose and why:

- Comment overstates what the code does, and the code is right → **fix the comment**, and make it name
  the narrower class truthfully rather than deleting the sentence.
- Comment states the intended invariant and the code genuinely does not implement it → **do not
  silently implement it.** That is a behaviour change in a crate four repos depend on. Write the
  comment down to what is true *and* file `tasks/topology/038-<slug>.md` describing the gap, so the
  real fix is a task somebody chooses rather than a side effect of a comment sweep.
- If a decision in `embarch-topology/decisions/*.md` is the thing that is wrong, **stop** — amending a
  decision is not this task's scope. Report it and it becomes its own unit.

## Done when

- [ ] All three files read end to end; the two counts above stated explicitly in your report.
- [ ] Every finding either fixed in this diff or filed as a follow-up task, with no third category.
- [ ] `cargo build` / `cargo test` / `clippy --all-targets -- -D warnings` green in
      `embarch-topology`.
- [ ] A `changelog.d/` fragment written for this repo if anything changed; none if nothing did.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
