# embarch-chat decisions: The VS Code launcher

**Status:** active, 2026-11-26.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 123 — The launcher is thin: Start shows the tab already open, and pre-flights the address

**Moved from `embarch-ui` decisions 3, 28 and 101 on 2026-11-26** (EMB-303), the launcher having lived here since 29. **Carried:** all of 28, 3's thin-launcher stance, and 101's status-bar states. **Stayed in `embarch-ui`:** 101's unit (`embarch-ui.service`, its environment, one instance by construction) and the old `vscode-extension/` packaging in 3. What the launcher does with the unit is 102.

**Thin.** It opens the UI in the system browser and reaches into the editor for convenience, not as a second UI to keep in sync. *Rejected: a VS Code webview* (CSP and localhost plumbing for never leaving the editor) and *a native TreeView* (a second presentation layer on the same JSON API).

**Start probes, then focuses.** A 400 ms loopback GET, true on any response, tells whether the address is answered, and by what: the unit, or something else. A focus attempt decides whether to open a tab, so Start no longer stacks duplicates. Nothing is spawned (102), so the probe's backstop is the status bar.

**The tab is activated, not reported**, through Windows UI Automation from WSL via `powershell.exe`: `SelectionItemPattern.Select()`, then `SetForegroundWindow`. Measured 0.41 to 0.54 s a round trip (1.7 s un-minimizing); the `AttachThreadInput` fallback for the foreground lock has never fired. **Four invariants, each a measured defect** (`src/launcher/focus.ts` carries the script):

- **`-cmatch 'Tab$'`, the `c` is load-bearing.** A `TabItem` search also finds page widgets and every Electron app on Chromium's window class (VS Code, Slack, Spotify), which end in lowercase `tab`; browsers' own end in `Tab` or `BraveTab`. `-match` ignores case, and a first attempt clicked an in-page widget.
- **Enumerate every window, never `FindFirst`.** Children come in z-order, so the handle varied by run; one browser owned four windows. Search first, raise the window whose strip holds the tab.
- **Restore only when `IsIconic`.** An unconditional `SW_RESTORE` demotes a maximized window.
- **Inline `-Command`, no `.ps1` shipped.** `Restricted` execution policy fails `-File` with `UnauthorizedAccess` and does not govern `-Command`; `-ExecutionPolicy Bypass` is not used.

**No browser is named:** windows match `Chrome_WidgetWin_1` (Brave, Chrome, Edge, Vivaldi, Opera). Chrome verified, Edge inferred, never opened; Firefox would be a second strategy, not a wider regex.

**One strategy behind a registry.** `FocusStrategy` (`supports()`, `focus(title)`) has one member, WSL plus Chromium on Windows; another topology is a new file and one registry line. Unsupported, or on any failure (no window, no matching tab, no `powershell.exe`, a timeout, a throw), Start opens a tab. **Focus is never the reason nothing opens**, it never notifies, and one output-channel line names the strategy.

**`<title>EmbArch</title>` is a load-bearing interface.** The match is exact, so no decoy is focused (a substring match on `embarch-ui` hit one). Renaming it is the original bug returning with no error; `assets/index.html` says so and `extension.ts`'s constant cites this decision. A tab's UIA `Name` is not the title: Brave appends `- Memory usage - 34.6 MB`, `- Audio playing` and the like, stripped before the otherwise exact comparison.

**Accepted:** UIA puts Chromium in accessibility mode, costing memory and CPU per tab; at 16 ms on a nine-window desktop it is very likely already on.

**Status-bar states** (with 102's unit): running; stopped; `(external)`, answering but not as the unit; `(not installed)`. Every click goes to `start()`, which focuses a running UI and starts a stopped one, never to `stop()`.

*Rejected: a notification saying it is already open* (answers another question; tab activation proved reachable), *a Chromium `--app` window* (hardcodes a browser, drops the tab strip), *a `chrome.tabs` extension* (a second artifact and a channel to it), *an SSE-subscriber-count endpoint* (a server change, and it still cannot raise anything).
