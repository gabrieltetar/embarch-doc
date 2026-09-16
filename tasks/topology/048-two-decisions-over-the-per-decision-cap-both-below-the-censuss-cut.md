# 048 — two `embarch-topology` decisions are over the per-decision cap, both below the census's cut

**State:** done — leg 119
**Source:** leg 118, 2026-09-16. Leg 117's suite-wide per-decision census reported five breaches and
filed four tasks, of which `topology/047` — decision 25, the largest decision entry in the suite — was
one. Leg 118 landed all four and then found the census had never been capable of seeing the rest:
`check-doc-size.py --decisions` prints the **twenty largest decisions in the suite** and marks which
are over cap, so an unpinned breach below that line is printed nowhere, and 27 pinned over-cap entries
fill the slots. Read through `decision_state()` directly, five unpinned breaches remain and two of
them are here. Neither is a regression and neither was touched by `topology/047`. The mechanism is
`tasks/doc/064` (owner-reserved; `scripts/`).
**Scope:** topology
**Hardware:** none — doc prose only. No board, no probe, no live Core, no deploy, no enrolment.
**Owner:** no
**Compacts:** `embarch-topology/decisions/validation.md`, `embarch-topology/decisions/link-declares.md`
**In flux:** no, both, and each was checked separately rather than answered once for the line.
Decision 21 is the Nordic arm the self-reported-ID gate gained; the arm landed, and what is still open
is a **hardware** gap — `nRF54L10`, `nRF54L05` and `nRF54LM20A` take that arm with no such silicon
ever on this bench. A hardware debt is not doc flux: a board would *add* a measurement, not rewrite
the decision. Decision 20 is the role-uniqueness and link-interface pair that closed the day the dev
bench went back to being an nRF54L15DK; both gaps named in it are closed.

## What

Two entries, both over the 4,096 B per-decision cap, neither pinned in
`scripts/decision-size-baseline.json`:

```
4,301 B  embarch-topology/decisions/validation.md#21      (+205 B, 105% of cap)
4,176 B  embarch-topology/decisions/link-declares.md#20   (+ 80 B, 102% of cap)
```

Both are small breaches — 80 B is under a paragraph. For each, the same fork `topology/047` faced and
answered with a compaction:

- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full.
- **One decision that has accreted several arguments** → split into two numbered decisions and update
  `embarch-topology/decisions.md`'s index, same commit. **A new decision number is the most expensive
  thing in this suite to reverse**, so the burden of proof is on this branch.

Decision 20's own opening — *"Two independent gaps, one event"* — is worth reading against that fork
before choosing. It says in as many words that it carries two things. At 102% of cap the split is
still a hard case to make, and `topology/047` made the opposite call on a much more split-shaped
entry by asking the right question: **does any inbound citation want to point at the two halves
separately?** Answer that with a grep, not an impression.

## Watch for

- **The safety claims must not end up reading as tested.** Decision 21's whole point is that *"a
  comparison that could not be made is not a comparison that succeeded"*, and that the gate had never
  once run against Nordic silicon before that arm. Decision 20's role-uniqueness half exists because
  *nothing errored and the file looked correct* while two rows claimed the same role. Both are
  descriptions of silent failure, which is the category `DOC-COMPACTION-PASS.md` calls hot: cut
  narrative, never the mechanism.
- **Decision 25 is now 4,001 B with 95 B of margin** after `topology/047`. Do not spend that margin
  from the side — if your work touches `validation-classifier.md` at all, check its size before you
  push.
- **The `core/064` failure mode, which hit this class twice in leg 118 alone.** A cut justified as
  "provenance" or as "duplicates decision N" is exactly where a live claim goes missing: once when a
  retired decision's compaction cut a live-route behavioural fact (`tasks/core/065`), once when a
  "duplicates decision 35" justification covered only part of the cut paragraph
  (`inbox/umbrella-locate-api-list-targets-shape-orphaned.md`). If you justify a cut by pointing at
  another decision, **open that decision and confirm it covers the whole hunk, sentence by
  sentence** — not the topic.
- **Quote every cut hunk verbatim and completely** in this task file. Err toward over-inclusion.
- **Do not add pins to `scripts/decision-size-baseline.json`.** `scripts/` is owner-reserved, and
  pinning an over-cap decision is the papering-over move.
- **Grep the whole doc repo for inbound `decision 20` and `decision 21` citations first**, and
  remember a bare `decision 20` in another sub-project's file means *that* sub-project's 20.
- **Report before/after byte counts and the margin left** for each entry you touch.

## Dispatch note — leg 119, 2026-09-16

**In reserve for `topology`: nothing.** No `embarch-topology` file is inside the last 10% of its cap,
so you have file-level room and this is purely the per-decision cap. If your work does push a file
into reserve, file `tasks/topology/<NNN>-compact-topology.md` in the same commit
(`scripts/check-task-numbers.py --next topology` for the number — **do not read the directory**).

**The census that filed this task is itself unreliable, so do not use it to check your work.**
`check-doc-size.py --decisions` prints only the twenty largest decisions in the suite and 27 pinned
over-cap entries fill those slots, so it cannot confirm a smaller entry is now under cap
(`tasks/doc/064`, owner-reserved). Count the bytes of each entry you touch directly and report them.

## Done when

- [x] `embarch-topology` decision 21 is at or under 4,096 B, or split, with the branch justified.
- [x] `embarch-topology` decision 20 likewise, **or** left untouched with a follow-up task filed.
- [x] The untested-silicon statement in decision 21 and the silent-failure mechanism in decision 20
      both survive.
- [x] `embarch-topology/decisions.md`'s index matches, if anything was split. (N/A — neither split.)
- [x] Every inbound citation to a touched decision still resolves to the claim it was citing.
- [x] Every cut hunk quoted verbatim in this task file.
- [x] No pin added to `scripts/decision-size-baseline.json`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Resolution

**Both compacted, neither split.** Measured directly against `decisions()`'s own algorithm (heading
line through the next `### ` or EOF, `.encode()` length) rather than the census, per the dispatch
note:

```
before                                          after                        margin
4,301 B  validation.md#21      (105% of cap)    3,992 B                      104 B
4,176 B  link-declares.md#20   (102% of cap)    3,717 B                      379 B
```

**The split-vs-compact fork, answered by grep, not impression.** Decision 20's own opening —
"Two independent gaps, one event" — and its own `decisions/enrollment.md` predecessor task
(`tasks/topology/019`) had already flagged the seam explicitly: "decision 20's role-uniqueness half
vs. its link-interface half" as a candidate split, back when 019 chose a *file*-level split instead
and left decision 20 as one entry. Grepping the whole doc repo for inbound `decision 20`/
`embarch-topology decision 20` citations found both halves cited **separately** from
`embarch-topology/spec.md` itself (line 69: role uniqueness; line 75: link interface), and the
link-interface half cited on its own, by bare `embarch-topology decision 20`, from
**`embarch-api/decisions/client-crate.md:57`** and (in wording, not name) from `.claude/leg.md:432`,
which quotes decision 20's own phrase "a bench that flashed, booted, ran, and timed out" verbatim.
That is real split-shaped evidence — but `embarch-api/decisions/client-crate.md` is another
sub-project's doc, out of this task's scope (`Scope: topology`) and not mine to edit. Splitting
decision 20 would either (a) leave that cross-repo citation ambiguously resolved once the content it
quotes moves to a new number, which I cannot fix from here, or (b) require an `inbox/` drop asking
`embarch-api`'s owner to retarget its own citation — real cost, for an 80 B (102%) overage that
compaction clears with 379 B of margin to spare. Per the task's own framing, "a new decision number
is the most expensive thing in this suite to reverse, so the burden of proof is on this branch" — and
the burden is not met at 102% once the fix is cross-repo. Decision 21 has no comparable "two
arguments" shape (continuous narrative about one arm), so compaction was the only fork considered
for it.

**Cold content cut, quoted verbatim and completely.**

Decision 20 (`decisions/link-declares.md`) — the whole cut is the investigation-log tail of the
"guess was invisible" paragraph, already preserved almost verbatim as
`embarch-decision-reversals.md` row 105 (`reversals/rows-93-109.md`, tagged `topo 20` — not edited,
just confirmed it already carries this), so nothing here is lost from the corpus, only from the live
decision text:

> Two hypotheses were checked and discarded before the port was suspected: that the identity gate's
> attach left the core halted (**refuted by reading the debug status register: halt clear, sleep set,
> i.e. running**) and that the overlay had not applied (**refuted in the generated devicetree**). What
> settled it was **writing a real handshake frame to each candidate by hand** — one returned nothing,
> the other returned an ack plus the bench's own log lines.

Kept unedited, verbatim, right before that cut: "**What made it expensive was that the guess was
invisible.** Selection logged a warning into Core's log and returned a result **indistinguishable
from a determined answer**, reported with full confidence. **The observable symptom was a bench that
flashed, booted, ran, and timed out waiting for a handshake — which says nothing about a port having
been chosen at all.**" — the exact clause `.claude/leg.md:432` quotes, and the whole silent-failure
mechanism the task's "Watch for" section calls out. The role-uniqueness half (`.claude/leg.md`'s other
citation target, `tasks/topology/004`, `embarch-decision-reversals.md` row 104) was not touched at
all — it was not the source of the overage and needed no cut.

Decision 21 (`decisions/validation.md`) — five small provenance/phrasing cuts, none removing a claim,
an invariant, a rejected alternative, or the untested-silicon list. Verbatim, in order:

> was right and it held. What it also meant is that

→ "held. What it also meant is that" (one adjective-clause dropped; "the rule held" unchanged in
meaning).

> The observed pair is a confirmation of the derivation, not its source.

→ "The observed pair confirms the derivation, it is not its source." (reworded shorter, same claim).

> which is why a single relation serves the classic parts and the nRF54L series alike.** **The limit
> is written into the code rather than left implicit:** that file has fallbacks

→ "so **one relation serves the classic parts and the nRF54L series alike.** That same code falls
back" (dropped the "limit is written into the code rather than left implicit" meta-sentence — pure
narration about the code's own legibility, not a claim a reader needs; the fallback→mismatch
invariant right after it is untouched).

> and the same exposure the first arm already carries, accepted on the same terms.

→ "the same exposure the first arm already carries." (dropped "accepted on the same terms" — restates
the preceding clause).

> **Why this matters more here than it did on the first chip**, and why it is a decision rather than a
> bug fix:

→ "**Why a decision, not a bug fix:**" (dropped the "matters more here" framing clause; decision 10's
citation and the two-boards-same-family point right after are untouched).

> because the two sides reach the registers by routes that share nothing. The JTAG side reads two
> hardcoded absolute addresses over the probe; the board's side goes through the vendor HAL's own
> device-ID accessor, which has never heard of those constants.

→ "because the two sides reach the registers by routes that share nothing: JTAG reads two hardcoded
absolute addresses over the probe; the board's self-report goes through the vendor HAL's own
device-ID accessor, which has never heard of those constants." (merged two sentences into one,
dropped "The" / "side" twice; the route-independence claim — why the match means anything — is
unchanged).

> [measured 2026-08-31, reproduced 2026-09-06 22:07:51Z and 22:15:45Z from Core's own handshake log]

→ "[measured 2026-08-31, reproduced 2026-09-06]" (dropped the intra-day timestamps and the
provenance clause naming where the reproduction was read from — classic "provenance and dates," per
`DOC-COMPACTION-PASS.md`'s cold list; the fact that it was reproduced, and on what date, survives).

> The **second** word is the one that carries the weight: a wrong address there would still have
> produced a plausible 64-bit value and a distinct-looking ID, and could not have produced the HAL's
> `DEVICEID[1]`.

→ "The **second** word carries the weight: a wrong address there would still have produced a
plausible, distinct-looking 64-bit value, and could not have produced the HAL's `DEVICEID[1]`."
(dropped "is the one that" and merged "plausible 64-bit value and a distinct-looking ID" into
"plausible, distinct-looking 64-bit value" — same two properties, one clause).

**Kept unedited, in full:** the `"not a pass: a comparison that could not be made is not a comparison
that succeeded"` quote; the fallback-register `mismatch`-not-`undeclared` invariant; the hex values
(`6fcddc36cb781b71`/`cb781b716fcddc36`/`834f2559f10a6cdf`/`2f77b9c3f85b29e9`); the entire
"What it does not confirm" paragraph, including "`nRF54L10`, `nRF54L05` and `nRF54LM20A` share the
arm and no such silicon has been on this bench" — the sentence `embarch-topology/open.md` and this
task's own preamble both depend on.

**Citations checked, not just grepped.** Every in-scope inbound citation
(`embarch-topology/spec.md:69,75`, `decisions/enrollment.md:31`, `decisions/links-port.md:25,27`,
`decisions/scope.md`, `open.md:15`, `history/topology.md:61`) still resolves to the claim it cited —
none of the cut text was itself the target of a citation; I read each inbound `decision 20`/
`decision 21` hit in the whole doc repo (including other sub-projects' files, which I did not edit)
before cutting and confirmed the cut material was investigation narrative or provenance detail, not
anything a citation pointed at. No `inbox/` drop was needed: the one candidate finding (the
cross-repo split-shaped citation from `embarch-api/decisions/client-crate.md`) argues *against*
touching decision 20's number, so there is nothing for `embarch-api`'s owner to act on.

**Hardware debt:** none. This is doc prose only; nothing here needs a board.

**In reserve:** neither file. `decisions/validation.md` is now 4,589 B and `decisions/link-declares.md`
is 7,708 B, both well under the 12,288 B (12 KB) decision-group cap — no `tasks/topology/<NNN>-compact-topology.md`
needed.

**Gate:** `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings` all
green in `embarch-topology` (no code touched by this task). `scripts/check-docs.py`: all 11 checks
green. `scripts/check-doc-size.py`: exit 0, both entries now under cap (3 unrelated unpinned
over-cap decisions remain elsewhere in the corpus — not topology's, not this task's scope, and this
check does not fail the gate on an unpinned overage). `scripts/check-client-names.py --repo
<code worktree>`: clean. `scripts/check-ownership.py --scope topology` (doc worktree) and
`--code-repo` (code worktree): both OK.

**`spec.md` alone, for the human question:** yes. Neither cut removed anything `spec.md` states or
depends on — `spec.md`'s own decision-20 citations (role uniqueness at line 69, the interface guess
at line 75) and its decision-21 citation (line 123, the confirmed register pair) all still name
claims the decisions text still carries in full; what was cut was investigation log and provenance
detail that `spec.md` never restated in the first place. Someone working on link/role enrollment or
the Nordic identity arm today can still get everything they need from `spec.md` plus a citation
lookup — the two decisions are shorter, not thinner.
