# ui: history

**Status:** active, 2026-09-02. Assembled from `changelog.d/` fragments by `scripts/build_changelog.py`; newest window first. Capped at 20 KB: over that, whole windows roll off the end, oldest first — never the newest, so a single over-cap window stays and says so — into [archive/](archive/).

## 2026-11

### Added
- ui: the Desk tab draws the weekly Promptu sheet: bar count, numbers, groups, lines with ✓/✕ and notes, the feel line and Apply; hidden at open 0 ([shell 56](../embarch-ui/decisions/shell.md)).
- The Desk tab shows an agent's GitHub review-replies draft, one editable box per thread, and the posted URLs after Send (EMB-205).

### Changed
- Compacted ui decisions/shell.md and spec/tabs.md: decisions 58, 59 moved to page-links.md and the Tab folders text to spec/tab-folders.md, verbatim.
- The Study Designer keeps a loaded study's declared measurements through save, run and pre-flight, lists their names, and refuses a save with ones the crate rejects (ui decision 104).
- embarch-ui sends Core the person's token, not the agent's; a missing person token stops the UI at start ([decision 103](../embarch-ui/decisions/core-token.md)).
- embarch-ui reads embarch-ui/config.toml under the user config dir when EMBARCH_UI_CONFIG is unset; `service install` names its config ([102](../embarch-ui/decisions/ui-config.md)).
- The Study Designer reads the bench's build from `dev_bench_version`; against a Core that does not send it, the build shows as unavailable.
- A Desk tab session row whose folder was deleted says "folder gone" where its Jump or Open chat button was, instead of losing the button silently.
- embarch-ui's README points at embarch-chat's launcher and describes its status bar states.
- embarch-ui: spec.md and open.md compacted by moving role/catalog invariants and trace open items to spec/roles.md and open/trace.md.
- A tab.toml must name label, icon (an .svg) and panel; a tab missing one is left off the page and logged.

### Fixed
- The Desk tab counts a note as the desk does (U+0085 trimmed, U+FEFF kept), and its desk-switch warning survives typing and says "nothing was added" only after an Add.
- The Desk tab's Pick up title and empty note say "no card on the board": the list also shows an issue whose card the view window hides (EMB-115).

### Removed
- Removed four embarch-ui routes nothing called: topology role-board, link, profile apply, and study-designer GATT data; they answer 404 (EMB-311).
## 2026-10

### Added
- A link into the page selects what it names: `#desk?item=`, `#live-study?study=`, `#topology?board=` (decision 58, amending 31). Deployed 2026-10-25.
- Atlas tab: the open project's `embarch-atlas` graph as a stack map, every part a generic symbol with net and firmware names, citations to page and code line (decisions 52-54).
- Desk tab: a + continuation card for time after a ✓, its dialog adding to the sent entry (embarch-desk decision 64).
- The validate pass and dashboard show a bench board by name instead of as a leftover role (decision 55).
- embarch-ui: `tests/browser/drive_prompt.py` renders the operator-prompt modal headless against a prompting host study in `stub_core.py` (decision 69).
- A host study's operator prompt opens a modal on any tab with a countdown, Confirm and Cancel and a sound; the UI now follows studies started elsewhere.
- ui: a saved study that carries an out-of-date `.eap` protocol shows an advisory note in the Study Designer tab (changed/gone, with differences); it still runs as saved. ui decision 68.
- Topology tab: picking one of several ports under one USB serial declares its interface; validate fails a direct route those ports share with none declared (decision 10; suite/052).

### Changed
- The Dashboard tab is gone; the Desk replaces it (decision 56), backed by the new embarch-desk.
- The Desk tab deals waiting time tiles into a hand under the Slack bar; a work card keeps a chip per day (embarch-desk decision 57).
- The VS Code launcher ships inside embarch-chat's extension (embarch-chat decision 29); vscode-extension/ is the old copy.
- The open project became the open desk; opening one proposes its saved bench (decision 57).
- ui: the Topology signals table names a bench-board origin and the signal dialog can pick one, keeping it on re-save (decision 67).
- Split embarch-ui decision 37 (Time chart live feed) verbatim out of decisions/time-chart.md into time-chart-live.md; the Time chart file is out of reserve (ui/095).
- `embarch-ui/spec.md` back in reserve: the tab-navigation paragraph lives only in `spec/tabs.md` now, at its newer wording (ui/089).
- Browser drive scripts read geckodriver/UI ports only via EMBARCH_GECKO_PORT / EMBARCH_UI_PORT (tests/browser/addr.py); old names error ([decision 65](../embarch-ui/decisions/browser-drive.md)).
- `build_and_flash` now logs why it built the board it did on every path, and the stored build log keeps the version, board, flash and reset lines, including a flash failure.
- The enrol dialog now says when an enrol vacated or displaced a role, in Core's own sentence ([decision 61](../embarch-ui/decisions/topology-roles.md)).
- Tile dialog sends hours only when edited; new Use computed button clears the override (ui decision 59).
- embarch-ui open.md compacted 5,117 to 4,366 B: settled halves removed (already in decisions 21, 34, 37, 38), Debug-level hardware result moved into decision 32.

### Fixed
- `ui` live-tail diff republishes a grown trailing line instead of dropping it, and no longer replays a sent line when the line repeats earlier — decision 70.
- Desk tab: Start work says what happened on the card pressed, under its button; a pushed view no longer hides a failed start (it read as nothing at all).
- The Topology tab redraws its diagram when the board-type pickers answer, so the bench box shows its label on first draw, not the raw qualifier.
- Topology browser drive script now isolates the recent-projects file and passes all 81 checks.
- The Time chart now says when a sample strip or live mark lane is capped, how many were not drawn and how far the strip reaches ([decision 66](../embarch-ui/decisions/time-chart.md)).
- Desk Slack browser driver waits for the toggle and reports a setup timeout as a named FAIL, not a crash.
- A Data card's table is re-fetched when it loads, so a study opened mid-run no longer ends on the partial table; see [embarch-ui decision 64](../embarch-ui/decisions/live-study.md).
- Desk Slack reply goes to the message it was drafted for, not what now sits at that list position; a message gone from the list is not sent to ([decision 63](../embarch-ui/decisions/shell.md)).
- Topology: Validate no longer says every check passed over a warning or an empty bench; /api/enroll refuses a board with no chip itself, like the role route (ui decision 48).
- Console: a Text tap that never sends a newline now publishes its partial line as cut lines at 8 KB instead of growing and re-sending it for the whole run (decision 32).
- Live Study: a slow read for a study no longer open is dropped, and a project switch reloads the saved-study picker.
- A live study's badge reads `running N/M` from the first step instead of `pending` for the whole run; see embarch-ui/decisions/live-study.md decision 33.
- Saved-study write-back stays in the run's repo, an unreadable taps sidecar refuses the load, and .eap delete scans every declared block (ui/084).
