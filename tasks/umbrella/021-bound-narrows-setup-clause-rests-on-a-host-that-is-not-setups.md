# 021 — `bound-narrow`'s new `setup` clause reads a `host` that is not the one `setup` reads, and its `Remote` branch is unguarded

**State:** open
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

- [ ] Item 1 is fixed, or decision 22's "can never disagree" sentence is corrected to what is
      true, with the losing option argued against.
- [ ] Item 2 has a guard or an argued-and-tested reason the `Remote` branch is right.
- [ ] Item 3 has one reading of decision 37 recorded in `reporting.md`.
- [ ] Gate green; `changelog.d/umbrella-*` fragment dropped.
