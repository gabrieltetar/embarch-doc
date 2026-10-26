# 091 — The Enroll tab says when an enrol moved a role

**State:** open
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
