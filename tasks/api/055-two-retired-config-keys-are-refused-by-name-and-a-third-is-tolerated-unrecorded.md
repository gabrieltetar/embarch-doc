# Two retired config keys are refused by name and a third is deliberately tolerated, and only the tolerance is unrecorded

**State:** claimed — leg 064

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

- [ ] The decision to refuse two retired keys by name and tolerate `artifact_path_for_core` is
      recorded as a numbered decision, stating the field-compatibility reason for the exception and
      what would end it.
- [ ] It says what a future retired key should do by default, so the next one is not a coin flip.
- [ ] `open.md`'s prose about the gap is replaced by a citation, not left duplicating the decision.
- [ ] **No code change.** The load behaviour as shipped is what the decision should record;
      if the conclusion turns out to be that `artifact_path_for_core` *should* be refused, that is a
      different task and it must say so rather than being folded in here.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped, `status.d/`
      fragment for anything suite-level it made false.
