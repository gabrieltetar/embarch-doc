# embarch-ui: spec

**Status:** active, 2026-09-20. Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md). What a capture means once it reaches the browser: [spec/capture-rendering.md](spec/capture-rendering.md). What each tab does: [spec/tabs.md](spec/tabs.md).

## What it is

The one place a firmware engineer looks to exercise suite features **by hand** — day to day, not just when an agent needs a hardware read. It replaced three ad hoc surfaces rather than adding a fourth — `embarch-topology`'s board view, `embarch-study-designer`'s standalone builder, Core's enroll page.

It is **not** a build-toolchain project, a VS Code webview, a second owner of hardware mutation, or a replacement for `embarch-api`'s MCP/CLI surface — agents keep talking to `embarch-api`. It does *invoke* a build, through the same crate `embarch-api` does: owning the machinery and calling it differ.

## Shape

```
embarch-ui (one Rust binary, axum, zero-build)
  |
  +-- links embarch-study-designer  (action list, custom-action registry, study
  |                                  building, trace decode — pure data, no I/O)
  +-- links embarch-core-client     (one impl of "reach Core over HTTP+Bearer",
  |                                  shared with embarch-api)
  +-- links embarch-firmware-build  (config, west scan, target resolution and
  |                                  the build — also shared with embarch-api;
  |                                  a subprocess and files, no hardware)
  +-- links embarch-topology transitively only, `software` feature only, never
  |   `hardware` (decisions/wiring.md)
  |
  +-- HTTP + Bearer --> embarch-core
        every hardware-adjacent call, read or write — both halves of a role,
        signals, ports, alerts, status, dev-bench, chip resolution, the whole
        /study family, and POST /flash + POST /reset where a study builds its
        own DUT firmware (build local, flash/reset not), plus GET /logs/recent
        and nothing else under /logs. Which UI route reaches which: interfaces.md.
```

`vscode-extension/` (thin, TypeScript) pre-flights the address, spawns/stops the binary, and shows the page in the system browser, focusing the window and tab already open (28). It renders nothing itself.

**The `hardware` feature is the one it must never link:** a board read done in-process would enumerate whichever machine `embarch-ui` runs on, not Core's.

## The five tabs

One persistent left sidebar, one top status bar, client-side navigation by URL fragment (`#topology`, `#live-study`). **The open project is shell furniture, at the foot of the sidebar** (46): one firmware repo at a time, named on every tab and changed from a dialog the Study Designer's own card also opens. A fragment names a tab and nothing else (31). **A retired fragment resolves to the tab that absorbed it**, never to the last one that browser had open: `#enroll` is `#topology` (43). What each tab does: [spec/tabs.md](spec/tabs.md).

## Invariants

- **Every hardware-adjacent call, read or write, goes over HTTP+Bearer to Core.** Verified structurally: neither `probe-rs` nor `serialport` is in `cargo tree -e normal`. **A firmware build is not one of them** — `west` in a subprocess and files on disk, though flash and reset still go to Core.
- **Everything live reaches the browser as SSE** served by this binary; no client-side interval polling (no `setInterval` in `app.js`). Where a source has no push surface the polling is server-side, unseen by the browser.
- **A snippet list is ordered end to end**: picker, stored `Study` and `west -S` are one sequence, sorted into a set by nothing (reversals 114). **A saved study's `firmware_version` is rewritten only after a waved-through mismatch, never over `any`** (40).
- **The UI never decides which version provenance counts as verified** — answered server-side and rendered, never re-derived in JS.
- **A limit enforced server-side is *served*, never restated in `app.js` — and so is a vocabulary.** Action entries and labels, scalar types, log levels and their prose, caps, advisory dev-bench capacities and outpost header-flag names all come from the crate ([`embarch-study-designer` decision 73](../embarch-study-designer/decisions/authoring.md)); a test asserts `app.js` holds no copy. **An empty served vocabulary is an empty picker, i.e. a refusal**, never a guessed list.
- **An advisory capacity never gates**: dev-bench caps come from a build that may not be the bench in front of you, so a study past one says so and Run stays enabled. **One this tab could not read renders as *unknown*, never as "within caps"**; `POST /preflight` builds the list, two of three uncomputable in a browser.
- **A destructive edit that would break a saved study is refused, naming the studies.** Deleting or renaming a registered action, payload layout or `.eap` file scans `embarch/studies/` first and answers `409` with the studies and steps, leaving the form filled. **A file the scan cannot read is unscannable, never "no references"**: a directory it cannot fully read is not permission to delete.
- **One firmware repo is open at a time, and the shell says which** (46): the control is at the foot of the sidebar, the picker behind it is the only one, and every "no project open" refusal names it. Switching reloads every project-scoped surface — catalog, saved benches, studies, taps — because they describe the repo that was open a moment ago.
- **A role is a fixed slot holding two independent bindings** (44, 45): which **probe** serves it, and which **board type** is in it. A probe moves between boards and only two are ever identified, so neither is an attribute of the other and either can be declared alone. A **board type is a shape**, listed in the open repo's `embarch/boards.toml`, which **Rescan can only add to**; the dev-bench picker is the suite's own supported pair.
- **A catalog row lists what this repo can build it as** (47): its revisions and its variants — **not its apps, which are the study's axis** (49) — the pinned combination marked and a pin the scan no longer backs marked as stale. Never a cross product: Zephyr backs a pair only where a file does. The board type goes to Core; **the combination goes to `embarch/boards.toml` and Core is never told a revision**.
- **Picking a board type opens nothing**, and **leaves a stale `hardware_id` in place** so a validate pass can say the silicon no longer matches. Binding a probe is the only act that reads an identity, attaching as that board type's chip — **looked up, never typed** (48): a row stating none takes its targets' SoC through Core's `/resolve-chip`; a stated chip wins, nothing is written back, and an unanswerable one refuses here.
- **A page explains nothing it can show** (50): under a title, a path or state is the only note.
- **A diagram status is written only by a Validate pass**, keyed by role and dropped when that role's bindings change: a badge moving on the five-second poll would claim a check nobody ran.
- **Loading a saved bench never touches hardware** (44): `embarch/topologies/<slug>.toml`'s signals and dev-bench link are re-declared, and each enrolment is *proposed* for a human to confirm through the ordinary enroll — a file on disk is not evidence about what is plugged in.
- **Validate topology says what it checked and what it cannot.** A role is a live hardware-ID re-read; one missing either binding is *empty*, not failed; **a guessed dev-bench port is a warning, never a pass**; a signal route is checked only as far as declared, and says so. Core's reason is verbatim; a leftover role's finding carries the only control that clears it.
- **A study stores no board, variant or revision** (45): a run builds for the board type in the **DUT role**, read at the moment it runs, so a saved study follows the bench. It is not silently reinterpreted — the override is announced on the build log.
- **Unreadable renders as unreadable, not as a mismatch or empty list.** A bench not plugged in has no version to disagree with; a Core answering `404` to the signals route has not said there are no signals.

## Verification technique

**"Tested in Rust, never looked at" is how this UI's worst defects hid**, so `tests/browser/` is the one to reach for: a headless-Firefox harness driving the **running binary** through geckodriver against a stub embarch-core. The assets are `include_str!`-embedded, so the deployed artifact is the only thing that can be checked, and a state a bench will not produce on demand is testable. `drive.py` covers Live Study, `drive_build.py` the Build card and builds source, `drive_topology.py` the diagram, `drive_fonts.py` every page; `tests/browser/README.md` has the shape. **`tests/element_ids.rs`** (24) is the static half, catching the one shape a text scan can: no id declared twice, no id lookup dangling.
