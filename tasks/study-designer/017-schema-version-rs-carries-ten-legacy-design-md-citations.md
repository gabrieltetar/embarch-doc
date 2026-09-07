# 017 — `schema_version.rs` carries ten legacy `design.md §3 decision N` citations

**State:** done
**Source:** `embarch-reviewer` on `tasks/study-designer/016`, leg 031, 2026-09-07 — the reviewer
found *two* such citations that unit had newly authored; the supervisor fixed those two in scope
(`embarch-study-designer` **`f70e4ae`**) and found ten more while doing it. This task is the ten.
**Scope:** study-designer
**Hardware:** none
**Owner:** no

## Doc-size reserve — supervisor, leg start 2026-09-07 09:44

**`embarch-study-designer/decisions/crate.md` came *out* of reserve last leg** — 5,159 B at 42.0%
after unit 016's mission split, with the new `decisions/ci.md` at 7,462 B (91.1% of its own 8,192 B
cap is *not* where it sits — it has room). **No `embarch-study-designer` doc is in reserve today.**
`tasks/study-designer/006` stays `blocked` for a different reason (an in-flux FFI staticlib fact),
and it is **not** your job to touch it. You owe a compaction task only if your own edits push one of
your sub-project's docs into the last 10% of its cap.

**One suite-wide hazard applies to you: `suite/features.md` has 60 bytes of headroom** (20,420 of
20,480 B). It is *assembled* from `features.d/` fragments, so **a new `features.d/` fragment will
push it over its cap and turn the fold red.** This unit is doc-comment corrections and should not
ship a feature row — if you think it warrants one, put the row's text in this task file, do not
create the fragment, and say so.

## What

`src/schema_version.rs` cites decisions in the retired `design.md §3 decision N` form in **twelve**
places. Two were authored by unit 016 and are already corrected. The remaining **ten** are
pre-existing, at these lines as of `f70e4ae`:

| line | citation | whose decision |
|---|---|---|
| 1 | `design.md §3 decision 12` | this crate's own |
| 70 | `` `embarch-dev-bench/design.md` §3 decisions 7/18 `` | `embarch-dev-bench` |
| 147 | `§3 decision 47, `embarch-core/design.md` §3 decision 35` | own, and `embarch-core` |
| 155 | `` `embarch-outpost/design.md` §3 decision 9 `` | `embarch-outpost` |
| 198 | `` `embarch-dev-bench/design.md` §3 `` | `embarch-dev-bench` |
| 203 | `design.md §3` (decisions 31/32) | this crate's own |
| 214 | `§3 decisions 58-62`, `` `embarch-dev-bench/design.md` §3 `` | own, and `embarch-dev-bench` |
| 239 | `design.md` §3 (decision 52 area) | this crate's own |
| 312 | `design.md §3 decision 52` | this crate's own |
| 323 | `design.md §3 decision 12` | this crate's own |

**`design.md` does not exist for any sub-project.** Every one was split into
`spec.md` / `open.md` / `decisions/<mission>.md` on 2026-09-04, so each of these points a reader —
including a connecting agent with no cwd — at a file that is gone.

## The correct spellings, per `DOC-CONVENTIONS.md` *Referring to a decision*

- **This crate's own decision, cited from inside this crate:** the bare number — `decision 12`.
  `decisions/removed.md` already does this correctly for decision 19.
- **Another sub-project's:** `embarch-dev-bench decision 7`, `embarch-core decision 35`,
  `embarch-outpost decision 9` — repo name plus bare number, **no file**.
- **Prefer the bare number over a link either way.** A link names a *file*, and a mission split
  moves an entry between a sub-project's decision files without changing its number — which is
  what `tasks/doc/022` is, and what this leg hit for real in `history/study-designer.md`.

## Why now

This is the same defect `tasks/api/040` closed for `embarch-api`'s six MCP tool descriptions, in
the sub-project that is **the most depended-on crate in the suite** — three consumers in two
languages, one of them C through an FFI boundary. `embarch-api` decision 57 recorded the rule for
tool descriptions; nothing has swept Rust doc comments, and `cargo doc` does not flag a citation
that is merely wrong (only a broken *intra-doc link*, which these are not — they are prose).

**`embarch-study-designer` decision 68 is why no gate will ever catch these:** that decision, filed
by unit 016 in `decisions/ci.md`, deliberately keeps `cargo doc` warnings out of the gate. It is a
defensible call and this task is not an argument against it — it is the consequence, written down.

## Scope note

**Doc comments only, in `embarch-study-designer`.** Do not edit another sub-project's repo to
correct a citation *about* it — the citation lives here and is fixed here. If a decision number
turns out not to exist under the repo the citation names, **stop and report it** rather than
guessing which number was meant: a citation fixed to a different wrong number is the same defect
in new clothes, which is the trap `enroll_probe` fell into in `tasks/api/040`.

## Done when

- [x] All ten citations use a bare `decision N` (own) or `<repo> decision N` (another's), with no
      `design.md` and no `§3` anywhere in `src/schema_version.rs`.
- [x] Every number verified to resolve against the named sub-project's current `decisions.md`
      index — say in the task file which ones you checked and how.
- [x] A repo-wide `grep -rn 'design\.md' src/` reports what is left, if anything, and the task
      says whether that is a further sweep or nothing.
- [x] `cargo doc --no-deps --all-features` still reports **0** warnings — and run it after a
      `cargo clean -p embarch-study-designer`, because a cached green here is the worker's own
      previous run replayed, not a check.
- [x] Gate green; `changelog.d/study-designer-*` fragment.

## Closing notes — worker, 2026-09-07

**Scope turned out to be larger than "ten" once "no `§3` anywhere" (Done-when bullet 1) was taken
literally.** The ten table rows are the ten places `design.md` literally appears in
`schema_version.rs`, but the file also carried **twenty more** bare `§3 decision N` / `§3 decisions
N/M` citations with no `design.md` prefix (e.g. line 9 `(§3 decisions 17, 19)`) — same retired
form, just missing the file name half. All of those are this crate's own decisions (none pointed at
another sub-project), all verified to resolve (list below), and all fixed the same way: `§3
decision(s)` → `decision(s)`. `grep -n '§3\|design\.md' src/schema_version.rs` now returns nothing.

**One of the ten table rows didn't match the table's own description.** Row "239" was tabulated as
`design.md §3 (decision 52 area)`, but the actual text at that location (confirmed unchanged since
`f70e4ae` — no other commits landed on this file after the claim commit) is `(design.md §5.1)`: no
`§3`, no decision number at all — a citation to a *spec section* of the retired file, not a
decision. Since it doesn't resolve to any decision number under any spelling rule the task
describes, I did not invent one; I dropped the stale file/section pointer entirely (the sentence
reads fine without it — `GET /status` is already introduced as the connection-establishment check
two sentences later). Flagging this explicitly per the "stop and report rather than guess" rule,
even though the fix itself (delete a pointer to a gone file) needed no guess.

**Decision numbers checked, against each sub-project's current top-level `decisions.md` index**
(the `| Load this for | Decisions |` table, which is a set membership check — I did not open every
target file, since the index itself already resolves the number to a mission file):

- `embarch-study-designer` (own): 5 (versioning.md not needed, but table below), 7 — n/a;
  actually checked: **12, 17, 19, 24, 25, 27, 31, 32, 36, 39, 40, 41, 42, 43, 44, 47, 50, 52, 53,
  54, 58, 59, 60, 61, 62** — every one present in `embarch-study-designer/decisions.md`'s index
  (spread across `versioning.md`, `wire.md`, `streams.md`, `gatt.md`, `study.md`, `ble.md`,
  `declares.md`, `seals.md`, `removed.md`, `payload-meaning.md`, `protocols.md`,
  `protocol-exec.md`, `limits.md`). None missing.
- `embarch-dev-bench`: **7, 18** (`link.md`), **39** (`logging.md`), **41** (`protocols.md`) — all
  present in `embarch-dev-bench/decisions.md`'s index.
- `embarch-core`: **35** (`handshake.md`) — present in `embarch-core/decisions.md`'s index.
- `embarch-outpost`: **9** (`manifest.md`) — present in `embarch-outpost/decisions.md`'s index.

No number failed to resolve; nothing was guessed.

**Repo-wide `grep -rn 'design\.md' src/` (from the code worktree) reports 290 occurrences across 23
other files** (`study.rs`, `limits.rs`, `streams.rs`, `study_builder.rs`, `result.rs`,
`protocol.rs`, `ffi.rs`, `lib.rs`, `gatt.rs`, `sample.rs`, `gatt_extract.rs`, `outpost.rs`,
`merged_actions.rs`, `eap.rs`, `decoder.rs`, `crc.rs`, `registry.rs`, `bounded.rs`, `ids.rs`,
`vendor.rs`, `gatt_names.rs`, `eap_parse.rs`, `eap_interp.rs`) — **`schema_version.rs` itself is
now clean.** This is a further sweep, well beyond one unit: filed as
`tasks/study-designer/018-design-md-citations-repo-wide-sweep.md`, with the full per-file count and
a note that it likely splits into more than one unit.

**`cargo doc --no-deps --all-features`, run after `cargo clean -p embarch-study-designer`: 0
warnings.** `cargo build`, `cargo test` (108 + 9 tests, all pass), `cargo clippy --all-targets -- -D
warnings`: all clean, no `Cargo.toml` below the crate root.
