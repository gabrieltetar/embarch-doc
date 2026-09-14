# 066 — The ~104 citations outside `doctor.rs` are the half `umbrella/065` did not reach

**State:** open
**Source:** `tasks/umbrella/065` swept `src/doctor.rs` end to end on 2026-09-13 — ~129 citations
across checks 1–17, two wrong numbers found (both `decision 39` where the claim belonged to decision
33) and, for the first time in four days of sweeps, **zero false sentences.** That sweep stopped at
that file. The leg of 2026-09-13 18:3x counted the rest of the repo.
**Scope:** umbrella
**Hardware:** none — source comments only; no board, no live Core, no deploy, no install.
**Owner:** no

## What

```
23  src/locate.rs
17  src/setup.rs
14  src/install.rs
14  src/init.rs
 9  src/main.rs
 9  src/config.rs
 8  src/deploy.rs
```
…plus `state.rs` (5), `zephyr.rs` (3), `manifest.rs` (1), `env.rs` (1) — **~104 lines, eleven files,
none of them swept.**

**`check-decision-refs.py` resolves decision numbers only inside `*.md`**, so a wrong number in a
source comment fails no gate and never has.

## Why this half is not simply "more of the same"

`umbrella/065`'s clean result came with an explicit caveat in its own log entry, and this task is
how that caveat gets tested rather than carried:

> One honest reading is that `doctor.rs` is comment-heavy prose that gets re-read whenever a check
> changes, so it self-maintains in a way decision *bodies* do not. **That reasoning has not been
> tested and someone should not carry it forward as established.**

**These eleven files are the test.** If the self-maintenance theory is right, they should be
*dirtier* than `doctor.rs`, not cleaner — a `locate.rs` comment is not re-read every time a doctor
check is edited. If they come back just as clean, the theory is wrong and the real explanation is
something about this repo as a whole. **Either result is a finding worth writing down**, and this is
the rare sweep where the negative result is as interesting as the positive one.

Two specific things to watch for, both with live instances in this repo:

- **Same-number cross-repo collisions.** `umbrella/064` found one in `mirrors.md` on 2026-09-13: a
  bare `decision N` that reads as this repo's and is actually another's. `deploy.rs`, `install.rs`
  and `locate.rs` all legitimately talk about `embarch-core` and `embarch-api` behaviour, so they
  are where a bare number is most likely to mean a foreign decision. `umbrella/065` established the
  convention has taken in `doctor.rs` — all seven of its cross-repo citations were already
  labelled. **Check whether that is true outside `doctor.rs`.**
- **`embarch-umbrella` decision 14 is cited from at least four repos' comments.** The log already
  flags it: a decision cited that widely is one whose body has to stay true for all of them, and
  nothing checks that. If you meet a citation of 14 here, read the body against this file's use of
  it specifically.

## What to do

Take the files in the order listed and get as far as you honestly can. **A partial sweep with an
accurate boundary beats a rushed complete one** — file `tasks/umbrella/<next>` for the remainder,
naming exactly which files you reached.

For each citation:

1. **Resolve the number and say which repo's set it resolves against.** Where the referent is
   another repo's decision, use the labelled form `embarch-core decision N`. Same-repo citations
   stay bare. Do not invent a new form — the general question is owner-reserved (`tasks/doc/055`).
2. **Read the decision body against the sentence around the citation, not just the number.**
3. **Do not manufacture findings.** "Twenty-three checked, twenty-three held" is a real and
   reportable outcome. Say how many you actually read versus how many you counted, and — because of
   the theory above — **say plainly whether these files were dirtier or cleaner than `doctor.rs`'s
   2-in-129.**

## Done when

- [ ] The listed files are swept, or the boundary is stated exactly and the remainder filed.
- [ ] Every cross-repo citation in the swept files carries the labelled `<repo> decision N` form,
      or the task reports that it already did.
- [ ] The `doctor.rs`-self-maintains theory is answered with a number, not an impression.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment. A numbered decision only if something was actually *decided*.

## Reserve, for planning

`embarch-umbrella/decisions/bind.md` is 11,533/12,288 B — **755 B left, 93.9%** — filed against
blocked `tasks/umbrella/009`. Nothing else in this scope is in reserve. If your work leaves any
`embarch-umbrella` doc in the last 10% of its cap unfiled, file
`tasks/umbrella/<next>-compact-docs.md` in the same commit — **your own scope**, never `tasks/doc/`.
