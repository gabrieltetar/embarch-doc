# 045 — `study_designer.rs:1524` cites `§4.3` for `Uuid`'s serialize form, and `§4.3` was never about `Uuid`

**State:** done — leg 110, 2026-09-13.
**Doc-size reserve (supervisor, leg 110):** **no `embarch-ui` doc is in reserve** — all 13 files
currently inside the last 10% of their cap belong to other sub-projects. You have headroom; the
standing rule still applies, so if your work pushes any file into reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit (`scripts/check-task-numbers.py --next ui` for the
number).
**Source:** the `embarch-reviewer` on `ui/044`, 2026-09-13, flagged deliberately as a report note
rather than a finding — it is a citation-accuracy defect, not a contradiction of any decision, and it
predates the unit the reviewer was reading. Filed by the supervisor (leg 109).
**Scope:** ui
**Hardware:** none — one doc comment, no logic change.
**Owner:** no

## What

`embarch-ui/src/study_designer.rs:1524` cites `embarch-study-designer/interfaces/types.md §4.3` for
`Uuid`'s raw-array-versus-hyphenated `Serialize` form.

**`ui/044` checked this site and correctly left it alone** — its *file* is right, because the `Uuid`
material is `Action`/GATT content that did **not** move in `study-designer/038`'s split. What the
reviewer then found by going further is that the *section* was never right:

- `interfaces/types.md` carries no numbered headings and has not since the 2026-09-02 split, so
  `§4.3` resolves to nothing today.
- In the pre-split monolithic `design.md`, where `§4.3` did exist, **it was `Action`** — not this
  raw-array note.
- No interfaces file (`types.md`, `gatt-types.md`, `result-types.md`) and no
  `embarch-study-designer` decision describes that raw-array-versus-hyphenated split under any
  section number at all.

So this is an imprecise citation carried through the repo-wide `design.md` sweep (`eca2fa1`)
unchanged, and it has pointed at the wrong thing for longer than the split has existed.

## Done when

- [x] `study_designer.rs:1524`'s citation names something that is actually there. **Find where the
      raw-array `Serialize` form is documented before you edit** — if it is documented nowhere, say
      so in the task file and drop the section number rather than inventing one, which is what
      `ui/044` did with the dead `§4.8` on line 780 and is this repo's established precedent.

      Verified the `§4.3` claim by reading the pre-split `design.md` at `d0b7608^`
      (`embarch-study-designer/design.md`, the commit before the 2026-09-02 split): `§4.3` there was
      indeed `Action` (`### 4.3 \`Action\``, line 67), not the `Uuid` raw-array/hyphenated note —
      the reviewer's claim holds. Also confirmed `src/ids.rs` is where the fact this comment states
      actually lives: `pub struct Uuid(pub [u8; 16])` with a plain `#[derive(Serialize,
      Deserialize)]` (no custom impl), so the derived form genuinely is the raw 16-byte array the
      comment describes.

      Dropped the `§4.3` from `study_designer.rs:1524`, keeping the file citation
      (`embarch-study-designer/interfaces/types.md`) per note 3 — `types.md` carries no numbered
      headings since the split, so there is no replacement `§N` to invent, matching `ui/044`'s
      precedent on line 780 exactly.
- [x] A statement, either way, of whether the raw-array form is documented anywhere in
      `embarch-study-designer`. **If it is not, that is a finding worth more than this fix** — drop
      it in `inbox/` at the absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/` for the
      supervisor to file against `study-designer`, because an undocumented serialization form that
      two repos depend on is a different and larger problem than a bad pointer to it.

      **It is not documented anywhere in `embarch-study-designer`.** Checked `interfaces/types.md`,
      `interfaces/gatt-types.md`, `interfaces/result-types.md` (grep for `Uuid`/`hyphenated`/`array`/
      `16 bytes`: nothing describes the raw-array-vs-hyphenated split), every `decisions/*.md`
      (same), and the retired `design.md` — which explicitly punted on it even before the split:
      "exact byte/UUID representations (`[u8; 16]` vs. a `uuid`-crate newtype, `no_std`-compatible
      either way) are implementation detail, not a design choice left open here." The only place the
      fact exists is `src/ids.rs`'s type definition itself. Filed as
      `inbox/study-designer-uuid-serialize-form-undocumented.md`.
- [x] `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green in
      `embarch-ui`. A doc comment, so this is confirmation rather than risk.

      All three green, 2026-09-13.
- [x] `changelog.d/` fragment only if something reader-visible changed; say which way you judged it.
      `ui/044` judged the equivalent repoint not reader-visible and did not drop one.

      Judged not reader-visible — a doc comment over code, same call as `ui/044`. No fragment
      dropped.

## Sweep for the same shape (supervisor note 5)

`grep -rno '§[0-9][0-9a-z.]*' embarch-ui/src/ embarch-ui/assets/ embarch-ui/vscode-extension/`
(plus the doc-repo side, `embarch-ui/*.md` and `embarch-ui/decisions/*.md`) found:

- **Two more cross-repo citations with a numbered section**, both **valid, not defective**:
  `src/trace.rs:11`'s `` `embarch-outpost/spec.md` §5 `` and `assets/app.js:2542`'s
  `` `embarch-study-designer/spec.md` §5 `` — both files still carry a numbered `## 5.` heading
  (`Host-side outputs` / `Result storage` respectively) whose content matches what each comment
  claims. No `embarch-ui/*.md` doc citations of this shape found either. This class is clean here.
- **A different, related defect**: 13 instances of a dead `§3` prefix on `embarch-ui`'s own internal
  `decision N` citations (12 in `src/trace.rs`, 1 in `assets/app.js`) — a leftover from before this
  repo's `design.md` was split into `decisions.md`/`decisions/*.md` (`§3` was `design.md`'s own
  decisions section; the same file cites the same decision both ways, e.g. `trace.rs` has bare
  `decision 10` at lines 1/6/150/262/325 and `§3 decision 10` at 676/1971/2024/2062/3394/3571/3753).
  Out of this task's scope (which was specifically the two `embarch-study-designer/interfaces`
  citations) and not fixed here. Filed as `inbox/ui-stale-section-3-decision-prefix.md`.

Note (supervisor note 6): `check-docs.py`'s link checker does not check section anchors, so a green
gate run proves nothing about either the original `§4.3` defect or this sweep — both were verified
by hand against file contents/git history, not by any script.

## Why now

Cheap, and it closes `embarch-ui`'s half of a class the suite has now paid for four times in a
fortnight (`core/050`, `dev-bench/030`, `study-designer/039`, `ui/044`). After this, **both** of the
two `embarch-study-designer/interfaces` citations in `embarch-ui` are correct — the reviewer's grep
found exactly two in the whole repo, so this task finishes the sweep rather than sampling it.

## Not in scope

- `tasks/study-designer/041`, the same defect class in `embarch-study-designer`'s own docs
  (40 `§N` references into the retired `design.md`). Different repo, different owner, already filed.
- `study_designer.rs:780`, fixed by `ui/044` and landed at `364afe3`.
