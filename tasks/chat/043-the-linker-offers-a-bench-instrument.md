# 043 — The 💡 linker offers a bench instrument

**State:** done — instrument source and runner built; decision 116; references.md split, out of reserve
**Source:** EMB-414 — the 💡 linker cannot offer a bench instrument
**Issue:** EMB-414
**Scope:** chat
**Hardware:** none
**Owner:** no

## What

A draft says "set the load to 1 A and read the supply". Core knows the bench's
declared instruments by name, and the linker never sees them. The chat has no
Core client: its bench cards are read from tool results in the stream
(decision 15, `decisions/readouts.md`). It does find the `embarch-api` binary,
for Promptu's `--have` (`src/extension.ts`, `findBinary("embarch-api")`;
`embarch-promptu` decision 36). `embarch-api --json list-instruments` prints
`{success, instruments}` over Core's lease-open `GET /instruments`. An
instrument holds `name`, `protocol` (`scpi`), port, baud and terminators, and no
model or description (`embarch-topology/src/hardware/instrument.rs`). When this
is done, instruments are a kind on decision 112's interface:

- **A runner for `embarch-api --json <verb>`** in the chat's folder, which finds
  `embarch/embarch.toml` upward as every `embarch-api` verb does: a 10 s limit,
  a result cached 5 minutes, run only for the chat on screen and only before a
  cards call. No binary: no spawn. A failure (no config, Core unreachable, a
  non-zero exit) leaves the kind empty and logs once per cause. A later linker
  kind reuses this runner, so keep it separate from the source.
- **A source** offering every declared instrument when the draft names one, or
  carries an instrument word: instrument, supply, PSU, load, meter, multimeter,
  DMM, scope, oscilloscope, analyzer, SMU. A declaration has nothing else to
  match words against.
- **Written** `instrument "<name>" (<protocol>)`.
- No lease and no hardware: a list read.

The runner's existence, the 10 s / 5 minute figures, the word list and the
written form are the owner's planning choices; mark them in the decision as
his to strike, as 113 to 115 do.

## Where to look

- `src/extension.ts` — `findBinary`
- `src/promptu/service.ts` — `embarchApiPresent`, the same detection
- `src/assistant/` — the sources of 113 to 115, the pattern to follow
- `test/fake-promptu.mjs`, the model for a fake `embarch-api`;
  `test/references.test.mjs`
- `embarch-doc/embarch-chat/decisions/references.md` (112 to 115),
  `decisions/assistant.md`

## Where the doc goes

A new decision beside 113 to 115, since its subject is a linker kind.
**`decisions/references.md` is in reserve: 12,126 of 12,288 B, 162 B left, out
of reserve at 11,059 B.** Its compaction task, `tasks/chat/042`, is `blocked`
on `In flux: yes`, which parks the pass, not the reserve, so the compaction
rides in this unit (`DOC-BUDGET.md`). **Split first, verbatim**
(`DOC-COMPACTION.md` §2): move the per-kind decisions (113 to 115) into a new
topic file with only relative link prefixes changed, leave 88 and 112 where
they are with a pointer, and put your decision in the new file. Carry `chat/042`'s
**Must not delete:** list (decision 88's measured figures and its Rejected
list; the `Assumed, not measured` sentences of 112 to 115). Say in your report
whether `references.md` ended out of reserve; the supervisor closes `chat/042`
at the fold. Do not edit `chat/042` yourself. If your work pushes any other
file into reserve, file `tasks/chat/<NNN>-compact-chat.md` in the same commit
per `tasks/README.md`.

## Done when

- [x] With a fake `embarch-api` listing `eload` and `psu`, "set the load to 1 A"
      offers both, written `instrument "<name>" (scpi)`; "ask eload for its
      voltage" offers `eload` by name.
- [x] A draft with no instrument word and no name gets no instrument line.
- [x] No binary means no spawn; a failing binary logs once and offers nothing.
- [x] Cards calls within 5 minutes spawn the verb once; a chat off screen spawns
      nothing.
- [x] The decision says it, and `references.md` is out of reserve.
- [x] Gate green.

## Notes

- `references.md` is 6,003 B, out of reserve; decisions 113 to 115 moved verbatim to `references-kinds.md` (8,888 B) with 116 beside them. 88 and 112 untouched, so every `Must not delete:` item of `tasks/chat/042` survives.
- The gate's `check-decision-refs.py` is red on one line only: `history/chat.md:9` cites decision 114 at `references.md`. `history/` is not a chat worker's to write; filed to the spool for the supervisor. Repoint it at `../embarch-chat/decisions.md`.
- Hardware-verification debt: none to a board, but the instrument kind is not seen against a real `embarch-api` and a declared bench; tested on `test/fake-api.mjs` only.
