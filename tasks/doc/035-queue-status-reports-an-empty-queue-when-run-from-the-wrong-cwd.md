# 035 — `queue-status.py` reports a completely empty queue, silently, when its cwd is outside the instance

**State:** open
**Source:** leg 065's supervisor, 2026-09-10. Hit at step 0 of that leg and again at its close;
diagnosed the second time.
**Scope:** doc
**Hardware:** none
**Owner:** required — the fix is in `scripts/`, which `protocol.md` §2 reserves.

## What

Run from a cwd that is not inside the instance checkout, `queue-status.py` prints:

```
REFILL OWED -- 0 dispatchable, below the 4 low-water mark (units_per_leg); and 0 distinct
scope(s) (none), below a wave of 6 -- ...
```

Run against the same repo with `--root /home/gabriel/Github/embarch/embarch-doc`, it prints **38
dispatchable across 8 scopes**. No error, no warning, no non-zero exit distinguishes the two. The
`--root` default is resolved relative to the process's cwd, so `embarch-fleet/embarch-doc` — a path
that does not exist — yields an empty scan rather than a failure.

**A supervisor agent's cwd is reset between every Bash call**, to the session's primary working
directory, which for a leg spawned by the listener is `embarch-fleet` and not the instance. So the
wrong answer is the *default* answer for the actor that depends on this script most.

## Why this is worth fixing rather than remembering

`.claude/leg.md` routes three separate decisions through this script's output, and **all three fail
in the same direction — toward doing no work:**

1. **Refill.** `--refill-owed` exit 0 means "sweep the sources now". A leg that believes the queue
   is empty sweeps eight `open.md` files it did not need to read, which is cost, not damage.
2. **The dream, and this is the damaging one.** `.claude/leg.md`: *"If refill also finds nothing,
   dream and end the leg"* — post three proposals with `--action` (which **notifies the owner**)
   and exit. A leg that gets a false zero here, and whose refill sweep is also thin, **pages the
   owner about a dry queue that has 38 tasks in it, and ends without doing any work.** Under the
   relay the listener will not respawn it into another dream for 6 hours.
3. **The listener's own pre-recovery count**, which decides whether to spawn a leg at all.

I got the false zero at step 0 of leg 065 and only caught it because the number (`0 dispatchable`)
was implausible against a queue I had just read the `inbox/` of. **That is not a check; that is
luck.** A leg with no prior expectation would have believed it.

## Two candidate fixes, and the first is nearly free

1. **Fail loudly instead of returning empty.** If the resolved root has no `tasks/` directory, exit
   non-zero with the path it tried. A missing instance is not an empty queue, and every caller
   would rather have an error than a zero.
2. **Resolve the default root from `fleet.toml` the way `fold-commit.py` already does** — it
   locates the instance checkout regardless of cwd, falling back to `fleet.toml`'s `doc_repo`, and
   that asymmetry between the two scripts is itself the smell. Whatever `fold-commit.py` does here
   is the behaviour `queue-status.py` should have.

Both are in `scripts/`, so no leg can make either change.

## Done when

- [ ] `queue-status.py` run from any cwd either returns the true count or fails with the path it
      tried — never `0 dispatchable` for a populated queue.
- [ ] The same check is applied to any other fleet script that defaults a root from cwd
      (`check-doc-size.py` and `collect-open-questions.py` are the ones a leg calls most; I did not
      audit them).
- [ ] `.claude/leg.md`'s dream instruction says explicitly that a zero from `queue-status.py` must
      be confirmed against a second reading before a dream is posted — the dream is the one action
      in a leg that both notifies the owner and forfeits the leg.

## Filed from `inbox/` by leg 066, 2026-09-10 — and independently reproduced

Numbered `doc/035` and moved into the queue unchanged except for this section and the heading.
It parses; `Hardware: none` is correct; `Owner: required` is correct, because both candidate
fixes are in `scripts/`.

**I hit the same class of failure at my own step 0, on a different script, before I had read this
drop** — which is worth recording because it says the diagnosis generalises rather than being one
script's bug:

```
$ python3 /home/gabriel/Github/embarch/embarch-fleet/scripts/check-doc-size.py --due
python3: can't open file '.../embarch-fleet/scripts/check-doc-size.py': [Errno 2] No such file
EXIT=0
```

**Both repos have a `scripts/` directory**, and they hold overlapping but different sets of
files. `embarch-fleet/scripts/` has `usage-budget.py` and `fleet-tick.py`; the instance's
`embarch-doc/scripts/` has those *and* `check-doc-size.py`, `queue-status.py`,
`collect-open-questions.py`, `fold-commit.py` and the rest of the gate. A leg's cwd is
`embarch-fleet`, so a bare `scripts/<name>` resolves against the wrong one for exactly the
scripts a leg depends on most — silently succeeding for some names and failing for others.

Note the exit code above: **the shell reported `EXIT=0`** for a Python interpreter that could not
open its own script, because the exit status came from a pipeline's `tail`. That is a second,
independent way this class of failure reads as success, and it is not in the drop. A leg that
wrapped this in `| tail` and checked `$?` — which is the natural shape, since these scripts are
verbose — would conclude "nothing overdue" from a script that never ran.

**This drop's own third `Done when` bullet is the one I would act on first**, and it names
`check-doc-size.py` as an unaudited candidate. It was right to.

Worked around for this leg by running every script from the leg worktree with an explicit
`--root`, which is a workaround a supervisor has to remember, which is the whole complaint.
