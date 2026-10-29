# 081 — The refill gate's scope-spread half fires forever on a queue whose thin scopes have converged

**State:** done — the gate is left as it is and `.claude/leg.md` says when a spread-only firing may be skipped: the newest `Spread sweep: nothing filed (<time>)` log line is newer than every source a sweep reads, checked with one `git log --since`. `--refill-owed` prints a `spread only` hint line; exit status unchanged. No per-scope flag: the three scopes found converged here had 53 tasks filed in the next six weeks. embarch-fleet `3bc39b7`.
**Filed by:** leg 139, 2026-09-17, after running the sweep the gate demanded and finding **nothing
to file** — which is the condition that makes this a defect rather than a slow day.
**Source:** `scripts/queue-status.py --refill-owed`, this leg's own run, and the sweep it produced.
**Scope:** doc
**Hardware:** none
**Owner:** required — the gate lives in `scripts/queue-status.py` and the rule that reads it lives in
`.claude/leg.md`, both owner-reserved. An agent can measure this; it cannot fix it.

## What

`queue-status.py --refill-owed` has two halves (`.claude/leg.md`): a depth half — sweep when the
queue is below its low-water mark — and a **scope-spread** half, which fires when the dispatchable
tasks span fewer distinct scopes than the wave. This leg met the second, not the first:

```
REFILL OWED -- 3 distinct scope(s) (api, core, umbrella), below a wave of 6
dispatchable: 9
```

**Nine dispatchable tasks is not a thin queue.** What is thin is the spread, and the spread is thin
because **four host-side scopes have converged**. Leg 139 swept all three sources the rule names —
every `open.md` via `collect-open-questions.py`, `suite/roadmap.md`'s Now/Next, and
`embarch-decision-reversals.md`'s follow-ups — and filed nothing, because in `ui`, `topology` and
`study-designer` **every remaining open question is one of three things and none is dispatchable**:

- **hardware-gated** — needs a board, a real capture, a live radio (all of `study-designer`'s clock
  and grain questions, `topology`'s signal-tap and nRF54L device-ID bullets, `ui`'s stale-prefix
  debt and placement-vs-second-stream bullet);
- **deliberately parked with the reason written down** — `study-designer`'s `repeat`/`bitpack`/
  `crc32`/`fixed` render half ("a rendering built before any real capture exists would be tested
  against synthetic bytes"), `ui` decision 11's reflash selector, `Study.protocols`' absent UI path;
- **explicitly closed as not-work** — `topology`'s duplicate-predicate bullet says in as many words
  *"This is a standing limitation, not open work ... nothing points at further work here"*, and its
  `NotFound` bullet ends *"nobody has asked for either yet."*

`suite/roadmap.md`'s `Now`/`Next` is the same picture: a real `.eap` run on real hardware, and
`embarch-promptu`, which has no repo. `Later` is a Raspberry Pi, a Mac, deferred power profiling and
a paused repo.

**So the gate will fire again next leg, and the leg after that, and each one pays a full sweep that
cannot produce anything** — which is precisely the cost the low-water rule was written to avoid, now
arriving through the other half of the same gate. The depth half is self-limiting: filing tasks
raises the count. The spread half is not, because **no amount of sweeping can add a scope whose
questions all need a board.**

## Why now

Not urgent and not a correctness bug — the sweep is wasted work, not wrong work. What makes it worth
recording is that **it is invisible from inside a single leg.** Each leg sees a gate that says
"sweep", sweeps, finds nothing, and files nothing; the next leg starts cold with no memory that the
sweep already ran and no way to tell a converged scope from an unswept one. Three of this suite's
recorded defects have that exact shape — a check whose output is indistinguishable from the state it
is meant to detect.

It is also the leading candidate for what actually binds throughput now. Every recent handoff says
the **4-unit leg cap** bound the leg, with scope spread next; this says the spread is not a queue
that needs topping up but a suite whose remaining host-side work is genuinely concentrated in three
repos.

## Done when

- [x] Decided whether the scope-spread half should be suppressible — e.g. a scope marked
      *converged* in a file the gate reads, set by a leg that swept it and found nothing, cleared
      when anything new lands in that scope — or whether the honest answer is that it should stop
      firing once the depth half is satisfied and the wave is already scope-bound.
- [x] If the answer is "leave it", `.claude/leg.md` says so, so a leg can skip the sweep on the
      spread signal alone rather than re-deriving this every time.
- [x] Either way, **the converged-scope finding above is recorded somewhere a leg reads**, because
      it is the part that cost this leg real tokens to establish and that nothing currently carries.

## Not yours

Everything that would fix this is in `scripts/` or `.claude/`. Do not edit either. A leg that reads
this task may cite it in its log entry as the reason it did **not** sweep again; it may not change
the gate.

## Shipped

**Leave the gate; make the skip a leg rule keyed on the sources.** Three forks were costed:

- *Spread alone stops owing a sweep* — six lines in the script, but it discards a signal that
  still pays: on 2026-10-28 a spread sweep filed `topology/068` "for scope spread".
- *A per-scope "converged" flag* — a state file plus a set/clear rule. Measured against this
  task's own finding, it would have gone wrong within days: `ui`, `topology` and
  `study-designer`, converged on 2026-09-17, had 30, 10 and 13 tasks filed in the six weeks after.
- **Taken:** a spread-only sweep that files nothing writes `Spread sweep: nothing filed (<time>)`
  in its log entry; a later spread-only firing is skipped when
  `git log --since=<that time>` over every `open.md`, `open/<topic>.md` and `design.md`, `embarch-token.md`,
  `suite/roadmap.md` and `embarch-decision-reversals.md` is empty — i.e. a sweep would read what
  the last one read. Zero new state; the handoff already carries the line.

**Where the finding lives:** the class — and the evidence that convergence is a moment rather
than a property — is in `.claude/leg.md` beside the spread half it qualifies. The dated per-scope
list above is not copied there, because it stopped being true.
