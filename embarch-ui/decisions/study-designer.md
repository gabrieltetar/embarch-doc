# embarch-ui decisions: The Study Designer tab

**Status:** active, 2026-09-02.

Authoring a study: the two version fields and security. Which firmware repo is open: [project.md](project.md). GATT capture and its pickers: [gatt-capture.md](gatt-capture.md). How the tab's panels are laid out: [designer-panels.md](designer-panels.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 11 — The two version fields, the reflash selector, and provenance on a result

The human surface for [embarch-study-designer](../../embarch-study-designer/decisions/declares.md) decision 40.

**The two `requires` fields are prefilled from live bench state, not left blank** — dev-bench's from Core's `GET /dev-bench/hello`, the DUT's from the configured project's own `git describe`. Prefilling is what makes a mandatory field a help rather than a tax: the common case is "the builds currently in front of me," and **typing a hash by hand to express that would guarantee people paste `any` to get past it**, defeating the decision.

**`any` is a visible, deliberate choice** — a checkbox that visibly takes the field over, with the input still showing the literal and going disabled rather than being cleared, so **the checkbox *is* the statement instead of a way of not making one.** A blank field is refused rather than quietly upgraded to `any`, because `Requirements::validate` treats blank as the not-thought-about case and **silently promoting it to a deliberate answer would erase the distinction the whole decision rests on.**

**Reflash lives in the run dialog, never in the saved study** — the study is the experiment, the run dialog is this particular run, the same split decision 10 makes for signal routes. A mismatch is shown *before* the run with both strings, next to the override, so the choice is made against the actual discrepancy rather than in the abstract. **Unreadable is rendered as unreadable, which is not a mismatch:** a bench that is not plugged in has no version to disagree with, and presenting that as a discrepancy would be a claim about a gap nobody established.

**A result renders how each version was established, not just what it was.** `Declared` renders dashed, muted *and* italic — three signals, because one a reader can miss is the same as none — and `verified` is decided server-side, **never re-derived in JavaScript**, since a UI deciding for itself which variants count is the easiest way to reintroduce the defect decision 40 closes.

**The reflash selector is built, and this half of the decision is reversed** (2026-09-18, [reversals](../../embarch-decision-reversals.md) row 113). It shipped saying reflash was deliberately terminal-only, on three options: duplicate `embarch-api`'s orchestration here — the duplication decision 1 exists to prevent — depend on `embarch-api`, a direction the suite has nowhere, or land the rest and name the gap, which is what happened. **The reasoning was right about all three and the list was incomplete**: the fourth option is to move the machinery somewhere both crates can reach, which is what `embarch-core-client` had already done between these same two crates. `embarch-firmware-build` is that (`embarch-api` decision 78), and the Build card is what it buys — see [firmware-build.md](firmware-build.md) decision 38. What is unchanged: the flash still goes over HTTP to Core, and `flashed_firmware_version` is still only set when this process genuinely put the image there.

**The version argv and its never-move-the-tree rule now live in `embarch-core-client::version`**, re-exported by `embarch-api` — `embarch-ui` cannot depend on `embarch-api` directly, and the alternative was a second copy of that rule in a crate that would never see its tests.

**Tap authoring landed with this: a Trace view with no way to author a tap is a view of nothing**, so a Streams card now authors a whole-study outpost trace tap. **Neither the encoding nor the scope is offered as a choice:** an outpost capture is study-scoped with no live feed by design and its encoding is the one thing a trace tap can be, so **a menu whose other entries are all wrong would be worse than no menu.** Routes must be declared before taps — Core's pre-flight refuses an undeclared signal's tap.

### 12 — A security level in the step table, and a declared-GATT picker

The human surface for [embarch-study-designer](../../embarch-study-designer/decisions/gatt.md) decisions 44 and 45.

**Security is an ordinary step**, authored like any other, its level a four-option select carrying **one line of what each means in practice** rather than the bare Zephyr constant — "encrypted, authenticated (LESC)" is what an engineer picks by. *Not* a hidden toggle on the connect step and *not* something the UI inserts on the author's behalf: **the whole argument for a separate action is that a failed elevation must be legible as itself.**

**The declared GATT is picked, not typed** — three ways in matching the three sources: vendor services from the built-in list, the extractor run against the configured firmware repo with the revision it read shown, or hand-authored. The picker's job is to make "say which GATT you know this DUT to have" a two-click action, because **the alternative — an engineer skipping it — puts the suite straight back to inferring.**

**A reconciliation result is rendered as a diff, not a pass/fail badge.** Declared-but-absent, present-but-undeclared and present-with-different-properties each read differently — **the interesting outcome is usually the middle one**, and a red or green dot throws away the only useful part.

### 22 — The stream-name cap is served on the actions response, not restated in `app.js`

`MAX_STREAM_NAME_LEN` (`embarch-study-designer::limits`) bounds a `StreamTap.name`, but the GATT-tap default name — a characteristic label truncated so it fits before `build_study` ever sees it — was sliced to a literal `32`. `ActionsResponse` now carries `max_stream_name_len` beside `max_monitor_targets` (decision 17), and `app.js` slices to that field.

**No fallback length when the field is missing** — unlike `sdMaxTargets`'s default-16, a wrong guessed cap here would let an over-long name through as confidently as a right one. `app.js` does not slice at all until it has seen a real value; a name too long for the true cap is refused by `build_study` at submit time, same as it always was before this default existed (task `ui/003`).

### 20 — The run badge counts the step *now running*, not the steps finished

Core's `current_step` is **the 0-based index of the last step that finished**, absent until one has ([`embarch-core/interfaces.md`](../../embarch-core/interfaces.md), `GET /study/{id}`; embarch-core decision 43). This badge added one — arithmetic for a *count* convention Core does not send — so a two-step run showed nothing in step 1 and `running 1/2` for all of step 2: **one short whenever a step was in flight**.

**"The step now running" is a choice, not the smaller fix.** While a study runs this badge is the *only* thing on the run card saying where it is — the per-step rows arrive only on completion — so the question in front of it is "which step am I waiting on", not "how much is done". The count reading answers it only by subtraction, and its first frame, `running 0/2`, reads as *nothing is happening* while step 1 executes.

**Its cost:** the number is clamped to `total_steps`, because after the last step lands a one-poll window has Core still reporting `running`, where the honest ordinal is `3/2`. So a run's last moment reads `2/2` with nothing running — bounded, brief, ending in `completed`. **That window is ~1 s**, this file's `POLL_INTERVAL`; the 5 s constant is `main.rs`'s dashboard poll, a different loop. A zero-step study gets **no counter** rather than `1/0`.
