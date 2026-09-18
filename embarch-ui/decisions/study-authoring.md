# embarch-ui decisions: Authoring surfaces the Study Designer grew

**Status:** active, 2026-09-17.

Split out of [study-designer.md](study-designer.md) when it reached its size cap ([../../DOC-BUDGET.md](../../DOC-BUDGET.md)) — a verbatim move, nothing shortened. That file keeps the tab's older choices: the version fields, security, declared GATT, opening a project, the run badge, the stream-name cap. This one holds the two surfaces added when the tab learned to author every field a `Study` carries (`tasks/ui/070`). What each is served, and the routes behind them: [../interfaces.md](../interfaces.md).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 29 — The `.eap` editor is a textarea with a gutter and bands behind it, in the one dialog that needs its own CSS

Decision 17 set the rule that a new dialog should need no new CSS, and six dialogs have held to it. This one does not, and the reason is arithmetic rather than taste: a file list beside an editor at the standard `min(720px, 92vw)` is a **40-column editor**, and an `.eap` `source` line is ~100 characters before anything is wrong with it. `.dialog-wide` plus an `.eap-*` block is the exception, stated rather than smuggled.

**A plain `<textarea wrap="off">`, not a `contenteditable` renderer.** The textarea keeps native caret, undo, IME, clipboard and screen-reader behaviour, and a rewrite would have cost all five to gain syntax colour for a grammar whose errors are already **one per line**. `wrap="off"` is load-bearing: a wrapped line makes one source line occupy two rendered rows, and every gutter number and every error band below it is then wrong.

**One `--eap-line`, read by the gutter, the textarea and the bands.** Two copies of a line height is how a band lands one line off the error it describes, which is worse than no band. Bands sit **behind** the text rather than over it — a band is context, and text read through a highlight is harder to read than it was.

**Staleness is rendered, not hidden.** A Check describes the text it was run against; one keystroke later it may describe a different file, so the bands grey out and the status says so. Greyed rather than cleared: an error that was there a moment ago is still information, and dropping it silently reads as *fixed*. **A line-0 error gets no band** — an unreadable file has no line to point at — and still lists below the editor, where every error row clicks through to its line via `setSelectionRange` on the real textarea.

**Dirty state guards file switching, the backdrop and Escape**, and nothing auto-saves. This dialog holds a file in the engineer's repo, not a retypeable form. The file list is **patched on select, never re-rendered** — re-rendering destroys the node the click landed on, which is decision 17's own focus bug.

Guard compliance ([`tests/element_ids.rs`](../../../embarch-ui/tests/element_ids.rs)): **no new lookup wrapper**, because that guard hardcodes four names and an `eapEl()` would hide every lookup inside it; and **no id built by concatenation** — per-file and per-error elements key off `data-*`, which is where the instinct for per-line ids goes instead.

The editor background is `--bg-surface-2` and **not `--bg-surface-inset`**, which stays dark in the light theme.

### 30 — A saved study can be run as it is on disk, and its refusal to load is unchanged

`api_studies_load` answers `409` for a study with no `_embarch_ui_rows` — one written by hand or by an agent — and that refusal is **right and unchanged**: there are no rows to load back. What was missing was a way to run one anyway, which is the whole reason such files exist. Until 2026-09-17 the only studies that could carry protocols, record checks or a log level were the exact ones this tab could neither edit nor launch.

`POST /studies/{slug}/run` reads the file, **recomputes all three seals** (`embarch-study-designer` decision 26 — a hand-written file's seals are whatever its author typed), runs the crate's own pre-flight locally, and submits. The local pre-flight is `validate_taps`, `validate_protocol` per carried protocol, and **the two `RunProtocol` index checks `validate_protocol` cannot make**, because it never sees an `Action`; both would otherwise reach a hand-written C array subscript on the bench.

**A deserialize failure is stated as a fact about that file**, with serde's own line and column — not as a `502` about a round trip that never happened, and not as a bare message with no path. Capacity diagnosis stays `embarch-api`'s (`capacity::explain` is private to that binary), so the message points at `embarch-api run-study --study-file`, which can say more.

In the browser it lives in the Load dropdown's own area, not a second list: it is the same library, and the only difference is that this file has no rows. A run-only study is recognised from the listing's `editable` flag **before any fetch**, so the browser never calls the load route to be told `409`. The preview touches neither `sdRows` nor `sdTaps` and **says so out loud** — a read-only panel under an unrelated table is otherwise the most natural thing in the world to misread as *this is what is loaded*.

Run goes through the **existing** version-check dialog (`sdPendingRun` plus `sdDispatchRun` is the whole refactor): the question it asks is the same question either way, and a second dialog would be a second place to get that answer wrong. It reads the **file's** `requires`, not the table's. Capacity is deliberately not reported for a stored run, because `/preflight` builds from the step table and saying nothing beats reporting another study's numbers.
