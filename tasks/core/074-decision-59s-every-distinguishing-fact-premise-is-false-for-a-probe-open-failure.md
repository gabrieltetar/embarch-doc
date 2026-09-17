# 074 — Decision 59's "every distinguishing fact was already present" is false for a probe-open failure; `kind` may not cover that case

**State:** done — agent/core/074-decision59-open-fail, 2026-09-17
**Filed by:** leg 135, from `inbox/core-decision59-open-fail-not-classified.md`, written by the
`topology/056` reviewer. Filed verbatim below except for this header block and the two supervisor
notes marked as mine. I re-checked the `Hardware: none` claim myself and it holds: every question
here is answered by reading `embarch-core`'s `src/api.rs`, `src/hardware.rs` and `src/study.rs`, and
the only test the fix could need is a mock or a held handle — no board, no probe, no live Core.
**Source:** embarch-reviewer, reviewing `topology/056` (code `fb754d7` in `embarch-topology`, doc
`b3c5827` in `embarch-doc`). Not a contradiction inside `embarch-topology` itself — decision 12
there supports that unit's narrowing. This is a downstream premise in `embarch-core` that the same
unit's corrected text now falsifies.
**Scope:** core
**Hardware:** none.
**Owner:** no

**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` is **11,356/12,288 B (932 B
left)**, filed as `tasks/core/046` and blocked — **do not write into it.** Nothing else of core's is
in reserve. Run `python3 scripts/check-doc-size.py --pressure` before and after; if your work pushes
a file into the band or leaves one there unfiled, file `tasks/core/<NNN>-compact-core.md` in the
same commit.

**Supervisor note 1 — this task is one half of a pair, and it is deliberately the half that runs
first.** `tasks/topology/058` asks whether `embarch-topology`'s `validate_known_timed` should start
routing its probe-open failure through `raise()` (constructing a `TopologyMismatch` and logging an
alert) or accept that it stays silent. That is a *behaviour* question in a shared crate. **This task
is the fact-finding half: what does `embarch-core` do with such a failure today, and what does the
written record claim?** Answer that from the code as it stands. **Do not change
`embarch-topology`, and do not assume its behaviour will change** — if your conclusion depends on
which way `058` goes, say so explicitly and state both branches rather than picking one. `058` is
deliberately not dispatched in the same leg as this task.

**Supervisor note 2 — amending decision 59 is in scope; writing a new numbered decision is a
judgement call you must justify.** Decision 59 is the standing rationale for the current `/validate`
response shape and it quotes a sentence the suite has now retracted, so correcting its premise is a
correction, not a new choice. If you conclude a *third* `kind` arm is warranted, that is a wire
change with consumers in `embarch-api`, `embarch-ui` and the user guide — **do not implement it**;
say so, and drop it in `/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path) in full task
format. Documenting it as an accepted gap is the cheaper outcome and is a legitimate answer.

**Supervisor note 3 — a second reviewer finding was folded into this task rather than filed
separately, because it is the same sentence from the other side.** `inbox/core-072-review-third-503-producer.md`
(written by `core/072`'s reviewer, merge `76a48ed`, and deleted by me when I folded it in) is
**item 2 below**. It is a defect in text that landed forty minutes before this task was written, in
the same two files, about the same status code. Doing both in one unit is the only way they get a
consistent answer; splitting them would have two workers writing the same bullet. **Both items are
required for this task to be done.**

---

## Item 1 — decision 59's completeness premise

## What

`embarch-core/decisions/surfaces.md` decision 59 justifies adding `kind: "not_attached" | "mismatch"`
to `ValidateMismatchResponse` with: **"No change in `embarch-topology`: `TopologyMismatch` already
carried `live_hardware_id: Option<String>` (that crate's own doc comment: `"None when the enrolled
probe couldn't even be opened"`), so every distinguishing fact was already present at every call
site — Core was the one collapsing it."**

`topology/056` (`src/hardware/validate.rs`, module header and `TopologyMismatch::live_hardware_id`'s
doc comment) just corrected that exact quoted sentence: `live_hardware_id: None` means the probe was
**not found in `Lister::list_all()` at all** — it is specifically **not** the "attached but `.open()`
fails" case (held by another process, permission denied, a half-wedged J-Link). That case never
constructs a `TopologyMismatch` in the first place; `validate_known_timed` returns a bare
`anyhow::Error` from `probe_info.open()`, un-logged and not downcastable — there is no
`live_hardware_id` field for it to be `None` or `Some` in.

So decision 59's premise — that `embarch-topology` already carried every distinguishing fact and
Core merely had to unpack `live_hardware_id.is_none()` into a `kind` — was true for exactly two cases
(not-attached, mismatch) and silently assumed away a third that `embarch-topology` itself never
surfaced as a `TopologyMismatch`: probe-open failure. `embarch-core/interfaces/topology.md`'s own
`/validate` row repeats the same collapse, describing the `503 not_attached` case as "when the
enrolled probe couldn't be opened at all (unplugged, most likely)" — conflating "not enumerated" with
"enumerated but `.open()` failed," the identical ambiguity `topology/056` just resolved in the other
direction.

## Why now

This is the "shipped doc inherited the same wrong paraphrase" case the `topology/056` unit flagged as
worth checking (`tasks/core/041`'s resolution text paraphrases `live_hardware_id` the same wrong way
the old `embarch-topology` comment did). `041` itself is closed and not worth reopening on its own,
but decision 59 — which is *not* closed, is the standing rationale for the current `/validate`
response shape, and is quoted verbatim from the now-corrected sentence — draws a completeness
conclusion ("every distinguishing fact was already present... Core was the one collapsing it") that
no longer holds. If `embarch-core`'s handler genuinely has no third arm, a probe that is attached but
fails to open falls through to whatever generic error path exists outside the
`kind: not_attached | mismatch` split `041` built specifically so a caller (including the fleet's own
alert-vs-open rule) never has to parse `reason` text — which is exactly the failure mode `041` was
written to close.

The reviewer could not check `embarch-core`'s actual handler code (`hardware.rs`/`api.rs`) from the
doc repo, so it could not say whether this is live-broken or already handled some other way — only
that the written rationale for the current shape rests on a premise the doc repo itself has now
retracted elsewhere. **Establishing that is this task's first job, and "it is already handled" is a
correct outcome.**

---

## Item 2 — the `503` bullet `core/072` just landed names two cases and the code has three

**Do not take this on my word or the reviewer's — re-derive it.** `core/072` (merge `76a48ed`)
rewrote `embarch-core/interfaces.md`'s `503` bullet and `embarch-core/spec.md`'s matching sentence to
say `503` *"carries two distinct meanings"*: `hw_lock` contention everywhere, and `/validate`'s JSON
`kind: "not_attached"` on that one route. `core/072`'s reviewer re-derived a third producer from
`src/api.rs`: **`POST /flash` and `POST /reset`** (`flash_handler` ~446, `reset_handler` ~574) both
call `describe_topology_error` (`api.rs` 201–219), which returns
`(StatusCode::SERVICE_UNAVAILABLE, "probe not attached for role …")` — **plain text, after `hw_lock`
was already successfully acquired**, whenever the `TopologyMismatch`'s `live_hardware_id` is `None`.
That is neither `hw_lock` contention nor `/validate`.

The reviewer reports this is inside decision 59's own scope rather than outside it: decision 59 says
in its own words that *"`flash`/`reset` … ran the identical check mid-attach … fixed the same way …
(`describe_topology_error`/`describe_gate_error`)"*, and `tasks/core/041`'s commit (`f1c18cc` in
`embarch-core`) built both `/validate`'s `kind` field and `describe_topology_error`'s 503/409 split
in one diff — reportedly confirmable with `git log -p -S describe_topology_error -- src/api.rs`, and
pinned by the test `flash_reset_path_leads_differ_between_not_attached_and_mismatch` (`api.rs`
~2045). **Check that history yourself.**

**What it costs a reader:** a caller following the new text's *"check which route answered"* rule
still misdiagnoses a detached probe on `/flash` as lock contention, because on those two routes the
two causes share a status code and differ only in message text — which the new bullet never says.

**A revert is available and is the worse option.** `76a48ed` touches only
`embarch-core/interfaces.md`, `spec.md`, `interfaces/result-layout.md`, `decisions/surfaces.md`, two
`changelog.d/` fragments and a task file, and nothing has touched those hunks since — but reverting
restores the older, also-wrong *"plain text on every non-2xx / 503 means `hw_lock`"* invariant. Fix
forward.

**Also settle the `502`:** the reviewer checked `study.rs`'s dev-bench gate (`describe_gate_error`)
and reports it folds into `502` rather than being a fourth `503` producer — but that `502` may carry
the same not-attached/mismatch distinction in its text lead. Say whether a caller needs to be told.

---

## Done when

**Item 1:**

- [x] Confirmed, from `embarch-core`'s actual `/validate` handler, what status and `kind` a
      probe-open (attached-but-`.open()`-fails) failure produces today — quoted from lines you read,
      not inferred.
- [x] If it is not distinguishable from a generic 500/unhandled error, decided whether it needs its
      own `kind` (a third arm) or is documented as an accepted gap, and **decision 59 and
      `interfaces/topology.md`'s `/validate` row amended to stop asserting "every distinguishing fact
      was already present."** Per supervisor note 2, do not implement a third arm.
- [x] Checked whether `flash`/`reset` and `study.rs`'s dev-bench gate (decision 59's
      `describe_topology_error`/`describe_gate_error`) have the same blind spot in their plain-text
      paths, and said so either way.

**Item 2:**

- [x] `interfaces.md`'s `503` bullet and `spec.md`'s matching sentence name **every** case the code
      produces — re-derived by you from `src/api.rs`, not copied from item 2's text — or item 2 is
      reported as not holding, with the lines that show it.
- [x] Said explicitly whether `502`/`describe_gate_error` needs a caller-facing mention.
- [x] Items 1 and 2 leave **one** consistent account of `503` across `interfaces.md`, `spec.md` and
      `interfaces/topology.md`. A half-corrected invariant is worse than either side — that is
      `core/072`'s own instruction, and `core/072` is the unit that just broke it.

**Both:**

- [x] Nothing corrected on the strength of this task's own description — every change rests on a line
      you read.
- [x] A `changelog.d/` fragment.
- [x] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-core`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Resolution

Both items held, re-derived from source rather than taken on the task's own word. No code changed
anywhere, in either `embarch-core` or `embarch-topology`.

**Item 1 — the completeness premise does not hold, and it is broader than "probe-open."** Read
`embarch-topology/src/hardware/validate.rs` (the sibling checkout `../embarch-topology` this crate's
`Cargo.toml` path-dependency actually resolves to) rather than assuming the task's paraphrase:
`validate_known_timed` (226–277) only calls `raise()` — the one function that constructs a
`TopologyMismatch` and logs an alert — from exactly two places: the probe absent from
`Lister::list_all()` (234–243, `live_hardware_id: None`) and a live hardware-ID mismatch (261–271,
`live_hardware_id: Some`). Every failure *between* those two points — `probe_info.open()` (246–248),
`check_target_powered` (249–250), `probe.attach` (251–253), `session.core(0)` (254–256), and
`hardware_id::read` (257) — returns a bare, non-downcastable `anyhow::Error` via `?`, with no alert
logged. So the gap is not only "attached but `.open()` fails"; it is the whole mid-attach path after
the probe is found, five failure points wide, none of them ever reaching `TopologyMismatch`. The
crate's own corrected doc comment (`topology/056`, `fb754d7`, prose-only, no new decision number)
already says this precisely for `live_hardware_id`; I confirmed it against the function body itself
rather than trusting the comment alone.

Traced what `embarch-core` does with that bare error at all four call sites that reach
`validate_known_timed` (via `validate_serial_timed`/`validate_role_timed`):
- `src/api.rs`'s `validate_handler` (1055–1123): neither `TopologyMismatch::downcast_ref` (1091) nor
  `NotEnrolled::downcast_ref` (1115) matches a bare error, so it falls to `Err(internal_err(e))`
  (1120) — plain-text `500`, the full `{e:?}` chain, no `kind` field at all.
- `src/api.rs`'s `describe_topology_error` (201–219), used by `flash_handler` (446) and
  `reset_handler` (574): the `None => internal_err(e)` arm (217) — plain-text `500`.
- `src/study.rs`'s `describe_gate_error` (905–917), used by `enforce_dev_bench_gate` (894): the
  `None => format!("{e:?}")` arm (915) — folded into `502 BAD_GATEWAY` by both its callers (`study.rs`
  374, 968, 972, 1043, 1051, per that function's own doc comment, 897–904).

So decision 59's "every distinguishing fact was already present... Core was the one collapsing it" is
false for this case: there is no fact to collapse — `embarch-topology` never produced one. **Per
supervisor note 2, no third `kind` arm implemented.** Amended decision 59's own last paragraph
(`decisions/surfaces.md`) in place to record what it got right (no wire change needed for `kind`'s two
existing arms) and what it did not (the completeness claim), and corrected
`interfaces/topology.md`'s `/validate` row, which repeated the same "couldn't be opened at all"
conflation this task's Item 1 quotes. Documented as an accepted, previously-unrecorded gap, not fixed
in code — a third `kind` arm is a wire change with consumers in `embarch-api`/`embarch-ui`/the user
guide, out of scope here.

**Item 2 — held, and `interfaces.md`'s bullet undercounted by one.** `describe_topology_error`'s
`not_attached` arm (203–209) returns `StatusCode::SERVICE_UNAVAILABLE` — a real, tested third `503`
producer (`api.rs`'s own test `flash_reset_path_leads_differ_between_not_attached_and_mismatch`,
2049–2060, pins both status and lead-text distinction), reached from `flash_handler`/`reset_handler`
*after* `hw_lock` is already held (`acquire_hw_lock` at 413/567 runs first). That is a different
`503` than `acquire_hw_lock`'s own contention `503` (103–123) — same status, same plain-text shape,
distinguished only by the message's own lead word (`probe not attached for role …` vs
`hw_lock held by …`), never by anything structural. `interfaces.md`'s bullet named only two meanings
(`hw_lock` contention, `/validate`'s JSON `kind`) and missed this third one entirely — fixed by
rewriting the bullet to name all three and say explicitly that two of them share status and shape.

**`spec.md`'s "matching sentence" checked and left alone.** It only asserts "plain text on every
non-2xx except `POST /validate`" and points to `interfaces.md` for detail — it never itself claimed
"two distinct meanings" for `503` (that phrase is `interfaces.md`'s alone), and the plain-text/JSON
split it does assert is still exactly true after this fix (`/flash`/`/reset`'s `not_attached` `503` is
still plain text, not JSON). No edit needed there; verified rather than assumed.

**`502` does need the caller-facing mention, and now has one.** `describe_gate_error`'s two arms
(906–916) carry the same not-attached/mismatch distinction in their lead words that
`describe_topology_error`'s do — confirmed by reading both functions side by side. Added one sentence
to `interfaces.md`'s `404`/`502` lead saying so, so a caller of `study.rs`'s dev-bench gate knows to
read the body's lead the same way a `/flash`/`/reset` caller now has to for `503`.

**One consistent account of `503` now exists across all three files.** `interfaces.md` carries the
full three-producer account and the accepted-gap note; `spec.md` points to it without repeating or
contradicting it; `interfaces/topology.md`'s `/validate` row matches `interfaces.md` and no longer
conflates "not found" with "found but failed to open."

**Doc-size reserve:** `python3 scripts/check-doc-size.py --pressure` run before and after — same 14
parked files both times, `decisions/auth.md` untouched (still 11,356/12,288 B). None of the three
edited files (`decisions/surfaces.md` now 8,705 B, `interfaces.md` 6,067 B,
`interfaces/topology.md` 3,744 B — `spec.md` unchanged at 8,456 B, not edited) entered the reserve
band. No compaction task filed.

**Not done, correctly:** no third `kind` arm, no new numbered decision, no change to
`embarch-topology`, `decisions/auth.md` untouched, no handler/status/response-shape change anywhere
(`git status`/`git diff` on the code worktree shows zero changes).

**Gate:** `cargo build --all-targets`, `cargo test` (209 passed, 2 ignored, 0 failed),
`cargo clippy --all-targets -- -D warnings` all green in the code worktree (doc-only unit, run for
baseline — unaffected). `python3 scripts/check-docs.py` (11/11 green),
`python3 scripts/check-ownership.py --scope core` (doc worktree, base `d69d3644b574`, 3 paths, all
owned) and `--scope core --code-repo` (code worktree, 0 paths changed) both green,
`python3 scripts/check-client-names.py --repo <code worktree>` clean against 7 denylist entries.

**Hardware-verification debt:** none. Every claim here is settled by reading `embarch-core`'s
`src/api.rs`/`src/hardware.rs`/`src/study.rs` and `embarch-topology`'s `src/hardware/validate.rs` — no
board, no probe, no live Core, per this task's own `Hardware: none` line.

## Not yours

- **Do not change `embarch-topology`** — `tasks/topology/058` owns that half and is not in flight.
- **Do not change any handler, status code or response shape in `embarch-core`.** A third `kind` arm
  is a wire change; it goes in `inbox/`, not in a commit.
- **Do not touch `embarch-core/decisions/auth.md`** — in reserve, parked under `tasks/core/046`.
