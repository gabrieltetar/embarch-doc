# 074 — Decision 59's "every distinguishing fact was already present" is false for a probe-open failure; `kind` may not cover that case

**State:** claimed by agent/core/074-decision59-open-fail, 2026-09-17 11:34
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

- [ ] Confirmed, from `embarch-core`'s actual `/validate` handler, what status and `kind` a
      probe-open (attached-but-`.open()`-fails) failure produces today — quoted from lines you read,
      not inferred.
- [ ] If it is not distinguishable from a generic 500/unhandled error, decided whether it needs its
      own `kind` (a third arm) or is documented as an accepted gap, and **decision 59 and
      `interfaces/topology.md`'s `/validate` row amended to stop asserting "every distinguishing fact
      was already present."** Per supervisor note 2, do not implement a third arm.
- [ ] Checked whether `flash`/`reset` and `study.rs`'s dev-bench gate (decision 59's
      `describe_topology_error`/`describe_gate_error`) have the same blind spot in their plain-text
      paths, and said so either way.

**Item 2:**

- [ ] `interfaces.md`'s `503` bullet and `spec.md`'s matching sentence name **every** case the code
      produces — re-derived by you from `src/api.rs`, not copied from item 2's text — or item 2 is
      reported as not holding, with the lines that show it.
- [ ] Said explicitly whether `502`/`describe_gate_error` needs a caller-facing mention.
- [ ] Items 1 and 2 leave **one** consistent account of `503` across `interfaces.md`, `spec.md` and
      `interfaces/topology.md`. A half-corrected invariant is worse than either side — that is
      `core/072`'s own instruction, and `core/072` is the unit that just broke it.

**Both:**

- [ ] Nothing corrected on the strength of this task's own description — every change rests on a line
      you read.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-core`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

- **Do not change `embarch-topology`** — `tasks/topology/058` owns that half and is not in flight.
- **Do not change any handler, status code or response shape in `embarch-core`.** A third `kind` arm
  is a wire change; it goes in `inbox/`, not in a commit.
- **Do not touch `embarch-core/decisions/auth.md`** — in reserve, parked under `tasks/core/046`.
