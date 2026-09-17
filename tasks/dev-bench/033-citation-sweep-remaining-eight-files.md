# 033 — Citation sweep: the eight files `032` did not reach

**State:** claimed — leg 129, 2026-09-16.
**Source:** `dev-bench/032`, 2026-09-16. That unit fully swept `app/src/ble_bridge_real.c` (56
instances) and `app/src/serial_protocol.c` (44 instances) — decision-existence, repo-label and
sentence-truth, per-instance — and fixed 5 wrong decision numbers plus 4 false/unsupported
sentences. It ran out of budget before the rest of the tree. This names exactly what is left.
**Scope:** dev-bench
**Hardware:** none — C comments and doc-comments only, same classification as `dev-bench/031`/`032`.
**Comment-only.** If a fix needs anything but a comment, stop and leave this task `open` saying
so; that version of the work is `toolchain` and belongs in the main checkout.
**Owner:** no

## What is left, by `031`'s re-census (unchanged by `032`, which did not touch these files)

```
app/tests/serial_protocol/src/main.c      38
app/src/ble_bridge.h                      20
app/src/eap.h                              7
app/src/dev_bench_log.h                    7
app/tests/dev_bench_log/src/main.c         6
app/src/dev_bench_log.c                    5
README.md                                  5
app/src/study_ffi.h                        4
```

`032` measured its own two files by grep **instance** count (`-o`, not `-c`) rather than trusting
`031`'s line-count floor, and found both noticeably higher than the line-count census implied:
`ble_bridge_real.c` 55 lines / **56 instances**, `serial_protocol.c` 44 lines / **44 instances**
(one line there carries two citations). Re-derive the same way for these eight rather than
trusting the line counts above as instance counts.

## A head start: one defect already found to repeat here

`032` found `serial_protocol.c` citing **`embarch-study-designer` decision 50** (BleUnbond) twice
for the `security_level: Option<SecurityLevel>` field, which is actually decision **44**
(`Action::BleSecurity { level }` — ble.md) — confirmed by cross-checking `main.c`, which already
cites decision 44 correctly for the same field. The identical wrong-number defect is **already
present in `app/tests/serial_protocol/src/main.c`**, at least at two sites:

```
app/tests/serial_protocol/src/main.c:981   (`embarch-study-designer` decision 50), None here --
app/tests/serial_protocol/src/main.c:1479  exact silent degradation decision 50 exists to refuse, which is why
```

Read both in full context before fixing — `1479`'s sentence ("exact silent degradation... exists
to refuse") is the same silent-degradation argument ble.md decision 44 makes for `BleSecurity`
itself, so this is very likely the same 50→44 fix, but confirm against the surrounding code (is it
really about `security_level`, and not a genuine `BleUnbond` reference that happens to sit near the
word "degradation") before changing it.

## Method

Same as `dev-bench/031`/`032`: for each citation instance, (1) does the cited decision exist in the
repo the citation's form names — bare means `embarch-dev-bench`'s own, per
`DOC-CONVENTIONS.md`'s "Referring to a decision"; (2) read the cited decision's body and the
sentence around the citation — a resolving number is not evidence the claim holds; (3) check every
number in the cited sentence, not just the decision number; (4) check any `file:line` suffix for
drift. Carry `study-designer/056`'s method too: a citation can resolve, be current, be correctly
labelled and still be wrong, if a nearer same-repo decision already says the thing.

**The known collision to keep checking for:** `embarch-dev-bench` and `embarch-study-designer` each
have their own decision 36 and their own decision 39 (unrelated content), and a bare number far from
any labeled anchor reads, under the bare-form convention, as `embarch-dev-bench`'s own — which can
be the wrong repo's decision. `032` found this exact shape twice in ways worth re-checking for in
these eight files:

- A citation naming a *wire-field's existence* decision (correctly `embarch-study-designer`, e.g.
  decision 43 for `BleConnect.target_name` existing at all) versus a citation naming *this
  firmware's own implementation choice* about that field (correctly `embarch-dev-bench`'s own
  decision, e.g. decision 32 for the exact-match scan filter) are different decisions even when the
  same field is being discussed one paragraph apart. `032` found `ble_bridge_real.c` citing decision
  43 (study-designer) where the sentence was actually describing dev-bench's own decision 32's
  exact-match rule.
- A percentage or measurement stated as "decision N's own finding" is not automatically true just
  because decision N is topically nearby — `032` found a `~96% SRAM` figure attributed to a decision
  that only ever stated a `25 KB` overflow amount, with no percentage anywhere in the corpus matching
  96% (the closest recorded figures are 87.04%, 87.83%, 90.87%, 98.5%, none of them 96%).

## Done when

- [ ] All eight files fully swept, every citation checked for existence, repo label, and sentence
      truth, counted as instances.
- [ ] The `app/tests/serial_protocol/src/main.c:981`/`:1479` decision-50→44 candidates confirmed or
      corrected.
- [ ] Wrong numbers and false sentences reported as separate counts, with the total checked.
- [ ] Any `file:line` citation checked for drift.
- [ ] A statement that `app/src/` and `app/tests/` are swept out, once these eight are done — no
      further follow-up task needed unless this one also runs out of budget.
- [ ] Mechanical checks green (grep gate zero, comment-block balance, 100-column limit,
      `check-client-names.py`), and the report says plainly that nothing was compiled.
- [ ] `changelog.d/dev-bench-*` fragment reporting the counts.

## Not yours

`history/dev-bench.md` is assembled from fragments.
