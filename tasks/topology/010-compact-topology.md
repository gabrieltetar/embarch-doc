# 010 — Compact `embarch-topology/decisions/enrollment.md` and `spec.md`

**State:** done
**Source:** `scripts/check-doc-size.py` — both entered reserve on leg 023's bench unit
(`tasks/topology/002`), which added a confirmation paragraph and its limits to decision 21 and
rewrote `spec.md`'s "Where it stands" from *unexercised* to *measured*
**Scope:** topology
**Hardware:** none
**Owner:** no

**Compacts:** embarch-topology/spec.md, embarch-topology/decisions/enrollment.md, embarch-topology/decisions/alerts.md
**In flux:** no
**Must not delete:**

**From decision 21** — the whole point of the paragraph this leg added is that two mechanisms with
**nothing in common** reach the same registers, so any shortening that drops *why* they are
independent turns a proof into an assertion. Keep: that the JTAG side reads **two hardcoded absolute
addresses** while the board's side goes through **the vendor HAL's own device-ID accessor, which has
never heard of those constants**; and that **the second word is the one carrying the weight**,
because a wrong address there would still have yielded a plausible 64-bit value. The pair
`6fcddc36cb781b71` / `cb781b716fcddc36` is the evidence and is not re-derivable once the board is
unplugged. Keep the **negative** half too — that the DUT has **no self-report path at all**, so its
readback rests on the address rather than corroborating it, and that `nRF54L10`/`nRF54L05`/
`nRF54LM20A` share the arm with no silicon ever attached. **A compaction that keeps the confirmation
and drops its limits is strictly worse than leaving the file long**, because what remains reads as a
stronger result than was obtained.

Also keep decision 21's pre-existing statement that fallback registers come back **mismatch** rather
than **undeclared** — the one way that arm can be wrong — and decision 15's paragraph on what
enrolment structurally *cannot* catch ("right chip, wrong physical board"), which is the exact thing
this leg's three alert-log identity refusals show the validate-time gate catching.

**From `spec.md`'s "Where it stands":** that the mismatch path was exercised **without inducing
anything** — two physically different nRF54L15 DUT boards alternating on one probe serial — and,
separately, that **no agent can induce one**, because every route runs through `enroll`, which
overwrites the record the test needs, and there is no topology override on the store path — its only
variable being Windows' `ProgramData`, unsettable for an already-running service. **Do not shorten
that back to "the store path is compiled in"**: it was written that way on 2026-09-06 and is false on
the primary deployment platform, which a reviewer caught. That
second sentence exists to stop the next reader spending a leg looking for a way to fake a mismatch.
Keep the count (**three**, not six — the other three alerts are probe-not-attached and carry no live ID) and that each names both the recorded and the live ID.

## `spec.md` is not in reserve, it is at the wall

**10,239 of 10,240 bytes — one byte.** Leg 023 hit the hard cap twice writing this
unit and got under it by moving the alert log's end-to-end guarantee out to
`decisions/alerts.md` decision 12, where it belongs anyway, and then by deleting
two `**` from a phrase. **The next unit in this sub-project that writes one
sentence into `spec.md` will be refused**, not warned. Treat `spec.md` as the
first file to compact, not the second, and do not assume the reserve rules give
you room: they do not apply at the cap.

The relocation is worth knowing about so nobody re-adds it: the paragraph
explaining that `raise()` records the alert and builds the caller's error in one
function — so an alert row proves the caller got the refusal — now lives in
`decisions/alerts.md`, and `spec.md` cites decision 12 for it in one clause.

## Reserve line (supervisor, leg 024, measured at dispatch)

`check-doc-size.py --pressure` right now, for this sub-project only:

- `embarch-topology/spec.md` — **10,239 / 10,240, 1 byte left.** At the wall, not in reserve.
- `embarch-topology/decisions/enrollment.md` — 11,800 / 12,288, **488 bytes left.**
- `embarch-topology/decisions/alerts.md` — **PAID, 49.4%.** It is out of reserve and this task's
  `Compacts:` list still names it; **close that item and say so**, do not shorten the file further.

Nothing else in `embarch-topology` is in reserve. If your work spends the reserve in a file this
task does not already cover, file `tasks/topology/<NNN>-compact-topology.md` in the same commit
(`tasks/README.md` has the shape). Note the path is `tasks/topology/`, your own scope — not
`tasks/doc/`, which `check-ownership.py` refuses to a worker.

## The human question

Can `spec.md` alone answer what someone needs to work on `embarch-topology` today? Answer it in the
supervisor log in your own words — no script answers it and the gate does not either
(`DOC-COMPACTION-PASS.md`).

## Note on the likely shape

`decisions/enrollment.md` is 11,800 / 12,288 and holds five decisions (14, 15, 16, 20, 21), of which
**20 and 21 are both long bench narratives about the same event — the day the bench went back to
being an nRF54L15DK.** `DOC-COMPACTION.md` §2 names a **mission split** as the cheaper move where
one fits, and a split along "what enrolment records" versus "what live validation asserts" plausibly
does. Consider that before prose surgery.

## Done when

- [x] Both files are out of reserve, or a split has moved the content somewhere with room.
- [x] Every item on the **Must not delete:** list survives, verified against the pre-image rather
      than from memory.
- [x] `scripts/check-decision-refs.py` still resolves and no decision is renumbered.
- [x] The human question is answered in the log entry.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Outcome

**Method: mission split first, prose surgery second.**

`decisions/enrollment.md` split along the line §2 named. **Decision 21 moved
byte-for-byte** into a new `decisions/validation.md` — *what live validation
asserts* — leaving 14, 15, 16, 20 in `enrollment.md` as *what enrolment records*.
Nothing was restated, so the in-flux objection does not apply to that half, and
every **Must not delete:** item from decision 21 survives by construction:
verified `pre21.strip() == new21.strip()` against `git show
origin/main:embarch-topology/decisions/enrollment.md`, then re-verified needle by
needle in the post-image (both hardcoded absolute addresses, the vendor HAL
accessor that has never heard of them, the second word carrying the weight, the
`6fcddc36cb781b71` / `cb781b716fcddc36` pair, the DUT's absent self-report path,
the three unattached part numbers, and the fallback-registers-return-*mismatch*
limit). Decision 15's "right chip, wrong physical board" paragraph was not
touched at all.

`spec.md` was compacted by **choosing whole topics, not by vaguing sentences**.
Dropped: the `Win32_PnPEntity` two-probe measurement record, the `select`
code-path trace, and the CLI's before/after history — all of it either already in
decision 20 or cold under DOC-COMPACTION-PASS.md ("measurements · validation
records · the investigation log"), and all of it one `git log -p` away. Kept as
rules: role uniqueness, `guessed_among`'s meaning, that the declared *interface*
is the only thing separating `COM16` from `COM17` with the console on the
*higher* one, the failure signature (flashes, boots, runs, times out), and that
`guessed_among`'s trigger is an under-declared bench rather than a crowded one.
"What the consumers gave up" was rewritten as "What each consumer owns now" —
same facts, stated as current truth rather than as a migration.

**One §3 placement fix, not a byte shuffle:** "the declared *serial* path still
has no hardware evidence" moved out of `spec.md` into decision 17 in
`decisions/links.md`, where the declared-vs-fallback distinction is settled. A
reader of decision 17 is the one who would otherwise read the fallback's success
as the declared path's.

**Byte counts:**

| File | Before | After | % of cap |
|---|---|---|---|
| `embarch-topology/spec.md` | 10,239 | **8,913** | 87.0% |
| `embarch-topology/decisions/enrollment.md` | 11,800 | **7,868** | 64.0% |
| `embarch-topology/decisions/validation.md` | — (new) | 4,368 | 35.5% |
| `embarch-topology/decisions/links.md` | 9,995 | 10,390 | 84.6% |
| `embarch-topology/decisions.md` | 1,177 | 1,316 | 5.1% |

`decisions/alerts.md` — **item closed, not acted on.** It was already PAID at
49.4%; shortening it further would have been a compaction with no debt behind it.

`history/topology.md`'s link to decision 21 was repointed to
`decisions/validation.md` in the same commit, per the pass doc's rule that no
inbound link is left broken.
