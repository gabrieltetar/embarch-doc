# embarch-ui decisions: The VS Code launcher

**Status:** active, 2026-09-02.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 3 — VS Code integration is a thin launcher, not an embedded webview or a native VS Code UI

It manages the `embarch-ui` server process and opens it in the system browser. *Rejected: a VS Code Webview* — real CSP and localhost-connect plumbing, in exchange for never leaving the editor. *Rejected: a native TreeView built from VS Code's own toolkit* — **a second presentation layer hitting the same JSON API.** Neither matched the actual ask, which was **reach into the editor for convenience, not a second UI to keep in sync with the first.**

**It lives in a subdirectory of `embarch-ui`, not a sibling repo** — matching decision 1's own framing, and no marketplace packaging constraint forces a split: the packaging tools all work rooted at a subdirectory. A real TypeScript tree with start/stop commands, a status-bar toggle, and settings for binary path, host, port, config path and auto-start. **Since 2026-10-23 the launcher ships inside `embarch-chat`'s extension** (`embarch-chat` decision 29), commands and settings unchanged, and that repo's `./reinstall.sh` is its recovery path; that extension is a webview, which `embarch-chat` decision 6 sets against this decision for it alone. `vscode-extension/` below is the old copy, still in this repo.

**Distribution is an internal `.vsix` only, never the public Marketplace**, matching the suite's single-engineer, not-yet-public posture: a listing would need a publisher account, which does not exist (the icon does, as of 2026-09-09 — decision 25). **The consequence of sideloading is that nothing reinstalls it**: a VS Code server update re-provisions its extensions directory and drops the extension silently, while the `embarchUi.*` settings survive in the client's own settings — so the symptom is the three commands quietly absent from the palette, with no error, which reads as a deleted command rather than a missing extension. `vscode-extension/reinstall.sh` is the recovery path and is idempotent. **It does not use `vsce`**, which needs an `npm` and a network this bench does not have: it borrows the `node` bundled inside the VS Code server to compile, and writes the `.vsix` with python's `zipfile` — the manifest is generated from `package.json`, pinning `ExtensionKind` to `workspace` so the extension runs remote-side, where the Linux binary it spawns actually is.

**Verified by packaging and installing it for real**, which found one gap: packaging **refused over a relative license field pointing outside the packaged subdirectory**, fixed by copying the license in and naming it plainly. There was no `node` on this bench at all, resolved at the time with a user-local portable Node; that Node is gone as of 2026-09-09 and the server's bundled one replaced it. The remote-CLI shim here does not support an Extension Development Host, so **a real install of the `.vsix` — exactly the chosen distribution path — stood in for one.** Live-confirmed by the repo owner afterwards in their own Windows VS Code over Remote-WSL against the real debug binary.

### 28 — Start shows the window and tab already open, and pre-flights the address instead of inferring from a failed bind

Decision 3's launcher opened a tab on **every** `EmbArch UI: Start`, stacking duplicates, and saw a server started elsewhere only after a spawn failed to bind. Now a 400 ms loopback GET, true on any response, decides whether to spawn; a focus attempt, whether to open a tab. Spawn-then-infer stays as the backstop for a port race.

**The tab is activated, not reported**, via Windows UI Automation from WSL through `powershell.exe`: `SelectionItemPattern.Select()`, then `SetForegroundWindow`. Measured **0.41–0.54 s** a round trip (1.7 s un-minimizing); the `AttachThreadInput` fallback for the foreground lock has never fired.

**Four invariants, each a measured defect:**

- **`-cmatch 'Tab$'` — the `c` is load-bearing.** A `TabItem` search also finds page widgets and every Electron app sharing Chromium's window class (VS Code, Slack, Spotify), all ending in lowercase `tab`; the browser's end in `Tab` or `BraveTab`. `-match` ignores case; a first attempt clicked an in-page widget.
- **Enumerate every window, never `FindFirst`**: children come in z-order, so handles varied by run; one browser owned four windows. Search first, raise the window whose strip holds it.
- **Restore is gated on `IsIconic`**: an unconditional `SW_RESTORE` demotes a maximized window.
- **Inline `-Command`, no `.ps1` shipped**: `Restricted` execution policy fails `-File` with `UnauthorizedAccess` but does not govern `-Command`. `-ExecutionPolicy Bypass` is not used.

**No browser is named**: windows match `Chrome_WidgetWin_1`, covering Brave, Chrome, Edge, Vivaldi and Opera. Chrome verified; Edge inferred, never opened. Firefox would be a second strategy, not a wider regex.

**One strategy behind a registry.** `focus.ts`'s `FocusStrategy` (`supports()`, `focus(title)`) has one member, WSL plus Chromium on Windows; native Linux (AT-SPI), native Windows or macOS is a new file and one registry line. Unsupported, or on any failure — no window, no matching tab, no `powershell.exe`, a timeout, a throw — Start opens a tab as before. **Focus is never the reason nothing opens**; it never notifies; one output-channel line names the strategy.

**`<title>EmbArch</title>` is a load-bearing interface.** The match is exact, so no decoy tab is focused — a substring match on `embarch-ui` hit one in testing. Renaming it is **the original bug returning with no error**; `assets/index.html` says so; `extension.ts`'s constant cites this decision. Short, it fits a tab (Brave truncates near 46 characters) and keeps an em dash off the command line. **A tab's UIA `Name` is not the title**: Brave appends `- Memory usage - 34.6 MB`, `- Audio playing`, …, which break an equality test intermittently; they are stripped before the otherwise exact comparison.

**Accepted:** UIA puts Chromium in accessibility mode, costing memory and CPU per tab; at 16 ms on a nine-window desktop it is very likely already on here.

**A third status-bar state, `embarch-ui (external)`**: answering, not spawned by this window, formerly `(stopped)`. Its click goes to `start()`, which focuses, not `stop()`, which can only kill this extension's child.

*Rejected: a notification saying it is already open* — answers a different question; an earlier draft did, claiming tab activation unreachable, which measurement disproved. *Rejected: a Chromium `--app` window* — exact focus, but hardcodes a browser and drops the tab strip and address bar. *Rejected: a `chrome.tabs` browser extension* — most reliable and matches on URL, at a second artifact plus a channel to it. *Rejected: an SSE-subscriber-count endpoint* — real liveness, at a server change plus a keepalive staleness window, and it still cannot raise anything.
