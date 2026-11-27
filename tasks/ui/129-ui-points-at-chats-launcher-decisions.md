# 129 — ui points at chat's launcher decisions

**State:** open — `chat/052` landed: the chat decision is **123**, `embarch-doc/embarch-chat/decisions/launcher.md`.
**Source:** EMB-303 — The launcher's decisions sit in embarch-ui while its code lives in embarch-chat
**Issue:** EMB-303
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

The second of two units. `chat/052` restated `embarch-ui` decision 28's
launcher behaviour and invariants as **`embarch-chat` decision 123**
(`embarch-doc/embarch-chat/decisions/launcher.md`). It carried 28 whole; from
3, the thin-launcher stance and the rejected webview and TreeView (3's old
`vscode-extension/` subdirectory, `.vsix` and `reinstall.sh` packaging
paragraphs stayed with ui); from 101, the status-bar states and "every click
goes to `start()`" (the unit itself, its environment and the one-instance rule
stayed with ui; what the launcher does with the unit is chat 102). Chat 123 is
36 B under the per-decision cap, so this unit does not need to touch it. When
this is done:

- Ui decision 28's heading stays (numbers are permanent) and its body becomes a
  one-line pointer saying it moved to that chat decision, per
  `DOC-CONVENTIONS.md`'s rule for a moved decision's pointer.
- Decision 3's first paragraph no longer says the launcher lives in a
  subdirectory of `embarch-ui`; it says where it lives now (`embarch-chat`,
  chat decision 29) and keeps only what is still ui's.
- Decision 101 keeps what is about the UI service and points at chat for what
  chat 052 took from it.
- Any other ui doc that cites decision 28 for launcher behaviour cites the chat
  decision instead (a `grep -rn '28' embarch-doc/embarch-ui/` read by eye, and
  `scripts/check-decision-refs.py`).

**Not yours:** `embarch-doc/embarch-chat/` and `embarch-chat`. The untracked
`embarch-ui/vscode-extension/` directory on disk is the owner's.

## Done when

- [ ] Ui decision 28 is a pointer to the chat decision; decision 3 is true about
      where the launcher lives; 101 points at chat for the launcher's part.
- [ ] `python3 scripts/check-docs.py` green; `embarch-ui` code untouched unless
      a comment there cites decision 28 for launcher behaviour.
- [ ] `changelog.d/` fragment.
