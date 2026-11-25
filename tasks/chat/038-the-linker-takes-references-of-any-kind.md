# 038 — The 💡 linker takes references of any kind

**State:** done — decision 112; linker takes sources, one <references> block, cue-word gate
**Source:** EMB-408 — the linker only knows issues and PRs, in one hard-coded block
**Issue:** EMB-408
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

Today the linker (decision 88) knows two kinds: `deskReferences(index, draft,
opts)` in `src/assistant/references.ts` builds its documents from
`index.issues` and `index.prs`, finds the keys and PR numbers the draft names
(`named`), scores titles by word rarity (`byWords`) and returns
`DeskRef {id, line, issue?, prs}`. The block is `<desk_references>`, at most
`REFS_LINES = 8` lines and `REFS_CHARS = 2400` characters (`contextBlock` in
`src/assistant/prompts.ts`); `REFERENCES_RULE` speaks of "an issue, a PR, a test
or a file"; `referenceText` writes an issue or a PR; `parseCards` turns a `ref`
card into `referenceEdit`; `assistInput` in `src/views/chatHost.ts` passes the
desk's index alone. When this is done, the linker takes lines from any number of
sources, so each later kind is one source file, while issues and PRs behave as
decision 88 says.

- **A source interface.** A source gives entries
  `{kind, key, words, names, line, text(find)}`, as `embarch-promptu`'s
  `docs/contract.md` §15.1 fixes it (read it from that repo's `origin/main`;
  follow it where it is more exact than this list). The desk's issues and PRs
  become the first source, their line and their written text unchanged.
- **One matcher over every source**: names first, then words, scored within a
  kind (a word's rarity counts among that kind's entries, so thousands of
  entries of one kind do not drown a PR), then merged best first.
- **The block**: `<references>`, at most 12 lines and 3,600 characters, at most
  4 lines per kind before the best of the rest fill it; each line
  `[r3] <kind>: <line>`. The caps are constants in `spec/constants.md`.
- **The cue-word gate**: a source marked high-volume offers lines only when the
  draft names one of its entries exactly or carries one of the source's cue
  words. Issues and PRs are not gated, as today.
- **The rule names only the kinds present** in the block, so a draft with only
  PR lines sends the prompt it sends today but for the block's name and tags.
  Haiku still names a line by id and the vague phrase; the text is still the
  extension's.
- `referenceText` **asks the entry**; `copiesTitle` checks every entry's title,
  so a title written to steer the cards still reaches no draft. One
  "References" submenu stays.
- **Fixtures**: the recorded `cards-refs` call replays by the prompt's TASK line
  (`test/fake-claude.mjs`), so it still applies. Do not make real Haiku calls
  to re-record it; leave it, and say in the decision that a later unit records
  it.

Files, as the issue lists them: `src/assistant/references.ts`,
`src/assistant/prompts.ts`, `src/assistant/assistant.ts` (`cards`),
`src/assistant/edits.ts` (`CATEGORIES`), `src/views/chatHost.ts`
(`assistInput`), `test/references.test.mjs`, `test/refs-index.mjs`.

## Why now

EMB-408: `embarch-promptu` build step 5 (`embarch-doc/embarch-promptu/decisions/chat.md`
16, extending this repo's decision 88) gives the linker six more kinds, and
EMB-410 to EMB-415 each add one as a source file on top of this. The block
size, the per-kind cap and the cue-word gate are the plan's recommendations
(Promptu's `docs/forks.md` L10, L11, L16), which the owner may strike later; build
them as stated.

**A new numbered decision is yours to write**: "The linker takes references of
any kind", in `embarch-doc/embarch-chat/decisions/assistant.md`, amending 88's
block and caps (88's text stands, with a dated pointer to the new one). Each
later kind unit amends the new decision with its row. Update `spec/input.md` and
`spec/constants.md`.

No file is in reserve on the size ledger at dispatch. `decisions/promptu.md`
(decision 96) has 204 B left; leave it alone.

## Done when

- [x] Every test in `test/references.test.mjs` passes, changed only where it
      names the block or a line's tag.
- [x] A test source of a second kind shows: at most 4 of its lines when issues
      also match; 12 lines and 3,600 characters at most; a gated source offering
      nothing without a cue word or a name, and its line when the draft names an
      entry exactly.
- [x] The cards prompt for a draft with only PR lines names no other kind.
- [x] A reference card naming a line of the test kind is written from that
      entry's `text`, never from Haiku's words.
- [x] The new decision says it; `spec/constants.md` carries the caps.
- [x] Gate green (`gate.md`'s npm bullet: `npm ci`, `build`, `typecheck`,
      `test`, `test:webview`).
- [x] `changelog.d/` fragment dropped; `status.d/` fragment for anything
      suite-level it made false.

## Result

Decision 112 (`embarch-chat/decisions/references.md`, with 88 moved verbatim out of `assistant.md`, which the new decision would have put in reserve). Code: `src/assistant/refsBase.ts` (entry and source types, text helpers), `refsDesk.ts` (the desk's issues and PRs, the first source), `references.ts` (`linkReferences`, the block caps, the kind rows the rule reads). Choices to know: issues and PRs share one scoring pool, as 88 scores them, so its tests hold; a gated source offers by words only on a cue word and, on a name alone, only the named entries. The recorded `cards-refs` call is not re-recorded (no Haiku call): a later unit records it against the new prompt.
