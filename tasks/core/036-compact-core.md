# 036 — `embarch-core/open.md` is 102 bytes inside its reserve floor

**State:** open
**Source:** `core/022`'s fold, leg 073, 2026-09-10 — the 111 B the supervisor restored on the
reviewer's finding (`inbox/core-open-md-compaction-residue.md`) put the file back inside reserve
after `core/022`'s squeeze had cleared it. Filed as a fresh debt rather than reopening `core/022`,
so the ledger points at an `open` task instead of a `done` one holding an unpaid balance —
`DOC-COMPACTION.md` §2.
**Scope:** core
**Hardware:** none
**Owner:** no

**Compacts:** embarch-core/open.md
**Size debt due:** 2026-09-26
**In flux:** no. Inherited from `core/022`, which answered this for this exact file and gave the
reason: `core/009` acted as the flux-maker and what is left is a squeeze on a small file.
`interfaces.md` — the file the old `In flux: yes` block in `tasks/core/022-compact-core.md` is
about — is not on this task's `Compacts:` line and is already paid.
**Must not delete:** the two claims restored at `core/022`'s fold, because deleting either is the
defect this task exists downstream of. (1) The `Alert` subject-discriminator bullet's
*"Not-needed-**yet**, with a named trigger"* and *"physically possible"* — the hedge is the whole
content of the bullet, and a flat "Not needed" turns an open, trigger-gated deferral into a closed
judgement inside a file whose purpose is open questions. (2) The Espressif port-selection bullet's
*"the missing replacement knob outlives that confirmation"* — decision 23 removed four env
overrides with no stated replacement, and without this sentence the bullet reads as though
confirming the ESP32-C5's enumeration would close the gap. Also inherited unchanged from
`core/022`: the `GET /serial-log` caller-side-ceiling measurement, the
`404`/`502`-vs-`503` vocabulary paragraph, and `GET /study/{id}`'s `current_step`
"consequence, not an invariant" sentence — see `tasks/core/022-compact-core.md`.

## What

`embarch-core/open.md` is **4,022 B against a 5,120 B cap, 1,098 B left against a 1,200 B floor**
— 102 B inside reserve. It needs roughly 102 B cut, and no more than that: this file has been
squeezed twice already (`core/009`, then `core/022`) and the second pass overshot into real
content.

## Why this one is harder than the last two

**The easy seams are gone, and the last pass proved what happens when you keep cutting anyway.**
`core/022` cut 640 B, of which 111 B was not connective prose but two claims — and its commit
message's verbatim residue list did not name them, which is the only reason a reviewer could catch
it by arithmetic rather than by re-reading the whole file. Whoever takes this should expect to find
102 B of genuine filler or **to conclude there is none and say so**, which is a real and acceptable
outcome: `DOC-COMPACTION.md` §2 prefers a split, and if neither a split nor a safe squeeze exists,
the finding is that this file's cap is wrong for what it holds, not that the file is too long.

A split is worth considering seriously here and has not been tried. The file already carries six
named sections — Never exercised, Unverified diagnoses, Designed not built, Structural limits,
Owed decisions, Moved elsewhere — and a verbatim move states nothing new.

## Done when

- [ ] `embarch-core/open.md` is clear of its reserve floor (≤ 3,920 B), **or** this task closes
      with a written argument that no safe cut or split remains, naming what was considered.
- [ ] Every `Must not delete:` item above is still readable, in full, at its address.
- [ ] The commit message quotes the **first dozen words of every deleted hunk verbatim**
      (`DOC-COMPACTION-PASS.md`) — this is the accounting `core/022` got wrong, and it is what
      makes the residue checkable without re-reading the file.
- [ ] The commit message answers the human question in the compactor's own words: can
      `embarch-core/spec.md` alone answer what someone needs to work on `embarch-core` today?
- [ ] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).
