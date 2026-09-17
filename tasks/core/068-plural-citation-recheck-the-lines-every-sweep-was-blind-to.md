# 068 — Plural-citation re-check: the 11 lines every `core` sweep was structurally blind to

**State:** done — worker agent/core/068-plural-citation-recheck, 2026-09-16. 15 lines / 37 instances
checked (re-census found 4 more than the filed 11, all line-wrapped), 0 wrong numbers, 0 false
sentences; no edits needed. A generalizable second census gap found and filed to inbox.
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-core` was declared citation-swept after `core/058`, `core/066` and `core/067`. **Every one
of those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match `decisions 17, 18`
or `decisions 31/32`** — so these lines were never in any sweep's input at all. This is not a
re-read of checked work; it is the first read.
**Scope:** core
**Hardware:** none — doc comments, one `Cargo.toml` comment and one workflow comment. Nothing is
built for a board, no probe, no live Core, no deploy, no study. Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `core`:** one file, `embarch-core/decisions/auth.md` at
**11,356/12,288 B (932 B left)**, filed as `tasks/core/046` and **blocked**. Nothing else in scope
is in reserve. A source-comment sweep should not need to write it; if it does, say why. If your work
leaves a `core` doc inside the last 10% of its cap with nothing filed against it, file
`tasks/core/<next free NNN>-compact-core.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Eleven lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git` and `target`:

```
src/logs.rs:4                     `embarch-topology` decisions 2/8/14
src/stream_store.rs:178           `embarch-outpost` decisions 17 and 18
src/outpost_manifest.rs:198       `embarch-outpost` decisions 17, 18
.github/workflows/release.yml:24  embarch-umbrella decisions 27/29
Cargo.toml:26                     embarch-topology decisions 2, 4, 8
src/service.rs:107                decisions 4/7            (bare — own repo)
src/study.rs:1255                 `decisions 30/31`        (bare — own repo)
src/study.rs:1916                 `embarch-outpost` decisions 4, 17, 18
src/study.rs:2910                 `embarch-outpost` decisions 17, 18
src/study.rs:4259                 `embarch-study-designer` decisions 31/32
src/main.rs:165                   decisions 31/32's        (bare — own repo)
```

**Eleven lines, roughly 28 distinct decision instances** — each line cites two to three numbers and
every number is its own claim. Treat the line count as a floor and report the instance count you
actually checked.

`.github/workflows/release.yml:24` is the exact line `core/067`'s re-census found by accident and
which its reviewer confirmed the filing census had missed; it is listed here for completeness, and
if `core/067` already checked it, say so and move on rather than re-deriving it.

## How

Same pass the chain has run eleven times, unchanged except for the census pattern:

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** `ui/054` found two sites spelled
   `Decision` at the start of a sentence that a case-sensitive grep skipped. Report your number
   against the eleven above.
2. **For each cited number, check the decision exists in the file the citation points at**, and
   remember a bare `decision NN` in another sub-project's file means *that* sub-project's NN. Three
   of the lines above are bare and are `embarch-core`'s own.
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** This is the half that finds real defects: `api/102` found a comment citing a
   real, existing, topically wrong decision, and `study-designer/054` found a citation that was
   correct when written and went false when another repo amended the decision it cited. A number
   that resolves is not the same as a sentence that holds.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation — a stale path, a count, a constant — is a finding for `inbox/`, not an edit; `api/102`
   did exactly that and `tasks/api/103` came out of it.

## Done when

- [x] Every plural-form citation line in `embarch-core` has had the existence-and-truth pass.
- [x] The report states the instance count checked against the eleven-line floor.
- [x] Each defect found is either fixed here or filed with its reason for not being fixed here.

## Result

**Re-census with `[Dd]ecisions [0-9]` reproduced exactly the filed 11 lines** — no additions from
case-insensitivity (the ui/054 class of miss did not recur here). **But `grep` is blind to a second,
different case: a citation whose "decisions" and its numbers fall on opposite sides of a line
wrap.** `grep -rlIE '[Dd]ecisions[[:space:]]*$'` found four such lines, all in `study.rs`, none in
the filed 11:

| Site | Decision(s) cited | Repo | Verdict |
|---|---|---|---|
| `logs.rs:4` | 2, 8, 14 | topology | correct — `crate.md` #2, `consumer-boundary.md` #8, `enrollment.md` #14 (its own text: "decision 8's principle, honoured for enrolling as well as validating") |
| `stream_store.rs:178` | 17, 18 | outpost | correct — `clocks.md` #17/#18, matches `arrival_file`'s `frame_index,rx_utc_ms,frame_bytes` |
| `outpost_manifest.rs:198` | 17, 18 | outpost | correct — same pair, `stamped_frames` |
| `release.yml:24` | 27, 29 | umbrella | correct — already confirmed by `core/067`; re-confirmed here (`release.md` #27,29) |
| `Cargo.toml:26` | 2, 4, 8 | topology | correct — `crate.md` #2, `consumer-boundary.md` #4/#8, matches the dependency-move rationale |
| `service.rs:107` | 4, 7 | **umbrella, not bare** | correct — `install.md` #4, `topology.md` #7. **The filing task misread this as "bare — own repo"**: the repo prefix `` `embarch-umbrella` `` sits on the line *above* `decisions 4/7).` (source wraps `(`embarch-umbrella`\ndecisions 4/7).`), invisible to a single-line grep match on line 107 alone. |
| `study.rs:1255` | 30, 31 | core, bare (confirmed) | correct — `streams.md` #30 (streams/ capture), `handshake.md` #31 (the gate immediately preceding this function, cited twice more at `study.rs:1065`/`1121`) |
| `study.rs:1916` | 4, 17, 18 | outpost | correct — `layout.md` #4 (per-record `cycles` stamp) + `clocks.md` #17/#18 |
| `study.rs:2910` | 17, 18 | outpost | correct |
| `study.rs:4259` | 31, 32 | study-designer | correct — `gatt.md` #31 `GattDiscover`/#32 `GattMonitorAll`, matching `gatt_services`/`gatt_activity` fields |
| `main.rs:165` | 31, 32 | **study-designer, not bare** | correct — same #31/#32 pair. **Also misread as "bare"**: `` `embarch-study-designer` `` sits on the line above (164), split by the wrap `` (`embarch-study-designer`\ndecisions 31/32's\n`gatt_services`/`gatt_activity`... ``. |
| `study.rs:1072-1073` (wrapped) | 17, 39, 40 | study-designer | correct — `seals.md` #17 ("validations never crossed the bench wire, asserted by decision 17 from the start" — `removed.md` #19's own words), `streams.md` #39, `declares.md` #40 ("host-side only... never cross the wire") |
| `study.rs:1084-1085` (wrapped) | 58, 60 | study-designer | correct — `protocols.md` #58 ("dev-bench **executes** it (decision 60)") |
| `study.rs:2313-2314` (wrapped) | 4, 17 | outpost | correct — `layout.md` #4 + `clocks.md` #17 |
| `study.rs:3689-3690` (wrapped) | 58-62 | study-designer | correct — all five decisions are the `.eap` protocol group (`protocols.md` #58/#59/#61, `protocol-exec.md` #60/#62), matching the section they head |

**15 lines, 37 instances checked (25 from the filed 11, 12 new). 0 wrong numbers, 0 false
sentences.** No edit made anywhere in `embarch-core` — every citation, including the four this
sweep's own census would otherwise have missed, already checks out.

**Two of the filing task's three "bare — own repo" calls were themselves wrong**, not because the
source is wrong (it isn't — both correctly name another sub-project) but because a **single-line**
census cannot see a repo prefix that wraps onto the *previous* line, the same structural blindness
this task exists to close, one level up. Filed to inbox as a second, generalizable census gap
(`grep` misses a citation split across a line wrap, independent of the plural-vs-singular issue) —
see `/home/gabriel/Github/embarch/embarch-doc/inbox/doc-citation-census-grep-misses-line-wrapped-citations.md`.

**Doc-size reserve:** untouched — no edit made to any `core` doc, `decisions/auth.md` unchanged,
nothing else entered reserve.

**Native Windows build not run** — no unattended leg can run it (WSL cross-check dies in `hidapi`'s
`build.rs`; the native path only works from the main checkout, not a worktree). Not claimed, not
counted as partial payment.
