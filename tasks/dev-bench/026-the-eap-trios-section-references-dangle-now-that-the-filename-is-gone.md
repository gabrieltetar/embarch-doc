# 026 — the EAP trio's `§` section references dangle now that the filename is gone

**State:** done — resolved by `dev-bench/029` before this task's worker started; see "Closed as
resolved elsewhere" below.
**Source:** leg 101, 2026-09-12, found while reading `dev-bench/019`'s merge diff. Verified against
`embarch-study-designer/spec.md` directly.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

## Dispatch note (supervisor, leg 107)

**`embarch-dev-bench` doc files already in reserve** — plan around them, do not discover them:
`open.md` 4782/5120 B (338 left), `spec.md` 9460/10240 B (780 left), `decisions/link.md`
11241/12288 B (1047 left). All three are filed against **blocked** compaction tasks
(`tasks/dev-bench/012`, `tasks/dev-bench/014`), which parks the *pass*, not the reserve: if your
work has to write into one of them, compact that file as part of this unit per
`DOC-COMPACTION.md` §2, carrying the parked task's `Must not delete:` list. If your work pushes
any **other** `embarch-dev-bench` doc file into reserve, file
`tasks/dev-bench/<next free NNN>-compact-dev-bench.md` in the same commit.

**`decisions/conventions.md` is new and it is the rule you are applying.** Leg 106 landed
`embarch-dev-bench` **decision 47** there yesterday, from `dev-bench/029`, and it is exactly about
this defect class: a bare section citation resolves to **a decision** where one owns the content, a
**live document** where the material moved there, or **nothing at all** where neither applies —
never a naked `§N`. Read it before you touch a line, and cite it in your commit message. Deleting
a dangling `§4.9` outright is a legal outcome under branch 3; inventing a plausible-looking
replacement is not.

**Do not guess `eap_interp.h:14`.** The task says so and it is the one line here that can be got
confidently wrong: `31/32` are `embarch-study-designer`'s **GATT** decisions, and `dev-bench/029`'s
worker already corrected a neighbouring citation from 31/32 to **59/60** (the wire-types/executor
split). Re-derive that line's claim against the decisions' actual text; if it resolves to nothing,
say so rather than repointing it.

## What

`dev-bench/019` correctly replaced `embarch-study-designer/design.md §3 decision N` with
`` `embarch-study-designer` decision N `` in eleven places. It was bounded to the filename, which was
right — but the **section numbers rode along and now point at nothing.** Six survive in the three
files it touched:

- `app/src/eap.h:1` — ``` `embarch-study-designer` decisions 58-62, §4.9. ```
- `app/src/eap.h:43` — `§4.9)` closing the `.eap` protocol-manifest banner
- `app/src/eap.h:84` — "Both worked protocols in **that doc's** §4.9 use **one**" — and "that doc"
  no longer names anything at all, the filename having been removed from the line above it
- `app/src/eap_interp.h:2` — `58-62, §4.9.`
- `app/src/eap_interp.h:14` — "The division is the one **§3** decisions 31/32 already set"
- `app/src/eap_interp.c:2` — `58-62, §4.9.`

**`embarch-study-designer/spec.md` has seven sections and no §4.9**, so each of these now reads as a
section of that repo's spec and resolves to nothing. Before `019` the section number was wrong-but-
attributed (it belonged to a deleted `design.md`); now it is wrong and unattributed, which is worse
for a reader because the line looks well-formed.

Note `eap_interp.h:14`'s "§3 decisions 31/32" is a **different** claim from the `§4.9` five: 31 and
32 are `embarch-study-designer`'s GATT decisions (`decisions/gatt.md`), not protocol ones, and that
line needs its own read before it is repointed — do not assume it is the same fix.

## Why now

This is the residue of a deliberately narrow unit, not a defect `019` introduced carelessly — its
bound was the point and it held. But a dangling `§` is exactly the shape this suite has already paid
for twice: nothing fails, a gate cannot see it (`check-decision-refs.py` reads `*.md` under a repo
root, and these are C comments), and a reader who goes looking concludes the citation is merely stale.

The same residue very likely exists in the six files `tasks/dev-bench/020`–`025` cover. **Do not
widen into them** — note in your report whether it does, so those tasks can be corrected to cover
both halves at once rather than repointing filenames twice.

**Confirmed for one of them, leg 105, 2026-09-13.** `dev-bench/021` repointed
`app/src/ble_bridge_real.c` and found **three** of its 39 citations were not decision references at
all: `design.md §4.3` and `design.md §4.3a`, section pointers with no decision number. They were
stripped to bare `§4.3` / `§4.3a` — the same treatment `019` gave `eap.h`'s `§4.9`, and the same
residue. So this task's class now has **nine** known instances, not six, and the three new ones are
in a file this task does not name. **Widen this task to cover `ble_bridge_real.c`'s two section
numbers as well**, or file the extra separately; it is recorded nowhere else. The reviewer confirmed
`embarch-study-designer/spec.md` has no numbered subsections at all (only `## 1.`–`## 7.`), so none
of these can be repointed at a successor section — deleting or re-attributing is the only honest
answer for every one of them.

## Done when

- [x] Each of the six references either names the real section of a real document, or is deleted.
      **Already true on `main` before this worker started.** `dev-bench/029` (leg 107, unit 4,
      commit `4816230`, landed 2026-09-13 12:49, *before* this task was claimed at `eb910cc`
      12:59) swept every bare `§N` this repo's C sources carried, including all six lines this
      task names, under the rule it wrote down as `embarch-dev-bench` decision 47
      (`decisions/conventions.md`). `eap.h:1`, `:43` and `eap_interp.c:2`, `eap_interp.h:1-2`
      dropped the redundant `§4.9` and kept the decision numbers (58-62), which already resolve.
- [x] `eap.h:84`'s "that doc's §4.9" no longer refers to an unnamed document. **Correction
      (`dev-bench/030`, 2026-09-13): the claim below that deletion was the right branch was wrong.**
      This worker checked only whether an `embarch-study-designer` decision states the
      one-arm-per-state rule; it does not follow that no decision does — `embarch-dev-bench`'s own
      decision 41 (`decisions/protocols.md`) states this exact claim, word for word, in the same
      repo as the comment. `dev-bench/030` repointed the line to `` `decision 41` `` (own-repo bare
      form) as a forward edit, per decision 47's first branch. The line now reads "`decision 41`
      records that both worked protocols use **one** arm per state".
- [x] `eap_interp.h:14`'s "§3 decisions 31/32" is read against `embarch-study-designer`'s actual
      decisions 31 and 32 and either repointed with the cross-repo form or corrected.
      `dev-bench/029` read it and found it a genuine miscitation — 31/32 are that repo's GATT
      decisions (`decisions/gatt.md`), unrelated to "wire types in the crate, executor here" — and
      corrected it by content to **decisions 59/60** (the primitive split / `RunProtocol` executor
      decision), which is what the sentence actually describes. This worker re-verified the fix by
      reading the live line rather than trusting the prior unit's say-so: `app/src/eap_interp.h:14`
      now reads `` `embarch-study-designer` decisions 59/60 already set: the wire types and the
      reference semantics live in the crate ``, and `embarch-study-designer/decisions/gatt.md`'s 31
      and 32 are indeed GATT-discovery decisions with no wire-type/executor content — 59/60 is the
      correct pair.
- [x] `grep -n '§' app/src/eap.h app/src/eap_interp.h app/src/eap_interp.c` — every surviving hit
      resolves to a section that exists. Re-run by this worker: **zero hits** in all three files.
      Nothing survives to check.
- [x] Host-side checks green. This worker made zero code changes (nothing left to fix), so no
      firmware behaviour is at risk. `west`/`ZEPHYR_BASE` remain unavailable in this worktree
      (standing debt, unrelated to this task). `scripts/check-docs.py` run from the doc worktree:
      green.

## Closed as resolved elsewhere

This task's worker (leg dispatch, 2026-09-13) found the code worktree already at commit `4816230`
— `dev-bench/029` had, in the same leg, already applied decision 47 retroactively to every bare
`§N` this repo's C sources carried, and its own commit message and "What was done" section name
`eap.h`, `eap_interp.h` and `eap_interp.c` explicitly, including the exact `eap_interp.h:14`
re-derivation to decisions 59/60 that this task's dispatch note warned not to guess. `git log`
shows `4816230` (029's landing) predates `eb910cc` (this task's own claim commit) by ten minutes,
so 029 closed this task's scope before this worker ever opened a file. No further code change was
needed or made; `grep -n '§'` across `app/src/eap.h`, `app/src/eap_interp.h` and
`app/src/eap_interp.c` returns nothing.

**The "widen to `ble_bridge_real.c`" note above is also moot.** `dev-bench/029`'s own scope
included `ble_bridge_real.c` (it lists 8 hits there, one deliberately left: `§1.3`, the real
Bluetooth Core Specification, per decision 47's exception). Verified directly: `grep -n '§4\.3'
app/src/ble_bridge_real.c` returns nothing; the only surviving `§` in that file is line 380's
`§1.3`, the external-standard citation this repo's own decision 47 says to leave alone. No separate
task is needed for it.

**Doc-size note:** `embarch-dev-bench/open.md` (93.4%) and `spec.md` (92.4%) are in reserve against
blocked `tasks/dev-bench/012`, and `decisions/link.md` (91.5%) against blocked `014`. Untouched by
this unit — no code or doc change was needed.
