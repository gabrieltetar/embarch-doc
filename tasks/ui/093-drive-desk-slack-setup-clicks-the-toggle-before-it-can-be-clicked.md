# 093 — `drive_desk_slack.py`'s setup clicks the Slack toggle before it can be clicked

**State:** open
**Source:** the 2026-10-26 06:01 leg, landing `ui/081` (`embarch-ui@35fa9da`). The worker reported 8/8; the supervisor's two re-runs on scratch ports (geckodriver 4933, UI 4898, stub desk 4996) passed every assertion they reached and then died in a scenario's *setup*: run 1 at scenario 2, run 2 at scenario 3.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`fresh()` in `tests/browser/drive_desk_slack.py` reloads the page, waits up to 15 s for the mention count without checking that the wait succeeded, and then clicks `#desk-slack-toggle`. On this machine geckodriver answered that click with `400 element not interactable: Element <button id="desk-slack-toggle"> could not be scrolled into view`, which the script raises as an `HTTPError` and exits on, so the scenarios after it never run. The assertions that did run all passed, so this is the harness and not the fix. Two likely causes, neither confirmed: the Desk tab is not laid out yet when the count arrives, or a pushed view re-renders the bar between the check and the click. `ui/092` fixed the same shape in `drive_topology.py` by polling for the state it needs instead of reading after a fixed wait.

**Also, from `ui/094`'s review (2026-10-26):** that unit moved this script onto `tests/browser/addr.py`
(`EMBARCH_GECKO_PORT`/`EMBARCH_UI_PORT`; see `tests/browser/README.md`), and its docstring's start-up line
(line 11 at `embarch-ui@954a24c`) came out as three lines run together, still naming the retired
`WEBDRIVER`. Rewrite it to the README's recipe while you are in the file. Run it only on scratch ports.

## Why now

The check is `ui/081`'s only evidence that a reply cannot go to the wrong Slack message, and a check that dies in setup two runs out of two here is evidence nobody can re-run.

## Done when

- [ ] `fresh()` waits until the toggle is displayed and clickable (or the bar is already open), and a wait that times out is reported as a named `FAIL`, not an uncaught `HTTPError`.
- [ ] Three consecutive full runs on scratch ports pass every check.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
