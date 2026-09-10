# Two retired config keys are refused by name and a third is deliberately tolerated, and only the tolerance is unrecorded

**State:** done by agent/api/055-retired-config-keys, 2026-09-10

## Supervisor dispatch note, leg 064, 2026-09-10 — where the decision goes, decided before dispatch

**Author the new decision in `embarch-api/decisions/shape.md`, not in `decisions/zephyr.md`.** The
argument, so the worker does not have to re-make it:

- `decisions/zephyr.md` is **14,238 B against a 12,288 B cap** — already over, not merely in reserve
  — and its compaction task `tasks/api/057-compact-api.md` is `blocked` on `In flux: yes`. This task's
  own "Why now" is right that the target must not be treated as having room; what it did not know is
  that a different file is the better topical home anyway.
- The subject is a **config-load policy that spans both project kinds** — refuse a retired key by
  name, except where scaffolded configs in the field still carry it — not a Zephyr-discovery choice.
  `decisions/zephyr.md` holds decision 13 (`soc_chip_overrides`) because that key was Zephyr-shaped;
  the *policy over retired keys as a class* is not.
- `decisions/shape.md` is 9,549 B against 12,288 B, with ~2.7 KB of headroom. Leg 063's `api/048`
  made the same pre-pick for the same reason and it landed clean.

So: cite decision 13 and the `[[projects.targets]]` refusal **by number, across files**, and do not
move either of them. **The shared-compaction sequencing this task proposes is no longer a
prerequisite** — it was a consequence of the old target file. `api/041`'s owed decision stays a
separate task; do not fold it in.

**Doc reserve for `api` you must plan around** — `decisions/tool-wrapping.md` 66 B left,
`decisions/core-link.md` 188 B left, `open.md` 261 B left, `spec.md` 815 B left, `decisions/build.md`
1,154 B left, `decisions/zephyr.md` over cap. Every one of those is filed already, and all are
`blocked` on `In flux: yes` — so **do not file a new `compact-api` task**; there are six. Your
`open.md` edit replaces prose with a citation and should make that file *shorter*; if it does not,
say so in your report.
**Source:** `embarch-reviewer` on unit `api/031` (code `96f0684` + `61e2b42`, doc `b8be146`, fold `9b366a1`), leg 059 — an owed decision the burndown constraint forbade that unit from authoring
**Scope:** api
**Hardware:** none
**Owner:** no

## What

`embarch-api` refuses `[[projects.targets]]` and `soc_chip_overrides` **by name** at config load,
so a config carrying a retired key gets told so instead of being silently misread. It does not
refuse `artifact_path_for_core`, and that asymmetry is deliberate: umbrella-scaffolded configs in
the field still carry that key, and refusing it by name would break them.

The tolerance is real and correct. What is missing is that it is recorded as `open.md` prose rather
than as a numbered decision, so the shape a reader infers from the code is *"two keys were done
properly and a third was forgotten"* — which is the opposite of what happened. `api/031` confirmed
nothing in its diff added a by-name refusal and that the gap is described in `open.md`; the
reviewer's note, passed on rather than acted on, is that the asymmetry deserves a decision.

## Why now

`api/031` landed under leg 059's burndown constraint, which forbids authoring a new numbered
decision, so the unit had nowhere to put a design judgement it had genuinely made.

**Filed now because of where it was living.** Like `core/023`'s owed decision, this one was
recorded in `embarch-fleet/supervisor-log.md` and nowhere else — not in an `open.md` "Owed
decisions" section, not as a task. That log folds daily and rolls into `log-archive/` past 40 KB.
Of the 2026-09-08 burndown's five owed decisions, one became a task (`outpost/015`), two went into
`open.md` sections (`api/041`, `core/009`), and two — this and `core/023` — went nowhere durable.

## The blocker whoever takes this will hit first

**`embarch-api/decisions/tool-wrapping.md` is at 12,222/12,288 B — 66 bytes left, the tightest file
in the suite** — and its compaction task, `tasks/api/047-compact-api.md`, is **BLOCKED**.
`embarch-api/open.md` is at **4,859/5,120 B (94.9%, 261 B left)** behind `tasks/api/026`, also
**BLOCKED**. So both the place a decision about config-key handling would naturally go and the
place its `open.md` prose currently lives are full, and neither can be relieved right now.

`api/041`'s owed decision (in `embarch-api/open.md`'s "Owed decisions" section) is queued behind the
identical blockage and names the same file. **These two should probably be settled together** —
they are both "a config/tool-surface choice this crate made and did not number", and paying the
compaction once for two decisions is cheaper than twice. Whoever sequences this should decide
whether the compaction is a prerequisite task or part of this one; do not dispatch it as though the
target file has room.

## Done when

- [x] The decision to refuse two retired keys by name and tolerate `artifact_path_for_core` is
      recorded as a numbered decision, stating the field-compatibility reason for the exception and
      what would end it. — `embarch-api/decisions/shape.md` decision 64.
- [x] It says what a future retired key should do by default, so the next one is not a coin flip.
      — decision 64: refuse by name unless a scaffolding tool this crate does not control has an
      installed base already writing the key.
- [x] `open.md`'s prose about the gap is replaced by a citation, not left duplicating the decision.
- [x] **No code change.** Verified against `src/config.rs` (no `deny_unknown_fields` on
      `ProjectConfig`, `artifact_path_for_core` no longer a struct field at all — the retired UNC
      mechanism, decision 15) before writing the decision; nothing in `src/` touched.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). `cargo build`/`test`/`clippy
      --all-targets -- -D warnings` clean in `embarch-api` (no diff there); `check-docs.py` 11/11
      green; `check-client-names.py` and `check-ownership.py` (both repos) clean.
- [x] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false. — `spec.md` untouched (nothing there named
      the gap); no suite-level fact changed, so no `status.d/` fragment. `decisions.md`'s index row
      for `decisions/shape.md` updated (decision list + size). `open.md`'s edit nets *shorter*
      (4,859 B → 4,763 B), consistent with the dispatch note's expectation.

## Report

Decision 64 lives in `embarch-api/decisions/shape.md`, per the dispatch note (not `zephyr.md`,
which stays over cap). Cites decision 13 and decision 53 by number; neither moved. `api/041`'s owed
decision was left alone, still in `open.md`'s "Owed decisions" section.

**Reserve near-miss, handled without a seventh `compact-api` task.** The first draft of decision 64
pushed `decisions/shape.md` to 11,455/12,288 B (93.2%, into reserve) and an interfaces/config.md row
I'd added for completeness pushed that file to 11,333/12,288 B (92.2%, also into reserve) — neither
file was on the dispatch note's reserve list, so no existing task covers either. Rather than filing
a sixth/seventh compaction task the note explicitly said not to add, I tightened the decision's prose
(three paragraphs down to two, no content dropped) and dropped the optional `config.md` row entirely
— it wasn't required by this task's Done-when. Final sizes: `decisions/shape.md` 10,742 B (87.4%,
outside reserve), `interfaces/config.md` unchanged at its original 11,008 B. `check-doc-size.py`
is green with no new debt to file.

No hardware, no code, no other sub-project touched. Findings outside scope: none — the reviewer's
note said only that the asymmetry deserved a decision, and it now has one.
