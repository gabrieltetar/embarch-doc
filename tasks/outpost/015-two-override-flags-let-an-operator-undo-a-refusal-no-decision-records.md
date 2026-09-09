# 015 — Two override flags let an operator undo a refusal that a numbered decision states unconditionally, and neither override is recorded anywhere

**State:** done — leg 061, worker on `agent/outpost/015-override-flag-decision`

**Dispatch note (supervisor, leg 061):** normal leg, not burndown — authoring the numbered
decision is in scope and is the point. **Doc-size reserve for `outpost`:**
`embarch-outpost/spec.md` 9,791/10,240 B (449 B left) filed against
`tasks/outpost/014-compact-outpost.md`, and `embarch-outpost/decisions/tracing.md`
7,408/8,192 B filed against `tasks/outpost/008`. Neither is blocked. `decisions/clocks.md` and
`decisions/manifest.md` — the two files this task is actually about — are **not** in reserve, so
write there. If you amend `spec.md:60`, keep it at or below its current length; if you spend
reserve, file `tasks/outpost/<NNN>-compact-outpost.md` in the same commit.

**Do not build or run the Zephyr `tests/unit` suite** and do not claim it green — no leg can, this
environment has no `west` and no `ZEPHYR_BASE`. That is a standing debt, not your unit's failure.
**Source:** `embarch-reviewer` on unit `outpost/005` (code `81cbba2`, doc `dab753a`), filed from `inbox/outpost-decision-18-escape-hatch-gap.md` by the supervisor, leg 058
**Scope:** outpost
**Hardware:** none
**Owner:** no

## What

`embarch-outpost` now has **two** operator flags in `scripts/decode_outpost.py` whose whole purpose
is to proceed past a refusal that a numbered decision states with no carve-out:

- **`--allow-unverified-join`** stamps `rx_utc_ms` anyway after the arrival join fails verification.
  `decisions/clocks.md` decision 18 says *"when neither fits, nothing is stamped and the stream
  index says why"* — unconditionally. The flag is new, landed by `outpost/005`.
- **`--allow-build-id-mismatch`** renders anyway after the manifest's build ID disagrees.
  `decisions/manifest.md` decision 9 is the analogous unconditional refusal, and `spec.md:60` states
  it as *"a mismatched manifest refuses to render the names"*. The flag is older and pre-dates this
  task.

**Neither flag appears in the text of the decision it overrides**, and neither has a decision of its
own. So each decision, read on its own — which is exactly how they are read, since `spec.md` and the
decisions tree are the two entry points — commits this project to a refusal that the shipped tool
lets an operator decline. The gap is a record gap, not a code bug: the refusal mechanism itself
matches its decision faithfully in both cases, and the reviewer verified that for the arrival join
line by line.

## Why now

`outpost/005` landed under leg 058's burndown constraint, which forbids a unit from authoring a new
numbered decision. That constraint is right — a decision is the most expensive thing in this suite to
reverse and burndown optimises for volume — but its cost here is visible and worth naming: the unit
made a genuine design choice (*may an operator force the exact stamp decision 18 says a host
refuses?*) and had nowhere to put it, so the choice landed in `spec.md` prose, `README.md` and a
changelog fragment. **The reviewer's own reasoning is the reason this is a task and not a shrug**: it
checked whether the practice was merely established, found that `--allow-build-id-mismatch` has the
identical gap, and correctly reported that this weakens the case for a contradiction without closing
the gap.

Filing both flags in one task is deliberate. Fixing them one at a time is how a suite ends up with
two overrides recorded two different ways, which is the defect `outpost/009` spent a whole unit
undoing on 2026-09-08.

## What the answer probably is, without pre-deciding it

The honest reading is that these two flags are one posture, not two accidents: *a refusal protects
the reader from a plausible-and-wrong rendering, and an operator who knows the capture's provenance
may accept that risk explicitly, at the command line, once, per invocation.* If that is right, the
cheapest correct shape is **one numbered decision naming the posture and both flags**, rather than
two decisions or two amendments — and then `spec.md:60` and `:61` cite it instead of citing the
decisions the flags override. But that is the judgement this task exists to make, not a conclusion
it should be dispatched with.

Note that `spec.md:61` as landed is **already honest** — it says the flag "stamps anyway, mirroring
`--allow-build-id-mismatch`'s posture toward decision 9", which describes the gap rather than
papering over it. The inaccurate claim was in `outpost/005`'s commit message ("decision 18 already
covers the design"), which is not a document anyone reads for truth. **So nothing currently on disk
needs correcting; something needs adding.** Do not "fix" `spec.md:61` by deleting that clause.

## Done when

- [x] The choice to let an operator override each refusal is recorded as a numbered decision — one
      covering both flags if they are one posture, and if they are not, the reason they are not is
      the part that gets written down.

      **Decision 23**, in `decisions/manifest.md` (both flags live in `scripts/decode_outpost.py`
      and manifest.md already hosted decision 9, the analogous refusal for one of them): one posture
      — explicit, command-line, once per invocation, never a config default — covering both
      `--allow-build-id-mismatch` and `--allow-unverified-join`. `decisions/clocks.md` decision 18
      and the `decisions.md` index both cross-reference it.
- [x] Whatever `spec.md:60` and `:61` cite is accurate afterwards: a reader who follows the citation
      lands on text that mentions the flag.

      Line 60 (manifest mismatch) now names `--allow-build-id-mismatch` and cites decision 23 — it
      previously named neither. Line 61 (unverified join) already named both flags; added the
      decision 23 citation.
- [x] `decisions/clocks.md` 18 and `decisions/manifest.md` 9 are consistent with the new decision —
      amended to name the carve-out, or left alone with the new decision naming them, but **not
      left stating an unconditional refusal that the tool does not implement.**

      Left decision 9 and decision 18's own text alone (they still state the refusal correctly for
      the no-flag case) and added one cross-reference sentence to each pointing at decision 23,
      which is where the carve-out is actually named.
- [x] **No code change.** Confirmed — `git diff --stat` against the code worktree shows nothing under
      `scripts/decode_outpost.py` or `src/`; this unit touched `embarch-doc` only.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). See report: `cargo build/test/clippy` clean
      in the code repo (no Zephyr `tests/unit`, standing debt); `check-docs.py`,
      `check-client-names.py`, `check-ownership.py` clean in the doc repo.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.

      `spec.md` and `decisions.md` updated (above). `open.md` needed no change — nothing there
      described either flag or referenced decision 9/18 as unconditional. No `status.d/` fragment:
      this is an outpost-internal record gap with no suite-level fact made false — nothing outside
      `embarch-outpost` cites decision 9 or 18's refusal as unconditional (checked via grep across
      the doc tree).

## Doc-size note for whoever takes this

`embarch-outpost/spec.md` is at **9,515/10,240 B** and in reserve, filed against
`tasks/outpost/014-compact-outpost.md` (state `open`, not blocked).
`embarch-outpost/decisions/tracing.md` is at **7,408/8,192 B**, filed against `tasks/outpost/008`.
Neither `decisions/clocks.md` nor `decisions/manifest.md` was in reserve as of 2026-09-09 — check
before you write, because a new decision is an addition and this is a sub-project with two files
already inside their last 10%.
