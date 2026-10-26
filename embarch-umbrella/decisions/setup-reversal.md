# embarch-umbrella decisions: Setup's dry run and uninstall

**Status:** active, 2026-10-26.

What `embarch setup` shows before acting and how it is reversed. Split verbatim out of [install.md](install.md) on 2026-10-26 (`umbrella/079`).

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 21 — `embarch setup --dry-run` prints the plan before an elevated run executes it

The elevation friction decision 7 flags is partly a **"what is this about to do to my machine" problem, worse when the answer requires trusting a binary you just downloaded.** It runs every detection step exactly as `setup` does, then prints the concrete actions — which service calls, which files, whether elevation is needed — **reusing `setup`'s own detection path, not a second parallel implementation.**

**Built 2026-09-04, and it was not the one-flag-and-an-early-return it looked
like.** `make_plan` did already run every detection step before anything acted —
but two of the three side effects, decision 28's copy and `PATH` write,
**post-date this decision's text and only ever printed *while* acting**, so an
early return would have silently omitted them. So: every location a run may
write to is resolved once into a `Locations` passed down rather than read at
each write; `install.rs` gained a read-only `plan_install` built from the same
constants and predicates the real `install_into` uses, so the two cannot drift;
and one `apply_plan` walks both modes. A dry run names the canonical directory
and each binary as copy / already-there / absent, the env file and rc file
`PATH` would gain, the `embarch-core install --bind` line and its elevation, and
the state file it would write — and calls a Core it would put there **"would be
installed by this run"**, never "just installed here".

**What establishes that it changes nothing is a test, not the early return:**
`apply_plan` driven with every writable location pointed at a sandbox and
`embarch-core` a script that would leave a sentinel if ever executed, then the
sandbox asserted untouched. `--dry-run` conflicts with `--uninstall` rather than
being quietly ignored by it.

### 25 — `embarch setup --uninstall` reverses a machine setup

`init --uninstall` already reversed a repo integration; **nothing symmetric existed for `setup` itself.** It stops and unregisters the Core service, removes the machine-wide token file (a fresh `setup` regenerates one, matching normal first-run behaviour), and — per decision 28 — **removes the canonical install directory and the real `PATH` additions**, where it originally only printed the line to remove. It does not touch a firmware repo's own integration; that stays `init --uninstall`'s job. **It exits `1` when any step it attempted failed, naming each in a final line** (so `setup --uninstall && …` stops with Core still installed); `setup` does the same when its own service install fails, per decision 7's "print the exact command, exit nonzero".
