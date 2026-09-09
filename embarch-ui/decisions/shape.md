# embarch-ui decisions: Shape and stack

**Status:** active, 2026-09-02.

One consolidated process replacing three ad hoc UIs, with no build toolchain.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 1 — One consolidated process, not a shared library three separate binaries keep depending on

The same "one implementation, many call sites" shape `embarch-topology` decision 8 established for topology detection — except **here the consolidation is the UI surface itself**, not just the logic behind it. `embarch-topology`'s and `embarch-study-designer`'s standalone UI binaries (413 and 812 lines) are retired outright, and Core's enroll page's HTML moves out of Core, which keeps the enroll endpoint it already had. Settled on the repo owner's own framing: "1 UI for the whole project, just like the topology project centralized all topology from the suite."

### 2 — Zero-build, Rust-served HTML — pushed to a real design system rather than replaced with a framework

The alternative was weighed on its actual merits: an SPA framework plus a bundler, with the built bundle vendored into the Rust binary so the *end user* still runs one binary — buying a real component/chart/table ecosystem and a faster path to polish, against **a second toolchain at build time, new CI legs, new supply-chain surface, and an explicit break of the suite's "Rust, one toolchain" principle.** Decided against, with the corollary that matters: **stop treating plain unstyled HTML as the ceiling** and actually invest in hand-rolled CSS, type and component design. Confirmed against real mockups (decision 8) before committing further.

### 3 — VS Code integration is a thin launcher, not an embedded webview or a native VS Code UI

It manages the `embarch-ui` server process and opens it in the system browser. *Rejected: a VS Code Webview* — real CSP and localhost-connect plumbing, in exchange for never leaving the editor. *Rejected: a native TreeView built from VS Code's own toolkit* — **a second presentation layer hitting the same JSON API.** Neither matched the actual ask, which was **reach into the editor for convenience, not a second UI to keep in sync with the first.**

**It lives in a subdirectory of `embarch-ui`, not a sibling repo** — matching decision 1's own framing, and no marketplace packaging constraint forces a split: the packaging tools all work rooted at a subdirectory. A real TypeScript tree with start/stop commands, a status-bar toggle, and settings for binary path, host, port, config path and auto-start.

**Distribution is an internal `.vsix` only, never the public Marketplace**, matching the suite's single-engineer, not-yet-public posture: a listing would need a publisher account and a real icon, neither of which exists. **The consequence of sideloading is that nothing reinstalls it**: a VS Code server update re-provisions its extensions directory and drops the extension silently, while the `embarchUi.*` settings survive in the client's own settings — so the symptom is the three commands quietly absent from the palette, with no error, which reads as a deleted command rather than a missing extension. `vscode-extension/reinstall.sh` is the recovery path and is idempotent. **It does not use `vsce`**, which needs an `npm` and a network this bench does not have: it borrows the `node` bundled inside the VS Code server to compile, and writes the `.vsix` with python's `zipfile` — the manifest is generated from `package.json`, pinning `ExtensionKind` to `workspace` so the extension runs remote-side, where the Linux binary it spawns actually is.

**Verified by packaging and installing it for real**, which found one gap: packaging **refused over a relative license field pointing outside the packaged subdirectory**, fixed by copying the license in and naming it plainly. There was no `node` on this bench at all, resolved at the time with a user-local portable Node; that Node is gone as of 2026-09-09 and the server's bundled one replaced it. The remote-CLI shim here does not support an Extension Development Host, so **a real install of the `.vsix` — exactly the chosen distribution path — stood in for one.** Live-confirmed by the repo owner afterwards in their own Windows VS Code over Remote-WSL against the real debug binary.

### 9 — Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui), created empty

Matching how `embarch-umbrella`, `embarch-topology` and `embarch-dev-bench` each started: the path dependencies decision 5 requires **needed a real repo to exist before implementation could begin in earnest.**
