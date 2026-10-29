# 124 — `install` refuses a registered service, and a reinstall drops its environment and restart policy

**State:** open
**Source:** `embarch-umbrella` [decision 22](../../embarch-umbrella/decisions/bind.md)'s 2026-10-29 measurement (`tasks/umbrella/033`, run by the owner's session against the live Core service)
**Scope:** core
**Hardware:** verify-only
**Owner:** no

## What

`embarch-core install` does what someone re-running it means on Windows, and a
reinstall does not silently lose service configuration. Three things measured
2026-10-29 on the live `com.embarch.core` service, all in `src/service.rs`:

1. **`install` over a registered service fails.** `install --bind 127.0.0.1`
   over a wide registration, and `install --bind 0.0.0.0` over a narrow one,
   each exited 1 with `[SC] CreateService FAILED 1073: The specified service
   already exists.` and changed nothing. Decide and record which: rewrite the
   registration in place (`sc config` on the binary path and arguments), or
   refuse with a message naming `embarch-core uninstall` first. `doctor` check
   17's fix lines (`tasks/umbrella/095`) wait on this choice.
2. **A reinstall drops the service's `Environment` registry value.** The live
   service carried `EMBARCH_SIGNAL_BAUD=460800`; after `uninstall` + `install`
   it carried none. `install` writes `Environment` only when `EMBARCH_TOKEN` is
   set, and then writes only the token. Anything set there by hand — the signal
   baud is the one in use — disappears without a word. Preserve it, or say so.
3. **The restart policy is never applied on Windows.** `install` passes
   `RestartPolicy::OnFailure`; `service_manager`'s `sc` backend warns
   "sc.exe does not support automatic restart policies through 'sc create'",
   and `sc qfailure` afterwards shows no actions (reset period 0). Apply it
   with `sc failure`, or drop the claim from the code.

## Why now

Measured by the owner 2026-10-29 while settling `umbrella/033`. The service was
restored by hand: wide bind, `EMBARCH_SIGNAL_BAUD=460800` re-set, restarted. It
has had no restart-on-failure since, and nobody can say whether it ever did.

## Done when

- [ ] Item 1 decided as a numbered decision and built, with a test.
- [ ] Item 2: a reinstall keeps the service's existing `Environment` entries,
      or `install` names what it dropped.
- [ ] Item 3: `sc qfailure` after `install` shows the restart actions, or the
      policy is removed from `install` and the decision says why.
- [ ] **Hardware debt:** the live check reinstalls the Core service, so it is
      owner-run. Leave a debt line in `embarch-core/open.md`.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); changelog fragment.
