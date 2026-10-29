# embarch-umbrella decisions: Locating `embarch-api`

**Status:** active, 2026-09-13.

Split out of [doctor.md](doctor.md) on 2026-09-13 (`tasks/umbrella/059`), decision 42 moved
verbatim. It is not a check — `doctor.md`'s own mission is what `doctor` checks — but the
resolution mechanism check 1 and several others consume, and it had grown to 47% of that file
on its own.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/doctor-chain.md](../interfaces/doctor-chain.md)'s check 1 row.

### 42 — `locate_api` reads the agent CLI's own registration and `setup`'s install directory, not just `PATH`

[`open.md`](../open.md) recorded "check 1 does not locate that binary **here**" from three directions, never as its own item.

**It is a defect, and this machine's own filesystem is the evidence** [measured 2026-09-06]: `setup` had installed `embarch-api` at [decision 28](install.md)'s canonical location and written the sourcing line into `~/.bashrc`, but `locate_api` consulted only `EMBARCH_API_BIN` and `PATH`. That directory reaches `PATH` only through a shell rc file, so `command -v embarch-api` succeeds in an interactive shell and fails under `bash -c` and `bash -lc`. So check 1's verdict on a correctly installed suite turned on whether `doctor`'s shell was interactive: with Core located and the API not, a hard **Fail**, `not-found` — [decision 38](topology.md)'s false red, one binary over.

**Separate from decision 38**, `embarch-core`'s version of this question: this settles which `embarch-api` checks 8, 10 and 11 are statements *about*.

**Three sources, and the ranking is the decision.** After the explicit `EMBARCH_API_BIN`: *(a)* the command the agent CLI is registered to run, *(b)* `PATH`, *(c)* decision 28's canonical location (from `install.rs`'s own directory function, not a second spelling of it). (c) is last because a `PATH` hit is what the machine would run *by name*; it is there at all because of the rc-file gap above.

**(a) ahead of `PATH` is the contested rank, and this bench settles it** [measured 2026-09-06]: it carries **two `embarch-api` binaries with different contents and the same `--version`** — the installed copy and the debug build the registration names. Ranking `PATH` first would make checks 8, 10 and 11 statements about a binary nothing here runs, exactly the mixed install [check 11](schema-skew.md) exists to catch. Being an agent's MCP server is what `embarch-api` is *for*, so the registration is a **reading**, not a guess (decision 38's rule). It is read **once, in the driver** — check 10 already reads it ([decision 40](mcp.md)) — so the two checks cannot disagree about *what the registration says*, though they can still name different files: `EMBARCH_API_BIN` outranks it, and a registration naming a missing file is filtered out of the locator while check 10 spawns it anyway, so the divergence is printed, not assumed away.

*Rejected: rank the registration behind `PATH`, or drop it.* Stale JSON naming an old build would outrank a fresh install — a real cost, and why a missing-file registration falls through. It loses anyway: a stale entry is still **what the agent runs**, and hiding it is the invisible mixed install `open.md` complained about. *Rejected: call it by-design and delete the three bullets.* Right on a machine whose `embarch-api` is a debug build out of a checkout (not an installed suite); but it requires believing `setup` installs a binary `doctor` is then right not to find.

**Checks 8 and 11 have both run inside a live `doctor`**, [decision 44](budgets.md)'s 2026-09-07 bench run: one pass runs the full chain, so check 11's recorded verdict means check 8 ran too. The CLI shapes both assume were observed against both binaries on this bench [2026-09-06]: check 11's matches [decision 35](schema-skew.md), check 8's [decision 17](projects.md).

**`init` passes no registration**, deliberately: it *writes* one, and handing it back its own output would let a dev path propagate into a fresh repo. It gains (c), the half it was missing.

**The residual, stated rather than fixed.** Decision 28 writes its `PATH` line into `.bashrc`/`.zshrc` only, so `embarch-api` is still off `PATH` for a script, a CI job or an agent (`bash -lc` too: it writes no `.profile`) — `install.rs`'s question, not this one.
