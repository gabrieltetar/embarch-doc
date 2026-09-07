# 029 — embarch-umbrella's spec.md and open.md are back in reserve

**State:** claimed by agent/umbrella/029-compact-umbrella, 2026-09-06 19:06

## Doc-size reserve for `embarch-umbrella` (supervisor, leg 025)

Read this before you plan. `scripts/check-doc-size.py --pressure`, taken at dispatch:

- `spec.md` **9,237 / 10,240 B (90.2%)** — 1,003 B left. Yours to pay.
- `open.md` **4,653 / 5,120 B (90.9%)** — 467 B left. Yours to pay.
- `decisions/bind.md` **11,409 / 12,288 B (92.8%)** and `decisions/doctor.md`
  **11,346 / 12,288 B (92.3%)** — **not yours.** They sit behind
  [`009`](009-compact-docs.md), which stays `blocked` on `In flux: yes`. Do not
  compact them, and **do not use them as destinations** — moving prose into a file
  already 92% full is not a payment.
- Destinations with real room: `decisions/reporting.md` **8,920 / 12,288** and
  `decisions/schema-skew.md` **7,241 / 12,288**, as this task's own body says.

If your pass leaves any `embarch-umbrella` file in reserve that nothing has filed
against, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit
(`tasks/README.md` has the shape). Not `tasks/doc/` — `check-ownership.py` refuses
that path to every worker.

*Original state line follows.*

**State (before this claim):** open — **unblocked and mostly paid; it is a worker's now, not a bench unit's**

**No longer blocked.** The `In flux: yes` reason below was that `spec.md`'s `doctor` table was
being rewritten row by row and `open.md` held five bullets a single bench session could close or
rewrite. **That bench session ran** (`umbrella/027`, 2026-09-06): every check has a live verdict,
three of `open.md`'s bullets are settled or restated against measurement, and check 17's protocol has
moved to [`033`](033-settle-check-17s-two-fail-arms-against-a-real-narrow-bound-core.md). What is
left here is ordinary compaction. **`In flux:` is now `no`** for these two files;
[`009`](009-compact-docs.md) still owns `decisions/doctor.md` and `decisions/bind.md` and **stays
blocked** — do not read this as unparking it.

**What was paid, and what came back.** `umbrella/027` took `spec.md` **9,660 → 9,128 B** and
`open.md` **4,823 → 4,535 B**, both clear. **Its reviewer then found three clauses that outran what
the run measured, and correcting them cost the headroom back**: `spec.md` **9,237 B (90.2%)**,
`open.md` **4,653 B (90.9%)**. That is the honest trade and it is recorded rather than trimmed away
— the corrections were an unmarked inference in the durable doc, a sentence contradicting decision
33, and a restored scope statement the pass had dropped undisclosed. **~350 B of accuracy against
~350 B of headroom**, and a compaction pass that shaved them back out would be undoing the review.

**A worker running this needs ~600 B across the two files** and should look at
`decisions/reporting.md` (8,920 / 12,288) and `decisions/schema-skew.md` (7,241 / 12,288) as
destinations — both have room and both are the right mission for what is still in `spec.md`'s
check-table prose.

Paid inside the supervisor's bench unit `umbrella/027`,
per `supervise.md`'s rule that where a file in reserve sits behind a compaction task
blocked on `In flux: yes`, **the actor writing into it compacts it as part of its own
unit** — it is the only one that can shorten what it is rewriting without writing a clean
statement of something about to be wrong. That is exactly what happened: the live `doctor`
run made three of `open.md`'s bullets false, so shortening them was not a density pass, it
was reporting a measurement.

**How, so nobody looks for deleted content.** `spec.md`: the `--json` per-check field
enumeration and the message-shape rule's mechanism **moved** into
`decisions/reporting.md` (decision 43), where the reporting contract already lives, leaving
a rule and a citation; the "designed-and-unbuilt is not only the tail of the table"
paragraph merged into the sentence above it; two check rows dropped a restatement of the
general "a number it could not obtain is a warn" rule that the paragraph below the table
already states once. `open.md`: the decision-42 locator bullet **closed** (that run used
the wider locator and found a mixed install), the check-17 experiment protocol **moved** to
`tasks/umbrella/033`, and three bullets rewritten to what is now measured.

**Where `009`'s inherited clause went**, since this section exists so nobody hunts for deleted
content: `009`'s protected note that check 17's two Fail branches have never met a real
narrow-bound Core — **and which half of that debt each arm settles** — left `open.md` and now lives
in [`033`](033-settle-check-17s-two-fail-arms-against-a-real-narrow-bound-core.md), intact. The
debt dies when `033` runs. The `spec.md` scope sentence about `embarch-api`'s two front-ends was
dropped by the pass **undisclosed**, caught by the reviewer, and is **restored** in shortened form
in `spec.md`'s opening paragraph.

**Both `Must not delete:` items below survive**: `spec.md` still states the one-line /
no-multi-space rule and check 6's exemption is in decision 43 with the reason the exemption
is exactly one check, and `open.md` still carries checks 4 and 12 as a stated coverage gap —
now alongside the **larger** gap the live run exposed. [`009`](009-compact-docs.md) is
untouched and still owns `decisions/doctor.md` and `decisions/bind.md`; **it does not unpark
with this.**

**One placement forced by the cap, recorded rather than buried.** A new observation — that
check 14's `WslHost`/`Remote` arms cannot be reached on a set-up machine — went into
`tasks/umbrella/032` and **not** into `open.md`, because `open.md` had no room for it. That
is the reserve deciding placement, which this log has flagged for three legs. The task file
is a defensible home; it was not the one chosen on the merits.

---

*Original filing follows.*

**State (original):** blocked
**Source:** scripts/check-doc-size.py, spent by `umbrella/024`
**Scope:** umbrella
**Hardware:** none
**Compacts:** embarch-umbrella/spec.md, embarch-umbrella/open.md
**Owner:** no

## What

`umbrella/024` put both files back in reserve on 2026-09-06:

- `spec.md` **9,154 → 9,660 B (94.3%)**, 580 B left — one paragraph under the
  `doctor` table stating the shape of every `detail` and `fix` (one line, no run
  of two or more spaces), the one exemption, and that a module-wide test holds
  the pure judges to it.
- `open.md` **4,527 → 4,823 B (94.2%)**, 297 B left — one bullet: that guard
  cannot reach checks 4 and 12, because neither has a pure judge.

Both were paid out by `umbrella/023` two units earlier — [`009`](009-compact-docs.md)'s
items for them are closed and struck through, which is why this is a new task
rather than a line there. `009` still owns `decisions/doctor.md` and
`decisions/bind.md`, and its `In flux:` reason is the same one below.

**No ride-along was possible.** `spec.md` was at 89.4% before this unit wrote a
word, so any addition at all lands in reserve; `024` shortened both additions
once (spec 660 → 506 B, open 430 → 296 B) and neither shave changes that. What
it did not do is squeeze — the alternative was to say nothing in `spec.md` about
an invariant the code now enforces, which is how a guard ends up undocumented
and then deleted by someone who cannot see why it exists.

Run `scripts/check-duplication.py embarch-umbrella` first, the way `009` says.

## Why blocked

**In flux:** yes — same reason as `009`, unchanged by this unit. `spec.md`'s
`doctor` table is still being rewritten row by row: check 17's entry is owed a
live narrow-bound Core and an answer to whether `embarch-core install
--bind 0.0.0.0` rewrites an existing narrow registration, and `open.md` carries
five bullets that a single bench session could close or rewrite. Compacting now
means writing a clean statement of things about to change.

**Unparks with `009`.** These are the same two files under the same flux, and
paying them in separate passes would have the second pass re-reading what the
first just rewrote. Whoever runs `009` should run this.

## Must not delete

Everything on [`009`](009-compact-docs.md)'s `Must not delete:` list, verbatim —
this task does not restate it and does not narrow it. Added by `024`:

- **`spec.md`'s statement that a `detail`/`fix` is one line with no multi-space
  run, and that check 6 is the exemption.** It is the only place the rule is
  written down for a human; the test asserts it but cannot say why the exemption
  is exactly one check. Shortening it to "messages are one line" loses the part
  that matters — *why* a wrapped literal breaks silently.
- **`open.md`'s note that checks 4 and 12 are outside the guard.** It is a
  stated coverage gap, not a to-do. Deleting it makes the guard read as
  module-wide when it is not, which is the exact failure mode — a green test
  believed to cover more than it does — that this whole unit was about.

## Done when

- [ ] `spec.md` and `open.md` both out of reserve.
- [ ] The unbuilt/built distinction survives, per row (`009`).
- [ ] No question disappears from `collect-open-questions.py` unless you can
      name it as answered.
- [ ] `DOC-COMPACTION.md` §7's question answered in the commit message.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
