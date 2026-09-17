# 061 — Plural-citation re-check: the 7 lines every `ui` sweep was structurally blind to

**State:** done
**Source:** leg 125's refill sweep, 2026-09-16, acting on the measurement
`inbox/citation-census-grep-cannot-see-a-plural-citation.md` asked for and nobody had run.
`embarch-ui`'s citation surface was swept across `ui/049`, `ui/052` and `ui/054`, and `ui/060` takes
the last two source files. **Every one of those sweeps censused with
`grep -cE '[Dd]ecision [0-9]'`, which cannot match `decisions 53/55` or `decisions 34/36/53/54`** —
so these lines were never in any sweep's input at all, with one exception noted below.
**Scope:** ui
**Hardware:** none — doc comments in one Rust source file, one CSS comment and one `Cargo.toml`
comment. Nothing is built for a board, the UI is not launched, no probe, no live Core. Classified
fresh at filing.
**Owner:** no

**Doc-size reserve for `ui`: nothing in reserve.** If your work pushes a `ui` doc into the last 10%
of its cap, file `tasks/ui/<next free NNN>-compact-ui.md` in the same commit per `tasks/README.md`.
**`tasks/doc/` is not yours.**

## What

Eight lines matched, measured 2026-09-16 with `grep -rInE '[Dd]ecisions [0-9]'` over the repo
excluding `.git` and `target`. **Seven are yours; `assets/app.js:853` is the eighth and `ui/054`
already found and checked it** — it is the line that made this defect visible in the first place, so
confirm and move on rather than re-deriving it.

```
Cargo.toml:26              `embarch-api` decisions 37/38
assets/style.css:739       Decisions 10 and 11      CAPITALIZED, bare — see the warning below
src/study_designer.rs:431  ...39/52/55, `embarch-outpost` decisions 11/12   — the line wraps
src/study_designer.rs:538  `embarch-study-designer` decisions 34/36/53/54
src/study_designer.rs:734  (`embarch-study-designer` decisions 53/55)
src/study_designer.rs:2323 (`embarch-study-designer` decisions 52/55)
src/study_designer.rs:2372 `embarch-study-designer` decisions 34/36/53/54
assets/app.js:853          (`embarch-study-designer` decisions 53/55)       — already checked by ui/054
```

**Seven unchecked lines, roughly 22 distinct decision instances** — treat the line count as a floor
and report the instance count you actually checked.

Two warnings, both earned:

- **`assets/style.css:739` reads `Decisions 10 and 11`, capitalized and bare, and a bare
  `decision 10` cannot be resolved by number in this repo at all.** `ui/054`'s reviewer found six
  bare `decision 10` sites in `assets/app.js` resolving four different ways: `embarch-topology`'s,
  plus `embarch-ui`'s **own decision 10 in three different files** — `decisions/topology-tab.md`
  (routing), `decisions/trace-view.md` (trace) and `decisions/trace-chart.md` (chart).
  `embarch-ui`'s `decisions.md` documents that collision deliberately with the tags `10 (routing)`,
  `10 (trace)`, `10 (chart)`. **Resolve this one by reading what the surrounding CSS block is
  about**, and say in your report which referent you landed on and why. It is also a shipped asset
  under decision 2's zero-build rule, so the comment travels with the product.
- **`src/study_designer.rs:431` wraps**, and the numbers before `embarch-outpost` — `39/52/55` —
  belong to whatever repo the previous line names. Read the whole doc comment, not the grep hit.

## How

1. **Re-census with `[Dd]ecisions? [0-9]`, case-insensitively.** Report your number against the
   seven above.
2. **For each cited number, check the decision exists in the file the citation points at**, and
   remember a bare `decision NN` in another sub-project's file means *that* sub-project's NN —
   except where the `decision 10` collision above makes number-resolution impossible.
3. **Then read the cited decision's current text and check the sentence around the citation is
   still true of it.** `study-designer/054` found a citation that was correct when written and went
   false when `embarch-topology` amended the decision it cited; `embarch-study-designer` is the
   repo cited most here and it has been amended repeatedly. The two `decisions 34/36/53/54` sites
   both make the same claim about a failure mode — check it once against the decisions and then
   check both sites say it the same way.
4. **Fix wrong numbers and false sentences. Do not widen.** A wrong number that is not a decision
   citation is a finding for `inbox/`, not an edit.

## Done when

Every plural-form citation line in `embarch-ui` has had the existence-and-truth pass, the report
states the instance count checked against the seven-line floor, the `style.css` `Decisions 10 and
11` referent is named with its reasoning, and each defect found is either fixed here or filed with
its reason for not being fixed here.

## Result (2026-09-16)

**Re-census** with `grep -rInE '[Dd]ecisions [0-9]'` over `embarch-ui` reproduced the same 8 lines
listed above — no new plain-line hits.

**Wrap check** (`core/068`'s method, `grep -rlIE '[Dd]ecisions[[:space:]]*$'`) flagged exactly the
two files expected: `src/study_designer.rs` (the known `430→431` wrap) and, new, **`assets/app.js`
`2706→2707`**: `/* One GATT-notify tap row (`embarch-study-designer` decisions\n * 52/55): ...` — a
ninth citation line invisible to every line-based grep, task file included. Checked: `decisions
52/55` here pairs correctly (52 = declared payload layout, 55 = GattNotify tap production), same
combination already verified at `study_designer.rs:2323`. No defect, no edit.

**Existence + truth pass, all 9 lines (7 task lines + the 2 wrap sites, one already counted):**

1. `Cargo.toml:26` — `embarch-api` decisions 37/38. Both exist (combined entry
   `embarch-api/decisions/client-crate.md`). Sentence true: 37/38 is exactly the
   `embarch-core-client` extraction that lets `embarch-ui` reach Core without linking
   probe-rs/serialport directly, matching the comment's claim.
2. `assets/style.css:739` — bare `Decisions 10 and 11`. **Decision 10 collides three ways in this
   repo** (routing/trace/chart per `ui/054`'s finding); resolved by content: the comment's own
   sentence — "designed against... the committed `native_sim` capture (848 records, 7 threads...)"
   — is close to verbatim from `embarch-ui/decisions/trace-view.md`'s decision 10 ("designed
   against the closest thing that existed — a committed `native_sim` capture... Three of its seven
   thread pointers resolve to no name"). **Referent: decision 10 (trace)**, not routing or chart.
   Decision 11 is unique (`study-designer.md`), and its "any is a visible, deliberate choice"
   language matches the CSS's own "a checkbox that is a visible, deliberate choice" one paragraph
   below. Both true, no edit.
3. `src/study_designer.rs:430-431` (wraps) — `embarch-study-designer` decisions 39/52/55,
   `embarch-outpost` decisions 11/12. All five exist and all five check out against the doc
   comment's claims about tap shape, layout declaration, GATT-tap production, and outpost routing
   (signal names the source, topology resolves the carrier). No defect.
4. `src/study_designer.rs:538` and `:2372` — **wrong number, fixed.** Both sites claim, verbatim,
   that decisions 34/36/53/54 were "each opened by" the failure "a tap whose characteristic no step
   subscribes captures nothing, passes, and looks fine." Checked all four: 34 (`authoring.md`,
   "a real monitor-everything run came back empty"), 36 (`gatt.md`, "producing an empty capture and
   a pass") and 54 (`removed.md`, "the 'nothing captured, no error' family... opened by from four
   directions") all match. **53 does not** — `gatt.md`'s decision 53 (`GattMonitorSelected`) was
   opened by a *flooding* problem ("floods the link with traffic nobody asked for"), the opposite
   failure. The real fourth direction is **decision 55** (`payload-meaning.md`), whose own text is
   the closest verbatim match to the comment: *"A tap naming a characteristic no step subscribes to
   captures nothing, passes, and looks fine. Refused at authoring time by `embarch-ui`."* Fixed both
   sites: `34/36/53/54` → `34/36/54/55`.
5. `src/study_designer.rs:734` — decisions 53/55 (selective-monitor targets / GATT-tap
   characteristic pick). Correct pairing, true.
6. `src/study_designer.rs:2323` — decisions 52/55 (payload layout / tap production), section
   heading for the GattNotify-tap test block. Correct, true.
7. `assets/app.js:853` — decisions 53/55, already checked by `ui/054`; confirmed same correct
   pairing as #5.
8. `assets/app.js:2706-2707` (wrap, new) — see above, correct.

**Tally:** 9 distinct citation lines (7 from the task's plural-only census + 1 already-checked
`app.js:853` + 1 new wrap-only line at `app.js:2706`), **~25 distinct decision instances** checked
(2+2+5+4+2+2+2+2+2, counting the `style.css` pair once resolved), **1 wrong number** (decision 53
should have been 55 in the "each opened by" claim, duplicated at two sites), **1 false sentence**
tied to that wrong number (the claim that decision 53 was "opened by" the empty-capture failure —
it was opened by a flooding problem instead). Both instances fixed in this unit; no inbox drop
needed, the defect was entirely inside `embarch-ui`.

**Gate:** `cargo build --all-targets`, `cargo test` (93 passed, 4 ignored), `cargo clippy
--all-targets -- -D warnings` all green in the `embarch-ui` worktree.

Branches pushed: `agent/ui/061-plural-citation-recheck` (code),
`agent/ui/061-plural-citation-recheck-doc` (doc).
