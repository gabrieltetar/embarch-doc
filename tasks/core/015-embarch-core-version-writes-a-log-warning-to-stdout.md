# 015 — `embarch-core --version` writes a multi-line log warning to **stdout**, so its output is unparseable

**State:** claimed (leg 045)
**Source:** supervisor bench unit `umbrella/027`, 2026-09-06 — live `embarch doctor --json` against
the installed Windows service exe
**Scope:** core
**Hardware:** none
**Owner:** no

## What was observed

`embarch-umbrella`'s check 1 runs `<binary> --version` and reads **`output.stdout` only**
(`embarch-umbrella/src/doctor.rs:161-167` — `String::from_utf8(output.stdout)`, trimmed; `stderr` is
never touched). The string it got back from
`/mnt/c/Users/tmp12/embarch-setup/embarch-0.1.0-x86_64-pc-windows-msvc/embarch-core.exe` was:

```
<ESC>[2m2026-09-07T00:24:33.426655Z<ESC>[0m <ESC>[33m WARN<ESC>[0m <ESC>[2membarch_core<ESC>[0m<ESC>[2m:<ESC>[0m failed to set up daily-rolling log file, continuing with stderr only: failed to initialize rolling log file appender in C:\ProgramData\embarch\logs

Caused by:
    0: failed to create log file: Access is denied. (os error 5)
    1: Access is denied. (os error 5)
embarch-core 0.1.4
```

The version — `embarch-core 0.1.4` — is the **last line**, after a blank line, an ANSI-coloured
tracing record and a two-level `Caused by:` chain. Reproduced on all three invocations.

Two things are wrong and they are independent:

**1. `--version` initialises logging at all, and prints diagnostics on stdout.** A `--version`
invocation does not open a log file for any reason a caller cares about, and whatever it prints
belongs on stderr if it prints at all. Anything parsing `--version` — check 1 today, a packaging
script tomorrow — gets a blob whose useful line is last and whose first line looks like an error.
Note the warning says it is "continuing with **stderr** only", which is where it evidently is not.

**2. The warning itself is real and is about the deployed service's own log directory.** A
non-elevated caller cannot create files in `C:\ProgramData\embarch\logs` (`os error 5`). The
service, running elevated, can — `dev-bench.log.2026-09-07` was written there the same minute. So
the *warning* is correct for the invocation that produced it and says nothing about the service's
health. Worth confirming that reading before changing anything: if the elevated service ever hits
this, it loses its log silently.

## Why it is filed here rather than fixed in umbrella

`embarch-umbrella` has its own defect on the receiving side — it interpolates this text into a
`detail` that is contracted to be one line (`tasks/umbrella/031`). **Both need fixing.** Normalising
in umbrella alone leaves `--version` unparseable for every other caller; fixing `--version` alone
leaves umbrella one foreign string away from the same break.

## Supervisor direction (leg 045)

**I located what I believe is the whole defect before dispatching, and you are to
verify it rather than inherit it.** `src/main.rs`'s `init_tracing()` has two arms.
The success arm writes to `std::io::stderr.and(file_writer)` — explicitly stderr.
The failure arm calls bare `tracing_subscriber::fmt::init()`, and **that default
writer is stdout, not stderr.** So the message that says "continuing with stderr
only" is emitted to stdout, which is exactly why check 1's `output.stdout` read
picked it up. Confirm this against `tracing_subscriber`'s actual default in the
pinned version before you write it down as the cause; if the default is stderr in
this version, the cause is somewhere else and you should say so rather than
patching what already works.

**Do not reorder `init_tracing()` past `Cli::parse()` to special-case
`--version`.** Its doc comment states a deliberate property — it runs
unconditionally at the top of `main` so that both entry paths sharing
`build_runtime()`, including `service::windows`'s SCM-dispatched callback, are
covered *by construction* rather than by each remembering to call it. Moving it
after the parse trades a real safety property for a cosmetic one. Fixing the
writer fixes `--version` for free and every other subcommand with it. If you
conclude the ordering genuinely must change, that is a design call worth a
numbered decision and an explicit argument for why the by-construction claim
survives — not a quiet edit.

**ANSI: check, do not assume.** The captured escapes came through a pipe, on
Windows, from the installed service exe. `tracing_subscriber::fmt` decides
`with_ansi` from a tty probe on some configurations and from a feature flag on
others. Establish which applies here before changing it, and if the escapes are
a consequence of the stdout/stderr bug rather than an independent one, say so —
two of the three Done-when items may close on one fix, and that is a better
outcome than three separate changes.

**The test should pin the writer choice, not require an unwritable directory.**
The Done-when asks for a test pinning `--version`'s stdout to one line. A test
that needs `C:\ProgramData` to be unwritable will not run anywhere. Prefer a
host test that exercises the fallback arm's writer selection directly.

**Decision numbers are global across `decisions/*.md`, not per file.** Take the
next number from the whole directory's maximum, not from the file you are
writing into.

**Native Windows build is a debt, not a gate item** (`protocol.md` §10) — record
it in the task file rather than attempting it from a worktree.

**Reserve line for `core`:** `embarch-core/open.md` is 4478/5120 B, **642 bytes
of headroom**, and its compaction task `tasks/core/022` is `blocked` on
`In flux: yes`. Nothing else in this sub-project is in reserve. If your work
spends that reserve — pushes a file into it or leaves one there — file
`tasks/core/<NNN>-compact-core.md` in the same commit per `tasks/README.md`.

**Out of scope:** `tasks/umbrella/031` is the receiving-side half of this defect
(umbrella interpolating a multi-line foreign string into a one-line `detail`).
Do not reach into `embarch-umbrella`; you own `embarch-core` and
`embarch-doc/embarch-core/` only.

## Done when

- [ ] `embarch-core --version` prints exactly the version line on stdout, whatever the state of the
      log directory. Whether it should initialise logging on that path at all is the design call.
- [ ] Any diagnostic it does emit goes to stderr, and the "continuing with stderr only" message is
      true of where it lands.
- [ ] ANSI colouring is off when stdout is not a terminal — the escapes above were captured by a
      pipe.
- [ ] A test pins the stdout of `--version` to one line, since the failure needs an unwritable log
      directory to reproduce and will not show up by accident.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
