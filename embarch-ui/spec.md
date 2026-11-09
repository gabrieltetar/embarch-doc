# embarch-ui: spec

**Status:** active, 2026-09-20. Repo: [gabrieltetar/embarch-ui](https://github.com/gabrieltetar/embarch-ui).

What is true now. Why: [decisions.md](decisions.md). Unresolved: [open.md](open.md). Reference: [interfaces.md](interfaces.md). What a capture means once it reaches the browser: [spec/capture-rendering.md](spec/capture-rendering.md). What each tab does: [spec/tabs.md](spec/tabs.md). The bench editor's model, files and canvas: [spec/bench.md](spec/bench.md); editing a bench: [spec/bench-editing.md](spec/bench-editing.md); making one live: [spec/bench-live.md](spec/bench-live.md).

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
  +-- reads <project>/embarch/atlas/ (the Atlas tab: files only, no Core call)
  |
  +-- HTTP + Bearer --> embarch-core
        every hardware-adjacent call, read or write — both halves of a role,
        signals, ports, alerts, status, dev-bench, chip resolution, the whole
        /study family, and POST /flash + POST /reset where a study builds its
        own DUT firmware (build local, flash/reset not), plus GET /logs/recent
        and nothing else under /logs. Which UI route reaches which: interfaces.md.
```

It runs as the systemd user service `embarch-ui.service`, one per machine with or without a VS Code window, written by `embarch-ui service install` and binding its address before anything else starts (101). The launcher (`embarch-chat` decisions 29, 102) reads that unit, starts, stops and restarts it through `systemctl --user`, and shows the page in the system browser, focusing the open window and tab (28). It renders nothing itself.

**The `hardware` feature is the one it must never link:** a board read done in-process would enumerate whichever machine `embarch-ui` runs on, not Core's.

## The six tabs

Plus any from a tab folder (100). Navigation, the sidebar, the UI's desk as shell furniture and fragment routing (`#topology`, `#live-study`, retired `#enroll`, `#dashboard`; 43, 46, 56–58), and what each tab does: [spec/tabs.md](spec/tabs.md).

## Invariants

- **Every hardware-adjacent call, read or write, goes over HTTP+Bearer to Core.** Verified structurally: neither `probe-rs` nor `serialport` is in `cargo tree -e normal`. **A firmware build is not one of them** — `west` in a subprocess and files on disk, though flash and reset still go to Core.
- **Everything live reaches the browser as SSE** served by this binary; no client-side interval polling (no `setInterval` in `app.js`). Where a source has no push surface the polling is server-side, unseen by the browser.
- **A snippet list is ordered end to end**: picker, stored `Study` and `west -S` are one sequence, sorted into a set by nothing (reversals 114). **A saved study's `firmware_version` is rewritten only after a waved-through mismatch, never over `any`** (40), in the run's own repo.
- **The UI never decides which version provenance counts as verified** — answered server-side and rendered, never re-derived in JS.
- **A limit enforced server-side is *served*, never restated in `app.js` — and so is a vocabulary.** Action entries and labels, scalar types, log levels and their prose, caps, advisory dev-bench capacities and outpost header-flag names all come from the crate ([`embarch-study-designer` decision 73](../embarch-study-designer/decisions/authoring.md)); a test asserts `app.js` holds no copy. **An empty served vocabulary is an empty picker, i.e. a refusal**, never a guessed list.
- **An advisory capacity never gates**: dev-bench caps come from a build that may not be the bench in front of you, so a study past one says so and Run stays enabled. **One this tab could not read renders as *unknown*, never as "within caps"**; `POST /preflight` builds the list, two of three uncomputable in a browser.
- **A destructive edit that would break a saved study is refused, naming the studies.** Deleting or renaming a registered action, payload layout or `.eap` file scans `embarch/studies/` first and answers `409` with the studies and steps, leaving the form filled. **A file the scan cannot read is unscannable, never "no references"**: a directory it cannot fully read is not permission to delete. Every declared `.eap` block is scanned; **an unparseable taps sidecar refuses the load.**
- **One desk, and so one firmware repo, is open at a time, and the shell says which** (46, 57): the control is at the foot of the sidebar, the picker behind it is the only one, and every "no project open" refusal names it. Switching reloads every project-scoped surface — catalog, saved benches, studies, taps — because they describe the repo that was open a moment ago.
- **Roles, bindings and the catalog row** (44, 45, 47, 48, 49): a role is a fixed slot holding two independent bindings, a probe and a board type; a catalog row lists what the repo can build the type as; picking a type opens nothing, and a probe binding looks its chip up, never typed. Rules: [spec/roles.md](spec/roles.md).
- **The Atlas tab draws what the atlas wrote and decides nothing** (52): no Core call, no write but a page-render cache (54); vocabulary, clusters and positions come from `graph.json`.
- **A page explains nothing it can show** (50): under a title, a path or state is the only note.
- **A diagram status is written only by a Validate pass**, keyed by role and dropped when that role's bindings change: a badge moving on the five-second poll would claim a check nobody ran.
- **Making a bench live never enrols** (44, 90): `embarch/topologies/<slug>.toml`'s declarations are applied, and each enrolment is *proposed* for a human to confirm through the ordinary enroll — a file is not evidence about what is plugged in.
- **A signal origin is a role or a bench board** (67): the table shows a board by its enrolled name; the dialog picks either, sends one, and a board-origin signal re-saves on its board.
- **Validate topology says what it checked and what it cannot.** A role is a live hardware-ID re-read; one missing either binding is *empty*, not failed; **a guessed dev-bench port is a warning, never a pass**; a signal route is checked only as far as declared, and says so. Core's reason is verbatim; a leftover role's finding carries the only control that clears it.
- **A study stores no board, variant or revision** (45): a run builds for the board type in the **DUT role**, read at the moment it runs, so a saved study follows the bench. It is not silently reinterpreted — the override is announced on the build log.
- **Unreadable renders as unreadable, not as a mismatch or empty list.** A bench not plugged in has no version to disagree with; a Core answering `404` to the signals route has not said there are no signals.
- **A tab comes only from the user's own config** (100).

## Verification technique

**"Tested in Rust, never looked at" is how this UI's worst defects hid**; the headless-Firefox harness in `tests/browser/` is the fix: [spec/verification.md](spec/verification.md).
