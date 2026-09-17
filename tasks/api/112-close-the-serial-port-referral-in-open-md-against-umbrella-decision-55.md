# 112 — Close the `serial_port` referral in `open.md` against umbrella decision 55

**State:** open — drained from `inbox/api-close-serial-port-referral.md` by leg 139, 2026-09-17, at
`umbrella/080`'s fold. Body unchanged apart from this line, the number, and the note below.

**Do not dispatch this concurrently with `tasks/api/109`.** `109` was in flight when this drop
arrived and its own `Done when` list includes *"`embarch-api/open.md` gains or loses a bullet to
match"* — two workers editing the same `open.md` in the same twenty minutes is a merge conflict at
best and a lost edit at worst. `109` lands first; then re-read `open.md` before starting this,
because `109` may have already rewritten the surrounding bullets. **Also check whether `109`'s own
answer changed what this bullet should say** — both are about what `init` does and does not
scaffold, and they may want to be one bullet rather than two.

**Owner:** no
**Source:** `embarch-umbrella decision 55` (`embarch-umbrella/decisions/projects.md`), landed by
`tasks/umbrella/080`, 2026-09-17.
**Scope:** api
**Hardware:** none

## What

`embarch-api/open.md`'s "Known wrong / unfinished" bullet — *"`embarch init` never writes
`serial_port` at all ... Not this crate's to fix"* — is answered. `embarch-umbrella` decision 55
settles it: `init` stays out of `serial_port` deliberately, for the same reason it refuses board
and chip as scaffolded fact (decisions 17, 41) — a serial port is *more* volatile than a board
(host-OS-assigned at enumeration, can renumber on a replug/power-cycle/reboot with no cable move),
so writing one at scaffold time would produce a stale value with no way for the config format to
say when it stopped being true.

Decision 55 also confirms the remedy `open.md`'s own referral pointed at is already correct and
already shipped: `list_serial_ports` (decision 70) discovers a port at call time, and `serial_log`
takes `port` as a per-call optional argument. No behavior change is implied on this crate's side —
the bullet is describing something already true and already documented in
`interfaces/tools-build-flash.md`. What's stale is only the framing: it currently reads as an open
gap owned by nobody, when it is a closed design decision with an owner and a citable number.

## Why now

A referral with no task behind it is the exact failure mode `tasks/umbrella/080` itself was filed
to close (see that task's `Filed by` note). Leaving `open.md`'s bullet as-is after the umbrella
side has answered it recreates the same "declines to fix, nobody hears" gap in miniature — the
answer exists now, but only umbrella's own decision corpus says so.

## Done when

- [ ] `embarch-api/open.md`'s `serial_port` bullet either removed (if nothing here still needs
      tracking) or rewritten to point at `embarch-umbrella decision 55` as the settled answer,
      dropping the "Not this crate's to fix" framing since it no longer reads as unresolved.
- [ ] Confirm no other `embarch-api` doc still frames `serial_port`'s absence from `init`'s schema
      as an open question rather than a cross-repo-settled one.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment if the wording change is reader-facing.
