# 125 — The UI shows which Core it is talking to

**State:** claimed by agent/ui/125-the-ui-shows-which-core-it-is-talking-to, 2026-11-26 14:29
**Source:** EMB-336 — embarch-ui does not show which Core it is talking to
**Issue:** EMB-336
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

Core's status says `service` or `development` with its key fingerprint
(`embarch-core/src/api.rs`, the status `mode` and the fingerprint, core
decision 129), and `embarch-core-client`'s `attest.rs` decides whether that
fingerprint is the installed one. The HIL design wants the person to see it on
every act, so a development Core cannot pass for the attested one
(`embarch-doc/notes/hil/12-prevention.md`, "The root of trust"). embarch-ui
reads Core's status for its snapshot and links the client with the person's
scope (ui decision 103), and shows neither. When this is done:

- **One line on every tab**: `service` or `development`, the first 16 hex
  characters of the fingerprint, and one of "matches the installed
  fingerprint", "does not match" or "no attested install on this machine",
  from the client's result.
- **A mismatch is a warning**, drawn as one.
- **No act is blocked here**: the client's token rule already decides what is
  sent.
- A Core too old to report a mode or a fingerprint gets a line that says so,
  not a blank.

## Where to look

- `src/snapshot.rs` — the Core status read; `src/main.rs` and `assets/` — the shell
- `embarch-api/crates/embarch-core-client/src/attest.rs` — the fingerprint and
  which token it picks — read only
- `embarch-doc/embarch-ui/decisions/core-token.md` (103)

## Where the doc goes

A new ui decision, or 103 amended (`core-token.md` is 1.7 KB).
**`decisions/live-study.md` is in reserve** (`tasks/ui/123`): do not write it.
**`spec/tabs.md` is in reserve** (1,080 B left; `tasks/ui/126` is filed
against it): a line there is fine, a section is not.
`check-doc-size.py --pressure` lists `bench-live#90`, `launcher#28`,
`tab-folders#100` and `topology-tab#10`, `#43` near their limits: do not grow
those.

## Done when

- [ ] Fixture statuses for a service and a development Core each render the
      line with the right words.
- [ ] A mismatch renders as a warning; a Core with no mode renders a line
      saying so.
- [ ] A decision records the line.
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
