# 030 — `suite/user-guide.md` is 556 bytes from its cap, and the thing that filled it is the part that has to keep growing

**State:** open — announced 2026-09-11 by leg 091, `ts` `1789187481.992469`, 30-minute window per
`embarch-fleet/ops.md` §4. If this leg ends before the window closes, **read the thread and complete
the window rather than restarting it.**
**Source:** `tasks/suite/022`'s own fold, leg 085, 2026-09-11. Split out of `tasks/suite/004`,
which carried this file alongside two others on one `Compacts:` line and one shared date;
`user-guide.md` is now urgent and the other two are not, so it gets its own clock.
`DOC-COMPACTION.md` §2 — the commit that spends the reserve is the one that files the debt, and
this is that filing.
**Scope:** suite
**Hardware:** none
**Owner:** no

**Compacts:** suite/user-guide.md
**Size debt due:** 2026-09-18
**In flux:** no. §6 and §7.1 were just corrected against the code and are now true; §5.1's
placeholder argument has been stable since it was written. Nothing about this file is mid-change —
it is simply full.
**Must not delete:** inherited verbatim from `tasks/suite/004`, whose `user-guide.md` item this
replaces — **§5.1's argument for why `chip` and the board are placeholders**: *a wrong guess
flashes the wrong target instead of erroring*, and *`build_info.yml` records the last build, not
the board on your desk*. Both are the reason the placeholder is not an annoyance, and **both read
as boilerplate once shortened to "fill these in"**, which is exactly how they would be lost.
Additionally, from this task's own source: **§7.1's two lists must stay exhaustive over the tool
surface** — the defect `suite/022` fixed was a split that named 7 of 23 tools and omitted every
destructive one, and a compaction that trims the lists back to examples re-creates it.

## What

`suite/022` landed two correctness fixes in this file and grew it **23,796 → 25,044 B against a
25,600 B cap**. That is **97.8% of cap, 556 B of headroom, and 2,004 B inside the 23,040 B reserve
floor.** One more paragraph puts it over.

`suite/022`'s own "Done when" asked for the file to end no larger than it started, on the filer's
expectation that both fixes would shrink it. **That was wrong, and the reason is worth keeping.**
The §6 fix roughly broke even. The §7.1 fix could not: making the permission split **exhaustive**
over 29 tools cannot be done in fewer bytes than the 7-tool version it replaced — 29 tool names
are 29 tool names. The checkbox was left unmet with this task filed in its place.

## Why a squeeze is the wrong first move here

Two things point the same way.

**The tool lists are the part of this file that must keep growing.** They grow by one line every
time `embarch-api` gains a tool, which is the mechanism that made §7.1 wrong in the first place —
it named 7 of what was then 23. A file already at 97.8% of cap cannot absorb that, so shaving
prose elsewhere buys one or two more tools and then the same task is filed again.

**Every squeeze this suite has run on a full file has cost it a fact.** `api/026` and `api/031`
each cut a file to within single digits of its floor and each deleted a claim recorded nowhere
else; both were restored by a reviewer, by hand. `tasks/api/060` and `tasks/core/036` reached the
same conclusion independently and said so rather than cutting further.

## The candidate direction, and the one thing that blocks it

**Split §7 (and §7.1) into its own `suite/agent-guide.md`.** It is genuinely a different document
for a different reader — the human-facing walkthrough §1–§6 ends where "how an agent should be
allowed to drive this" begins — and it is the exact content `embarch-promptu` exists to make
installable (`embarch-promptu/design.md` §2 items 1 and 2 both point at §7.1 and, as of `suite/022`,
no longer restate it). A split would leave `user-guide.md` around **21.8 KB, clear of its reserve
floor**, and give the permission lists a file with room to grow.

**What blocks it is not the writing.** A new `suite/*.md` needs a cap entry in `DOC-BUDGET.md`,
which is owner-reserved — no worker and no supervisor may add one. So either the owner adds the
entry and this becomes an ordinary verbatim split, or this task falls back to a squeeze against the
`Must not delete:` list above. **Recorded as a fork for the owner rather than guessed at.**

## Two smaller things a pass here should also do

- **Check whether `embarch.md` §6 or `suite/studies-guide.md` cite `user-guide.md` §7 by section
  number.** If §7 moves to another file, those citations break the way six decision citations broke
  in this same leg (`tasks/doc/044`) — silently, with the gate green.
- **`suite/studies-guide.md` is 23,396 B and also inside reserve**, still on `tasks/suite/004`'s
  line. If the split argument above is accepted for this file, ask whether the same seam exists
  there before running two unrelated passes.

## Done when

- [ ] `suite/user-guide.md` is clear of its 23,040 B reserve floor, **or** this task closes with a
      written argument that no safe cut or split remains and says which of the two forks above was
      taken and why.
- [ ] Every `Must not delete:` item above is still readable in full — in particular §7.1's lists
      are still exhaustive over `embarch-api`'s tool surface.
- [ ] The commit message quotes the **first dozen words of every deleted hunk verbatim**
      (`DOC-COMPACTION-PASS.md`) and answers its human question in the compactor's own words.
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
