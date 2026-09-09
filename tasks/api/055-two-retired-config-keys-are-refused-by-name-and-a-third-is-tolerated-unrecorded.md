# Two retired config keys are refused by name and a third is deliberately tolerated, and only the tolerance is unrecorded

**State:** open
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
