# 010 — The study-designer progress badge is one step short for the whole run

**State:** claimed by agent/ui/010-progress-badge, 2026-09-06 18:50
**Source:** found by `agent/core/012` while documenting Core's `current_step`; `embarch-core/decisions.md` decision 43
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-ui/assets/app.js`, in the study-designer run card:

```js
var progress = state.current_step != null && state.total_steps != null
  ? " " + (state.current_step + 1) + "/" + state.total_steps
  : "";
badge.textContent = "running" + progress;
```

That `+ 1` is correct for a `current_step` meaning **"how many steps have
finished"**. Core does not send that. Core sends **the 0-based index of the last
step that finished**, and `null` until one has — now stated in
`embarch-core/interfaces.md`'s `GET /study/{id}` row and pinned by a test, and
deliberately not renumbered because this renderer and the shared Core client's
poll de-duplication both already read it (decision 43).

So on a two-step study the badge reads: nothing while step 1 runs (`current_step`
is `null`), then `running 1/2` for the whole of step 2. It is one short at every
moment a step is actually in flight. The 1-based index of the step now running is
`current_step + 2`, or `1` when `current_step` is `null`, clamped to
`total_steps` for the brief window after the last step lands and before Core
flips `status` to `completed`.

Cosmetic — a progress indicator, not a correctness property — which is exactly
why Core chose to document its number rather than change it under three other
surfaces that print it verbatim.

## Why now

Core's side of this landed in `core/012` and states the contract this file is
reading wrong; leaving the renderer as it is means the newly-documented meaning
has one known consumer that disagrees with it. `embarch-core` may not write
`embarch-ui`, so this is a drop rather than an edit.

Worth deciding at the same time, in `embarch-ui`'s own words: whether the badge
should show *the step now running* or *steps finished*. Both are defensible; the
current code shows neither.

## Reserve line (supervisor, leg 024, measured at dispatch)

One file in `embarch-ui` is in reserve: **`embarch-ui/decisions/trace-view.md` — 11,080 / 12,288,
1,208 bytes left**, filed against [`009-compact-ui.md`](009-compact-ui.md), which is **blocked** on
`In flux: yes`. Nothing else in `embarch-ui` is in reserve, and this unit has no business in
`trace-view.md` — the run badge is not the trace view. **If you find yourself writing there, stop
and say why in your report**; you would then also owe that file's compaction as part of this unit,
carrying `009`'s `Must not delete:` list, which is not what this task is for.

If your work pushes any other `embarch-ui` doc into reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the **same commit** (`tasks/README.md` has the shape). The path is
`tasks/ui/`, your own scope — not `tasks/doc/`, which `check-ownership.py` refuses to a worker.

**Note on the source of truth for the number you are fixing:** `embarch-core/decisions.md`
decision 43 was reorganised earlier in this same leg by `core/014` — a mission split — and the
decision itself did not move; it is still in `embarch-core/decisions/studies.md`, and
`embarch-core/interfaces.md`'s `GET /study/{id}` row is unchanged. Read those two at `origin/main`
rather than from any earlier memory of them.

## Done when

- [ ] The badge's arithmetic matches the meaning `embarch-core/interfaces.md`
      states, with the intended reading (`step now running` vs `steps finished`)
      named in a comment beside it so the next reader does not re-derive it.
- [ ] The `current_step == null` case shows something sensible for the first
      step rather than dropping the counter entirely.
- [ ] `embarch-ui/src/study_designer.rs`'s `RunState::Running.current_step` says
      in its own doc which meaning it is passing through — it is a straight copy
      of Core's field and nothing on that path currently says so.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
