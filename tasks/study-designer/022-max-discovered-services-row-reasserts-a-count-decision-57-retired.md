# 022 — `limits.md`'s `MAX_DISCOVERED_SERVICES` row reasserts the service count decision 57 exists to retire

**State:** done
**Source:** `embarch-reviewer` on `study-designer/011` (doc merge `f22a6b4`), filed
as an `inbox/` drop 2026-09-07 and promoted here by leg 047. This is the first
finding in this log that a reviewer caught and the supervisor did not — the
supervisor had flagged the row's `[measured]` tags and mis-framed the actual
problem.
**Scope:** study-designer
**Hardware:** none — this is a documentation-accuracy question. Confirming which
service count is current reads `reference-dut-fw` source, not a board.

## What

`embarch-study-designer/interfaces/limits.md`'s `MAX_DISCOVERED_SERVICES` row
says `reference-dut-fw`'s `lib/ble/ble_def.h`/`ble.c` declares **2** services
today, sourced from `src/limits.rs:80-84`'s doc comment (written `c8bb166`,
2026-08-23).

`decisions/gatt-extract.md` **decision 57** was written 2026-08-31 — later —
and exists *precisely because that two-file bounded read undercounts*. Its own
words: *"Validated against the real checkout: three services where a bounded
read found two."* So the row asserts as current fact a number a locked decision
already established as an artifact of the known-incomplete extraction method,
and it does so **without citing decision 57 at all** — the row `011` replaced
did cite it, and said 3 declared / 7 via live discovery.

The file now also contradicts itself with nothing bridging the two: the
surviving `MAX_MONITOR_TARGETS` row a few lines down still says *"7 services in
total once an encrypted link reaches the rest of the table"*.

## Why now

`011` was not wrong to do what it was asked — it reconciled the doc against the
crate's own doc comment. **The upstream cause is that `src/limits.rs:80-84`'s
comment was never updated when decision 57 landed**, so the doc faithfully
transcribed a stale source. The fix therefore spans both repos, and is a
statement about what a real DUT declares — which is exactly the class of fact a
supervisor must not author at a fold from a source read. Left alone, a reader
hitting `limits.md` gets a worse answer on that one row than the file gave
before `011`.

## Done when

- [x] `src/limits.rs:80-84`'s doc comment and `interfaces/limits.md`'s
      `MAX_DISCOVERED_SERVICES` row agree with decision 57's validated
      3-services finding — **or**, if the two-file extractor's 2 is genuinely
      what the code bounds against today, the constant's rationale says so
      explicitly. Either way both cite decision 57.
- [x] `MAX_DISCOVERED_SERVICES` and `MAX_MONITOR_TARGETS` no longer read as
      contradicting each other unexplained (2 declared vs 7 total, same DUT).
- [x] The row carries an honest provenance tag: the `[measured <date>]` on
      these rows is the date `git log -S` says the *constant was written*, and
      the counts behind it are transcribed from the crate's own doc comments —
      a read of `reference-dut-fw` source, not a live measurement. Do not call
      that measured.

**On the tag:** `DOC-CONVENTIONS.md`'s "Measured vs. assumed constants" section
defines exactly two brackets — `[measured <date>]` and `[assumed]` — and neither
fits a number that is a transcription of a source-level doc comment rather than
either a live measurement or a placeholder guess. Per the dispatch note, I did
not bend `[measured]` to cover this case. Instead the `MAX_DISCOVERED_SERVICES`
row now carries no bracket tag at all: it names decision 57 as the source of the
count, `src/limits.rs:80-84` as where it's transcribed, and the 2026-08-23 date
as when *that comment* was written (confirmed via `git log -S
MAX_DISCOVERED_SERVICES -- src/limits.rs`, which shows one hit: `c8bb166`). If
this suite wants a third bracket for "transcribed from a source read, not a
live measurement," that's a `DOC-CONVENTIONS.md` change outside this task's
scope (that file is not `study-designer`'s to edit) — flagging it here rather
than deciding it unilaterally.

## Do not revert

A plain `git revert f22a6b4` would take the other 43 constants `011` correctly
enumerated with it. Hand-edit the one row.

## Dispatch note — leg 048

**Do not go and re-derive the service count from `reference-dut-fw`.** That repo is
not yours to read for a fact you then assert, and re-deriving it is how this defect
was created in the first place: `011` transcribed a bounded read and stated it as
current fact. **Decision 57 is the validated answer already on record** — three
services declared where a bounded read found two, seven via live discovery once the
link is encrypted — and it was written *after* the comment you are fixing. Restore
the citation and the numbers from the decision; add nothing the decision does not
already say.

**Fix the upstream cause, not only the symptom.** `src/limits.rs:80-84`'s doc
comment in `embarch-study-designer` is what a future doc pass will transcribe again.
Make it cite decision 57 rather than restate a count, so the next transcription
cannot go stale independently of the decision.

**On the `[measured]` tag** — the third Done-when item is the one most likely to be
skimmed. The date on those rows is when `git log -S` says the constant was written.
That is provenance about the *constant*, not a measurement of the *DUT*. Whatever
tag you land, a reader must not be able to read it as "someone put a board on a
bench and counted." If `DOC-CONVENTIONS.md` gives you no tag that says "transcribed
from a source read", say so in the task file rather than bending an existing one.

**Doc-size reserve for `study-designer`, so you plan rather than discover.**
`decisions/registry.md` is **11,827 / 12,288 B — 461 B left**, filed under
`tasks/study-designer/019`. `open.md` (4,331 / 5,120) and `spec.md` (9,183 / 10,240)
are parked under `tasks/study-designer/006` `[BLOCKED]`. `interfaces/limits.md` —
the file you are editing — is not in reserve, and this change should be roughly
byte-neutral anyway.

**Reserve rule you owe:** if your work pushes any `study-designer` file into reserve,
or leaves one there that nothing has filed, file
`tasks/study-designer/<next free NNN>-compact-study-designer.md` in the same commit.
