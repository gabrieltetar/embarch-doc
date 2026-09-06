# 006 — no Rust repo in this suite is `rustfmt`-clean, and nothing in the gate has ever looked

**State:** open — **announced and parked by leg 016**, `#embarch-fleet` `ts 1788678196.359869`
(2026-09-06 01:03 MDT); window closes **01:33 MDT**. The announcement states the intended arm
(decline, and record why) and names the repos. If this leg ends before the window closes, the
next leg **completes this window rather than restarting it** — read that `ts` for a reply first.
A reply saying go runs it immediately; cancel drops this back to plain `open` with the reply
quoted here.
**Source:** `api/019`'s worker, 2026-09-06. It ran `cargo fmt` reflexively, watched it rewrite
**18 files / ~780 lines it had not touched**, reverted all of that and re-applied its own
change by hand so the commit stayed one file. Then it reported the fact rather than quietly
working around it.
**Scope:** suite — it is a question about every Rust repo at once and about
`protocol.md` §10's gate, so it is the supervisor's under §8, never a worker's.
**Hardware:** none
**Owner:** partly. **Adding `cargo fmt --check` to §10 is `../../embarch-fleet/protocol.md`
and therefore the owner's.** Deciding the suite's posture and recording it is not. Adding a
`fmt` job to each repo's `.github/workflows/` is inside the code repos and is reachable — but
only after the posture is decided, and the format-the-world commit is the expensive half.

## What

Counted by leg 015 at `main`, `cargo fmt --check` reporting files that differ:

| repo | files rustfmt would rewrite |
|---|---|
| `embarch-core` | 289 |
| `embarch-umbrella` | 209 |
| `embarch-api` | 147 |
| `embarch-topology` | 53 |

**Not one repo is clean, and the gate has never asked.** §10 runs `build`, `test` and
`clippy --all-targets -- -D warnings`; formatting is absent from it, from every repo's CI, and
from every worker's instructions. So the suite has no formatting policy — not a deliberate
one and not an enforced one, just an absence nobody has had to look at.

**The reason it matters now is the trap it sets for a worker, not the diff itself.** A worker
that types `cargo fmt` — a reflex, and a reasonable one — produces a diff hundreds of files
wide that is entirely outside its task, entirely outside its sub-project in a shared repo, and
which `check-ownership.py` will happily allow because in a code repo the worker owns the whole
tree. `api/019`'s worker caught itself. **The next one may not**, and a fold that lands 780
unrelated reformatted lines under a one-line task's message is unreviewable by construction.

## The choice, and both arms are defensible

- **Adopt it.** One format-the-world commit per repo, `cargo fmt --check` added to §10 and to
  each repo's CI. Cost: four commits that rewrite most of the suite and make
  `git blame`/`git log -S` on any of those lines land on a mechanical commit — which matters
  here more than usual, because this suite's whole review surface is *why* a line is the way
  it is. Benefit: the trap closes permanently and the question never recurs.
- **Decline it, and say so.** Record that the suite does not enforce `rustfmt`, that no gate
  will, and — the load-bearing half — **tell workers not to run `cargo fmt`**, so the trap is
  closed by instruction rather than by formatting. Cost: the absence stays, and someone will
  ask again.

**What must not happen is the third thing, which is what happens today**: no posture, no
instruction, and each worker deciding privately whether to reformat the repo.

## Why now

`api/019`'s worker hit it, reverted ~780 lines by hand to stay in scope, and said so — which
is the only reason it is visible at all. It is exactly the class of thing that never surfaces
through a failure, because the failure is a merge that looks fine.

## Done when

- [ ] The suite has a recorded posture on `rustfmt`, with the rejected arm argued against
      rather than listed, and a reversal condition.
- [ ] If declined: the "do not run `cargo fmt`" instruction reaches workers. That text lives
      in the fleet repo, so the fleet-side half is **dropped to the owner in `inbox/`**, not
      edited.
- [ ] If adopted: each repo is formatted in its own commit, separate from any behaviour
      change, and the check is wired where the posture says it belongs.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
