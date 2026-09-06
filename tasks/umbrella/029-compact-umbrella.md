# 029 — embarch-umbrella's spec.md and open.md are back in reserve

**State:** blocked
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
