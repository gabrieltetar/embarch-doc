# 010 — Check 1 fails on a correctly set-up wsl-host machine, and takes check 14 with it

**State:** claimed by agent/umbrella/010-doctor-check-1-fails-on-a-healthy-wsl-host, 2026-09-05 18:10
**Source:** the owner's live `embarch doctor` run, 2026-09-05 — the first one ever made against the real installed suite
**Scope:** umbrella
**Hardware:** none

## What

On the owner's machine — `wsl-host`, Core running as the Windows service, `embarch
setup` just run and clean — `doctor` opens with:

```
[ 1] FAIL binaries found — embarch-core: not found; embarch-api: /home/gabriel/.local/share/embarch/bin/embarch-api
       fix: download the suite archive and unpack both binaries next to `embarch`, or set EMBARCH_CORE_EXE / EMBARCH_API_BIN
```

**Nothing is wrong with the machine.** On `wsl-host` the Core that matters is a
Windows `.exe` registered as a service; there is no Linux `embarch-core` to sit
beside `embarch`, and **`setup` itself says so in the same session**:

```
  embarch-core  not next to this binary, skipped
  embarch-core is already running — nothing to install.
```

So `setup` treats a missing local Core as correct on this topology and `doctor`
treats it as a hard failure. One of the two is wrong and they are the same
sub-project.

**It cascades.** Check 14 reports `WARN — skipped, embarch-core not located (see
check 1)`, so the flashing-backend check cannot run on the suite's primary
topology at all. Check 15 is separately degraded (the running Core serves no
`core_version`), which means **three of sixteen checks are dark on the one
machine the suite is actually used on.**

The fix is a judgement, not a patch: either check 1 becomes topology-aware — on
`WslHost`, locate the Windows Core through the service's own `BINARY_PATH_NAME`,
which `deploy-core` already reads — or the check keeps its shape and the
`embarch-core` half becomes an explicit not-applicable on this class. **The
first is better if check 14 is to work**, since it needs a real binary to ask.

## Why now

This is the *first* line of the first live `doctor` run, and it is a red on a
healthy install. A tool whose opening line is a false failure teaches its user
to skim the rest — which is the whole value of the other fifteen checks.

## Done when

- [ ] `doctor` on `wsl-host`, with Core running as the Windows service and no
      Linux `embarch-core` anywhere, does not FAIL check 1.
- [ ] Check 14 either runs on that topology or says why it cannot, in terms that
      are not "see check 1".
- [ ] A decision entry says which of the two readings won and why, and
      `spec.md`'s doctor table row for check 1 matches it.
- [ ] Gate green, `changelog.d/umbrella-*` fragment dropped.
