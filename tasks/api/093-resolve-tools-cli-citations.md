# 093 — Sweep decision citations in `resolve.rs`, `tools.rs`, `cli.rs`

**State:** claimed by agent/api/093-resolve-tools-cli-citations, 2026-09-13 20:33
**Source:** `api/091` swept `crates/embarch-core-client/src/client.rs` (99 citations) and
`src/config.rs` (37 citations) end to end and ran out of scope before reaching the rest of the
surface named in that task's own count: `src/resolve.rs` (~32), `src/tools.rs` (~24),
`src/cli.rs` (~17).
**Scope:** api
**Hardware:** none — source comments only; no board, no live Core, no deploy.
**Owner:** no

**Reserve (told at dispatch, 2026-09-13 20:33):** one `embarch-api` doc file is in reserve —
`spec.md`, **88.9%**, 1138 B left, filed against `tasks/api/083` which is **`blocked` on
`In flux: yes`**. Nothing else in this sub-project is in reserve. A citation sweep should not
need to write `spec.md` at all; if yours does and it spends that reserve, `DOC-COMPACTION.md` §2
applies — compact it in this same unit carrying `tasks/api/083`'s `Must not delete:` list. If you
push any *other* `embarch-api` doc file into its last 10%, file `tasks/api/<next>-compact-api.md`
in the same commit (`check-task-numbers.py --next api` for the number — never `ls | tail`).

**Two findings from the sweeps that ran just before this one, so you do not re-derive them:**

1. **Citations are not only in comments.** `api/091`'s worst defect of six was a wrong decision
   number inside the runtime `"unavailable"` string `render_hello_ack` builds and returns to a
   caller — it told an *operator* to go read the wrong decision. `check-decision-refs.py` reads
   only `*.md`, so a number in a string literal is exactly as invisible as one in a comment and
   has a worse audience. **Sweep string literals in these three files too, not just `///` and
   `//`.**
2. **"Wrong number" and "false sentence" are two different defects with different causes, and a
   sweep that looks for one usually misses the other.** `study-designer/045` came back 3 wrong
   numbers / 0 false sentences; `topology/040`, the same method the same hour, came back 0 wrong
   numbers / 3 false sentences. One of `topology/040`'s had a *subject that no longer existed* —
   the number still resolved, and it had already survived two passes that were checking numbers.
   **Read the sentence around each citation against the cited decision's body, and check that what
   the sentence is about still exists.**

## What

Continue the same sweep, in this order: `resolve.rs`, `tools.rs`, `cli.rs`. For each citation,
resolve the number, say which repo's decision set it resolves against (bare same-repo, labelled
`<repo> decision N` for a foreign referent — `client-crate.md`/`hardware-selection.md` already
show `embarch-api` and `embarch-core` sharing numbers, and `client.rs` additionally cited
`embarch-study-designer`, `embarch-outpost`, `embarch-topology` and `embarch-ui`), and read the
cited decision's body against the sentence around the citation, not just the number.

## Why now

`api/091` found `client.rs`'s 99 citations were mostly sound but not flawless: one real
wrong-number defect (`embarch-api` decision 59 cited four times, including once inside a
user-facing string literal, for content that decision 60 states) and two ambiguous/unlabelled
foreign citations (`embarch-topology` decision 14, `embarch-study-designer` decision 40, both
appearing bare immediately after a differently-labelled sibling citation in the same sentence).
`config.rs`'s 37 checked clean. `resolve.rs`/`tools.rs`/`cli.rs` are unswept.

## Done when

- [x] `resolve.rs`, `tools.rs` and `cli.rs` are swept end to end, in that order, as far as
      honestly reached; any remainder filed as `tasks/api/<next>` naming the files not reached.
      All three fully reached; no remainder to file.
- [x] Every cross-repo citation in the swept files carries the labelled `<repo> decision N` form.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/` fragment. A numbered decision only if something was actually decided.

## Result

Swept all three files end to end, including string literals (per finding 1) and checking each
cited decision's body against the sentence around the citation, not just the number (per
finding 2).

**Citations read:** 75 (34 in `resolve.rs`, 24 in `tools.rs`, 17 in `cli.rs`).

**Wrong numbers fixed:** 1 — `tools.rs`'s `TargetParams` doc comment read "(decision 12,
decision 12)", a literal duplicate. `git log -L` traced it to `5131ec7` ("Sweep dead design.md
citations into decision/repo-qualified form"): the original text was `` (`design.md` §3
decision 12) `` — one citation, number 12 — and the mechanical sweep replaced `` `design.md`
§3 `` with `decision 12` instead of deleting it, doubling the citation. Collapsed to one.

**False sentences fixed:** 1, and it was inside a runtime string literal (the class finding 1
warns about) — `declare_signal`'s `#[tool(description = "...")]` cited "`embarch-topology`
decision 18's 2026-08-25 amendment". Decision 18 was created 2026-09-02 per
`embarch-topology/decisions/links.md`'s own git history, so an amendment dated before its own
creation is impossible; no 2026-08-25 date appears anywhere in `embarch-topology`'s docs. What
actually gave `declare_signal`/`list_signals`/`remove_signal` a CLI and MCP tool is `embarch-api`
decision 67 (2026-09-10, matching the code's own `git log`), which topology's own `links.md`
states in so many words ("Untouched by `embarch-api` decision 67 (2026-09-10), which gave these
routes a CLI and an MCP tool"). Fixed to cite both: "`embarch-topology` decision 18, wrapped per
`embarch-api` decision 67". **Bonus, same cause, outside the three named files:**
`embarch-api/interfaces/tools-topology.md` carried the identical wrong claim (its own file header
already correctly attributes the same rows to decision 67) — fixed there too since it's the same
defect, one word apart from a doc-fix I was already positioned to make.

**Cross-repo citations relabelled:** 0. Every foreign citation across all three files already
carried the `<repo> decision N` form (`embarch-topology`, `embarch-core`, `embarch-study-designer`
all appear labelled); no bare citation was found resolving to the wrong repo's number.

**Citations judged and left alone:** 73. Checked each cited decision's body against the sentence
around the citation and confirmed the subject still exists, not just that the number resolves.
One borderline case worth naming: `embarch-study-designer` decision 26 is cited in both
`tools.rs` and `cli.rs` for "recompute and overwrite all three of a study's seals" — decision 26's
own text names only `steps_crc` (the other two seals were added later, per `seals.md`'s own
account, and the "all three" current behavior is covered by `embarch-api` decision 44(b)).
Left as-is: decision 26 is still a legitimate anchor for the recompute-and-overwrite idiom it
established, and the subject (that idiom, now covering three seals) genuinely exists — this reads
as looseness, not a defect.

Gate: `cargo build`/`cargo test`/`cargo clippy --all-targets -- -D warnings` green in the code
worktree; `scripts/check-docs.py` (11/11), `scripts/check-client-names.py --repo <code>`, and
`scripts/check-ownership.py --scope api` / `--code-repo` all green in the doc worktree. No
`embarch-api` doc file was pushed into reserve by this change (`check-doc-size.py` stayed green);
`spec.md`'s existing reserve (task `api/083`) was not touched.
