# 065 — `doctor.rs` carries 116 bare decision citations and no gate can resolve one

**State:** claimed by agent/umbrella/065-doctor-citations, 2026-09-13 18:00
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

- [ ] Every citation examined in the range you took is either confirmed against the cited body or
      fixed, with **wrong numbers and false sentences counted separately**.
- [ ] Cross-repo citations carry their repo name.
- [ ] A follow-up task is filed for the remainder, naming the check number you stopped after — or a
      line in the fold saying the file is fully swept.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/umbrella-*` fragment.
