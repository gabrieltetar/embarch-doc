# 032 — Citation sweep: `app/src/`, the files `dev-bench/031` did not reach

**State:** done
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

- [x] `ble_bridge_real.c` and `serial_protocol.c` fully swept, every citation checked for
      existence, repo label, and sentence truth, counted as instances.
- [x] Wrong numbers and false sentences reported as separate counts, with the total checked.
- [x] Any `file:line` citation checked for drift.
- [x] A follow-up task filed naming exactly which files remain (the six smaller ones above, if
      not reached), or a statement that `app/src/` and `app/tests/` are swept out.
- [x] Mechanical checks green (grep gate zero, comment-block balance, 100-column limit,
      `check-client-names.py`), and the report says plainly that nothing was compiled.
- [x] `changelog.d/dev-bench-*` fragment reporting the counts.

## Report

Re-derived the census as grep **instances** (`-o`), not the line-count floor `031` handed off:
`ble_bridge_real.c` 55 lines / **56 instances**, `serial_protocol.c` 44 lines / **44 instances**
(one line carries two citations) — both noticeably above the line-count floor, consistent with
`031`'s "~40% higher" observation holding again here (this pair ran closer to +14%/+10% by line
count, but the floor-vs-instance gap is the same shape).

**5 wrong decision numbers fixed:**
- `ble_bridge_real.c`: `decision 29`→`30` (the FIFO-overflow ring buffer is decision 30's, not the
  generic inbound-pipeline decision 29 — the same collision `031` fixed once in `main.c`, found
  again here).
- `ble_bridge_real.c`: `decision 43`→`32` (the scan filter's *exact-match* rule is dev-bench's own
  decision 32; decision 43 is `embarch-study-designer`'s — correct only for the wire field's
  *existence*, not this firmware's matching behaviour).
- `ble_bridge_real.c`: bare `decision 34`, in a four-decision list about a study silently passing
  with nothing captured, was dev-bench's own decision 42 (the whole-study-tap-never-closed bug) —
  the other three in the list (36, 53, 54) are `embarch-study-designer`'s and were also missing
  their repo label, now added.
- `serial_protocol.c`: `decision 50`→`44`, twice (encoder and decoder), for the
  `security_level: Option<SecurityLevel>` field — decision 50 is `BleUnbond`; decision 44 is
  `BleSecurity { level }`, confirmed by `main.c` already citing 44 correctly for the same field.

**4 false/unsupported sentences fixed (citation resolved, content did not hold):**
- `ble_bridge_real.c`'s header claimed this file is "built by workspaces/nordic/" — false since
  decision 26: `ble_bridge_real.c` also builds unchanged under `workspaces/espressif/`. Reworded to
  name both, framed as decision 16's stub/real split rather than a specific workspace.
- `ble_bridge_real.c` attributed "~96% SRAM" to "decision 27's own finding" — decision 27 states a
  25 KB overflow, no percentage, and no recorded figure anywhere in this repo's decisions is 96%
  (87.04%, 87.83%, 90.87%, 98.5% are the ones on record). Reworded to cite the two real overflow
  decisions (27's 25 KB, 40's 37 KB) without inventing an unverifiable percentage.
- `ble_bridge_real.c` cited "decision 16's own doc comment" for the file's own opening paragraph
  about `deadline`/`timeout_ms` — decision 16 is the native_sim/stub split and says nothing about
  timeout semantics; that paragraph carries no decision number of its own. Reworded to point at
  this file's own header instead of a decision that doesn't cover it.
- (counted above) the missing `embarch-study-designer` labels on decisions 36/53/54 in the
  four-decision list.

**No `file:line` citations exist in either file** (checked via `grep -nE '\.[ch]:[0-9]+'`) — nothing
to check for drift there.

**Toolchain debt, restated, not re-verified:** no `Cargo.toml` in this repo, no `west`/Zephyr SDK in
this sandbox — `cargo build`/`test`/`clippy` select nothing here and neither a `native_sim` build nor
the `app/tests/serial_protocol` ztest suite was built or run. Verified instead: the grep gate (zero
matches for anything client-identifying), comment-block balance (`/*`/`*/` depth returns to 0 in
both files), the 100-column limit (no line over 100 columns in either file), and
`check-client-names.py --repo <code worktree>` (clean against all 7 denylist entries).
`check-decision-refs.py` also passes (all 2163 references resolve after the edits).

Follow-up filed: `tasks/dev-bench/033-citation-sweep-remaining-eight-files.md`, naming the eight
files `031`'s census still lists and handing off the `security_level`/decision-50 defect already
confirmed to repeat in `app/tests/serial_protocol/src/main.c` (lines 981, 1479).

## Not yours

`history/dev-bench.md` is assembled from fragments.
