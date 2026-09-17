# 080 — `init` never writes `serial_port`, so every config reaches the serial tools without one

**State:** claimed — leg 139, 2026-09-17, branch `agent/umbrella/080-init-serial-port`
**Filed by:** leg 138's refill sweep, 2026-09-17. `embarch-api/open.md` has carried this as a
referral — *"Not this crate's to fix"* — with a named owner and no task behind it, which is how a
cross-repo gap sits still indefinitely: the repo that found it correctly declines to fix it, and the
repo that owns it never hears.
**Source:** `embarch-api/open.md`, the bullet *"`embarch init` never writes `serial_port` at all"*,
which points at `embarch-umbrella` decision 17 (`embarch-umbrella/decisions/projects.md`).
**Scope:** umbrella
**Hardware:** none — this is a schema-and-reasoning question about what `init` scaffolds. **Do not
attempt to discover a real port**, and do not run `init` against the owner's real configs.
**Owner:** no

## Dispatch note — leg 139, 2026-09-17

**Doc-size reserve for `umbrella`, measured at dispatch.** Three files are in reserve and all three
are filed against *blocked* compaction tasks, so nobody else is paying them:

- `embarch-umbrella/decisions/install.md` — **12,071/12,288 B, 217 B left** (`tasks/umbrella/079`,
  blocked). Effectively full. Nothing goes here.
- `embarch-umbrella/decisions/bind.md` — 11,533 B, 755 B left (`tasks/umbrella/009`, blocked).
- `embarch-umbrella/open.md` — 3,954 B, 1,166 B left (`tasks/umbrella/077`, blocked).

**The file you will almost certainly write is `decisions/projects.md`, and it is the trap here.**
Decision 17 lives there. It is **10,881/12,288 B — 88.6%, 1,407 B left — which is *just under* the
reserve line and therefore invisible to `check-doc-size.py` today.** An amendment to decision 17's
body of any real length will push it across. If it does, you file
`tasks/umbrella/<next free NNN>-compact-docs.md` **in the same commit** (`tasks/README.md` has the
shape), with a `**Size debt due:**` date and a per-file `In flux:` answer. That is your job because
you hold the one piece of context nobody else will — whether this subsystem is still moving. It is
**not** your job to do the compaction.

Run `python3 scripts/check-doc-size.py --pressure` yourself before you push and act on what it says
about `projects.md`; do not take my number as final, since your own edit is what moves it.

**`DOC-PROTOCOL.md` says edit decision 17's body, not append a note beside it.** If the reasoning
genuinely does not belong inside 17, a new numbered decision is correct — but check
`embarch-umbrella/decisions.md` for the next free number against `main`, and be aware two legs in a
row have had a task number collide because two actors picked "next free" against different views of
`main` within the same twenty minutes. The same hazard applies to decision numbers.

**"It stays out, deliberately" is the likely answer and it is a full unit.** The task is right that
this is not a licence to write it without argument: if you land there, the decision must say what a
caller with no configured port is expected to do, and it must engage with why a serial port is
*more* volatile than a board rather than less.

**Ownership is checked on both your branches.** `embarch-api/**` is not yours in any form,
including `embarch-api/open.md`. Drops go to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by
**absolute** path — a relative one lives only inside your worktree and is deleted with it.

## What

Decision 17 replaced `init`'s board-guessing with a **minimal discovery schema** for a Zephyr/west
repo — no build command, no chip, no artifact paths — deferring those to call time because `init`
had been silently picking a dev board's build over the production one. `serial_port` is not in that
schema either. The consequence `embarch-api` records is that **every config reaches
`list_serial_ports` and `serial_log` (`embarch-api/decisions/hardware-selection.md` 70) with no
port configured.**

**Settle it either way and write the reasoning down.** The two honest answers:

- **It belongs in the schema.** Then say what `init` writes and where it gets it, and confront the
  objection decision 17 was built on — a scaffolded value that names the last build rather than the
  board on the desk is exactly the "hardware fact nothing compares against the hardware" problem
  `embarch-api/open.md`'s first bullet already names for `board`. A serial port is *more* volatile
  than a board, not less: it is assigned by the host OS at enumeration and changes when a cable
  moves.
- **It stays out, deliberately.** Then decision 17's own body should say so by name, so the next
  reader does not re-derive the question — and `embarch-api/open.md`'s referral should be able to
  point at a sentence rather than at an absence.

**The second is the more likely answer and that is not a reason to write it without argument.** If
you land there, the decision has to say what the caller is expected to do instead, because
"resolved per call from the selected SoC" (decision 17's phrase for chip) is not obviously the same
story for a serial port.

**Not yours:** `embarch-api`'s side of this. If the conclusion implies a change to how
`list_serial_ports` or `serial_log` behave when no port is configured, that is an `inbox/` drop for
the `api` scope, written to the absolute path `/home/gabriel/Github/embarch/embarch-doc/inbox/`.

## Why now

The referral has been standing in `embarch-api/open.md` with no task behind it, and a bullet that
names another repo as the owner is the one kind of open question that cannot close by itself. It is
also cheap: reading decision 17 and one `embarch-api` decision, and writing a paragraph.

## Done when

- [ ] `embarch-umbrella`'s decision corpus records, by name, whether `init` writes `serial_port` and
      why — amending decision 17's body if that is the right home
      (`DOC-PROTOCOL.md`: edit the body, do not append a contradicting note beside the old text),
      or as a new numbered decision if the reasoning does not belong inside 17.
- [ ] If the answer is "it stays out", the decision says what a caller with no configured port is
      expected to do.
- [ ] `embarch-umbrella/open.md` carries nothing that contradicts the answer.
- [ ] Any `embarch-api`-side consequence is dropped to `inbox/`, not made here.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.
