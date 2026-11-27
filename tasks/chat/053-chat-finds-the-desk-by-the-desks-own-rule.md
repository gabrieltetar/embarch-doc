# 053 — chat finds the desk by the desk's own rule when no setting names it

**State:** open
**Source:** EMB-305 — four clients re-derive the desk's token and port, and one copy has drifted
**Issue:** EMB-305
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

`src/extension.ts`'s `cfg()` defaults `embarchChat.deskUrl` to
`http://127.0.0.1:4891` and `embarchChat.deskTokenPath` to the fixed string
`~/.config/embarch-desk/desk-token`. The desk itself (`embarch-desk/src/paths.rs`)
reads its config folder from `EMBARCH_DESK_CONFIG_DIR` (the folder itself),
else `$XDG_CONFIG_HOME/embarch-desk` (an empty value counts as unset), else
`~/.config/embarch-desk`, keeps its token in `desk-token` there, and listens on
`EMBARCH_DESK_PORT` (a value that does not parse as a port falls back) else
4891. So a scratch desk on another port or folder works with every client but
chat until someone edits a setting.

When this is done, one TypeScript module is chat's only copy of that rule, and
when the engineer has **not** set `deskUrl` or `deskTokenPath` (tell a set
value from the default with `inspect()`, not by comparing strings), chat derives
the default from the extension host's environment with exactly the desk's
precedence. A value the engineer set still wins, the settings stay machine
scope, and a folder rule naming another desk (`activeDesk()`) is unchanged.
The settings' descriptions in `package.json` say the default follows the
desk's own rule. Tests cover each precedence step, an empty `XDG_CONFIG_HOME`,
an unparsable port, and a set value winning.

`embarch-core-client` holds the Rust clients' copy (`tasks/api/223`); the
decision you write says chat holds the TypeScript one and names that module as
its counterpart.

**Not yours:** every other repo. You never touch hardware.

## Where to look

- `src/extension.ts` (`cfg()`, `makeClient`, `expandHome`), `package.json`
  (`embarchChat.deskUrl`, `embarchChat.deskTokenPath`)
- `embarch-desk/src/paths.rs` (read only: the rule)
- `embarch-doc/embarch-chat/decisions/desk.md`

## Where the doc goes

A new decision in `decisions/desk.md`, with its index row. Check
`scripts/check-doc-size.py --pressure` first: `decisions/launcher.md` has 36 B
left and is not where this goes.

## Done when

- [ ] With neither setting set, chat's desk URL and token path follow the
      desk's precedence from the environment; a set value wins; tests cover it.
- [ ] One module holds the rule; `package.json`'s descriptions match.
- [ ] Gate green (`npm ci`, `npm run build`, `npm run typecheck`, `npm test`,
      `npm run test:webview`); decision and index row; `changelog.d/` fragment.
