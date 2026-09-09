# embarch-ui decisions: The Study Designer tab

**Status:** active, 2026-09-02.

Authoring a study: the two version fields, security, and opening a firmware project. Authoring GATT capture and its pickers is in [gatt-capture.md](gatt-capture.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 11 — The two version fields, the reflash selector, and provenance on a result

The human surface for [embarch-study-designer](../../embarch-study-designer/decisions/versioning.md) decision 40.

**The two `requires` fields are prefilled from live bench state, not left blank** — dev-bench's from Core's `GET /dev-bench/hello`, the DUT's from the configured project's own `git describe`. Prefilling is what makes a mandatory field a help rather than a tax: the common case is "the builds currently in front of me," and **typing a hash by hand to express that would guarantee people paste `any` to get past it**, defeating the decision.

**`any` is a visible, deliberate choice** — a checkbox that visibly takes the field over, with the input still showing the literal and going disabled rather than being cleared, so **the checkbox *is* the statement instead of a way of not making one.** A blank field is refused rather than quietly upgraded to `any`, because `Requirements::validate` treats blank as the not-thought-about case and **silently promoting it to a deliberate answer would erase the distinction the whole decision rests on.**

**Reflash lives in the run dialog, never in the saved study** — the study is the experiment, the run dialog is this particular run, the same split decision 10 makes for signal routes. A mismatch is shown *before* the run with both strings, next to the override, so the choice is made against the actual discrepancy rather than in the abstract. **Unreadable is rendered as unreadable, which is not a mismatch:** a bench that is not plugged in has no version to disagree with, and presenting that as a discrepancy would be a claim about a gap nobody established.

**A result renders how each version was established, not just what it was.** `Declared` renders dashed, muted *and* italic — three signals, because one a reader can miss is the same as none — and `verified` is decided server-side, **never re-derived in JavaScript**, since a UI deciding for itself which variants count is the easiest way to reintroduce the defect decision 40 closes.

**The reflash selector is not built, and that was a decision rather than an omission.** `--reflash` sequences check → build → flash → submit, and **`embarch-api` owns the project config and the build machinery**; `embarch-ui` posts studies straight to Core and builds nothing — Core's study route accepts only a mismatch override and a *report* of what was already flashed, which is what keeps the provenance honest. Three options: duplicate that orchestration here — the exact duplication decision 1 exists to prevent — give `embarch-ui` a dependency on `embarch-api`, a direction the suite has nowhere, or **land the rest and name the gap,** which is what shipped: the run dialog says so and points at the CLI. Carried to [../open.md](../open.md).

**The version argv and its never-move-the-tree rule now live in `embarch-core-client::version`**, re-exported by `embarch-api` — `embarch-ui` cannot depend on `embarch-api` directly, and the alternative was a second copy of that rule in a crate that would never see its tests.

**Tap authoring landed with this: a Trace view with no way to author a tap is a view of nothing**, so a Streams card now authors a whole-study outpost trace tap. **Neither the encoding nor the scope is offered as a choice:** an outpost capture is study-scoped with no live feed by design and its encoding is the one thing a trace tap can be, so **a menu whose other entries are all wrong would be worse than no menu.** Routes must be declared before taps — Core's pre-flight refuses an undeclared signal's tap.

### 12 — A security level in the step table, and a declared-GATT picker

The human surface for [embarch-study-designer](../../embarch-study-designer/decisions/gatt.md) decisions 44 and 45.

**Security is an ordinary step**, authored like any other, its level a four-option select carrying **one line of what each means in practice** rather than the bare Zephyr constant — "encrypted, authenticated (LESC)" is what an engineer picks by. *Not* a hidden toggle on the connect step and *not* something the UI inserts on the author's behalf: **the whole argument for a separate action is that a failed elevation must be legible as itself.**

**The declared GATT is picked, not typed** — three ways in matching the three sources: vendor services from the built-in list, the extractor run against the configured firmware repo with the revision it read shown, or hand-authored. The picker's job is to make "say which GATT you know this DUT to have" a two-click action, because **the alternative — an engineer skipping it — puts the suite straight back to inferring.**

**A reconciliation result is rendered as a diff, not a pass/fail badge.** Declared-but-absent, present-but-undeclared and present-with-different-properties each read differently — **the interesting outcome is usually the middle one**, and a red or green dot throws away the only useful part.

### 14 — "Open project": the firmware repo is picked at runtime, and the config field becomes the default rather than the only way in

The config field's original reasoning was right — **a *guess* at which firmware repo an engineer meant is worse than a clear "not configured" state** — and this amends it rather than reversing it: an explicit human pick is not a guess, so a picker satisfies that reasoning better than the field does. What changes is that the field's *absence* no longer leaves the whole tab dead. It stays the zero-click default for a single-repo bench.

**A typed path with server-side validation, not a file picker, and this is a constraint rather than a preference.** A browser has no directory picker that yields a usable path, and even a real path would still have to be resolved server-side because **the server is what reads the files.** So the choice was a typed path with a real check plus a recents list, or a picker that looks better and cannot work.

**The invariant that makes this more than a text box: the repo path is read by three different things** — the saved-studies directory, the custom-action registry, and the static GATT extractor. **A switch has to move all three together or the tab shows one repo's studies beside another repo's registry.** The static-extraction cache **stopped being a `OnceLock` for exactly this reason:** it needs three states — not computed for this project, computed and empty, computed — and **a `OnceLock` cannot tell the first two apart** once the project became switchable.

**A repo with no `embarch/` directory is a first-time state, not a fault**, since the first save creates it — so the survey reports "is this a source repo" and "does it have studies yet" as separate answers and the acceptance rule only reads the first. **A bare `embarch/` subdirectory is not evidence of anything, and a live run is how that was learned:** the first rule counted it, and on this bench **that accepted `$HOME`**, because the suite's own parent folder is `~/embarch`. A directory *called* `embarch` says nothing about its contents; only something written inside it does. The rule is now `.git` **or** a firmware/Cargo marker **or** a real `embarch/` config, and a refusal names all of them rather than saying "invalid".

**Recent projects persist in the per-user data directory, not in the config file.** The config is a file an engineer writes and this process only reads; **writing a UI convenience into it would mean rewriting a human's own file, comments and all.** They go beside `embarch-api`'s own logfile, through the shared `user_dirs` rather than resolved twice. An unreadable or absent file is an empty list, logged, never an error: **a convenience list that can refuse to start the tab would be worse than no list.**

**"Create study" writes a study that is valid the moment it exists**, through the same builder a save uses rather than a shape only this route can produce: `requires` explicit-any on both fields (mandatory, no serde default — it has to be *said*), both CRCs sealed, both UI sidecars present — editable and loadable from creation, not only after its first save. A name whose slug already exists is a `409`, never a silent overwrite. Its route is deliberately **not** `/studies/new`, because **`new` is a perfectly good slug** and that path would be ambiguous with a real study of that name on the sibling route.

### 22 — The stream-name cap is served on the actions response, not restated in `app.js`

`MAX_STREAM_NAME_LEN` (`embarch-study-designer::limits`) bounds a `StreamTap.name`, but the GATT-tap default name — a characteristic label truncated so it fits before `build_study` ever sees it — was sliced to a literal `32`. `ActionsResponse` now carries `max_stream_name_len` beside `max_monitor_targets` (decision 17), and `app.js` slices to that field.

**No fallback length when the field is missing** — unlike `sdMaxTargets`'s default-16, a wrong guessed cap here would let an over-long name through as confidently as a right one. `app.js` does not slice at all until it has seen a real value; a name too long for the true cap is refused by `build_study` at submit time, same as it always was before this default existed (task `ui/003`).

### 20 — The run badge counts the step *now running*, not the steps finished

Core's `current_step` is **the 0-based index of the last step that finished**, absent until one has ([`embarch-core/interfaces.md`](../../embarch-core/interfaces.md), `GET /study/{id}`; embarch-core decision 43). This badge added one — arithmetic for a *count* convention Core does not send — so a two-step run showed nothing in step 1 and `running 1/2` for all of step 2: **one short whenever a step was in flight**.

**"The step now running" is a choice, not the smaller fix.** While a study runs this badge is the *only* thing on the run card saying where it is — the per-step rows arrive only on completion — so the question in front of it is "which step am I waiting on", not "how much is done". The count reading answers it only by subtraction, and its first frame, `running 0/2`, reads as *nothing is happening* while step 1 executes.

**Its cost:** the number is clamped to `total_steps`, because after the last step lands a one-poll window has Core still reporting `running`, where the honest ordinal is `3/2`. So a run's last moment reads `2/2` with nothing running — bounded, brief, ending in `completed`. **That window is ~1 s**, this file's `POLL_INTERVAL`; the 5 s constant is `main.rs`'s dashboard poll, a different loop. A zero-step study gets **no counter** rather than `1/0`.
