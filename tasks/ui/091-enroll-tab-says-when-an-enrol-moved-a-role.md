# 091 — The Enroll tab says when an enrol moved a role

**State:** claimed by agent/ui/091-enroll-tab-says-when-an-enrol-moved-a-role, 2026-10-26 04:12
**Doc reserve (dispatch, 2026-10-26):** `embarch-ui/spec.md` 9,099 / 10,240 B (1,141 B left, filed against `tasks/ui/089`, open) and `embarch-ui/open.md` 4,366 / 5,120 B (754 B left, filed against `tasks/ui/088`, blocked, In flux: yes). Prefer a decisions file; if you must write `open.md`, compact it in this unit carrying `ui/088`'s Must-not-delete list. **Test isolation, required:** `ui/083`'s ad-hoc run reached the owner's live desk on :4891 and possibly his real `XDG_DATA_HOME`. Every UI process you start uses `stub_core.py` (never live Core), `EMBARCH_DESK_PORT` set to a port nothing listens on, and scratch `EMBARCH_DESK_CONFIG_DIR`, `XDG_DATA_HOME` and `XDG_CONFIG_HOME`, as `tests/browser/README.md` now says. Never the default desk port, never the real desk config.
**Source:** embarch-api task 142 (api decision 87; `embarch-api` `9e4ca14`), on top of `embarch-core` decision 87. Filed from the worker's inbox drop `ui-enroll-result-shows-moved-role.md`, 2026-10-26.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-core-client`'s `EnrollProbeResponse` now carries optional `displaced`, `vacated` (both `EnrolledBoard`) and `vacated_kept` (bool), skipped when absent, plus `moved_roles_note()`. The UI re-serialises that mirror to the browser, so the fields already reach it when something moved. Have the Enroll tab show it (e.g. re-enrolling the dev-bench probe as `dut` vacated `dev-bench`).

## Why now

A user otherwise cannot tell a role moved; only a topology log line did.

## Done when

- [ ] The Enroll tab names the vacated/displaced role after an enrol that moved one (browser check against `stub_core.py`, which must learn to return the fields).
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); docs per `DOC-PROTOCOL.md`, `changelog.d/` fragment.
