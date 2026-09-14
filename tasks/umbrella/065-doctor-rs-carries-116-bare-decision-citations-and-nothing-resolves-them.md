# 065 — `doctor.rs` carries 116 bare decision citations and no gate can resolve one

**State:** done
**Source:** `tasks/umbrella/063`'s own closing note — it swept `locate.rs`, `init.rs` and `config.rs`
and deliberately left `doctor.rs` out as *"roughly another hundred bare citations in one file — not
a twenty-minute pass"*, adding that **nothing is filed for it**. The leg of 2026-09-13 17:5x counted
**116** and filed this.
**Scope:** umbrella
**Hardware:** none — source comments only; nothing is built for a board, nothing is run.
**Owner:** no

## What

`embarch-umbrella/src/doctor.rs` carries 116 lines matching `decision[s] N`. **`check-decision-refs.py`
resolves decision numbers only inside `*.md`**, so a wrong number in a source comment that happens
to look well-formed fails no gate and never has. This file is the single largest unswept
concentration in the repo.

## Why this class keeps being worth running

Across four consecutive days of these sweeps the headline number — how many citations were wrong —
has been the *less* interesting half of every result. The real yield has been **prose that a
decision made false and nobody updated**:

- `umbrella/063` fixed four things in three files. Only **two** were wrong numbers. The other two
  were sentences that went false when decision 38 landed **the same day** — `locate_core`'s
  precedence-order comment omitted a step that now runs ahead of both guesses, and
  `windows_core_service_binary_path`'s doc still said `locate_core` *"deliberately guesses"*.
- `core/054`, `ui/040` and `dev-bench/020` each found the same shape at a scale nobody had budgeted.

So **read the cited decision's body and then read the sentence around the citation**, in that order.
A number that resolves is not evidence the claim holds. Report the two categories separately.

## Bounding

116 citations is more than one pass. **Take `doctor.rs`'s checks in numeric order and get as far as
you honestly can inside your unit**, then file `tasks/umbrella/<next>` for the remainder, naming the
exact check number you stopped after so the next worker starts cleanly. **A half-finished sweep that
says precisely where it stopped is a good outcome here; a rushed complete one is not.** Do not pad
the count by skimming.

Two specific things to watch for, both seen in this repo already:

1. **Cross-repo numbers collide.** `doctor` reasons about `embarch-core`, `embarch-api` and
   `embarch-topology` constantly, so a bare `decision N` here may resolve against
   `embarch-umbrella`'s own index when it meant another repo's. Where a citation crosses a repo
   boundary, write `<repo> decision N` — the form `embarch-api` decision 57 fixed on.
2. **`embarch-umbrella` decision 14 is now cited from several repos' comments**, each correct in
   isolation. If `doctor.rs` adds another site, note it: a decision cited from four repos is one
   whose body must stay true for all of them, and nothing checks that.

## Reserve, for planning

`embarch-umbrella/decisions/bind.md` is 11,533/12,288 B — **755 B left, 93.9%** — filed against
blocked `tasks/umbrella/009`. `decisions/mirrors.md` is at 86.5%. A sweep that only fixes comments
should touch neither; if it does and leaves one in the last 10% of its cap unfiled, file
`tasks/umbrella/<next>-compact-docs.md` in the same commit — **your own scope**, never `tasks/doc/`.

## Done when

- [x] Every citation examined in the range you took is either confirmed against the cited body or
      fixed, with **wrong numbers and false sentences counted separately**.
- [x] Cross-repo citations carry their repo name.
- [x] A follow-up task is filed for the remainder, naming the check number you stopped after — or a
      line in the fold saying the file is fully swept.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/umbrella-*` fragment.

## Result

Read every one of the ~132 `decision[s] N` citations in `doctor.rs` (checks 1 through 17,
implementation and tests alike — the whole file, not a partial range), checking each cited
decision's own body first and then the sentence around the citation, per this task's rule.

**File is fully swept. No follow-up task needed.**

- **Wrong numbers: 2**, both the same defect in two places. `TokenAttempt` (check 4's gather/judge
  split doc, line ~701) and `DevBenchAttempt` (check 12's, line ~2253) each cited "decision 39" —
  reporting.md's check-16-path-field decision — for the claim that the gather/judge split lets a
  check be tested "without a network, a Core or a bench." That claim is decision 33's
  (schema-skew.md: "The comparison is a pure function over injected numbers... tested with no
  Core, no bench, no network"), not decision 39's, which is about nothing of the kind. Both fixed
  to cite decision 33.
- **False sentences: 0.** Every other citation's surrounding prose held up against the cited
  decision's current body, cross-repo citations included (`embarch-core` decisions 13/37/57,
  `embarch-api` decisions 15/52/53, `embarch-dev-bench` decision 25 — all verified against their
  own repos' decision files, all already correctly labeled with their repo name in this file's
  existing convention).
- **Cross-repo citations**: already correctly labeled everywhere (`embarch-core decision N`,
  `embarch-api decision N`, `embarch-dev-bench decision N`) — no bare numbers resolving against
  the wrong repo's index were found, unlike `umbrella/064`'s `mirrors.md` finding. `decisions/14`'s
  four-repo citation site this task's Bounding section flagged: `doctor.rs` does not add a fifth,
  and does not cite decision 14 at all.
- Touched only `src/doctor.rs` (2 one-word fixes); no `embarch-umbrella` doc file was edited, so
  `bind.md` (93.9%) and `mirrors.md` (86.5–86.7%) are untouched and no compaction task is filed.
