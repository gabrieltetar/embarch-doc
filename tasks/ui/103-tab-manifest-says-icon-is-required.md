# 103 — A tab manifest says `icon` is required

**State:** open
**Source:** Linear issue EMB-8, filed by the fleet: check that the tab folder docs say a manifest must name an icon
**Issue:** EMB-8
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

A reader of the manifest section in `embarch-ui/interfaces.md` ("Tab folders") learns, in that one place, that `tab.toml` must name an `icon`, and what happens to a tab whose manifest does not: it is left off the page and logged, and the other tabs still work.

Doc only, in `embarch-doc`. The code already does this, and this task does not change it.

## Why now

The manifest section shows `icon` as an example key and says what it does, and it never says the key is required. `embarch-ui/spec/tabs.md` has no word on it. Someone writing their first tab sees the tab vanish and has to find the reason in the UI's log.

This is also the first task through the fleet's Linear intake since `inbox/` was retired on 2026-11-03, so it carries `Issue:` and `finish` should move the issue to Done when the fold retires this file.

## Read this first

What the supervisor read at the split, to be checked against `src/tabs.rs` rather than taken from here:

- `Manifest.icon` is a `String` with no `#[serde(default)]`, so a manifest without it fails `toml::from_str` in `load`.
- The callers log `tab <id> is left out: <error>` and leave that tab off the page. `spec/tabs.md` already says the general form: "A tab that cannot be read is left off the page and logged, and the rest still work."
- `a_broken_tab_is_left_out_and_the_others_stay` covers a typo key, a missing panel file, a bad backend and a relative folder. It has no missing-`icon` case, so the behaviour for this exact manifest is read from the type, not from a test. If you state it, it has to be true from the code.

`label` and `panel` have the same shape, and the example marks `scripts`, `styles` and `backends` as optional. One sentence covering the required keys is fine if it reads better than one naming `icon` alone. Nothing wider than that: the rest of the section is out of scope.

## Dispatch notes

- **No code change.** The `embarch-ui` worktree is there to read. Leave it clean and do not push it; the supervisor lands the doc branch alone.
- **No new decision.** This states existing behaviour. `embarch-ui/decisions/tab-folders.md` decision 100 has 113 B left against its limit and this unit has no reason to touch it.
- Neither doc is in reserve. `embarch-ui/interfaces.md` is 12,560 B of a 15 KB cap.
- Edit the body, do not append. `spec/tabs.md` already links to the manifest section, so change it only if it says something this makes false.

## Done when

- [ ] `embarch-ui/interfaces.md`'s manifest section says `icon` is required and what happens to a tab without one, checked against `src/tabs.rs`.
- [ ] `embarch-ui/spec/tabs.md` does not disagree with it.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped. No `status.d/` fragment unless a suite-level fact moved.
