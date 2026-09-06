# 020 — check 17's remaining two holes, and decision 37's example list is stale

**State:** open
**Source:** `umbrella/018`'s reviewer, 2026-09-06, reviewing merge `5f978e7` / `c793301`.
All three reported as observations rather than contradictions — the reviewer returned **no
findings** — and filed here by the supervisor, who merged `018` knowing about them. Each was
verified against the shipped source rather than inferred; the line numbers below are the
reviewer's own reads.
**Scope:** umbrella
**Hardware:** item 1 is code-only. Item 3 names a **hardware-owed** assumption and is a
question to record, not to answer without a board.
**Owner:** no

## 1. `bound-narrow`'s `setup` fix line has the same hole `018` just closed in `bind-too-narrow`

`umbrella/018` removed `embarch setup` from `bind-too-narrow`'s fix because on that path
`setup` prints "already running", installs nothing, and rewrites the recorded topology class —
greening the check with the bind untouched. **`bound-narrow` kept its `setup` half, and it is
correct on the path the reviewer checked** (nothing answers, so `setup` really does install
`--bind 0.0.0.0`). But there is a narrower path where it is not:

If `doctor` runs **natively on the Windows side of a `wsl-host` machine**,
`windows_exe_from_wsl2` is false, so `infer_class` (`setup.rs:105`) returns `Local`, `setup`
installs `--bind 127.0.0.1`, and `setup.rs:334` writes `topology: "local"` into state — after
which check 17 **Passes `bind-matches` with the bind still narrow.** Same shape, one path over.

**This is not a contradiction of an earlier decision** — the claim was made in `018`'s own
diff, not left standing from before — which is precisely why it is filed rather than reverted.
The fix is likely one clause on the `bound-narrow` fix line, or a class guard, and it should be
argued for the same way `018` argued its three shapes.

## 2. `bind_registration_can_change_the_verdict` is blind to the `remote` class

`recommended_bind_address(Remote)` is `"0.0.0.0"` (`embarch-topology/src/software.rs:332`), so
on a machine whose recorded class is `remote`, a *local* Core answering at loopback now causes
**this** machine's `sc.exe qc` to be read and the **remote** Core's bind to be judged by it.
That is decision 31's "confident verdict about the wrong machine", which decision 38 says
governs generally.

**Pre-existing, and verified as such rather than assumed**: the hunk `018` replaced read
`if core_probe.winner_base_url.is_none()` with no class guard, so `bound-narrow` already
carried it. `018` extends the exposure to one more state; reverting `5f978e7` would not remove
it. The new predicate's doc comment and its five test cases cover `WslHost`, `Local` and `None`
only — **so the gap is visible in the tests as an absence, which is the good case.**

`embarch-topology` is another sub-project: read it, do not write it. If the right fix is in
that crate's contract, say so and stop.

## 3. Nothing has confirmed that `embarch-core install --bind 0.0.0.0` rewrites an existing narrow registration

**This is the load-bearing assumption under *both* Fail arms' fix lines**, and no arm of check
17 has ever met a real narrow-bound Core. If `install` fails on an already-registered service
rather than rewriting it, then both fix lines tell an operator to run a command that errors,
and the check's whole remedy is wrong while its diagnosis is right.

The reviewer could not settle it — it needs the Windows side. **Record it in `open.md` beside
check 17's existing verification debt** rather than answering it; `umbrella/018` already wrote
the experiment that must be run (a Core installed `--bind 127.0.0.1` on a `wsl-host` machine,
stopped for `bound-narrow`, running for `bind-too-narrow`, plus the wide-registration control),
and this is one more step in it.

## 4. Decision 37's example list is stale, one clause

`embarch-umbrella/decisions/reporting.md:19` still reads "check 10's `no-cli` is the case so
far (decision 40, in `decisions/mcp.md`)". **After `018` there are two deliberate reuses**, the second being
`bind-too-narrow` keeping its spelling for a strictly narrower state. The rule 37 states was
honoured by `018`; only its example is out of date. Cheap, and it is the entry that exists to
catch exactly this class of silent drift, so an example that undercounts it reads badly.

## 5. `features.d/umbrella-061`'s `Verified` column may now understate check 1

Added by leg 015 while running `suite/005`. That row asserted the `sc.exe qc` read "has never
run inside `doctor` on the live machine" — **false since 2026-09-05**: decision 38's closing
paragraph records check 1 locating the live service's binary by `BINARY_PATH_NAME` on the first
run after the `deploy-core` that had never landed, in the same measurement that made check 14
answer. The supervisor corrected the Status text in that pass.

**What it did not touch is the `Verified` column, which still reads `unit`** — deliberately,
because `suite/005`'s announced guardrails forbade changing a `Verified` value and because that
column is the owning scope's claim to make, not the supervisor's. `umbrella-090` next to it
reads `hw` on the strength of the same run. **Decide what check 1's row should say and set it**,
or record why `unit` is right despite decision 38's measurement.

## Reserve

`embarch-umbrella/decisions/doctor.md` is **in reserve at 11,519 / 12,288 B (93.7%)**, filed
against `tasks/umbrella/009-compact-docs.md` (`blocked`, `In flux: yes`). You will be editing
it. Under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 **the ride-along is yours**: bring it
below 90% in your own commit, carrying `009`'s `Must not delete:` list, and tick only that
file's item. `018` already trimmed ~900 B out of decisions 18/19/22(b)/22(c) to make room and
said it could go no further without deleting live reasoning — **so the honest move here is
likely a mission split rather than a squeeze**, the way `umbrella/012` and `umbrella/015` split
`doctor.md` before. `009` records eighteen rows / one unbuilt decision for `spec.md`'s doctor
table; refresh that if you change it.

## Done when

- [ ] Item 1 is fixed or argued closed, with the losing option argued against.
- [ ] Item 2 is either guarded or recorded as a deliberate exposure citing decisions 31/38;
      if the fix belongs in `embarch-topology`, say so and stop.
- [ ] Item 3 is in `embarch-umbrella/open.md` as a named step of check 17's verification debt.
- [ ] `decisions/reporting.md`'s decision-37 example counts both reuses.
- [ ] `decisions/doctor.md` is out of reserve and `tasks/umbrella/009` is updated.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/umbrella-*` fragment
      dropped.
