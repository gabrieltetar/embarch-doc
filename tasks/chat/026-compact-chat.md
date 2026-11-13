# 026 — `embarch-chat/decisions/sessions.md` is in reserve

**State:** done
**Source:** the EMB-91 landing added decision 105 to `decisions/sessions.md` beside 103's as-built text and left it at 11,394 of 12,288 B.
**Reserve at dispatch (2026-11-12):** `decisions/sessions.md` is now 12,745 of 12,288 B, 457 B over: the owner's decisions 106 (EMB-161) and 100's amendment (EMB-162) landed in it since filing, so check which decisions it holds before choosing the group to move. Also near its limit: `decisions/promptu.md` (decision 96), 204 B left; leave it alone.
**Scope:** chat
**Hardware:** none
**Owner:** no

**Compacts:** embarch-chat/decisions/sessions.md
**Size debt due:** 2026-11-17
**In flux:** no for a verbatim split, which restates nothing. Rewording waits: 103 was built on 2026-11-09 and 105 decided the same day, and neither has run in a live panel.
**Must not delete:** any decision's text or number; a decision moves whole, and `decisions.md`'s group index names its new file.

## What

Bring `decisions/sessions.md` out of reserve by a verbatim split: move whole decisions (the login, desk and handoff ones, 101, 103 and 105, are one candidate group) to a new group file under `decisions/`, and update the group table in `decisions.md`.

## Why now

`check-doc-size.py` fails on a file in reserve with no debt filed; adding decision 105 spent the reserve.

## Done when

- [x] `decisions/sessions.md` is clear of reserve (`scripts/check-doc-size.py --pressure` shows it not at all), or a successor re-files with a concrete plan.
- [x] Every moved decision is byte-identical in its new file, and `check-decision-refs.py` resolves every `decision N`.
- [x] Gate green (`../../embarch-fleet/gate.md`).

## Result

Moved 101, 103, 105 and 106 whole and verbatim to `decisions/logins.md` (6,463 B); `sessions.md` is 6,673 B (was 12,745 of 12,288), `check-doc-size.py --pressure` reports it PAID. `decisions.md`'s group table names the new file and marks the four moved. `check-docs.py` and `check-ownership.py --scope chat` green.

**Compaction question** (can `spec.md` alone answer what someone needs to work on this component today?): not asked of `spec.md`, because a verbatim split touches only `decisions/`; `spec.md` was not edited and nothing in it was cut, so its answer is what it was before. Nothing was deleted, so no cut needs quoting.
