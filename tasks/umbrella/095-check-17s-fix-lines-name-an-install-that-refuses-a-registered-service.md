# 095 — Check 17's fix lines name an `install` that refuses a registered service

**State:** open
**Source:** [decision 22](../../embarch-umbrella/decisions/bind.md)'s 2026-10-29 measurement (`tasks/umbrella/033`, run by the owner's session against the live Core service)
**Scope:** umbrella
**Hardware:** verify-only
**Owner:** no

## What

Check 17 prints what a real narrow-bound Core actually needs, and says only what
it observed. The 2026-10-29 run found three defects, all in `src/doctor.rs`'s
`judge_bind_address`:

1. **Both fix lines name a command that fails.** `bound-narrow` and
   `bind-too-narrow` both say `embarch-core install --bind 0.0.0.0`. Run over a
   registered service, in either direction, that exits 1 with `[SC]
   CreateService FAILED 1073: The specified service already exists.` and
   changes nothing. What widened the service was `embarch-core uninstall` then
   `embarch-core install --bind 0.0.0.0`, elevated. **Sequenced after
   `tasks/core/124`:** if that makes `install` rewrite a registration, the fix
   line stays and names the Core version that does it; if not, it names the
   two commands. `bound-narrow`'s `embarch setup` alternative is **unmeasured**
   against an existing registration — read `setup`'s install path; if it calls
   `embarch-core install`, it meets 1073 too and the offer goes or is fixed.
2. **`bound-narrow`'s detail is false when the service is stopped.** It says
   "The bind is why, not a stopped service" — observed with the service
   `Stopped` and registered `--bind 127.0.0.1`. The registration read can say
   whether the service is running; when it is not, say both.
3. **`bind-too-narrow` cannot fire from a NAT-networked WSL2 guest**, the
   topology check 17 exists for: the guest's `127.0.0.1` is its own, so a
   running narrow Core (Windows loopback answered 401, the gateway refused)
   reads as nothing answering and Fails `bound-narrow`. Decision 22 records
   this; the arm's doc comment does not. It is reachable from a
   mirrored-networking guest, never measured; keep the arm unless a reason to
   delete it is found.

## Why now

Measured by the owner 2026-10-29. A `doctor` fix line is what someone types
while something is broken, and this one fails at the moment it is needed.

## Done when

- [ ] Fix lines name a command that works on a registered service (per
      `core/124`'s outcome), with a unit test per arm.
- [ ] `bound-narrow` says "stopped and bound narrow" when the registration
      reads stopped; unit test.
- [ ] `bind-too-narrow`'s NAT unreachability recorded in its doc comment.
      Decision 22 is 11,022 B against a 11,059 B reserve line: an amendment
      for the fix-line change must cut what it adds, or file a debt.
- [ ] **Hardware debt:** the live re-check reinstalls the Core service, so it is
      owner-run, as `033` was. Leave a debt line in `embarch-umbrella/open.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); changelog fragment.
