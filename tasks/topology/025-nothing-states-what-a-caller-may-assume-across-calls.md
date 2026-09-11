# 025 — nothing states what a caller may assume about a resolution or validation answer across calls

**State:** claimed by agent/topology/025-caller-granularity-contract, 2026-09-10 18:52
**Source:** `embarch-topology/open.md` — "Call-site granularity is not fully specified. Resolution
and validation are fresh-every-call by construction, with no cache in the crate; **nothing states
what a caller may assume beyond that**, so a consumer wanting to hold an answer across calls has no
rule to read." Swept by the supervisor, leg 070, 2026-09-10.
**Scope:** topology
**Hardware:** none — this is a contract that exists to be written down; every fact it records is
already true of the code as it stands, and confirming it is a read of this crate plus its callers.
**Owner:** no

## What

`embarch-topology` resolves and validates fresh on every call and holds no cache. That much is
already recorded. What is missing is the *caller's* half: whether an answer this crate returns may
be held across calls, for how long, and what invalidates it.

Three consumers hold these answers today in different ways and none of them has a rule to read —
`embarch-core` (which links only the `hardware` half), `embarch-api`, and `embarch-umbrella`. The
task is to state the contract the crate actually offers, in its own docs, and to say so in terms a
consumer can act on: what is guaranteed fresh, what a caller may cache and under what invalidation
(a board being unplugged is the obvious one), and what it must never assume.

**Write the contract this crate already has, do not invent a stronger one.** If the honest answer
to "how long is a resolution answer good for" is "until the USB topology changes, which nothing
here observes", that is the answer and it belongs in writing. A rule promising more than the code
delivers is worse than the current silence.

Where the answer is genuinely a design choice rather than a description — for instance whether the
crate should offer an explicit invalidation signal at all — record it as a numbered decision in
this sub-project, per `../../embarch-fleet/protocol.md` §5 rule 4. That is within a worker's own
scope and needs nobody's approval.

## Why now

The open question has been standing unanswered while three consumers grew around it, and the cost
is asymmetric: the crate is cheap to describe today and expensive to describe after a fourth
consumer has assumed something different. Nothing here needs a board, so it is one of the few
`topology` items the fleet can close at all.

## Done when

- [x] `embarch-topology/spec.md` states what a caller may assume about a resolution or validation
      answer across calls, what invalidates one, and what is never cacheable — new section "What a
      caller may assume across calls".
- [x] The `open.md` bullet is rewritten to whatever is genuinely still open after that, or removed
      if nothing is — removed; nothing about it stayed open.
- [x] A numbered decision if and only if a choice was made rather than a description written —
      decision 29 (`decisions/scope.md`), recording that an explicit invalidation signal was
      considered and rejected.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10), `changelog.d/topology-*` fragment dropped,
      and a `status.d/topology-*` fragment for any suite-level fact this made false — none; no
      suite-level fact changed.

## Note

Adding the new section pushed `embarch-topology/spec.md` past 90% of its cap
(10001/10240 B). Per the dispatch note, paid the compaction debt in the same
commit: trimmed non-protected prose (the "It is not" bullets, the declared-
facts paragraph, the validation-assertion bullets, the consumer-ownership
bullets, "Where it stands") down to 9195/10240 B (89.8%), without touching
`tasks/topology/024`'s **Must not delete** list — the decision-28 sentence,
the process/call-site code block, and the "Storage and roles" section are
all untouched, verbatim. `024` stays blocked/open (still `In flux: yes` per
`004`/`020`) and its **Must not delete** list now also names this task's new
section.
