# 010 — Check 1 fails on a correctly set-up wsl-host machine, and takes check 14 with it

**State:** done, 2026-09-05 — `agent/umbrella/010-doctor-check-1-fails-on-a-healthy-wsl-host`
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

- [x] `doctor` on `wsl-host`, with Core running as the Windows service and no
      Linux `embarch-core` anywhere, does not FAIL check 1. Two layers:
      `locate_core` now reads the service's own `BINARY_PATH_NAME` (so there
      usually *is* a Core), and if that finds nothing, check 1 is a **Warn**
      with code `core-not-local` on `wsl-host` and `remote` — never a Fail
      where no local Core belongs.
- [x] Check 14 either runs on that topology or says why it cannot, in terms that
      are not "see check 1". It runs, given a located binary; its skip arm now
      names what is missing per class (`sc.exe qc`, a conventional location and
      `EMBARCH_CORE_EXE` on `wsl-host`) and carries code `core-not-located`.
- [x] A decision entry says which of the two readings won and why, and
      `spec.md`'s doctor table row for check 1 matches it —
      [decision 38](../../embarch-umbrella/decisions/topology.md), with
      [decision 31](../../embarch-umbrella/decisions/doctor.md) amended for
      check 14's half.
- [x] Gate green, `changelog.d/umbrella-*` fragment dropped.

## What was decided

**Reading (a) won — check 1 becomes topology-aware and actually finds the
Windows Core — with reading (b) kept as its fallback rather than as the
alternative to it.** (b) alone clears the red and leaves check 14 permanently
unanswerable on the suite's primary topology, since decision 31 has it shell out
to Core's own binary precisely because nothing else can answer about the right
machine. Both are built: located, or an explicit not-applicable Warn, never a
Fail where no local Core belongs. Full reasoning, and why the suite manifest is
*not* an instrument that can speak about a Windows Core from a Linux archive, is
decision 38.

Consistent with `umbrella/006`: the new behaviour is gated on the topology class
(decision 31's rule), and every arm of checks 1 and 14 carries a `code` per
decision 37.

## Hardware-verification debt

**None — but one verification debt, and it is free.** Everything asserted here
about the live `wsl-host` install rests on `sc.exe qc com.embarch.core` naming a
file `doctor` can then run, which no test on this branch can establish: the
shell-out is real, only its *parse* is unit-tested (against a verbatim capture
from this bench, `locate.rs`).

**The run that settles it is the live `embarch doctor` the owner already owes
for checks 11, 15 and 16**, so it costs nothing extra. What it should print:

- `[ 1] PASS binaries found — embarch-core: /mnt/c/Users/tmp12/embarch-setup/embarch-0.1.0-x86_64-pc-windows-msvc/embarch-core.exe (…)`, with the note that the manifest is the Linux one and check 15 owns Core's version.
- `[14]` a real `PASS`/`FAIL` naming per-family backends — **not** a `WARN` mentioning `sc.exe qc`. A `WARN` there means the registration read failed on the real service and the fallback is what is being exercised.
- If check 1 is instead `WARN … core-not-local`, layer (a) missed and layer (b)
  caught it: that is the honest degraded state, not a regression, and the next
  question is what `sc.exe qc com.embarch.core` prints by hand.
