# 045 — Comments in `embarch-topology`'s enrolment trio that state an invariant the code may not implement

**State:** done — leg 116, 2026-09-16; see "Closed" at the bottom. Zero-defect sweep — no source
change, nothing to fold in `embarch-topology`.
**Source:** refill sweep, leg 116, 2026-09-16 — from
[`embarch-decision-reversals.md`](../../embarch-decision-reversals.md)'s **shape 8, "the comment
names the right invariant; the code does not implement it"** (rows 100, 101, 102, 104). That shape is
the page's own statement of an unclosed pattern: **three of its four instances were found in a single
pass**, one had a test *asserting the loss as intended behaviour*, and the page's own diagnosis of why
they survive is the line to carry into this sweep — *"it names a class it does prevent, which reads as
though it had considered the space."* Nothing has run that pass over `embarch-topology`.
**Scope:** topology
**Hardware:** none — this is reading Rust source and its comments against each other, plus `cargo
test`. **No board, no probe, no live Core, no `validate`, no enrolment performed.** Do not run
`embarch-topology validate` or any CLI subcommand that touches hardware; if a question can only be
settled by attaching a board, that is a finding to report, not a thing to do.
**Owner:** no

**Doc-size reserve for `topology`: nothing.** No `embarch-topology/` doc is in reserve — you have
full headroom in all of them. (For contrast, five other sub-projects are in reserve right now.) If
your work somehow pushes one *into* reserve, file
`tasks/topology/046-compact-topology.md` in the same commit per `tasks/README.md`.

## Why this repo, and why these three files

`embarch-topology` is a **shared crate**: `embarch-api`, `embarch-core`, `embarch-ui` and
`embarch-umbrella` all path-depend on it. A comment here that promises a guarantee the code does not
keep is read by four repos' worth of callers, and this repo has already produced exactly this defect
once — `tasks/topology/020`, *"crate.md decisions 4 and 8 claim a uniqueness the crate cannot
enforce"*, now closed. So the class is proven present here, not hypothesised.

**Read these three files, in this order, and nothing else:**

| file | lines | why it is first |
|---|---|---|
| `src/hardware/hardware_id.rs` | ~555 | identity — the thing enrolment exists to pin |
| `src/hardware/enrollment.rs` | ~515 | the write side of that pin |
| `src/hardware/validate.rs` | ~570 | the read side that is supposed to refuse a mismatch |

~1,640 lines. **That bound is deliberate** — `src/` is 4,612 lines and a sweep that skims all of it
finds less than one that reads a third of it properly. The trio is chosen because the suite's single
most expensive documented hardware failure mode is *"a bench that flashed, booted, ran, and timed
out"* after a mismatch was papered over, and these three files are where that is meant to be
impossible.

## What you are looking for — and what you are NOT

**Looking for:** a comment (`//`, `///`, `//!`, or a `#[doc]`) that states something the code around
it is supposed to guarantee, where reading the code shows it does not. Concretely:

- A comment naming a class of input it rejects, where the rejection sits on only one arm of a `match`,
  behind an `if` that the other path skips, or after an early return.
- A comment saying two things "must" or "always" agree — a constant mirrored elsewhere, a field and
  its serialized name, an ID and its source — where **nothing in the code compares them**
  (reversals shape 4: *"a note describing a gap is not a mechanism for closing one"*).
- A `///` on a public function whose stated contract is stronger than what the body enforces —
  especially a claimed uniqueness, a claimed non-empty, or a claimed "never `None` here".
- A comment describing behaviour that was **true when written and was later moved or retired**
  (reversals shape 9). `git log -L` or `git blame` on the surrounding lines settles this cheaply.
- **A test that asserts the wrong behaviour as intended.** Row 102 is exactly this, and it is the
  hardest one to see, because a green test reads as evidence.

**NOT looking for:** citation numbers. `tasks/topology/036` already swept this repo's source comments
for dead decision references and closed. **Do not re-run that sweep**, do not "fix" a citation you
happen to pass, and if a citation looks wrong, note it in your report as a by-catch for a future task
rather than changing it — a citation fix inside this diff makes the shape-8 findings harder to review.

## How to report, and the discipline that matters most here

**Report a number, and report it red if it is red.** The immediately preceding legs have produced
several zero-defect sweeps, and the honest open question — raised independently by `ui/049` and
`umbrella/066` — is whether that means the corpus is clean or whether sweeps have converged on easy
files. **This sweep's value is the same whether it finds four defects or zero, but only if the zero is
trustworthy.** So:

- State **how many comments you read that make a checkable claim**, and how many of those you actually
  traced into the code. Those are two different numbers and the second is the real one.
- A comment you could not settle is **`unsettled`, named with its line number** — never rounded to
  "clean". `umbrella/066` reported 114/0 where the honest answer was 113/1, and `api/095` is the
  counter-example worth copying: it refused to resolve one citation either way and said so.
- If you find nothing, say **"0 findings in N traced claims"** and list the N. Do not pad the diff.

## Fix what you find, within scope

For each real finding, **change the side that is wrong**, and say in the commit message which side you
chose and why:

- Comment overstates what the code does, and the code is right → **fix the comment**, and make it name
  the narrower class truthfully rather than deleting the sentence.
- Comment states the intended invariant and the code genuinely does not implement it → **do not
  silently implement it.** That is a behaviour change in a crate four repos depend on. Write the
  comment down to what is true *and* file `tasks/topology/046-<slug>.md` describing the gap, so the
  real fix is a task somebody chooses rather than a side effect of a comment sweep.
- If a decision in `embarch-topology/decisions/*.md` is the thing that is wrong, **stop** — amending a
  decision is not this task's scope. Report it and it becomes its own unit.

## Done when

- [x] All three files read end to end; the two counts above stated explicitly in your report.
- [x] Every finding either fixed in this diff or filed as a follow-up task, with no third category.
      (0 findings — nothing to fix or file.)
- [x] `cargo build` / `cargo test` / `clippy --all-targets -- -D warnings` green in
      `embarch-topology`.
- [x] A `changelog.d/` fragment written for this repo if anything changed; none if nothing did.
      (Nothing changed — none filed.)
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## Closed 2026-09-16, leg 116

**53 comments read that make a checkable claim about current code behaviour. 22 traced into the
code and confirmed true. 4 left `unsettled` (named below, with line numbers — not rounded to
clean). 27 were rationale/history/citation-number text excluded per this task's own scope (`git
blame`-style "why," or a `decision N`/`task NNN` reference — `topology/036` already swept those and
closed) rather than a present-tense guarantee about what the code does. 0 findings in the 22 traced
claims.**

Read in the stated order, end to end: `hardware_id.rs` (555 lines), `enrollment.rs` (515 lines),
`validate.rs` (570 lines).

### The 22 traced claims (all confirmed true)

`hardware_id.rs`:
1. `classify_chip` checks `nrf54h` before `nrf54l` before the classic `nrf5`/`nrf9` prefix (:98-104)
   — traced: an nRF54H name would otherwise fall through to the classic arm (`"nrf54h".starts_with("nrf5")`
   is true), and the comment's claim that it's checked first, deliberately, to prevent that is exactly
   what the `if`/`else if` chain does.
2. Unrecognized chip returns `None`, "a named error, never a guess" (:92-113) — traced, the `else` arm.
3. `SelfReportedIdentity`'s four variants' stated semantics (:146-159) match what `compare_self_reported`
   actually returns for each (:199-222) — traced arm by arm.
4. `compare_self_reported` only has declared arms for `esp32c5` and the two Nordic `ChipFamily`
   variants, everything else `Undeclared` (:171-198, :208-211) — traced.
5. `is_nordic_deviceid_chip` is derived from `classify_chip` rather than re-matching, so it can't
   drift from `read`'s own arms (:225-237) — traced, it's a `matches!` on `classify_chip`'s output.
6. `nordic_expected_self_report`'s byte-swap relation and the "confirmed live 2026-08-31" pair
   (`6fcddc36cb781b71` / `cb781b716fcddc36`) (:239-277) — traced: swapping the two 8-hex-digit halves
   of the first string produces the second, exactly, and the file's own test at :343 asserts the same
   pair.
7. `esp32c5_expected_self_report`'s bit-shift relation (:279-297) — traced by hand-computing the
   claimed shifts against the file's own `esp32c5_pair` test helper (:399-414) and its asserted
   output `"9abc12345678"` (:421) — the arithmetic matches.
8. `read_words`' widening-is-compatible claim (:300-318) — traced: a two-word slice through the
   widened loop produces the same output the old two-word-only version did.
9. `requires_vendor_tool` in `embarch-core`'s `flash_backend.rs` "matches `nrf54h` as well" (:71-72,
   a cross-repo claim) — traced against the real git checkout at
   `/home/gabriel/Github/embarch/embarch-core/src/flash_backend.rs:124`:
   `c.starts_with("nrf54l") || c.starts_with("nrf54h")` — true.
10. `open.md` "records that `nRF54L10`/`nRF54L05`/`nRF54LM20A` take this same arm with no silicon
    ever attached" (:189-192) — traced against `embarch-topology/open.md`, which states this
    verbatim.

`enrollment.rs`:
11. `upsert`'s role-uniqueness fix (:162-184, the row-104 fix `topology/020` already closed) —
    re-traced against the current `retain` (:205-207): removes any board sharing `probe_serial` *or*
    `role*, so at most one board can hold either afterward. Matches the file's own
    `upsert_moves_a_role_to_a_new_probe_and_reports_the_displaced_board` test.
12. `amend`-based `set_link_port_serial`/`set_link_port_interface`/`clear_link_port_serial`/
    `clear_link_port_interface` all require a pre-existing role (:213-253) — traced, `amend` (:257-267)
    returns `Err` via `with_context` when no board matches `role`.
13. `find_by_role` returns the first match by file order, not an error, on a duplicate role
    (:142-149) — traced, plain `.find()` on the `Vec` in load order.
14. `link_port_serial`/`link_port_interface` are consumed by `port::Filter::resolve`, and
    `port::select`'s "lowest interface" fallback only applies when undeclared (:35-70) — traced with
    a targeted grep of `port.rs` (not a full read, per this task's file bound): `Filter::resolve` at
    `port.rs:349` reads both fields, and `select` at `port.rs:431` has the lowest-interface guess
    with the "GUESSING the lowest interface index" message at `:546`.
15. `hardware_id` field is "the probe-read (JTAG) hardware ID — not the bench's self-reported one"
    (:30-32) — traced, the only writer is `hardware_id::read`'s result in `validate::enroll` (:424).

`validate.rs`:
16. Module doc: "fails closed in every branch" and "every mismatch is durably logged... before the
    structured error is even constructed" (:8-11) — traced through `validate_known_timed` (:211-262):
    every `TopologyMismatch`-producing path goes through `raise()` (:145-161), which calls
    `alert::record` before constructing the `anyhow::Error`.
17. Module doc: "no second, independently-reasoned copy of this logic anywhere in the suite" (:1-6)
    — traced (cross-repo) against the real `embarch-core` checkout: `hardware.rs:171,305` and
    `study.rs:889` call `embarch_topology::hardware::validate_serial`/`validate_role` directly, no
    reimplementation.
18. "That gap is closed as of 2026-08-25... `HelloAck` now carries dev-bench's self-reported chip
    ID... this crate supplies the piece that makes it usable" (:24-34) — traced (cross-repo):
    `embarch-core/src/study.rs:784-816` calls `compare_self_reported` and refuses the handshake on
    `Mismatch`.
19. `enroll`'s doc: "as of `embarch-core` decision 61, [`resolve_probe`] delegates to
    [`select_probe`]... Decision 32 is closed; no selection-rule copy remains in either crate"
    (:382-395) — traced (cross-repo) against `/home/gabriel/Github/embarch/embarch-core/src/hardware.rs:92-99`:
    `resolve_probe` calls `embarch_topology::hardware::select_probe(probes, probe_serial, action)`
    directly, no inline copy. **Method note:** my first pass checked this against
    `/mnt/c/Users/tmp12/source/repos/embarch-core`, an rsync deploy target with no `.git` (not the
    canonical checkout), which still had the *pre*-decision-61 hand-rolled duplicate and looked like
    a real finding. Re-checked against the actual git checkout at
    `/home/gabriel/Github/embarch/embarch-core` and the claim is true there. Recorded here so nobody
    re-does that specific false alarm.
20. `Validation`'s two distinct timestamps — `board.confirmed_at_utc_ms` (enrolment time) vs.
    `validated_at_utc_ms` (read only after the hardware-ID compare passes) (:188-209, :258-261) —
    traced through the code and the file's own `validation_keeps_the_two_timestamps_distinct_in_json`
    test.
21. `select_probe`: zero probes is checked "first and unconditionally," ahead of the serial lookup
    (:318-323) — traced, the `probes.is_empty()` check (:329) precedes the serial-match branch (:342).
22. `enroll`: link-port facts are carried over keyed on `probe_serial`, "deliberately," and must not
    follow a role onto different silicon (:428-434) — traced, `enrollment::find(&serial)` (:435) keys
    on the new probe's own serial, not on `role`.

### The 4 `unsettled` claims (external vendor SDK source, not available in this environment)

- `hardware_id.rs:18-22` — `NRF54L_FICR_INFO_DEVICEID` address "sourced from a real user's report...
  (Nordic DevZone)." Silicon evidence is decision 21's, outside this task's three-file bound.
- `hardware_id.rs:24-33` — `STM32G0_UID`'s claims about `hal_stm32`'s `stm32g0*xx.h` and Zephyr's
  `hwinfo_stm32.c`. No STM32 HAL or Zephyr driver source is checked out anywhere reachable from this
  session.
- `hardware_id.rs:244-259` — the quoted `hwinfo_nrf.c` pseudocode. Not traced against actual Zephyr
  source; **corroborated, not verified**, by claim 6 above (the arithmetic and the live-bench test
  pair are self-consistent with what the pseudocode describes).
- `hardware_id.rs:283-287` — the quoted `hwinfo_esp32.c` byte assembly. Same: corroborated by claim
  7's arithmetic, not independently traced against Zephyr source.

### What this sweep explicitly did not do

No citation-number checking (`topology/036` already swept this repo's `decision N`/`file:line`
citations and closed — none re-verified or "fixed in passing" here, per this task's own scope). No
hardware touched: no probe attached, no `embarch-topology validate` run, no enrollment performed.
No file outside the three named was read in full — `port.rs` (claim 14) got two targeted `grep`s for
the two specific functions the enrolment-trio comments cite, not a read.

Gate: `cargo build --all-features`, `cargo test --all-features` (80 + 5 tests, all passing),
`cargo clippy --all-targets --all-features -- -D warnings` — all clean, zero warnings.
`embarch-topology` worktree has no diff from `main`; nothing to fold.
