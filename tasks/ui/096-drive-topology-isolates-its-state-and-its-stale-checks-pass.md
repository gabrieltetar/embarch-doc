# 096 — `drive_topology.py` stops writing the real recent-projects file, and its stale checks pass again

**State:** claimed by agent/ui/096-drive-topology-isolates-its-state, 2026-10-28 14:37
**Source:** refill sweep, 2026-10-28 leg — `embarch-ui/open.md`: "`tests/browser/drive_topology.py`
writes the real `~/.local/share/embarch/ui/recent-projects.json` without `EMBARCH_UI_STATE`; 3 of its
checks are stale since the Atlas tab."
**Scope:** ui
**Hardware:** none — a browser drive script against its own stub Core; geckodriver is installed.
**Owner:** no

## What

`tests/browser/drive_topology.py` launches `embarch-ui` without `EMBARCH_UI_STATE` (or a scratch
`XDG_DATA_HOME`), so every run rewrites the owner's real recent-projects list. `drive_links.py:112`
already shows the isolated shape. Give `drive_topology.py` the same isolation, and bring the checks
that went stale when the Atlas tab landed back to passing against today's UI, by fixing what each
one asserts rather than deleting it. If a check turns out to be asserting something the UI no longer
does on purpose, say which decision retired it, in the script's comment.

## Why now

Cheap, host-side, and a test that writes a real user file is one a person stops running. The
open.md bullet names both halves.

## Done when

- [ ] `drive_topology.py` runs with an isolated state path and never touches the real
      `recent-projects.json` (check by mtime before and after a run).
- [ ] Every check in it passes against a fresh build; the count before and after is in the task
      file's close note.
- [ ] The `open.md` bullet is removed (or narrowed to whatever is left), `changelog.d/` fragment
      dropped.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
