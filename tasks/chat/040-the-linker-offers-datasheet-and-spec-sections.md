# 040 — The 💡 linker offers datasheet and spec sections through the atlas

**State:** done — chat decision 114: atlas section source, embarchChat.atlasPath, fake-atlas tests
**Source:** EMB-411 — the 💡 linker cannot offer a datasheet or spec section
**Issue:** EMB-411
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A draft says "check the protection section of the switch's datasheet". The
repo's atlas knows that section and its page, and the linker never sees it: its
sources are the desk's issues and PRs (`src/assistant/references.ts`) and, since
`chat/039`, git branches and worktrees (`src/assistant/refsGit.ts`). The chat
knows the atlas only for citation links (`src/atlas.ts`, chat decision 16).
When this is done, the linker has an **atlas source** on decision 112's source
interface (`src/assistant/refsBase.ts`; `refsGit.ts` is the newest model):

- **Read:** `embarch-atlas refs --json` in the chat's folder, with a 10 s
  limit, and again only when the atlas's `current.json`, `atlases/` or `docs/`
  changed since (a stat before a cards call). The binary is a new
  `embarchChat.atlasPath` setting, `embarch-atlas` on PATH by default, as
  `embarchChat.promptuPath` is (`package.json`; `findBinary` in
  `src/extension.ts`). No binary, no atlas, or a failed run leaves the kind
  empty and logs once per cause.
- **Entries:** one per section; words from its title and id; each names its
  document's `doc_id` and `part`. The JSON is `embarch-atlas`'s `refs` verb
  (`atlas/109`, landed 2026-11-25); read its shape from that repo's
  `origin/main`.
- **Gated:** a cue word (datasheet, spec, specification, standard, section,
  chapter, table, manual, errata, app note), whole word in any case, or the
  document's part named in the draft.
- **Written:** `<doc_id> p<page> §<id> "<title>"`. The `<doc_id> p<N>` head is
  the shape decision 16's links match (`webview/chat/atlas.tsx`), so the same
  text is a citation link wherever the chat finds the atlas.
- **No prose links beyond decision 16's.**

The cue words, the 10 s limit and the change-stat refresh are the plan's
recommendations (plan choices 11, 12, 14, 15), which the owner may strike: say
so where the decision records them. Contract: `embarch-promptu/docs/contract.md`
§15 (read it from `origin/main` if the main checkout lags).

## Why now

EMB-411, one linker kind of `embarch-promptu` build step 5 (`embarch-promptu`
decision 16). Decision 112 made each later kind one more source and a row in
the decision; `chat/039` was the first. EMB-412 (Kconfig symbols and
devicetree nodes) is blocked on this one and shares its atlas source.

## Where the doc goes

Decision 112 lives in `embarch-doc/embarch-chat/decisions/references.md`
(8,010 B; decision 113 is the branch and worktree kind). Record the section
kind there, as a new decision in the same file per 112's "one more source and a
row here"; if that file would cross its cap, start a new topic file rather than
trimming. **`decisions/promptu.md` decision 96 is near its per-decision limit
(204 B left): do not touch it.** `spec/constants.md` takes the source's
constants. If your work pushes a file into reserve, file
`tasks/chat/<NNN>-compact-chat.md` in the same commit per `tasks/README.md`.

## Done when

- [x] With a fake `embarch-atlas` (modelled on `test/fake-promptu.mjs`) printing
      two documents' sections, "check the protection section of the switch
      datasheet" offers that section, written `<doc_id> p<N> §<id> "<title>"`.
- [x] The written text, rendered as prose with that atlas set, is a citation
      link.
- [x] No binary, an atlas-less folder, and a failing run each give no section
      line and one log line.
- [x] Two cards calls with no atlas change spawn the verb once.
- [x] A draft with no cue word and no part name gets no section line.
- [x] The decision says it, with the setting.
- [x] Gate green (`../../embarch-fleet/gate.md`): `npm ci`, `build`,
      `typecheck`, `npm test`, `test:webview`.
- [x] `spec`/`decisions`/`open.md` updated, `changelog.d/` fragment dropped,
      `status.d/` fragment for anything suite-level it made false.
