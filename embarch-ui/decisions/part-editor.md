# embarch-ui decisions: The part editor

**Status:** active, 2026-11-01.

A repo's part templates edited in the UI — phase 3 of [embarch-bench-editor-proposal.md](../../embarch-bench-editor-proposal.md). What a template is and what the vocabulary serves: [bench-model.md](bench-model.md) (71, 88). Editing a bench on the canvas: [bench-editing.md](bench-editing.md) (80–86).

Index: [../decisions.md](../decisions.md). Current truth: [../spec/bench-editing.md](../spec/bench-editing.md).

### 87 — A template is edited in a dialog that offers only what is served and shows every refusal verbatim

**A repo template is edited in a dialog over the Topology tab** (owner, 2026-11-01: built-ins plus a repo part editor), opened from the parts bin with `embarch:edit-part` and written through `POST`/`PUT /api/bench/parts` (71, 74). A save sends `embarch:parts-changed`, so the canvas re-reads the catalog and redraws the bench on screen, unsaved edits and all. The preview is the canvas's own drawing, `window.embarchBench.previewTemplate`, so a template looks in the editor as it will on the bench; `bench-parts.js` draws nothing of its own.

**It offers only what the vocabulary serves (88) and restates no word, rule or limit.** A value the served list lacks is kept, marked *(not in this build)* and sent, never swapped for a served word. **What a save refuses is the server's to say**: the refusal is shown verbatim, naming the field by its path (`connectors[0].functions[0].interface`, through `serde_path_to_error`, already in the tree through axum's `json` feature). A number field is text, sent as typed, because a number input reports unparseable text as empty and would drop the field instead of letting the server say what is wrong.

**A built-in opens read-only, with *Copy to this repo*** (`<id>-copy`, then `-copy-2`…), since a repo template may not take its id (71). **A file in `errors` opens on its error**; a fresh template under its id is offered only after a confirmation, never for a built-in's id, and saves only once the old file is gone, since `POST` never creates over a file (74). A `PUT` refused `version-changed` offers Reload; one answered `404`, the file removed since it was read, offers *Save as new*.

**A changed draft is never dropped without asking**: Cancel, Esc or another part opened over it asks first, and the canvas's leave guard asks about it (84). A project switch keeps it on screen with Save disabled, since it describes the repo that was open; an unchanged dialog closes when the tab is left. A press on the backdrop does not close it.
