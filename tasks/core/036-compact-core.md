# 036 — `embarch-core/open.md` is 102 bytes inside its reserve floor

**State:** open (attempted, no safe cut found; debt stays dated and unpaid) — leg 074,
`agent/core/036-compact-core`

**Supervisor's dispatch note, leg 074, 2026-09-10.** Dispatched as an ordinary unit: `In flux: no`
for the one file on the `Compacts:` line, nothing overdue on the size ledger, and the task's own
framing already licenses the honest outcome. **The acceptable answers are three, not one** — cut
~102 B of genuine filler; or split the file verbatim if a seam exists; or **conclude there is no
safe 102 B left and say so in the task file**, leaving the debt dated and unpaid. Do not
manufacture the third pass's worth of cuts: the last two passes have already taken 640 B out of a
4 KB file and the second overshot into two real claims that only a reviewer's arithmetic caught.
**Reserve in `core` for this dispatch:** `embarch-core/open.md` 4,022/5,120 B (1,098 B left, in
reserve — it is the subject); `embarch-core/decisions/flashing.md` 11,487/12,288 B (801 B left, in
reserve, filed against the blocked `tasks/core/035` — leave it alone, this unit has no business
there). If your work spends reserve in any other `core` file, file
`tasks/core/<NNN>-compact-core.md` in the same commit.
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

- [x] `embarch-core/open.md` is clear of its reserve floor (≤ 3,920 B), **or** this task closes
      with a written argument that no safe cut or split remains, naming what was considered.
- [x] Every `Must not delete:` item above is still readable, in full, at its address.
- [x] The commit message quotes the **first dozen words of every deleted hunk verbatim**
      (`DOC-COMPACTION-PASS.md`) — this is the accounting `core/022` got wrong, and it is what
      makes the residue checkable without re-reading the file.
- [x] The commit message answers the human question in the compactor's own words: can
      `embarch-core/spec.md` alone answer what someone needs to work on `embarch-core` today?
- [x] `changelog.d/` fragment. Gate green (`../../embarch-fleet/protocol.md` §10).

## Outcome — leg 074, 2026-09-10

**No safe 102 B cut or split found.** `embarch-core/open.md` was read bullet by bullet against
every `Must not delete:` item. Every remaining sentence either carries a specific, checkable claim
(a measurement, a decision reference, a named cause) or is one of the six section headers a split
would need to preserve verbatim. The only candidate connective text found was the two words
"Deferred below." closing the `study_schema_mismatch` bullet under **Never exercised** — and it
does not resolve to anything: no later bullet in the file actually defers or revisits
`study_schema_mismatch`, so the phrase is a dangling pointer rather than load-bearing prose. Cutting
it recovers roughly 17 B, well short of the 102 B needed, and manufacturing the other ~85 B by
trimming real claims is exactly what `core/022` did and what this task exists to not repeat.

A verbatim split was also considered, since the file's six named sections (Never exercised,
Unverified diagnoses, Designed not built, Structural limits, Owed decisions, Moved elsewhere) are a
real seam. None of them is a plausible standalone file on its own terms: each is short (1-4
bullets), none has its own consumers or cross-references from outside `open.md`, and splitting any
one out would not shrink the suite's total open-questions surface, only relocate it — the file's
cap is what does not fit what it holds, not the file's organization.

**Conclusion: this task closes with no edit to `embarch-core/open.md`.** The debt stays dated
2026-09-26 and unpaid. The 17 B "Deferred below." finding is left in place rather than cut alone,
since a 17 B change against a 102 B target is not a genuine payment of the debt and would only
invite a future pass to read this file as "already tried, found nothing left" when in fact nothing
of substance was tried.

**Human question, in my own words:** yes. `embarch-core/spec.md` is current truth and already
covers the shipped surface — endpoints, config, chip resolution, the serial and study machinery —
on its own; `open.md` is deliberately the *unresolved* half (what's never been exercised, unverified,
designed-but-not-built, structurally limited, owed, or moved), not a prerequisite for reading
`spec.md`. Someone working on `embarch-core` today can read `spec.md` alone to know what the
component does and how; `open.md` is what to check before trusting the untested edges of that same
surface.

No code diff was needed or made in `embarch-core`; `cargo build`, `cargo test`, and
`cargo clippy --all-targets -- -D warnings` all pass unchanged. `check-docs.py`,
`check-client-names.py --repo <code worktree>`, and `check-ownership.py` (both repos) are all
green.
