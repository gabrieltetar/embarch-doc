# 044 — The 💡 linker offers a Linear project or document

**State:** claimed by agent/chat/044-the-linker-offers-a-linear-project-or-document, 2026-11-25 12:34
**Source:** EMB-413 — the 💡 linker cannot offer a Linear project or document
**Issue:** EMB-413
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A draft says "follow the bring-up notes" or "file it under the logger project".
The chat's `RefIndex` is `{desk_id, synced_ms, issues, prs}`
(`src/desk/client.ts`), re-read when `/view`'s `refs_ms` moves
(`src/deskService.ts`, `syncRefs`). The desk's `GET /refs` gains `projects` and
`documents`; `embarch-promptu` decision 16 gives the linker Linear projects and
docs. When this is done, both are kinds on decision 112's interface, written
from the index as issues and PRs are:

- `RefIndex` **gains optional** `projects` **and** `documents`; an older desk
  omits them and they read as none.
- **Two sources** from the mirrored index; nothing new is fetched and nothing
  runs on a keystroke.
- **Projects**: words from the name; not gated (a desk's scope holds few).
  **Documents**: words from the title and its project's name; gated on doc,
  document, notes, write-up, spec, design, RFC, page, or a document's URL in the
  draft.
- **Named**: a Linear project or document URL in the draft finds its entry with
  no cue word.
- **Written** `Linear project "<name>" (<url>)` and
  `Linear doc "<title>" (<project>, <url>)`, each title through `clipTitle` and
  each in `copiesTitle`'s check, since anyone can title a document.
- No prose links.

The ungated projects, the document cue words and the written forms are the
owner's planning choices; mark them in the decision as his to strike, as 113 to
116 do.

## Where to look

- `src/desk/client.ts` — `RefIndex`, `refs`
- `src/deskService.ts` — `syncRefs`, its log line
- `src/assistant/references.ts` — `clipTitle`, `copiesTitle`, the source interface
- `src/assistant/refsDesk.ts` — the issue and PR source, the pattern to follow
- `test/refs-index.mjs` — add invented projects and documents; `test/references.test.mjs`
- `embarch-doc/embarch-chat/decisions/references-kinds.md` (113 to 116),
  `decisions/assistant.md`, `interfaces/desk.md` (`GET /refs`)

## Where the doc goes

A new decision in `decisions/references-kinds.md`, beside 113 to 116. That file
is 8,888 of 12,288 B and enters reserve above 11,059 B, so a long decision may
push it in: if it does, file `tasks/chat/<NNN>-compact-chat.md` in the same
commit per `tasks/README.md`, answering `In flux:` yourself (EMB-415 adds one
more kind after this). `decisions/references.md` (88, 112) was just paid down;
do not grow it.

## Done when

- [ ] With the extended `refs-index.mjs`, "follow the bring-up notes" offers the
      document, written `Linear doc "<title>" (<project>, <url>)`.
- [ ] "under the logger project" offers the project.
- [ ] A document URL in the draft finds its entry with no cue word.
- [ ] A document title written to steer the cards reaches no draft: the
      reference is quoted and clipped, and another card carrying it is dropped.
- [ ] An index with no `projects` or `documents` behaves as today.
- [ ] The decision and `interfaces/desk.md` say it.
- [ ] Gate green.
