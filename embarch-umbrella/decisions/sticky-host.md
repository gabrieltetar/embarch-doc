# embarch-umbrella decisions: What a saved `--host` means later

**Status:** active, 2026-09-10.

**New file, not squeezed into [bind.md](bind.md).** That file is 11,447/12,288 B — 841 B left,
already in reserve with its own compaction parked (`tasks/umbrella/009-compact-docs.md`) — and
`umbrella/020`/`022` set the precedent of a sibling topic file over a second squeeze
([DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2). This decision is adjacent to decision 22 —
both are about check 17's and check 2's neighbour, `state.rs`'s `host` field — but it settles a
different question: not where Core is listening, but what a *found* `saved.host` is evidence of.

Index: [../decisions.md](../decisions.md). Current truth: `state.rs`'s doc comment on `host`, and
`doctor.rs`'s check 2 (`check_service`).

### 48 — `saved.host` is "an explicit `--host` was once given", not "this machine is `remote`"

**The field.** `state::State.host` is written by `apply_plan` on *every* `setup` run, for every
concluded class, as `host.map(str::to_string).or(saved.host)` — the current run's `--host` flag if
one was given, else whatever was already on disk, carried forward untouched. There is no branch on
`class` anywhere in that expression. A `local` or `wsl-host` conclusion does not clear it, and
nothing else in this crate clears it either — the bullet this decision closes, `open.md`'s "still
sticky", names exactly that gap and leaves it unmade here (see below).

**What that makes the field mean.** Not "the remote host for a `remote` machine" — a `local` or
`wsl-host` run never had a remote host to record, yet the field can still hold one, left over from
whichever earlier `setup` invocation last passed `--host` (on this machine or a previous topology
this same state file survived). `state.rs`'s "Only meaningful for `remote`" comment describes what
the field is *for* — `infer_class` reads a host to decide `Remote` — but not what a **stored**
value actually attests to, which is narrower: *at some past run, some `--host` was typed.* It says
nothing about whether that run's conclusion still holds, or whether any run since has needed a
host at all.

**What check 2 may infer from finding one.** `check_service` reads `config_host.or(saved_host)`
and feeds the result to `setup::infer_class`, the same function `setup` itself uses — deliberately,
so the two commands never disagree about which class an unreachable Core "should" be (`bind.md`
decision 22's shared-input principle, applied here to check 2 rather than check 17). Given that
function's contract (`host.is_some()` ⇒ `Remote`, unconditionally), check 2 is entitled to conclude:

- **"An explicit `--host` is on record, from `config.core.host` or a saved one"** — check 2 already
  says which, per `umbrella/026`.
- **"`infer_class` would call this machine `remote` right now, given that host"** — that is a fact
  about the function, not about the bench, and it is exactly what the Fail detail and fix line
  claim: an inference, named as one.

**What check 2 may not infer:**

- **That the machine's *current* topology is `remote`.** `saved.host` surviving a later `local` or
  `wsl-host` `setup` means the stored value can postdate the class it is being read alongside — the
  two are written independently and neither is validated against the other at read time.
- **That the host string is still reachable, correct, or even the same remote Core the operator
  meant.** Nothing revisits it between runs; it is cached, not re-verified.
- **That a missing `saved.host` means no `--host` was ever given.** It means none survived to this
  read — `apply_plan` only ever adds or forwards, so absence is as uninformative as presence is
  over-informative, in the opposite direction, on a machine whose state file predates persisting it.

**Why this is a Fail-detail concern and not a fix.** Check 2's existing "which evidence" framing
(`umbrella/026`) already stops short of asserting the class *is* correct — it says what was
*inferred* and from what. That phrasing turns out to be exactly right for a sticky field: it is
honest about a value that can be stale by construction. No wording change is needed there; this
decision is the record of *why* it was already right, so a future edit does not "fix" it into
overclaiming.

**Deliberately does not change when `saved.host` is cleared.** Clearing it on a non-`remote`
conclusion — the fix `open.md` still names as unmade — changes what a real `doctor` run reports on
a real machine, which needs the bench to confirm and is out of scope for a documentation decision.
That half stays open.

### 51 — `apply_plan` clears `saved.host` on a non-`remote` conclusion

Decision 48 left this unmade. Settled now: **clear**, not keep.

**Why clear rather than keep.** `saved.host` exists to answer one question — "is an explicit
`--host` on record?" — and `infer_class` treats its mere presence as sufficient to conclude
`Remote` (`host.is_some()` ⇒ `Remote`, unconditionally; decision 48's "field" section). A machine
that just concluded `local` or `wsl-host` has, by that same run, answered the question the other
way: no host applies here. Leaving the old value in place means the *next* run with no `--host`
flag reads a leftover from a session or topology that no longer holds, and `infer_class` calls it
`Remote` again — the class this decision's own bug report describes as "steer a later run" wrong.
Keeping it would only ever help one case (an operator alternating between the same two machines
without retyping `--host` each time), and that case still has to retype the flag's *sibling*
information — `EMBARCH_TOKEN` isn't sticky either — so the saving was partial regardless.

**The rule.** `apply_plan` writes `state.host` as `plan.host` only when `plan.class` is
`TopologyClass::Remote`; every other concluded class writes `None`, discarding whatever
`make_plan`'s `host.map(str::to_string).or(saved.host)` carried forward. `make_plan` itself is
unchanged — the carry-forward still has to happen there so a `remote` run with no `--host` this
time can still resolve one from the saved value; the new branch is only in what gets written back
out afterward.

**What this changes for check 2.** Nothing in `check_service` itself — it still reads
`config_host.or(saved_host)` off whatever the state file holds, and decision 48's account of what
it may and may not infer from finding a value is unaffected. What changes is how often it *finds*
one: a `saved_host` surviving into a later read now only ever postdates the most recent `remote`
conclusion, not an arbitrarily older one from a different topology entirely.

**Not verified against a real machine.** The state-transition unit test (`setup.rs`) covers a
`remote` run that saves and a subsequent non-`remote` run that clears; confirming this on the
primary bench — a real `--host` given, a real `local` re-run, a real `doctor` after — is
`open.md`'s hardware debt, unchanged by this decision.
