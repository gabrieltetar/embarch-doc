# embarch-chat decisions: What it is, where it lives, how it looks

**Status:** active, 2026-10-23.

The ask, the panel it replaces, the repo it lives in, how it shipped, and its look. **The ask, in the owner's words:** "its own Claude Code chat basically, with improvements tailored to my needs" — so that a chat can be started, seen and answered from EmbArch itself instead of handing off to claude.ai (`embarch-desk` decision 44).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

## Shape

### 1 — It lives in a VS Code panel

An extension of EmbArch's own, beside the code.

### 2 — It replaces the Claude Code panel for the owner's work

VS Code stays for reading and editing code, and any chat can still open in Claude Code's panel.

### 3 — What pulls hardest: the work item, the library, every thread, the bench, the atlas

It knows its **work item** and starts briefed; it carries the owner's **prompt library** as one-click actions; **every thread at a glance**, waiting-on-you first; **bench-aware**; **atlas integration**.

### 4 — Start work did not wait for it

Start work kept opening the Claude Code panel (`embarch-desk` decision 43) until this existed. The desk's chat setting, `chat_panel`, **off by default**, decides which panel Start work opens; it is on since the deploy of 2026-10-23.

### 6 — `embarch-promptu` became `embarch-chat`

One new repo for the extension and the library, the sub-project count unchanged; promptu's three planned pieces — a permission split, a `CLAUDE.md` fragment, a build → flash → serial log → diagnose loop — are library entries (39, and the `build-flash-verify` skill). Its two deferred questions are answered: the packaging is a Claude Code plugin (13), the repo its own. Decision 1 sets `embarch-ui` decision 3's "no webview" aside for this extension only. **Rejected:** inside `embarch-desk` or `embarch-ui`'s launcher (wrong repo's concern), a sub-project beside promptu.

### 29 — `embarch-ui`'s launcher moved into this extension

One sideloaded extension, so the silent drop a VS Code server update causes costs one reinstall (`./reinstall.sh`). 436 lines moved once: the same `EmbArch UI:` commands and `embarchUi.*` settings, **left to the standalone launcher while both are installed**, which the log says. `embarch-ui`'s own `vscode-extension/` is still in that repo ([open.md](../open.md)). **Rejected:** two extensions, and one script reaching across both repos.

### 23 — It ships whole

As the desk's v1 did (`embarch-desk` decision 21). **Rejected:** the library first (usable in Claude Code's panel at once), the panel first.

## Layout and look

### 17 — The list sits left, the chat right

The list behind its own activity-bar icon, the chat in the secondary sidebar where Claude Code's panel is, any chat also openable as an editor tab. **Rejected:** both stacked on the right (the list folds away), every chat a tab (chats compete with code).

### 21 — The webview is Preact bundled with esbuild

An event stream feeding a constantly changing UI renders better from state than by hand-patched DOM. About 4 KB. VS Code's theme variables give the surfaces; the accents are EmbArch's (53). **Rejected:** plain DOM (`embarch-ui` decision 2's posture), React (about 140 KB).

### 52 — The webviews' text is IBM Plex Sans, shipped in the extension

`embarch-ui`'s variable Latin file (45 KB) and its OFL licence ship in the `.vsix` and load from the webview's own origin under the existing CSP; code, diffs and tool output keep the editor's font. **Rejected:** VS Code's UI font, a CDN (`embarch-ui` decision 42's silent failure).

### 53 — EmbArch supplies the accents and semantics; VS Code keeps the surfaces

Amends 21's all-theme-variables colouring. In dark and light themes cyan marks buttons, links, focus and selection; blue, amber, green and red mark running, waiting, done and failed. High-contrast themes keep VS Code's colours. Measured in Firefox, every accent is at least 4.6:1 on VS Code's default sidebars. **Rejected:** `embarch-ui`'s full palette (a pane that matches no VS Code theme), VS Code-only colours, red as the accent (`embarch-ui` decision 25).

### 91 — The chat sits in a column, and steps indent under the prose

Shaped with the owner in three rounds of questions, 2026-10-26. Everything ran edge to edge inside an 8 px gutter: a wide editor tab gave lines too long to read, the sidebar felt tight, and prose, steps and cards all began at one edge. **A pane wider than the column centres it**: timeline, cards, status lines and composer share one column, 80 % of the pane and never under 56rem (about 730 px at 13 px), and the header stays full width as the pane's title bar. A fixed 56rem, as first built, left a maximised landscape window looking like a portrait screen [owner, same day]. The composer's top rule runs the pane's width; a turn's rule stops at the column. **Prose wraps at 64rem** (about 140 characters a line) inside the column, and code, tables and steps keep its full width. The owner's bubble ends at the column's right edge. **The gutter grows with the pane**, `clamp(8px, 2.5vw, 16px)`. Steps, folded runs and thinking sit one gutter in from the prose, and a subagent's report sits inside its step. The column is padding, `max(gutter, (100% − column) / 2)` with `column` = `max(56rem, 80%)`, so the timeline's scrollbar stays at the pane's edge. It is sized in rem, so the smaller text inside it does not narrow it. **Rejected:** a fixed column, at 56rem or 80rem; a left-anchored column; one width for prose and code (at 80 % of a 1600 px pane prose runs about 210 characters a line); wider gutters with no cap; a marker rail beside each block; the header inside the column; notes indented with the steps.

### 54 — "EmbArch" at the right of the status bar starts a chat, in the mark

A one-colour icon font (the E cut back a pixel from the A, edges snapped to the 16 px grid, generated by `tools/make_glyph.py`); the same shape is the sidebar icon, and a chat's editor tab shows the two-colour mark, one file per theme. **Rejected:** a codicon, the thin letters (the E fades at 16 px).
