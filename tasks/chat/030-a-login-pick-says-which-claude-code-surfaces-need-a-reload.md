# 030 — A login pick says which Claude Code surfaces need a reload

**State:** done
**Source:** EMB-168, a session finding: after the window's login is changed, Claude Code's account dialog keeps naming the login the window opened on, while new chats run on the picked one
**Issue:** EMB-168
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

Measured by the owner on 2026-11-12: a window opened on one login, its pick was
changed to the other, and a new Claude Code chat ran on the picked login. That
chat's "Account & usage" dialog still named the first account, while its usage
figures came from the chat's own process, so one dialog paired one account's
name with the other's figures.

The cause, as the issue reads the Claude Code extension's bundle: the extension
host runs `claude auth status --json` once and caches it, dropping the cache
only on its own events (a `/login`, a settings change). A pick in EmbArch Chat
changes what `claude-login` resolves for the next process and tells the Claude
Code extension nothing, so the cached account stays until the window reloads.

Make a pick honest about that, at `embarchChat.pickLogin` in
`src/extension.ts`, with `src/loginState.ts` as the mirror `claude-login`
reads:

- If a supported route exists to make the Claude Code extension re-read the
  account (a command or setting it already reacts to), use it, and say in
  `spec.md` which route and how you confirmed it exists.
- Otherwise the pick offers a window reload in the same step and says why: the
  account dialog keeps the old login until a reload. Never reload without the
  owner's click.

Then amend `embarch-chat` decision 106's text (`decisions/logins.md`) to say
which Claude Code surfaces follow a pick at once and which need a reload. That
is an edit to an existing decision's body, not a new decision.

You cannot run a real window, so do not claim the dialog changed. Say what was
tested, and leave a hardware-free verification debt in the task file for the
owner: one real pick and a look at the dialog.

**No new numbered decision** (burndown). If the fix needs one, file it with
`scripts/fleet-linear.py file --from decision` and say so in the task file.

**What you may change.** Only `embarch-chat` and `embarch-doc/embarch-chat/`.

**Doc reserve.** No `embarch-chat` file is in reserve at filing. Decision
`promptu` #96 has 204 B left; this unit should not touch it.

## Why now

The owner moved EMB-168 to Fleet Ready. He reads the account dialog to learn
which seat a chat is billing, and it named the wrong one.

## Done when

- [x] After a pick, either the Claude Code account dialog follows without a manual step, or the pick offers a reload in the same step and says why.
- [x] Decision 106's text says which Claude Code surfaces follow a pick at once and which need a reload.
- [x] A test covers the new pick behaviour.
- [x] Gate green (`../../embarch-fleet/gate.md`); `changelog.d/` fragment dropped.

## Outcome

No supported re-read route: Claude Code 2.1.326's package.json commands hold none, and the only setting its host reacts to (`claudeCode.environmentVariables`) is the owner's, which a pick must not rewrite. So `embarchChat.pickLogin` offers Reload Window (with Later) when the effective login changed, via `pickNotice` in `src/loginState.ts`; it never reloads unasked. Decision 106's body amended (no new decision). Test: `loginstate.test.mjs` covers the notice text and the unchanged-pick case; the extension command itself is not covered (the mock has no reload path). npm build, typecheck, test, test:webview green.

## Verification debt (owner, no hardware)

One real pick in a window opened on the other login: confirm the notice appears, Reload Window reloads, and the account dialog then names the picked login. Not run here.
