# 021 — `bound-narrow`'s new `setup` clause reads a `host` that is not the one `setup` reads, and its `Remote` branch is unguarded

**State:** done — `agent/umbrella/021-infer-class-inputs`, 2026-09-06
**Source:** `umbrella/020`'s reviewer, 2026-09-06, reviewing merge `08ccd6f` / `0824325`.
Both items below were reported as **observations, not contradictions** — the reviewer returned
no findings and the supervisor merged knowing them. Each is a read of the shipped source with
line numbers; re-derive rather than trust them.
**Scope:** umbrella
**Hardware:** none — both items are code and a decision amendment. Item 1 changes what a fix
line *says*, not what any check does to a machine.
**Owner:** no

## 1. `setup_would_infer` shares `infer_class` but not its inputs, so "cannot disagree" is not what ships

`umbrella/020` fixed `bound-narrow`'s `setup` offer by calling `setup::infer_class` — and
decision 22's new amendment justifies that as **"shared rather than mirrored so the two can
never disagree."** The reviewer checked the inputs rather than the callee:

- `setup.rs:207` → `make_plan(host, port)` → `infer_class(host, …)`, where `host` is **only the
  `--host` CLI flag** (`main.rs:183`), with no fallback.
- `doctor.rs:2763` passes doctor's `host`, which is `config.core.host` **or** `saved.host`.

`saved.host` is sticky: `setup` writes `host.map(...).or(saved.host)`, so a `--host` from any
earlier run survives a later `setup` that reclassifies the machine. In the state
`recorded: wsl-host`, `saved.host: Some(_)`, nothing answering, narrow registration,
`setup_would_infer` is `Remote` and the fix line prints *"re-run `embarch setup` from here,
which infers **remote** and passes it for you"* — while a bare `embarch setup` infers
`wsl-host`, and `embarch setup --host …` skips the local install entirely.

**The remedy's direction survives; the class it names does not.** This is
`embarch-decision-reversals.md` **shape 8** in miniature — the comment names the right
invariant and the code does not implement it — and the false witness here is a decision
amendment written in the same commit.

**Why it was not reverted:** `doctor`'s check 2 (`doctor.rs:361`) has passed the same
config-or-saved `host` to the same function since it shipped, so `020` adopted an existing
convention rather than contradicting a standing decision. That makes it a defect to fix
deliberately, not a merge to undo.

Either make the two calls agree on `host`, or **stop claiming they cannot disagree** and say in
decision 22 what the shared call actually buys. Do not weaken the fix line to vagueness to
dodge the question — naming the class is what made the clause useful.

## 2. The `Remote` branch of the same predicate is reachable, unguarded and untested

`recommended_bind_address(Remote) == "0.0.0.0" == needed`, so the `bound-narrow` fix offers
`embarch setup` when `setup_would_infer` is `Remote` — **but `setup` inferring `Remote`
installs nothing.** That is precisely the failure the same amendment used to justify deleting
the `setup` half from `bind-too-narrow`: *"`setup` can never install there, so the offer is
unconditionally wrong."*

The new tests pin `setup_would_infer` to `WslHost` and `Local` only. **The gap is visible in
the tests as an absence**, which is the good case and the same shape `020` itself was filed to
close one path over.

## 3. Decision 37 was edited in the same commit and may already be inconsistent

`reporting.md`'s reuse list was updated to "**Two so far**" while `bound-narrow` and
`bind-too-narrow` **both narrowed again** in that commit (the `remote` sub-case moved out from
under them). `bind.md` argues the guard restored an intended referent rather than moving one —
"the predicate had no class guard from the day check 17 shipped" — which is defensible. But
the sub-project's reading of 37 is one day old and has now been applied two ways. **Settle
which reading is 37's**, in `reporting.md`, so the next narrowing does not have to re-decide it.

## Reserve

At filing: `embarch-umbrella` has **no file in reserve** — `umbrella/020` split
`decisions/doctor.md` to 6,188 B (50.4%), created `decisions/bind.md` at 8,465 B (68.9%), and
repaid `open.md` to 89.9%. `open.md` is 0.1 percentage points under its line, so **an item-2
entry there will re-enter reserve**; plan for it. `tasks/umbrella/009` remains `blocked`,
`In flux: yes`, for `spec.md`'s doctor table.

## Done when

- [x] Item 1 is fixed, or decision 22's "can never disagree" sentence is corrected to what is
      true, with the losing option argued against.
- [x] Item 2 has a guard or an argued-and-tested reason the `Remote` branch is right.
- [x] Item 3 has one reading of decision 37 recorded in `reporting.md`.
- [x] Gate green; `changelog.d/umbrella-*` fragment dropped.

## What shipped

**Every one of the reviewer's reads was re-derived and every one held.** `setup::setup` takes
only the `--host` CLI flag (`main.rs`'s `Command::Setup { host, .. }`), passes it straight to
`make_plan` → `infer_class`, with no fallback; `apply_plan` writes `host: plan.host` where
`plan.host` is `host.map(…).or(saved.host)` **for every class**, so `saved.host` is sticky
exactly as described; `doctor`'s `host` is `config.core.host` **or** `saved.host` and was
being handed to `setup_would_infer`. And `recommended_bind_address(Remote)` is `0.0.0.0`, so
the `Remote` branch was reachable and unguarded. Line numbers had shifted by a few but every
claim was true as stated.

**Item 1 — fixed the input, and argued the retraction down.** `setup_would_infer` is now
`setup::infer_class(None, core.as_ref())`: the fix line predicts one exact invocation, bare
`embarch setup`, so it is fed that invocation's own arguments. The losing option — retract
decision 22's "can never disagree" sentence and leave the code — was cheaper and is argued
against in [decision 22](../../embarch-umbrella/decisions/bind.md): nobody reads a decision at
the moment of choosing, the **fix line** is what a human is printed while deciding what to
type, and a doc that accurately describes a lie is not the honest ending. The claim was also
corrected in place, since "shared function" alone never bought it — "shared inputs" is what
does.

**Item 2 — guarded and tested.** The gate on the `setup` offer was
`recommended_bind_address(setup_would_infer) == needed`, which is a proxy for "would a run
here install a wide-bound Core" and is not one. Replaced with an exhaustive `match` on the
class: `WslHost` offers, `Local` withdraws with *installs the narrow bind again*, `Remote`
withdraws with *installs nothing at all*. New test
`check_17s_bound_narrow_fix_withdraws_setup_where_setup_would_infer_remote` pins it and
asserts the `local` reason is **not** used for `remote`. A second test,
`a_bare_setup_run_never_infers_remote_whatever_this_machine_has_saved`, records the
consequence of item 1's fix: with the host at `None` the `Remote` arm is unreachable from the
driver, so it is a guard against a future call site and the test says which rather than
leaving the next reader to re-derive it.

**Item 3 — settled in
[decision 37](../../embarch-umbrella/decisions/reporting.md).** The reading recorded: a
deliberate-reuse record is owed where a code keeps its spelling for a state that *replaced*
the one its decision described, and is not owed where a fix stops it firing on states that
decision never described. Mechanically — if closing the change means rewriting the entry's
description of what the code names, it is a reuse; if the description already excluded what
you removed, it is a bug fix. Under it `bind-too-narrow`'s narrowing was a reuse and the
`remote` guard was not, so the count stays **two** and `bind.md`'s reading was the right one.
A change to a check's `fix` text is never a reuse at all.

**Found and not fixed:** `setup` writes `saved.host` for every class though `state.rs` calls
it "only meaningful for `remote`", and `doctor` **check 2** still infers the class from
`config.core.host` **or** `saved.host` — so a stale `--host` makes check 2 say `remote` on a
`wsl-host` machine. Recorded in [open.md](../../embarch-umbrella/open.md) with the reason for
abstaining: the `or(saved.host)` fallback's intent is undocumented and it does not preserve
the `remote` class either (nothing feeds it back to `infer_class`), so clearing it on a
non-remote class would change check 2's answer on real machines on a guess.

**No hardware debt added.** The existing one is unchanged and grows no new arm: check 17's two
Fail branches have still never met a real narrow-bound Core, and this unit changed a `fix`
string and one struct-field initialiser, both fully covered by host tests.

**Reserve spent, and filed.** `open.md` 4,601 → **5,080 B (99.2%)** and
`decisions/bind.md` 8,465 → **11,409 B (92.8%)**; both named in
[`tasks/umbrella/009`](009-compact-docs.md), which was reopened for them. `open.md` has 40
bytes left and `check-duplication.py` reports no cross-doc overlap in this sub-project, so the
next unit to write it cannot ride a compaction along — that is written into `009` explicitly.
