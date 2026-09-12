# 027 — `spec.md` says the `.dialog` modal is used in five places; the fifth re-implements both classes inline

**State:** claimed — leg 087, 2026-09-11.
**Source:** refill sweep, leg 087, 2026-09-11. `embarch-ui/spec.md`'s "Design system" paragraph,
checked against `assets/index.html`, `assets/style.css` and `assets/app.js`.
**Scope:** ui
**Hardware:** none — static markup and CSS; the four working modals are the reference.
**Owner:** no

## What

`embarch-ui/spec.md` describes *"a `.dialog`/`.dialog-backdrop` modal used in five places"*. Four
places use the classes (`assets/index.html` around lines 341, 362, 379 and 441). The fifth — the
Enroll tab's assign modal, around line 480 — uses **neither**: `#assign-dialog-backdrop` carries
`style="display:none; position:fixed; inset:0; background:oklch(0% 0 0 / 0.5); z-index:50;"` and
`#assign-dialog` carries `class="card"` plus inline `position:fixed; top:30%; left:50%;
transform:translateX(-50%); z-index:51; width:340px`. That is an inline re-implementation of
`assets/style.css`'s own `.dialog-backdrop` and `.dialog` rules, driven by the same show/hide code
in `assets/app.js`.

Give `#assign-dialog-backdrop` `class="dialog-backdrop"` and `#assign-dialog` `class="dialog card"`,
and drop the duplicated inline positioning so the two classes are the single source of the modal's
geometry — **keeping `width` inline if this modal is deliberately narrower than the other four**,
which is a real possibility and not a defect. **Compare the rendered geometry against the shared
rules before deciding what to keep**: if the inline values differ from `.dialog`'s in a way that is
load-bearing for this modal, say so in the change rather than flattening it, and then `spec.md`'s
"five places" is what needs correcting instead.

## Why now

The doc states a design-system fact — one modal treatment, five uses — that the markup makes false
in the one place a reader is least likely to check. The cost is the ordinary cost of a duplicated
rule: a change to `.dialog` reaches four modals and silently skips the fifth.

## Done when

- [ ] The assign modal uses `.dialog-backdrop` and `.dialog` (plus `card`), with only genuinely
      modal-specific properties left inline and each of those justified in the diff.
- [ ] Show/hide still works from `assets/app.js` unchanged, or the change to it is part of this
      unit and explained.
- [ ] `spec.md`'s sentence is true as written — or corrected, if the fifth modal turns out to be
      deliberately different.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10). `changelog.d/` fragment.

## Doc-size reserve in your sub-project (supervisor's dispatch note, leg 087)

**No `embarch-ui` doc is in reserve** as of this dispatch — you have full headroom. **If your work
puts one there** (past 90% of its cap), file `tasks/ui/<NNN>-compact-ui.md` in the same commit
(`tasks/README.md` has the shape; `scripts/check-task-numbers.py --next ui` gives a safe number).
Recording the debt is the job; paying it is not.
