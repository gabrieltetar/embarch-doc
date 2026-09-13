# embarch-umbrella decisions: Locating `embarch-api`

**Status:** active, 2026-09-13.

Split out of [doctor.md](doctor.md) on 2026-09-13 (`tasks/umbrella/059`), decision 42 moved
verbatim. It is not a check — `doctor.md`'s own mission is what `doctor` checks — but the
resolution mechanism check 1 and several others consume, and it had grown to 47% of that file
on its own.

Index: [../decisions.md](../decisions.md). Current truth: [../interfaces/doctor-chain.md](../interfaces/doctor-chain.md)'s check 1 row.

### 42 — `locate_api` reads the agent CLI's own registration and `setup`'s install directory, not just `PATH`

[`open.md`](../open.md) recorded "check 1 does not locate that binary **here**" from three directions and never as its own item, and the first question was whether it is a defect at all: a machine whose `embarch-api` is a debug build out of a checkout is not an installed suite, and reporting an absence there would be correct.

**It is a defect, and this machine's own filesystem is the evidence** [measured 2026-09-06]. `setup` had installed `embarch-api` at [decision 28](install.md)'s canonical location, beside `embarch` itself, and written the sourcing line into `~/.bashrc`. `locate_api` consulted `EMBARCH_API_BIN` and `PATH` and nothing else — and that directory reaches `PATH` only through a shell rc file, so `command -v embarch-api` succeeds in an interactive shell and fails in both `bash -c` and `bash -lc`. Check 1's verdict on a correctly installed suite therefore turned on whether the shell that ran `doctor` happened to be interactive; with Core located and the API not, it fell through to a hard **Fail**, `not-found`. That is [decision 38](topology.md)'s false red, one binary over.

**Filed here rather than beside 38**, which is the same question for `embarch-core`: `topology.md` answers "where is Core, and what may be done to it from here", and this involves no topology class, no WSL2 boundary and no elevation. What it settles is which `embarch-api` checks 8, 10 and 11 are statements *about* — the check chain's own subject.

**Three sources, and the ranking is the decision.** After the explicit `EMBARCH_API_BIN`: *(a)* the command the agent CLI is registered to run, *(b)* `PATH`, *(c)* decision 28's canonical location, computed from `install.rs`'s own directory function rather than a second spelling of it. (c) is last because a `PATH` hit is what the machine would run *by name*; it is there at all because of the rc-file gap above.

**(a) ahead of `PATH` is the contested rank, and this bench is the case that settles it** [measured 2026-09-06]: it carries **two `embarch-api` binaries with different contents and the same `--version`** — the installed copy, and the debug build the registration names. Ranking `PATH` first would make checks 8, 10 and 11 statements about a binary nothing here runs, while [check 11](schema-skew.md)'s stated purpose is catching exactly that mixed install. Being an agent's MCP server is what `embarch-api` is *for*, so the registration is a **reading** of what runs, the way `sc.exe qc` is for Core, and decision 38's "a reading beats a guess" is the same rule. It is read **once, in the driver** — check 10 was already reading it ([decision 40](mcp.md)) — so the two checks cannot disagree about *what the registration says*. They can still name different files: `EMBARCH_API_BIN` outranks the registration, and a registration whose command is not an existing file is filtered out of the locator while check 10 spawns it anyway. That is why the divergence is printed rather than assumed away.

*Rejected: rank the registration behind `PATH`, or leave it out.* It is user-editable JSON, and a stale entry naming an old build would then outrank a freshly installed binary — a real cost, and why a registration whose file is gone falls through rather than winning. It loses anyway, because that "stale" entry is still **what the agent runs**, and hiding it is precisely the invisible mixed install `open.md` complained about; check 1 names the divergence in its detail rather than choosing silently. *Rejected: call the whole thing by-design and delete the three bullets.* It requires believing `setup` installs a binary `doctor` is then right not to find.

**What the same sitting measured about the two checks that shell out** [2026-09-06, against the installed binary and the debug build alike]: `--json` and `--config` are top-level and must precede the subcommand — clap exits **2** otherwise, which is what [check 11](schema-skew.md) reports as an `embarch-api` too old to know `versions`; `versions` answered `host_type_schema_version` **17**, Core's own number, from both binaries; `list-targets` answered `{success: true, targets: [...]}` on exit 0 and `{success: false, error}` on exit 1, both on **stdout**, with its own log line on stderr. Every shape checks 8 and 11 had only read off `embarch-api`'s source is therefore observed. **Neither check has run inside a `doctor` yet** — that needs a live Core and stays in [`open.md`](../open.md).

**`init` passes no registration**, deliberately: it is the command that *writes* one, and handing it back its own output would let a dev path propagate into a fresh repo. It gains (c), which is the half it was missing.

**The residual, stated rather than fixed.** Decision 28 writes its `PATH` line into `.bashrc`/`.zshrc` only, so `embarch-api` is still off `PATH` for a script, a CI job or an agent — `bash -lc` included, since `.profile` is not among the files it writes. That is `install.rs`'s question; the locator is now correct either way, which is why it is recorded here rather than changed.
