# 024 — Plural-citation re-check: the 8 lines every `outpost` sweep was structurally blind to

**State:** done
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-outpost` was declared **completely** citation-swept after `outpost/021` and `outpost/022`.
**Every one of those sweeps censused with `grep -cE '[Dd]ecision [0-9]'`, which cannot match
`decisions 3 and 5` or `decisions 6, 7, 8, 9`** — so these lines were never in any sweep's input at
all. This is not a re-read of checked work; it is the first read, and "completely swept" was measured
with an instrument that could not see this form.
**Scope:** outpost
**Hardware:** none — C comments, one Kconfig help block, one CMake comment and one Python
module docstring. Nothing is built, nothing is flashed, no probe, no live Core, no study, no DUT.
Classified fresh at filing.
**Owner:** no

**Doc-size reserve for `outpost`: nothing in reserve.** If your work pushes an `outpost` doc into
the last 10% of its cap, file `tasks/outpost/<next free NNN>-compact-outpost.md` in the same commit
per `tasks/README.md`. **`tasks/doc/` is not yours.**

## What

Eight lines, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo excluding
`.git`:

```
Kconfig:93                          (decisions.md decisions 4, 17)
include/embarch/outpost.h:10        ../embarch-doc/embarch-outpost/decisions.md decisions 6 and 9
src/outpost_ring.c:10               decisions.md decisions 3 and 5
scripts/gen_outpost_manifest.py:4   ...decisions.md decisions 6, 7, 8, 9
src/outpost_hooks.c:10              decisions.md decisions 2 and 7
CMakeLists.txt:126                  decision 9's *selection* half ... and decisions 6/7/8's payoff
src/outpost.c:10                    ...decisions.md decisions 3, 4, 5
src/outpost_time.h:10               decisions.md decisions 3 and 4
```

**Eight lines, roughly 24 distinct decision instances** — every line cites two to four numbers and
each number is its own claim. Treat the line count as a floor and report the instance count you
actually checked.

**Every one of these is a file-header "Design:" line**, which is the highest-leverage citation form
in the repo and the one a reader is most likely to follow: it claims *this whole file implements
those decisions*. So the truth question here is sharper than usual — not just "does decision 5
exist" but "is `outpost_ring.c` still what decisions 3 and 5 describe". `CMakeLists.txt:126` is the
one exception, an inline claim about what the build step produces, and it mixes a singular and a
plural citation on one line.

`Kconfig:93` also makes a factual claim alongside its citation — *"so when it left the ring has no
bearing"* — which is checkable against the decisions' text.

## How

Same pass the chain has run eleven times, unchanged except for the census pattern:

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** `ui/054` found two sites spelled
   `Decision` at the start of a sentence that a case-sensitive grep skipped. Report your number
   against the eight above.
2. **For each cited number, check the decision exists in `embarch-outpost/decisions.md`.** These are
   all this repo's own, cited by path, which makes existence cheap to check and makes a wrong number
   cheap to miss.
3. **Then read the cited decision's current text and check the claim around the citation is still
   true of it** — for a file header, that the file is still the thing the decision describes.
   `study-designer/054` found a citation that was correct when written and went false when another
   repo amended the decision it cited; the analogous failure here is a decision amended in
   `decisions.md` after the header was written.
4. **Fix wrong numbers and false claims. Do not widen.** A wrong number that is not a decision
   citation — a stale relative path, a Kconfig symbol name — is a finding for `inbox/`, not an edit.
   Note that several of these lines carry `../embarch-doc/...` relative paths whose depth is a
   separate class of defect this chain has fixed elsewhere; if one is wrong, say so rather than
   silently correcting it, because the right depth depends on where the file is read from.

## Done when

Every plural-form citation line in `embarch-outpost` has had the existence-and-truth pass, the
report states the instance count checked against the eight-line floor, and each defect found is
either fixed here or filed with its reason for not being fixed here.

## Result, 2026-09-16

Re-censused with `grep -rInE '[Dd]ecisions [0-9]'`, case-insensitively: same eight lines as filed,
no additional case-variant sites.

Ran `core/068`'s wrap-check, `grep -rlIE '[Dd]ecisions[[:space:]]*$'`, over this repo: **zero
hits** — unlike core, topology and ui, `embarch-outpost` has no citation wrapped across a comment
continuation.

**8 lines, 21 distinct decision instances checked**: Kconfig:93, `outpost.h:10`,
`outpost_ring.c:10`, `outpost_hooks.c:10` and `outpost_time.h:10` each cite 2; `outpost.c:10` cites
3; `gen_outpost_manifest.py:4` and `CMakeLists.txt:126` each cite 4 (task filed this as "roughly
24" — the actual count is 21). Every cited number (2, 3, 4, 5, 6, 7, 8, 9, 17) exists in
`embarch-outpost/decisions.md`'s own index and its `decisions/*.md` group files — all this repo's
own, none a cross-repo trap. Read each citing file's surrounding code against its cited decision's
current text: **zero wrong numbers, zero false claims.** Every one of these eight headers still
accurately names what its file implements (markers/manifest for outpost.h; ring design/overflow
for outpost_ring.c; markers/ISR-name/thread-name/manifest for gen_outpost_manifest.py;
hooks/ISR-identity for outpost_hooks.c; transport/layout/overflow for outpost.c;
transport/layout for outpost_time.h; manifest-selection/markers-ISR-thread-payoff for
CMakeLists.txt:126). Kconfig:93's embedded factual claim ("so when it left the ring has no
bearing [on when the host says it happened]") is still true of decisions 4/17/20 today.

Two things read, checked, and deliberately left alone rather than fixed or filed:

- **Kconfig:93** cites decisions 4 and 17 for that "no bearing" sentence, which is near-verbatim
  decision 20's own wording (`decisions/transport.md`: "it carries its own DUT stamp, so when it
  left the ring has no bearing on when a host says it happened") — and the whole help block above
  it describes decision 20's drain-wait mechanism without ever citing 20. Decisions 4 and 17 are
  each independently true of what they're actually attached to (4: the record's own per-record DUT
  stamp; 17: the two-clock split that makes that stamp authoritative for placement), so nothing
  here is a wrong number or a false claim. Decision 20 would be the more direct source for the
  sentence as a whole; adding it would widen the citation past what this task asks, so left as is.
- **`src/outpost_hooks.c:10`** cites decisions 2 and 7, both confirmed true and current. The same
  file also implements decision 25's GPIO-dispatch hooks
  (`sys_trace_gpio_fire_callbacks_enter_user` / `sys_trace_gpio_fire_callback_user`, matching
  `decisions/tracing.md` decision 25 almost line for line) without citing 25 anywhere in the file,
  header or inline. That is an absent citation on a decision that is itself correctly numbered and
  current — not a wrong or false one — so it falls outside this task's existence-and-truth mandate
  on the numbers already present. Not filed to `inbox/`: no defect to hand off, just a completeness
  gap noted here per the task's instruction to report a line left unchanged with its reason.

Separate class of defect, reported per the task's own instruction rather than silently corrected:
three of these eight lines carry a `../embarch-doc/embarch-outpost/decisions.md` relative path
(`include/embarch/outpost.h:10`, `scripts/gen_outpost_manifest.py:4`, `src/outpost.c:10`) at two
different actual depths from the repo root (`outpost.h` two directories deep under `include/`;
the other two one directory deep) but all three use exactly one `../` — read as a literal
filesystem path each resolves to the wrong place, and inconsistently so between the three. Not
corrected here; the right depth depends on where the file is read from, and this task's mandate is
decision-number existence-and-truth, not path depth.

**Tally: 8 lines / 21 distinct decision instances / 0 wrong numbers / 0 false claims / nothing
fixed in the code repo.**
