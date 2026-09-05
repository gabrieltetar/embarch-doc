# 003 — `embarch setup --dry-run` is one flag and an early return away, and does not exist

**State:** claimed by agent/umbrella/003-setup-dry-run, 2026-09-04 21:15
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 21 read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none
**In reserve for this sub-project:** `embarch-umbrella/spec.md` — 9671/10240 B,
**569 B of headroom**, already filed against `tasks/umbrella/009-compact-docs.md`
(which is `blocked`, `In flux: yes`). `open.md` is out of reserve (88.1%). Plan
the `setup` row edit inside 569 bytes; if you spend past the cap or push
`open.md` back into reserve, file `tasks/doc/<NNN>-compact-umbrella.md` in the
same commit per `tasks/README.md` § "Compaction tasks".

## What

`embarch-umbrella` decision 21 says `embarch setup --dry-run` runs every
detection step exactly as `setup` does and prints the concrete actions — which
service calls, which files, whether elevation is needed — **reusing `setup`'s own
detection path rather than a second implementation.**

The flag does not exist. `Command::Setup` in `src/main.rs` carries `--host`,
`--port`, `--uninstall` and `--dev-bench-repo` only; the sole `--dry-run` in the
binary is `deploy-core`'s.

**The hard part is already done.** `setup::make_plan` runs every detection step
and returns a `Plan` before anything is acted on, and `setup` already prints the
elevated commands it would have a human paste. What is missing is the flag and a
return before the first side effect — plus deciding what `--dry-run` prints for
the steps that currently only print *while* acting (the canonical install and the
`PATH` write, decision 28, which post-date decision 21's text).

## Why now

Decision 21's reason is that elevation is partly a "what is this about to do to
my machine" problem, and worse when the answer requires trusting a binary you
just downloaded — which is exactly the first-day case umbrella exists for.
Cheap, and `spec.md` advertised the flag as shipped until 2026-09-03.

## Done when

- [ ] `embarch setup --dry-run` prints the plan and makes no change: no service
      call, no token file, no copy, no `PATH` or registry write.
- [ ] Decision 28's install and `PATH` steps are represented in the printed plan,
      not silently omitted.
- [ ] A test proves the dry run reaches no side-effecting call.
- [ ] `spec.md`'s `setup` row and decision 21's implementation note updated.
- [ ] Gate green; `changelog.d/` fragment dropped.
