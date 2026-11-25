# 046 — The linker offers a study's capture or trace

**State:** open
**Source:** EMB-415 — the 💡 linker cannot offer a study's capture or trace
**Issue:** EMB-415
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A draft says "compare it with yesterday's trace" or "the VBUS capture from the
soak run", and the linker never sees either. A study's captures are its stream
taps, and an outpost trace is a tap whose encoding is `OutpostTrace`
(`embarch-core/src/study.rs`, `StudyTapSummary`;
`embarch-study-designer/src/streams.rs`, `StreamEncoding`). Core lists every
retained study with its taps at `GET /studies`, and `embarch-api --json
list-studies [--limit N]` prints that list (`embarch-api/src/cli.rs`,
`list_studies`). `embarch-promptu` decision 16 gives the linker captures and
traces. When this is done:

- **Through the runner `chat/043` added** (`src/assistant/apiRun.ts`):
  `embarch-api --json list-studies --limit 20`, under the same cache and failure
  rules as `list-instruments` — one rule for both, which the decision states.
- **One entry per tap** of each listed study: kind `trace` when its
  `encoding_kind` is `outpost_trace`, else `capture`. A signal's live capture
  is not a kind.
- **Words** from the study's name and the tap's name. A study id in the draft
  names its taps with no cue word. Otherwise gated on capture, trace,
  recording, stream, tap, study, run, samples, log (and plurals), as
  `refsLinear.ts` gates documents.
- **Recency**: with last, latest, yesterday or today in the draft, newer
  studies score first; otherwise newest first among equals.
- **Written**: `trace "<tap>" of study <id> "<study name>" (OutpostTrace,
  <YYYY-MM-DD>)` and `capture "<tap>" of study <id> "<study name>"
  (<encoding_kind>, <YYYY-MM-DD>)`, with ` not rendered` added when the tap's
  `rendered` is false. Every name through `clipTitle` and `copiesTitle`'s check,
  as `chat/044` did.
- A study whose `taps` is null offers nothing and breaks nothing.

## Where to look

- `src/assistant/apiRun.ts` (the runner, its cache and its failure log),
  `src/assistant/refsInstruments.ts` and `src/assistant/refsLinear.ts` (the two
  newest sources, for shape), `src/assistant/references.ts` (`linkReferences`)
- `test/fake-api.mjs` (the fake `embarch-api`) and the linker's tests
- `embarch-api/src/cli.rs`, `list_studies`, for the JSON the fake must mirror;
  `embarch-core/src/study.rs`, `StudyTapSummary`, for the tap fields — read only
- `embarch-doc/embarch-promptu/decisions/chat.md` decision 16, read only

## Where the doc goes

A new chat decision. `decisions/references-kinds.md` is 10,772 of 12,288 B,
under its reserve line (11,059 B); a decision there will likely push it in, so
either put this one in a new topic file or, if you add it there and it enters
reserve, file `tasks/chat/<NNN>-compact-chat.md` in the same commit per
`tasks/README.md`. `check-doc-size.py --pressure` lists `promptu#96` with 204 B
left; do not grow it.

## Done when

- [ ] With a fake `list-studies` of three studies, "compare it with yesterday's
      trace" offers the newest trace first, written as above.
- [ ] "the vbus capture" offers the tap named `vbus` as a capture with its
      encoding.
- [ ] A study id in the draft offers its taps with no cue word.
- [ ] A study whose `taps` is null offers nothing and breaks nothing.
- [ ] `list-instruments` and `list-studies` share one cache rule, and the
      decision says so.
- [ ] Gate green (`npm test` with the desk binary, per `gate.md`).
