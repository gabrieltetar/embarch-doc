# 040 — twenty-two source comments cite other repos' decision numbers as if they were `embarch-ui`'s

**State:** claimed — leg 102, 2026-09-12, branch `agent/ui/040-foreign-decision-citations`.

**Doc-size reserve for `embarch-ui`:** nothing in reserve — no file of this sub-project is
inside the last 10% of its cap. If your work pushes one in, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit.

**Source:** leg 101's refill sweep, 2026-09-12. Verified by reading both sides and enumerating the
full set.
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`embarch-doc/embarch-ui/decisions.md:7`: *"Decision numbers are permanent and address this
sub-project, not a file. Cite them as `embarch-ui decision N`."* That index covers **1–26 only** —
`grep -hoE '^### [0-9]+' decisions/*.md` tops out at 26.

Twenty-two source comments cite a bare number above 26:

- `assets/app.js` — lines 853, 875, 889, 905, 939, 1054, 1055, 1129, 1136, 1147, 1174, 1179, 1192,
  1587, 1684, 2403
- `src/study_designer.rs` — lines 268, 445, 538, 1969, 2372
- `src/trace.rs` — line 2474

Two examples:

- `src/study_designer.rs:538` — ``the exact failure decisions 34/36/53/54 were each opened by``
- `src/trace.rs:2474` — ``` `embarch-core` clears the signal port's input on open (decision 30) ```

**The sweep found all but one resolve to `embarch-study-designer`; `trace.rs:2474` is
`embarch-core` decision 30.** Treat that as a lead and not as fact — **re-derive each one yourself
from the decision bodies**, not the headings, before you qualify it. The last three units of this
class (`core/008`, `topology/034`, `umbrella/043`) each found at least one citation that resolved to
a number in the right repo and a *body* about something else, and a heading-only check would have
waved it through.

This repo already knows the right form — the same files write
`` `embarch-study-designer` decision 56 `` correctly nine times — and the doc side writes
"(embarch-core decision 30)" at `decisions/trace-view.md:47`. That is what makes these twenty-two a
defect rather than a local convention.

## Why now

Fourth sub-project in this class this week. A bare number that *resolves in the wrong repo* is the
worst-behaved member of it: nothing fails, and a reader who follows the citation lands on a real
decision about something else and concludes the comment is stale rather than misrouted.

`assets/app.js` carries sixteen of the twenty-two, so this is mostly a JavaScript comment pass —
note that `tests/element_ids.rs` parses `app.js` as text, so re-run `cargo test` even though nothing
executable changes.

## Done when

- [ ] Every one of the twenty-two carries its owning repo in the settled cross-repo form
      `` `<repo>` decision N ``, with N unchanged and **the body confirmed to be about the thing the
      comment claims**. Report the count you checked against the count you changed; if they differ,
      the difference is the interesting finding.
- [ ] This returns nothing:
      ```
      grep -rnoE ".{25}decisions? [0-9]+(/[0-9]+)*" src/*.rs assets/app.js assets/index.html | grep -vE "embarch-[a-z-]+\`? decision" | grep -E "decisions? (2[7-9]|[3-9][0-9])"
      ```
- [ ] `embarch-ui` `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.

Two small adjacent things found in the same sweep. **Fix them only if they are genuinely one line
each; otherwise say so in your report and leave them**, rather than growing this unit:

- `src/study_designer.rs:543` — an error string reads `"captures {} , but no step…"`, a stray space
  before the comma. It is operator-facing.
- `src/snapshot.rs:93-97` — a comment says "the other three" and "four near-identical ones" beside a
  **six**-call `tokio::join!`. Stale prose with no doc side. Count the calls yourself before
  changing the number.

**Worktree note:** an `embarch-ui` worktree needs **three** sibling symlinks into its parent —
`embarch-study-designer`, `embarch-api` **and `embarch-topology`**. The last is the trap: `Cargo.toml`
does not name it, but `embarch-api/crates/embarch-core-client` path-depends on it, so without it the
first `cargo build` fails on a path inside the fleet's scratch directory. Your supervisor should have
made these; if a build fails that way, say so rather than making them yourself.

**Doc-size note:** no `embarch-ui` doc is currently in reserve. If your work puts one there, file
`tasks/ui/NNN-compact-ui.md` in the same commit — your own scope only, never `tasks/doc/`.
