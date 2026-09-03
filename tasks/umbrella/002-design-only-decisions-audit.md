# 002 — Six decisions are recorded as designs, and nobody has checked which shipped

**State:** claimed by agent/umbrella/002-design-only-decisions-audit, 2026-09-03 12:26
**Source:** embarch-umbrella/open.md — "Several later decisions are recorded as designs with no implementation note, and whether each shipped is not established here. … Reading the code is the way to close this, not reading this repo."
**Scope:** umbrella
**Hardware:** none

## What

`embarch-umbrella`'s docs carry a set of decisions whose implementation status is
unknown *to the docs*: `setup --dry-run` (21), the firewall and disk checks (22b,
22c), the MCP-handshake spawn (23), `doctor --prune` (26), the release version
assertion (27/29), and check 16, the bind-address-versus-topology check, which
`spec.md` marks design-only.

**Close each one against the source, one at a time**, and make the docs say what
the code does. For each: shipped, not shipped, or shipped differently from what
the decision describes — that third outcome is the valuable one and is the reason
this is worth a task rather than a skim.

This is exactly the drift `open.md` names, and it just bit for real: the same
bullet said "check 14 (bind address versus topology) is explicitly design-only"
while decision 31's flashing-backend check had **shipped as 14** in code, so two
different checks answered to one number until `umbrella/001` renumbered the
unbuilt ones to 16–19 on 2026-09-03. Assume more of that, not less.

**Read `embarch-umbrella/spec.md` and `decisions/` fresh** — several of its files
moved this morning under `umbrella/001`, and a stale copy in your head will send
you looking for the wrong numbers.

## Why now

Every one of these is a claim the suite's own docs make about a shipped binary,
and the numbering collision above shows the claims have already drifted from the
code at least once. It is entirely a reading task: no build to design, no
hardware, no wire.

## Done when

- [x] Each of the seven items above has a stated, evidenced answer — name the
      function or the absence, not "appears to".
- [x] `spec.md` describes what the binary does, with any design-only marker that
      is now false removed and any that is still true kept.
- [x] `decisions/` gains an implementation note wherever a decision shipped
      differently from what it describes. **Do not rewrite the decision** — the
      record of what was decided stays; the note says what was built.
- [x] `open.md`'s "Several later decisions…" bullet is rewritten to whatever is
      genuinely still unestablished, or removed if nothing is.
- [x] A `status.d/` fragment for anything in `suite/features.md` this makes
      false — the `embarch doctor` row and its neighbours are the likely ones.
- [x] **Build nothing.** If an item turns out to be unshipped, that is a finding
      to record, and a task for it belongs in `inbox/` — not work to do here.
      A doc-only branch is the expected shape of this task.
- [x] Gate green (`embarch-parallel-agents.md` §10).
- [x] `changelog.d/` fragment dropped.

## Result, 2026-09-03

**All seven settled from the source; none needed a running binary or hardware.
Every one of the seven is unbuilt**, and four of them were claimed as shipped by
`spec.md`.

| Item | Verdict | Evidence |
|---|---|---|
| `setup --dry-run` (21) | not built | `Command::Setup` in `src/main.rs` has `--host`/`--port`/`--uninstall`/`--dev-bench-repo` and no `--dry-run`; the only one in the binary is `deploy-core`'s. `setup::make_plan` — the reusable detection path the decision asks for — does exist |
| bind address vs topology (22a, check 16) | not built; **design-only marker correct, kept** | `doctor()` assembles exactly checks 1-15; `recommended_bind_address` is called only from `setup` at install time |
| firewall (22b, check 17) | not built; marker correct, kept | no `firewall` anywhere in the crate |
| disk space (22c, check 18) | not built; marker correct, kept | no disk measurement anywhere in the crate |
| MCP handshake spawn (23) | not built | `check_mcp` runs `claude mcp get embarch` and passes on exit zero; nothing spawns the registered command, no `initialize` is sent |
| `doctor --prune` (26) | not built, **including the always-on reporting half** | no `--prune` and no occurrence of the word; no check reads `study_results/` or measures the build tree |
| release version assertion (27/29) | not built **in any repo** | this repo's `release.yml` never reads `Cargo.toml`'s version or the tag; read-only check found the same in core, api, topology; the other four have no release workflow |

**Two more of the same class, found while reading and not on the list:**

- **Decision 18** — check 5's Linux "attached but not permitted" branch does not
  exist. `check_probes` has no USB device-tree lookup and **no `Fail` branch at
  all.** `spec.md` asserted it twice.
- **Decision 17's amendment** — check 8 still uses `zephyr::count_valid_targets`,
  the local approximating scanner the amendment says was replaced by a shell-out
  to `embarch-api`'s listing. Everything else in decision 17 shipped.

**No second numbering collision.** Decisions 1-34 are all present, none
duplicated, none missing; 27/29 is the recorded pair. One provenance gap, not a
collision: `spec.md`'s check 19 (tail of Core's log) descends from **`embarch-core`
decision 16**, not from any umbrella decision — the citation was lost in
compaction and is restored.

Six `inbox/` drops, in the main checkout (a worktree's `inbox/` is gitignored and
dies with the worktree): `umbrella-doctor-mcp-handshake`,
`umbrella-doctor-probe-not-permitted`, `umbrella-doctor-prune`,
`umbrella-setup-dry-run`, `umbrella-doctor-target-count-shellout`, and
`suite-release-tag-version-assertion` (suite scope — it touches four repos).

**Code branch has no commits.** Nothing was built, by instruction.

## Watch for

If you find that a *number* is wrong somewhere — a check, a decision reference —
say so loudly in your report. `umbrella/001` found one collision already, and a
second would mean the numbering needs a rule rather than another repair.
