# 013 — Decision 23's "unprivileged CLI" rationale may contradict the directory's own documented ACL

**State:** claimed — leg 035, 2026-09-07, branch `agent/topology/013-decision-23-acl-rationale`.
**Scope:** topology
**Hardware:** none
**Source:** `embarch-reviewer` on `topology/012`, leg 034, 2026-09-07 — raised explicitly as *not* a
finding against that unit, because the unit's diff neither introduces nor contradicts it. Filed by
the supervisor so it does not evaporate with the review.

**Doc-size reserve in `embarch-topology` (leg 035, measured at dispatch): none.** No
`embarch-topology` file is in reserve — `spec.md` is 8,993 / 10,240 B (87.8%), `open.md` 4,206 /
5,120 B (82.1%), `decisions.md` 1,320 B. `spec.md` was at its **hard cap** two legs ago and
`topology/010` took it off, so treat its 1,247 B of headroom as hard-won rather than spare: put a new
or amended decision in `decisions.md`, which is nearly empty, and keep `spec.md` edits to the
sentence that is actually wrong. **If your work pushes any file into reserve, or leaves one there
that nothing has filed, file `tasks/topology/<NNN>-compact-topology.md` in the same commit**
(`tasks/README.md` has the shape; the path is `tasks/topology/`, never `tasks/doc/`).

## What

`embarch-topology` **decision 23** (landed by `topology/012`, doc `8b01ced`) records that the
enrollment store shares a machine-wide root with `embarch-core`'s token file, and gives as its
**stated rationale** that the location is one where an admin-owned Windows service and an
**unprivileged CLI** both see the same file.

`embarch-token.md` describes the Windows ACL on `%ProgramData%\embarch` as explicitly restricted to
**the creating account, SYSTEM and Administrators.**

If that ACL description is accurate, then an unprivileged CLI run by a *different* account than the
one that created the directory cannot read it — and decision 23's rationale is wrong in exactly the
case it was written to cover. The convention itself would still be right (both crates agreeing on
one location is the point); it is the *reason given* that would be false, which is the more
dangerous defect, because a later change will be argued against the stated reason.

## Why this is worth a task rather than a note

**A fact with no home attracts wrong citations** — that is `topology/012`'s own lesson, and it took
three actors to learn it there. This is the same shape one level up: a decision whose *rationale* is
unverified will be cited as though it were measured. Decision 23 is brand new and currently the only
record of the convention, so if its rationale is wrong it is wrong in the single place anyone will
look.

## What to do

Settle which of the two documents is right, on evidence:

- Read what actually creates `%ProgramData%\embarch` and with what ACL — `embarch-core`'s installer
  or service startup, whichever creates it. Do not infer the ACL from the doc that describes it;
  that doc is one of the two things in tension.
- Determine whether an unprivileged CLI in the real deployment is the *same* account that created
  the directory. On this machine Core runs as a Windows service and the CLI runs as the user, which
  is the case that matters and the case decision 23 names.
- Then either correct decision 23's rationale to the true one, or correct `embarch-token.md`'s ACL
  description — **and say which was wrong**, because one of them has been wrong in a doc for some
  time and the reason it went unnoticed is worth a sentence.

**If the ACL half turns out to be `embarch-core`'s to fix, that is `embarch-core`'s task, not
yours** — file it in `/home/gabriel/Github/embarch/embarch-doc/inbox/` and do not reach across.

## Note on verifying this without a Windows box

The Windows ACL cannot be observed from WSL. If settling this needs a real `icacls` reading on the
Windows side, that is a **hardware/owner step**: say so, record what you did establish from source,
and leave this `open` rather than concluding from the source alone. Decision 23's rationale is a
claim about a deployed system, and this suite has already paid for an inferred fact asserted as
measured.

## Done when

- [ ] Which of decision 23's rationale and `embarch-token.md`'s ACL description is wrong is
      established, on evidence, and the wrong one is corrected.
- [ ] If it cannot be settled without a Windows-side observation, that is recorded as the answer and
      this task stays `open` naming exactly what reading is needed.
- [ ] Gate green.
