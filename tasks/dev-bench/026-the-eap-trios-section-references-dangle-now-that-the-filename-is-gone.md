# 026 — the EAP trio's `§` section references dangle now that the filename is gone

**State:** open
**Source:** leg 101, 2026-09-12, found while reading `dev-bench/019`'s merge diff. Verified against
`embarch-study-designer/spec.md` directly.
**Scope:** dev-bench
**Hardware:** none
**Owner:** no

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

- [ ] Each of the six references either names the real section of a real document, or is deleted.
      Deleting is a legitimate answer: `` `embarch-study-designer` decision 61 `` is a complete
      citation on its own, and a section number that adds nothing is not worth researching.
- [ ] `eap.h:84`'s "that doc's §4.9" no longer refers to an unnamed document.
- [ ] `eap_interp.h:14`'s "§3 decisions 31/32" is read against `embarch-study-designer`'s actual
      decisions 31 and 32 and either repointed with the cross-repo form or corrected — say in your
      report which, and why.
- [ ] `grep -n '§' app/src/eap.h app/src/eap_interp.h app/src/eap_interp.c` — every surviving hit
      resolves to a section that exists.
- [ ] Host-side checks green. The Zephyr `tests/unit` ztest suite cannot be built from a worktree
      (no `west`, no `ZEPHYR_BASE`); that is a standing debt, not this unit's. Comment-only changes
      cannot alter firmware behaviour — say plainly what you could and could not run.

**Doc-size note:** `embarch-dev-bench/open.md` (93.4%) and `spec.md` (92.4%) are in reserve against
blocked `tasks/dev-bench/012`, and `decisions/link.md` (91.5%) against blocked `014`. Stay out of all
three; a comment repoint should need none of them.
