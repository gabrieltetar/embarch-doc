# 107 — A Desk tab session row whose folder is gone says so

**State:** open
**Source:** Linear issue EMB-117, filed by a worker
**Issue:** EMB-117
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A session row on the Desk tab whose folder no longer exists says so, in the place its Jump or chat button would be. Since `desk/016` (`embarch-desk` `377c116`, decision 71 amended) the desk marks such a row `folder_missing: true` and answers `folder_uri: null`, so the tab's buttons that need `folder_uri` drop off the row and nothing says why. A row whose folder exists is unchanged.

## Why now

A user looking for a chat whose folder a landing deleted sees the row lose its buttons with no reason given.

## Where to look

- `assets/desk.js` — the session row builder that draws Jump (`data-jump-folder`) and the chat button from `r.folder_uri` and `r.cwd` (around the `r.client === "embarch-chat"` branch)
- `embarch-doc/embarch-desk/interfaces/chat-routes.md` — the `folder_missing` field; it is `desk`'s, so read it, do not edit it

## Dispatch notes

- One file of code. Say it in the row's own words, for example "folder gone" with the path in its title; no new style is needed if an existing muted class fits.
- Burndown is on: no new numbered decision. None should be needed; if an existing `embarch-ui` decision describes the session row's buttons, amend it in place.
- No `embarch-ui` doc in `embarch-doc` is in reserve. Decision entries near their limit (bytes left): `launcher#28` 22, `tab-folders#100` 113. Leave those two alone unless this task needs them.

## Done when

- [ ] A session row whose `folder_missing` is true says its folder is gone where its Jump or chat button would be.
- [ ] A row whose folder exists is unchanged.
- [ ] Gate green (`../../embarch-fleet/gate.md`, the Rust bullet); `changelog.d/` fragment dropped.
