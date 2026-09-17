# 055 — Three `spec.md` guarantees `embarch-topology` does not actually provide

**State:** claimed by agent/topology/055-three-spec-guarantees, 2026-09-17 01:26
**Source:** leg 133's refill census of `embarch-topology`'s docs against its source. **Filed so they
survive**: they existed only in a census report, and `supervisor-log.md` folds daily and rolls into
`log-archive/`, so anything living there alone is on a timer. Nothing dispatches from a log entry.
**Scope:** topology
**Hardware:** none. All three are settled by reading Rust. **Do not attach a probe, do not enrol
anything, and do not run `validate` against a live machine** — item 1 is about what the identity gate
*would* conclude, not an observation of it, and `refuse_if_core_reachable` makes a live run
unavailable to an unattended leg anyway.
**Owner:** no

**Doc-size reserve for `topology`:** nothing of topology's is in reserve. Run
`python3 scripts/check-doc-size.py --pressure` before and after; if you push a file into the band,
file `tasks/topology/<NNN>-compact-topology.md` in the same commit.

**Every coordinate below came from a census pass and was read by that pass, not by me.** Re-derive
each line you act on and **correct the record in your report where it has drifted** — the previous
two census-sourced tasks in this fleet found the *shapes* exact and the line numbers off by 1–2.
**"This one does not hold" is a correct and welcome outcome for any of the three.**

Partial is acceptable and expected. If you reach only some, fix those and **file a follow-up task
naming exactly which remain**, the way this task names them.

## 1 — The identity gate is promised never to pass an undeclared chip; the code passes any chip on string equality

`spec.md` (reported line 82):

> *"**A same-chip link:** the board on the runtime link is the same silicon the JTAG probe verified,
> comparing its JTAG-read identity against its self-report. **Two chip families have a declared
> relation; every other chip returns *undeclared*, never a pass.**"*

The same promise sits on the function itself — `src/hardware/hardware_id.rs` (reported 195): *"Every
other chip returns [`SelfReportedIdentity::Undeclared`], which is **not** a pass: a comparison that
could not be made is not a comparison that succeeded."* — and `decisions/validation.md` 21 frames it
as the gate's founding rule.

**But `compare_self_reported` (reported 199–212) checks equality first** (reported 203–207):

```rust
// Equality is conclusive for any chip: two mechanisms agreeing on a
// factory-unique value is not a coincidence a wrong board can produce.
if self_reported.eq_ignore_ascii_case(jtag_read) {
    return SelfReportedIdentity::Match;
}
```

So **any** chip — including every chip with no declared relation — returns `Match` whenever the two
strings happen to agree case-insensitively. The declared-relation arms are the *fallback* for when
they differ.

**It is reachable, not theoretical.** `classify_chip` (reported ~105) has an `Stm32G0Uid` arm and
decision 25 records a real board enrolled off it. An STM32G0 has no arm in `compare_self_reported`,
so *per the doc* it can only ever come back `undeclared` — while in fact, if the self-report
hex-encodes the same UID words in the same order `read_words` does, it comes back `Match`.

**The judgement is yours and I want the reasoning.** The comment at the equality shortcut argues the
shortcut is deliberate policy, which suggests **the doc sentence is what should move**, in both
places plus decision 21's framing. Establish that from the code before you write it; if you instead
conclude the shortcut should be narrowed, that is a behaviour change on the suite's safety gate and
belongs in `inbox/` with your reasoning, **not** in this unit.

## 2 — "The displaced row is returned, not dropped" holds only for the first duplicate, and role uniqueness is a write-path rule rather than a store invariant

`spec.md` (reported line 69):

> *"**A role is unique.** Enrolling displaces any other board holding that role; the displaced row is
> **returned, not dropped** (decision 20)."*

`src/hardware/enrollment.rs`'s `upsert_at` (reported 196–211) disagrees with itself in cardinality —
`find` (one) versus `retain` (all):

```rust
let displaced = store.boards.iter()
    .find(|b| b.role == board.role && b.probe_serial != board.probe_serial)
    .cloned();

store.boards.retain(|b| b.probe_serial != board.probe_serial && b.role != board.role);
```

With two rows sharing a `role`, **both are deleted and only the first is returned**;
`src/hardware/validate.rs` (reported 457–468) then logs exactly one `tracing::warn!` naming one
displaced probe, so the second row vanishes with no record anywhere.

**That store state is the state decision 20 was written about** — *"moving a role onto different
silicon left two rows both claiming the same role"* — nothing de-duplicates on load (`load_at`,
reported 98–107, is a plain `toml::from_str`), and `find_by_role`'s own doc comment (reported 147)
says the violation is tolerated by design: *"More than one entry sharing `role` returns the first (by
file order) rather than erroring — a soft, best-effort lookup."*

**Two distinct costs, and the fix should address both or say why not.** The flat claim *"a role is
unique"* reads as a store invariant when it is only a write-time rule, so a consumer reasoning *"role
lookups are unambiguous"* is reasoning from the wrong premise — which is the downstream damage
decision 20 catalogues. And the *"returned, not dropped"* guarantee exists so enrolment can say out
loud that one board replaced another; on a hand-edited or pre-2026-08-31 `enrollment.toml` the
operator is told one board was replaced while two records were deleted, a silent loss in the one path
the guarantee was added to make loud.

**Before you decide this is a doc fix, check whether anything anywhere de-duplicates the store** —
the census found nothing in this crate and `find_by_role`'s comment argues nothing does. Say which
way you checked.

## 3 — `spec.md` says only declared intent persists, and the crate also writes a durable alert log

`spec.md` (reported line 52):

> *"**The only state that persists anywhere is a human's declared intent, inside the crate.**
> Consumers call functions and **never parse a topology file directly.**"*

`src/hardware/alert.rs`'s `record` (reported 87–104) appends unconditionally to
`paths::alert_log_path()` — `<machine_data_dir>/topology/alerts.jsonl` (`src/hardware/paths.rs`,
reported 29–42) — and `paths.rs`'s own header names both files. **`spec.md` contradicts itself inside
one file**: its Shape block (reported 30–37) lists the durable alert log as something the crate owns,
and `decisions/alerts.md` 12 makes that log's durability load-bearing.

**What it costs.** Anyone acting on line 52 — resetting a bench's topology state, deciding what to
back up or gitignore, sizing a fresh machine, reasoning about what write permissions Core's service
account needs — accounts for `enrollment.toml` and misses `alerts.jsonl`, which grows unboundedly
(`record` only appends; `recent` trims at read time, reported 108–130, never on disk).

**This is the weakest of the three and it may be a qualifier rather than a defect.** A charitable
reading takes line 52 to mean *"the only persisted **input**"* — nothing persisted is ever consulted
as a source of truth for resolution. **Decide which reading the sentence should carry and say so**;
shrinking this to a one-clause qualifier is a legitimate outcome, and so is concluding the sentence
is fine as written.

## Done when

- [ ] Each of the three is either **fixed** or **reported as not holding**, with the evidence, one by
      one.
- [ ] Nothing is "fixed" on the strength of this task's own description. Every change rests on a line
      you read.
- [ ] Item 1's outcome states explicitly whether the doc moved or the code did, and why — and if the
      doc moved, **all three sites** (`spec.md` 82, `hardware_id.rs`'s doc comment, decision 21's
      framing) are consistent afterwards, not just the first one found.
- [ ] Item 2 says whether anything de-duplicates the store, and how that was checked.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      in `embarch-topology`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

**Do not change the identity gate's behaviour** (item 1) and **do not add store de-duplication or
migration** (item 2). Both are behaviour changes to the suite's hardware-identity safety property,
which is the one thing enrolment exists to guarantee; a doc that overstates a guarantee is a smaller
problem than a guarantee that changed without hardware to exercise it. If you conclude code must
move, drop it in `inbox/` (absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/`) with your
reasoning.

**Do not write a new numbered decision.** Items 1–3 are corrections restating what the code always
did, which record no choice. Amending an existing decision (21 or 20) to match shipped behaviour is
in scope; authoring a new numbered one is not — if you think one is genuinely needed, drop it in
`inbox/` instead.

### Also found by the same census, filed separately — do not do it here

`tasks/topology/056` carries a fourth finding: `validate`'s probe-*open* failure produces neither a
`TopologyMismatch` nor an `alerts.jsonl` row, which the type's own doc comment claims it does. Leave
it alone.

### Claims the same census checked and found the code honours — do not re-sweep these

Recorded so this unit does not re-spend budget. **Second-hand, so do not cite them as verified
either** — they are "nobody found a problem here", not "proven correct": the
`wire`/`software`/`hardware` feature split and its six named wire types; `validate_serial_timed` /
`validate_role_timed` beside unchanged `validate_serial` / `validate_role` (decision 26); all three
`select_probe` behaviours and decision 33's quoted error strings, verbatim; `ExcludingRule`'s four
variants and their remedies including the WSL2 zero-ports lead-in (decision 27); `guessed_among`
being triggered only by the lowest-interface rule and not by a crowded bench; signal mismatches
deliberately not reaching `alerts.jsonl`; `Direct` versus `ViaDevBench` validation semantics;
`classify_chip`'s ordering, its nRF54H `None` and the narrow `stm32g0` prefix (decision 25); the
absence of any topology-shaped env var (only `ProgramData` and `WSL_DISTRO_NAME`, decisions 2/3/9);
and the CLI's `refuse_if_core_reachable` gating enroll/validate/set-dev-bench-link (decision 28).
