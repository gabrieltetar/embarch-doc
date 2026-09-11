# 050 — Write down what `doctor` check 2 is entitled to infer from a sticky `saved.host`

**State:** done — leg 078, 2026-09-10
**Reserve for this scope:** `decisions/bind.md` 11,447/12,288 B (841 B left) and `open.md`
4,493/5,120 B (627 B left) are both in reserve, with `umbrella/009` and `umbrella/038` parked on
them. Put the new decision in a sibling topic file rather than squeezing `bind.md` — that is what
`umbrella/020` and `umbrella/022` did on this same file and it is the preferred move
(`DOC-COMPACTION.md` §2). `open.md` is being *narrowed* by this unit, so it should end smaller; if
it does not, file the debt.
**Source:** `embarch-umbrella/open.md:15`, against decision 22 in
[embarch-umbrella/decisions/bind.md](../../embarch-umbrella/decisions/bind.md). `umbrella/026`
already fixed the `Fail` detail half; the bullet itself says the **intent** half is "undocumented
and unfixed". Surfaced by leg 076's refill sweep.
**Scope:** umbrella
**Hardware:** none
**Owner:** no

## What

`state.rs` carries a comment saying `saved.host` is "only meaningful for `remote`", while `setup`
writes it for **every** class — and `doctor` check 2 reads it regardless. Those two statements
cannot both be the intent. Settle it in one numbered decision that says plainly what check 2 is
entitled to conclude from a `saved.host` it finds, given that the field is sticky and is written on
paths where the comment says it means nothing.

**This task documents the intent; it does not change the clearing behaviour.** Changing when
`saved.host` is cleared alters what a real `doctor` run reports on a real machine, which needs the
bench to confirm and is therefore not dispatchable here. After this lands, `open.md`'s bullet
should narrow to just that unmade behaviour change, so the queue still shows the remainder.

## Why now

A comment and the code that ignores it are a disagreement with no failing test, and check 2 sits
downstream of both — so whichever of the two a future reader believes, they will write a check-2
change that is correct against half the system. Decision 22 is the file where this belongs and it
is silent on the question.

## Done when

- [x] One numbered `embarch-umbrella` decision states what `saved.host` means per class, that
      `setup` writes it for all of them, and what check 2 may and may not infer from finding one.
      Decision 48, `embarch-umbrella/decisions/sticky-host.md`.
- [x] `state.rs`'s "only meaningful for `remote`" comment either agrees with that decision or is
      corrected to. Corrected.
- [x] `embarch-umbrella/open.md:15` narrows to the unmade clearing-behaviour change, which still
      needs a bench. Bullet shrank 4493 B → 4313 B.
- [x] `decisions/bind.md` is at 11,447/12,288 B — **in reserve, 841 B left.** Untouched; decision 48
      went into the new sibling file `decisions/sticky-host.md` instead, per
      [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 and the `umbrella/020`/`022` precedent.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build`/`test`/`clippy -D warnings`
      in `embarch-umbrella`, `check-docs.py`, `check-client-names.py`, and `check-ownership.py
      --scope umbrella` (both branches) all pass.
- [x] `changelog.d/` fragment (`umbrella-sticky-saved-host.decided.md`). No suite-level fact was
      made false — this is a scoped documentation decision — so no `status.d/` fragment.

## Not done here

Clearing `saved.host` on a non-`remote` `setup` conclusion is a real behaviour change on real
machines and needs the bench to confirm; `open.md` keeps it open as hardware debt.
