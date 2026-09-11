# doc — a suite-wide convention for "has this check arm actually run"

**State:** blocked — the decision this task asked for is **made** (box 1, below); what is left is
one edit to an owner-reserved file and no agent may make it. See `## Blocked` at the foot.
The §8 window announced by leg 073 on `ts 1789093650.796139` closed at 20:57:31 MDT with no reply,
and leg 074 executed the task at 20:58 MDT. Leg 074 did not restart the window.
**Source:** tasks/umbrella/032 (check 14's `WslHost`/`Remote` skip arms are unreachable on a
set-up machine) — the umbrella half landed in `embarch-umbrella/spec.md` (a `measured` marker
on a check-table row, cited to a decision that records a real run) and
`decisions/doctor.md` decision 31.
**Scope:** suite
**Hardware:** none
**Owner:** required — `DOC-CONVENTIONS.md` is owner-reserved. Written unbolded on purpose:
`queue-status.py` matches this value literally and a bolded one parses as not-required
(`tasks/doc/039`, filed by this same leg).

**Filed under `suite/` rather than `doc/` by leg 042.** The drop was written
`Scope: doc`, but its whole subject is `DOC-CONVENTIONS.md` — a shared
suite-level doc that `protocol.md` §3 reserves to the supervisor. `suite/` is
the mechanism that keeps a task off a worker; `doc/` is not. Running it needs
the §8 announcement-and-park window, so a leg takes it as its own unit or
leaves it.
**Hardware:** none

## What

`embarch-umbrella/spec.md`'s `doctor` check table now marks a row `measured` only once a real
run has hit that arm, and says so in prose next to the table (per-file, since `DOC-CONVENTIONS.md`
is off limits to a worker). Three instances of the same shape have now turned up across the
suite — umbrella decision 18 (check 5's Linux-only probe scan), umbrella decision 31/check 14
(this task), and embarch-topology's `TopologyClass::Local`-gated branch named in 032's own "why
this is worth recording" section (leg 022) — which suggests "exercised vs. designed-only" is a
suite-wide table-shape question, not an umbrella-only one.

## Why now

032's supervisor direction (leg 041) was explicit that the durable answer belongs in
`embarch-umbrella/spec.md` first, as a sub-project-local convention, and that generalizing it
into `DOC-CONVENTIONS.md` is a refused branch for a worker — "say so in an inbox drop and leave
the suite-wide half there." This is that drop.

## Done when

- [x] A decision made (by the owner or a supervisor, not a worker) on whether `DOC-CONVENTIONS.md`
      should adopt a `measured`-style marker as a suite-wide convention for check/table rows that
      distinguish an exercised arm from a merely-designed one, given it has now recurred three times.
      **Decided by leg 074, 2026-09-10 — adopt, but as a scope correction to the section that
      already exists, not as a new convention. Reasoning below.**
- [ ] If adopted, `DOC-CONVENTIONS.md` gets the convention and the other sub-projects with
      class/state-gated check tables (`embarch-topology`, and any other doctor-adjacent surface)
      get a pointer or a pass applying it. **Owner's — the exact edit is drafted below.**
- [ ] ~~If rejected~~ — not the outcome.

---

## The decision, leg 074, 2026-09-10

**Adopt it, and the cheapest correct form is one word in a section `DOC-CONVENTIONS.md` already
has.**

### The premise needed correcting first, in both directions

**Two of the task's three instances check out; the third does not, and I did not take it on
faith.** The two real ones are both in `embarch-umbrella/interfaces/doctor-chain.md`: check 14's
row carries a literal `**measured** (decision 38)`, and line 38 of that same file states the
local convention in prose — *"A row naming several arms says which have run, not only which were
written."* The third, cited as an `embarch-topology` `TopologyClass::Local`-gated branch, is **not
a table row and not a doc convention at all** — `embarch-topology` has no `interfaces/` directory
and no class-gated check table. It is a code branch. So the task's "it has recurred three times"
is really *twice in one file, plus a code-level analogue*, which on its own would be thin evidence
for a suite-wide rule.

**But the real evidence base is far larger than three, and it is in a different place.** Grepping
the eight `open.md` files for the shape — *an arm that was designed and has never been exercised*
— returns **17 bullets across five sub-projects**. A sample, quoting each file:

- `embarch-umbrella/open.md`: *"Check 17's two Fail branches have never met a real narrow-bound
  Core"*; *"Check 5's not-permitted fail has never met a real permission-denied probe"*; *"Check
  13's two `umbrella/034` findings are fixed but unverified against a real bench"*.
- `embarch-api/open.md`: *"`study_watch` has met a real embarch-core; the rest has not."*
- `embarch-ui/open.md`: *"The stale-prefix drop has never met a real stale prefix"*.
- `embarch-topology/open.md`: *"No signal tap has read a byte."*
- `embarch-study-designer/open.md`: *"`nRF54L10`/`nRF54L05`/`nRF54LM20A` take the same arm with no
  silicon ever attached."*

**That changes what the question is.** The suite does not lack a convention for "designed but not
exercised" — it has a strong one, and it is working: the fact goes in `open.md` as a bullet with
its own closing trigger, `collect-open-questions.py` sweeps every one of them, and a refill pass
reads them. Seventeen instances is not a gap; it is a convention being honoured.

### So what is actually missing, and why the umbrella table found it

**The `open.md` bullet is read by someone auditing what is unfinished. The table is read by someone
using the capability. They are different people and the second one never goes looking.** A reader
of `doctor-chain.md`'s check-14 row wants to know what check 14 does; nothing in that row would
have told them which of its arms has ever fired, and nothing would have prompted them to open
`open.md` to find out. `umbrella/032` arrived at the marker by hitting exactly that — and it
arrived at the *same word*, `measured`, independently.

**That independent convergence is the strongest signal here.** `DOC-CONVENTIONS.md` §"Measured vs.
assumed constants" already mandates `[measured <date>, <how>]` / `[assumed]`. The umbrella table's
author, solving a different problem in a different file, reached for the same marker with the same
meaning. Two independent arrivals at one marker is evidence the marker is right and that the
section's **scope line** is what is wrong.

### The scope line is wrong, and its own test already covers the new case

The section says *"Every load-bearing **constant** says which it is, inline"*, and its own earning
test is *"The bracket earns its place on an **inventoried** item — one in a table or declared list,
where provenance would otherwise be vague."*

A check-table row **is** an inventoried item in a table where provenance would otherwise be vague.
It fails the section's *stated scope* (it is not a constant) and passes the section's *stated
test* (it is inventoried, and its provenance is vague). When a rule's scope and its test disagree,
the test is usually the thing that was actually reasoned about. Here the test is also the suite's
founding invariant — `embarch-api/spec.md` §2's no-inference-as-fact — and there is no principled
reason that invariant should govern a number and not a behaviour. **A row that says a check has an
arm is a claim about behaviour, and an unexercised arm is an inferred fact stated as a measured
one, which is the exact failure the constant rule exists to prevent.**

### What this deliberately does not become

**Not a new marker, not a new section, and not a sweep.** Three refusals, each for a reason:

1. **No second vocabulary.** Inventing `exercised`/`designed-only` beside `measured`/`assumed`
   would give the suite two words for one distinction. The umbrella instance already shows one
   word carries both cases.
2. **No suite-wide pass applying it.** `DOC-CONVENTIONS.md`'s constant rule already settled this
   trade-off for itself and got it right: *"mark an inventory, leave good prose alone, and mark
   the rest as each doc reaches a compaction pass."* A sweep across every table in the suite would
   cost several units to mark rows nobody is currently misreading. The same clause should govern
   the extension.
3. **No change to the `open.md` bullets.** They are the durable record and they carry the closing
   trigger, which a table cell cannot. The table marker is a **pointer**, not a replacement — and
   the convention text should say so, or the 17 bullets start getting deleted as redundant.

### What leg 074 could not do

**Make the edit.** `DOC-CONVENTIONS.md` is owner-reserved and `protocol.md` §3's table is explicit
that *every* `DOC-*.md` is `never` for the supervisor, not merely for a worker. Verified directly
rather than assumed: `check-ownership.py --supervisor --stdin` on the path exits 1.

**This is a correction to how the task was filed, and it is worth recording.** Leg 042 moved the
drop from `doc/` to `suite/` on the argument that *"`suite/` is the mechanism that keeps a task off
a worker"* and that a supervisor would therefore take it under the §8 window. That is half right:
`suite/` did keep it off a worker, and the §8 window was genuinely owed for the *decision*. But
scope does not confer write access — a `suite/`-scoped task whose only deliverable is an edit to a
reserved file is not executable by the actor `suite/` routes it to. **The §8 announcement was
correct and the routing was not.** Either box-1 tasks like this should be filed `suite/` and box-2
tasks `doc/ + Owner: required`, or a task spanning both should say so in its header; leg 074 has
taken the second route by marking this one `Owner: required` for the remainder.

### The edit, drafted so the owner's commit is mechanical

In `DOC-CONVENTIONS.md` §"Measured vs. assumed constants" — retitle to **"Measured vs. assumed"**
and add, after the existing "mark an inventory, leave good prose alone" sentence:

> **The same bracket applies to an inventoried *arm*, not only an inventoried constant.** A row in
> a check or capability table that names several branches says which have **run** and which were
> only written: `measured` cites a live run, prose alone means reasoned but not observed.
> `embarch-umbrella/interfaces/doctor-chain.md` is the worked instance. This marks the table; it
> does **not** replace the `open.md` bullet, which is where the fact and its closing trigger live.
> Apply it as each doc reaches a compaction pass, not as a sweep.

`DOC-CONVENTIONS.md` is 7,961 B and the draft above is roughly 560 B, so size is no obstacle.

**One thing found while checking that, which is a fact about the repo rather than about this
task:** `check-doc-size.py` tracks **no cap at all** for `DOC-CONVENTIONS.md`. It is absent from
the gate's full listing, not merely out of reserve. I had assumed the 10 KB suite-level cap
applied and wrote that number here before verifying it; it does not. `DOC-BUDGET.md`'s table caps
`<sub-project>/spec.md`, `suite/*.md` and `embarch-decision-reversals.md` at 10 KB each and has no
row that reaches a top-level `DOC-*.md`. Whether that is deliberate — these are the owner's files
and a budget on them constrains only him — or an omission is `DOC-BUDGET.md`'s call and so the
owner's; it is recorded here rather than filed separately because it is one line and it is
directly adjacent to the edit above. Note that `DOC-BUDGET.md` *itself* is capped and tracked
(11,670/12,288 B, on the ledger as `tasks/doc/031`), so the absence is specific rather than a
blanket exemption for top-level docs.

## Blocked

**Blocked on one commit by the owner, and on nothing else.** The decision this task existed to
produce is made and recorded above; `DOC-CONVENTIONS.md` is owner-reserved, so the edit that
carries it into the corpus cannot be made by a supervisor or a worker. Verified directly rather
than inferred: `check-ownership.py --supervisor --stdin` on `DOC-CONVENTIONS.md` exits 1.

**Unparked by:** the drafted paragraph in "The edit, drafted so the owner's commit is mechanical"
landing in `DOC-CONVENTIONS.md`'s "Measured vs. assumed" section, or the owner deciding against it
and saying so in one line here. Either closes this task; **it does not need a fresh §8 window**,
because the window for the decision already ran and closed unanswered.

**This unpark condition is reachable** (`tasks/doc/032`'s concern): it is a single edit to a file
the owner writes routinely, with the exact text already drafted and its size already checked. No
hardware, no other task, no agent.

**Not blocked on, and deliberately not attempted:** box 2's second clause, *"the other
sub-projects with class/state-gated check tables get a pointer or a pass applying it."* The
decision above refuses that sweep on `DOC-CONVENTIONS.md`'s own existing grounds — mark as each
doc reaches a compaction pass — and the survey done for this task found no second table to sweep
anyway: `embarch-umbrella/interfaces/doctor-chain.md` is the only class-gated check table in the
suite.
