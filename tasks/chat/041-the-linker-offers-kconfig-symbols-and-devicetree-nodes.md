# 041 — The linker offers Kconfig symbols and devicetree nodes

**State:** done — symbols and nodes offered from 114's atlas read; decision 115
**Source:** EMB-412 — the 💡 linker cannot offer a Kconfig symbol or a devicetree node
**Issue:** EMB-412
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A draft says "turn on the shell's history option" or "the second I2C bus". The
atlas knows the Kconfig symbol by its prompt and the node by its label, and the
linker never sees either. `embarch-promptu` decision 16
(`embarch-doc/embarch-promptu/decisions/chat.md`) gives the linker both kinds;
the atlas holds them per built atlas (`kconfig.json`, `dt.json`) and
`embarch-atlas refs --json` lists them. `chat/040` added the atlas section
source (chat decision 114). When this is done:

- **Two kinds from `chat/040`'s atlas source**, no second run of
  `embarch-atlas`.
- **Symbols**: match words from the prompt; names `CONFIG_<NAME>`, and the
  bare `<NAME>` when the draft writes it in capitals with an underscore. Gated
  (plan choice 11) on a cue word: Kconfig, config, option, symbol, setting,
  `prj.conf`, menuconfig, or an exact name.
- **Nodes**: match words from labels, the node's name (the path's last part,
  unit address dropped) and compatibles split on `,` and `-`; names
  `&<label>`, a label, an alias, a path. Gated on: devicetree, DT, node,
  overlay, DTS, binding, compatible, alias, chosen, or an exact name.
- **Written** (plan choice 12): `CONFIG_<NAME> ("<prompt>")`, no value, since
  the atlas's value is its commit's; `&<label> (<path>, <compatible>)`, the
  path alone when the node has no label.
- **A stale atlas** (`stale` not empty) still offers; the card's `why` says the
  atlas is at an older commit.
- **Atlas only** (plan choice 4): a repo with no built atlas offers neither
  kind.

The decision must name plan choices 4, 11 and 12 as the owner's to strike.
Contract: `embarch-promptu`'s §15. If the atlas's `refs --json` output does not
carry what a kind needs (a symbol's prompt, a node's label or compatible), stop
and say so in this file: that is `embarch-atlas`'s change, not this one.

## Why now

`chat/040` landed the atlas read this shares and named EMB-412 as unblocked by
it; EMB-415 (a study's capture or trace) waits behind EMB-414 on the same
linker.

## Where to look

- `src/assistant/refs-atlas.ts` (`chat/040`'s source), `src/assistant/references.ts`
- `test/references.test.mjs` and the fake `embarch-atlas` from `chat/040`
- `embarch-doc/embarch-chat/decisions/references.md` (decisions 112, 114)

## Where the doc goes

A new decision in `decisions/references.md` beside 114. **Decisions near their
per-decision limit:** `promptu.md` 96 (204 B left); do not grow it. No `chat`
file is in reserve. If your work pushes one into reserve, file
`tasks/chat/<NNN>-compact-chat.md` in the same commit per `tasks/README.md`.
Run `npm test` with `EMBARCH_DESK_BIN` set (`embarch-fleet/gate.md`'s npm
bullet) so the desk-backed tests run instead of skipping.

## Done when

- [x] "turn on the shell history option" offers the symbol whose prompt says
      so, written `CONFIG_<NAME> ("<prompt>")`.
- [x] A draft naming `CONFIG_<NAME>` or `<NAME>` exactly gets its line with no
      cue word.
- [x] "the second I2C bus node" offers the node; `&i2c1` in a draft finds it
      by label; a path finds it too.
- [x] A stale atlas's card says so in its why.
- [x] Translated documents with no built atlas offer sections and no symbol or
      node.
- [x] A decision says it.
