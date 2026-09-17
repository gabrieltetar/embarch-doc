# 032 — Citation sweep: `app/src/`, the files `dev-bench/031` did not reach

**State:** claimed by agent/dev-bench/032-citation-sweep-app-src, 2026-09-16 22:03
**Source:** `dev-bench/031`, 2026-09-16. That unit swept `app/src/main.c` (1620 lines) and
`app/src/serial_protocol.h` (930 lines) — the two largest files by the chain's citation-line
census — decision-existence-and-sentence-truth, per-instance. It ran out of budget before the
rest of the tree. This names exactly what is left.
**Scope:** dev-bench
**Hardware:** none — C comments and doc-comments only, same classification as `dev-bench/031`.
**Comment-only.** If a fix needs anything but a comment, stop and leave this task `open` saying
so; that version of the work is `toolchain` and belongs in the main checkout.
**Owner:** no

## What is left, by `031`'s re-census (grep **line** counts,
`grep -cE '[Dd]ecisions? [0-9]'`, 2026-09-16 — a floor, not an instance count; `031` found
instance counts running ~40% higher than line counts on the two files it swept)

```
app/src/ble_bridge_real.c                 49
app/src/serial_protocol.c                 40
app/tests/serial_protocol/src/main.c      38
app/src/ble_bridge.h                      20
app/src/eap.h                              7
app/src/dev_bench_log.h                    7
app/tests/dev_bench_log/src/main.c         6
app/src/dev_bench_log.c                    5
README.md                                  5
app/src/study_ffi.h                        4
```

Take `ble_bridge_real.c` and `serial_protocol.c` first — the two largest of what remains.

## Method

Same as `dev-bench/031`: for each citation instance, (1) does the cited decision exist in the
repo the citation's form names — bare means `embarch-dev-bench`'s own, per
`DOC-CONVENTIONS.md`'s "Referring to a decision"; (2) read the cited decision's body and the
sentence around the citation — a resolving number is not evidence the claim holds; (3) check
every number in the cited sentence, not just the decision number; (4) check any `file:line`
suffix for drift.

## What `031` found, so this unit does not re-derive it

Two wrong-number defects, both fixed as comment-only edits in `031`:
- `main.c`'s "Inbound link RX" section header cited `decision 29` (the generic tap
  pipeline) for a section whose entire content — the FIFO-overflow/ISR fix, ~128-byte ceiling,
  ring buffer — is `decision 30`'s. Fixed to `decision 30`.
- `serial_protocol.h`'s `Hello`/`steps_crc` comment cited `embarch-study-designer` decisions
  "24/27" — decision 27 (`Sample` carries `unit`/`channel_id`) has nothing to do with `Hello`
  losing `steps_crc`; decision 24 alone supports the claim. Dropped the `/27`.

One label ambiguity found and **left alone** as a form question (`tasks/doc/055`/`tasks/ui/038`
territory, not `031`'s to settle): `embarch-dev-bench` and `embarch-study-designer` each have
their own decision 36 and their own decision 39, with unrelated content (chip-ID-in-HelloAck vs.
GATT capture windows; per-study log verbosity vs. the declared-tap model). Most citations of
these numbers in `main.c`/`serial_protocol.h` correctly carry the `embarch-study-designer` label
or sit close enough to one that the repo is unambiguous from context, but a few bare instances
of "decision 39" (main.c, the `transcript_tap_index` comment) and "decisions 31/32" (main.c,
`step_to_action` and its caller) sit far from any labeled anchor and read, under the bare-form
convention, as `embarch-dev-bench`'s own — which is the wrong repo's decision. Worth the same
check in whatever files this task covers: a same-numbered collision between the two repos is a
known failure mode here (`serial_protocol.h`'s own comment on schema v13 names it: "the two
repos' decision 39s collide by number... which is how `dev-bench/020` got it wrong on the first
pass").

One already-tracked stale claim, not re-filed: `serial_protocol.h:21-25`'s promise that the
hand-mirrored crate constants stay manual "until decision 8's west-module wiring lets this
firmware pull the constants directly" is false as written — decision 8 landed and does not do
that (its own text is explicit that it deliberately avoided west-module plumbing) — and this is
exactly `tasks/dev-bench/010`'s subject (open, unclaimed as of `031`). Nothing to add here.

## Done when

- [ ] `ble_bridge_real.c` and `serial_protocol.c` fully swept, every citation checked for
      existence, repo label, and sentence truth, counted as instances.
- [ ] Wrong numbers and false sentences reported as separate counts, with the total checked.
- [ ] Any `file:line` citation checked for drift.
- [ ] A follow-up task filed naming exactly which files remain (the six smaller ones above, if
      not reached), or a statement that `app/src/` and `app/tests/` are swept out.
- [ ] Mechanical checks green (grep gate zero, comment-block balance, 100-column limit,
      `check-client-names.py`), and the report says plainly that nothing was compiled.
- [ ] `changelog.d/dev-bench-*` fragment reporting the counts.

## Not yours

`history/dev-bench.md` is assembled from fragments.
