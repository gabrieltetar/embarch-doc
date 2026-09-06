# 007 — `embarch.md` §5's rustfmt cost was measured with a command that skips a whole crate

**State:** open
**Source:** `suite/006`'s reviewer, 2026-09-06, re-measuring the numbers recorded by leg 016.
Dropped in `inbox/` as `suite-rustfmt-cost-omits-a-path-dep-crate.md` and drained here by
leg 017.
**Scope:** suite
**Hardware:** none — re-checked at drain: six clean Rust checkouts and two doc edits, no board
and no machine. Claim stands.
**Owner:** no. `embarch.md` §5 and `suite/roadmap.md` are both `fleet_writable`. **`suite`
scope, so the supervisor executes it under `../../embarch-fleet/protocol.md` §8** — never
dispatched to a worker, and only after §4's 30-minute announcement window.

## What

`embarch.md` §5's new `rustfmt` bullet records **81 files, 1,245 hunks, 1,881 existing
lines** across six crates. Those numbers reproduce exactly, but they were produced by
`cargo fmt --check`, which formats **only the current package's own targets**. It does not
descend into local path-dependency crates, even ones inside the same repo.

`embarch-api` has one: `crates/embarch-core-client`, 10 tracked files in the `embarch-api`
repo, pulled in at `Cargo.toml:18` as `{ path = "crates/embarch-core-client" }`. It is not a
workspace member — `cargo metadata` reports `embarch-api` as the sole package — so
`cargo fmt --check` never sees it, and it contributes **6 files / 42 hunks / 66 lines** that
the recorded total omits.

Measured at `embarch-api` `943419b`, `embarch-core` `8be583f`, `embarch-study-designer`
`48cac00`, `embarch-topology` `9a56959`, `embarch-ui` `e89612d`, `embarch-umbrella` `08ccd6f`,
all clean, deduplicated by owning repo (`cargo fmt --all` reaches sideways into sibling repos
through `path = "../..."` deps, so a naive per-repo `--all` sum triple-counts
`embarch-study-designer` and `embarch-topology`):

| repo | files | hunks | existing lines |
|---|---|---|---|
| `embarch-study-designer` | 24 | 338 | 542 |
| `embarch-api` | **24** | **189** | **275** |
| `embarch-core` | 14 | 289 | 460 |
| `embarch-umbrella` | 11 | 212 | 272 |
| `embarch-topology` | 9 | 53 | 70 |
| `embarch-ui` | 5 | 207 | 328 |
| **total** | **87** | **1,288** | **1,947** |

Two clauses in §5 change:

- **"81 files, 1,245 hunks, 1,881 existing lines"** → 87 / 1,288 / 1,947. (`embarch-umbrella`
  is 212 hunks now, not the 211 recorded — see the drift note below; 1 of the 43-hunk delta
  is that, 42 are the missing crate.)
- **"largest first `embarch-study-designer` (24 files) then `embarch-core` (14)"** —
  `embarch-api` is also 24 files once its own crate is counted, so it ties for largest and
  `embarch-core` is third.

**The reason this is worth correcting rather than shrugging at is the reversal condition, not
the total.** §5 says the format-the-world commits fire "the moment `cargo fmt --check` is
added to §10 or to any repo's CI". That is the command that just under-measured. A §10 or CI
check spelled `cargo fmt --check` would be structurally blind to
`crates/embarch-core-client` — a gate that passes while six files stay unformatted, which is
the same shape as the `check-ownership.py` blindness the decision was written to work around.
**The check, whenever it lands, must be `cargo fmt --all --check` run per repo.**

## The drift claim is sound, and understated

Not a correction — the opposite. §5 cites `embarch-umbrella` moving 209 → 211 hunks. Both
endpoints are exactly reproducible and were measured the same way: leg 015's table
(`embarch-core` 289, `embarch-api` 147, `embarch-topology` 53) reproduces digit-for-digit
under `cargo fmt --check`, so leg 015 and leg 016 used the same command. Walking
`embarch-umbrella`'s tree at each commit of 2026-09-05/06:

    12:19 ddd3e4d  172      22:46 1489f36  207
    17:40 66e4a78  180      23:32 80f4cb8  209   <- leg 015's number
    17:59 1b41853  185      00:34 5f978e7  210
    18:03 81e20f4  185      01:13 8e70b78  211   <- leg 016's number
    21:26 d9844dd  190      01:28 08ccd6f  212   <- HEAD

**+40 hunks in thirteen hours, monotonic across eleven commits.** "209 → 211 across two units"
is the weakest two-point slice of that curve. The load-bearing evidence for the decision is
stronger than the sentence carrying it.

## The one wording claim that is not true yet

§5 ends: "the trap this closes is closed by instruction". Nothing a worker reads says this
today. Leg 016 knows — its own drop
(`inbox/workers-must-be-told-not-to-run-cargo-fmt.md`) says the sentence lives in
`embarch-fleet/`, which no leg may write, and that leg 016 pasted it by hand into two
dispatches. That drop is the right discharge and `tasks/suite/006` named it as such. But
`embarch-decision-reversals.md`'s own recurring shapes are exactly this: **shape 3**, "a help
string is documentation, and documentation is not a gate" (row 81), and **shape 4**, "a note
describing a gap is not a mechanism for closing one" (row 44). A decision recorded in the
present tense as *closed*, whose closing mechanism is an open inbox drop, is shape 1 —
"documented as implemented, wasn't" — waiting to happen. Present tense → conditional: *would
be closed by an instruction that does not exist yet*, with the drop named.

## Why now

Both fixes are one edit to one bullet in a `fleet_writable` file, and `suite/006` is closed
and its task file deleted, so nothing else will revisit these numbers. The reversal condition
is the part that decays silently: it is a standing instruction to a future session that names
a specific command, and that command is wrong in a way that will not fail loudly.

## Not a finding

Checked and clean, recorded so the next reviewer does not redo it: no standing decision is
contradicted — no `rustfmt` or formatting decision exists anywhere in the suite before this
one, `embarch-decision-reversals.md` has no formatting row, and `protocol.md` §10 does run
only build/test/clippy as §5 states. `embarch-dev-workflow.md` §6, the owner-reserved doc
that is arguably the more natural home, says nothing about formatting, so §5 does not
contradict it. `../../embarch-fleet/protocol.md` from `suite/roadmap.md` resolves in both the
owner's checkout and the leg worktree (via the `embarch-fleet` symlink at
`.worktrees/embarch-doc/`). `history/suite.md`'s repeated `## 2026-09` headings are
pre-existing `build_changelog.py` output, 5 before this unit and 6 after. The doc gate is
9/9 green in the leg worktree. The `suite/roadmap.md` **Later** line agrees with §5.

## Done when

- [ ] `embarch.md` §5 carries 87 / 1,288 / 1,947, and the "largest first" clause names
      `embarch-api` alongside `embarch-study-designer`.
- [ ] The reversal condition names `cargo fmt --all --check`, per repo, and says why the
      bare form is not enough.
- [ ] §5 no longer states in the present tense that the trap is closed, and points at the
      drop that would close it.
