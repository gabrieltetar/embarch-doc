# 054 — `embarch-core/src/api.rs`'s bare decision citations are unverified, and at least three name another repo's decision

**State:** done by agent/core/054-api-rs-bare-decision-citations, 2026-09-13
**Source:** the leg of 2026-09-13 17:0x, refill sweep. The carry-forward in
`supervisor-log.md`'s 2026-09-12 entry says plainly that the wrong-decision-number defect class
*"is bigger than assumed and no gate sees it"*, and that **no sweep has been filed yet for
`embarch-core`'s own source**. `check-decision-refs.py` resolves numbers only inside `*.md`, so a
wrong number in a `.rs` comment that happens to resolve fails nothing.
**Scope:** core
**Hardware:** none — comments and, where a claim has gone false, the prose around them.
**Owner:** no

## What

`embarch-core/src/api.rs` carries **~35 bare `decision N` citations** — no repo qualifier, so each
resolves by convention to `embarch-core`'s own decision N. Verify each one against the body it
resolves to, and fix what does not hold.

**Three known leads, found while filing this and not yet acted on.** All three sit beside an
`embarch_topology` symbol, which is what makes them suspicious — `embarch-topology` has 31
decisions, so a bare `decision 28` here silently resolves to `embarch-core` decision 28 instead:

- `api.rs:970` — `` (`embarch_topology::hardware::validate_role_timed`, decision 28 ``
- `api.rs:1110` — `` // configured" state (decision 28 ``
- `api.rs:1126` — `` (`embarch_topology::hardware::recent_alerts`, decision 28 ``

**Do not trust that list — grep for yourself.** The two units before this one (`umbrella/061`,
`062`) were each given a list of sites and each was told to grep instead; one list was right and
the sweep is what made that knowable.

## The method, which is the whole task

For each bare citation: resolve it in `embarch-doc/embarch-core/decisions/*.md`, **read the body**,
and ask whether the comment's claim is what that decision actually says.

- **Right number, claim holds** → leave it alone. Most will be this.
- **Wrong repo** → prefix the owning repo (`` `embarch-topology` decision 28 ``), and **re-derive
  the number in the target repo** rather than assuming the same number. `ui/040`'s reviewer caught
  two citations that were prefixed without being re-derived; that is the failure mode of this exact
  fix.
- **Right number, claim has gone false** → this is the finding that matters, and four consecutive
  units have hit it. **A citation repair that leaves a false claim intact is the defect class this
  suite keeps paying for** (`umbrella/062` fixed a link's depth while its target section had been
  dead four days; `core/053` fixed a filename while the sentence around it had also gone false).
  Reword the claim to what is true and say so in the commit message.
- **Number resolves nowhere** → say so in the commit; do not guess a replacement.

## Constraints

- **Comments and prose only.** No behavioural change, no refactor. If you find a real code defect,
  drop it in `/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path) and carry on.
- **Do not renumber or edit any decision.** If a decision body is the thing that is wrong, that is
  a drop, not an edit.
- **In reserve for `core`:** `embarch-core/decisions/auth.md` at 11356/12288 B (932 B left), filed
  against blocked `tasks/core/046`. You are unlikely to need to write a decision here at all; if
  you do and it spends that reserve, file `tasks/core/<NNN>-compact-core.md` in the same commit.

## Done

Swept every `decision N` citation in `api.rs` (55 individual citations across 53 comment sites —
grepping found more than the "~35" estimate, as flagged). 52 held: most bare and correctly resolving
by convention to their own `embarch-core` decision, the rest already correctly repo-qualified.
Three did not, all fixed in `db31be6`/`e4b5b72` (`embarch-core`):

- `api.rs:825` — bare `decision 17` (`set-dev-bench-link`'s CLI/endpoint split) resolves by
  convention to `embarch-core`'s own decision 17 ("CI everywhere", unrelated), but the claim is
  `embarch-topology` decision 17's own text almost verbatim. Prefixed `embarch-topology`; the number
  was already right, just unattributed — re-derivation confirmed it rather than changing it.
- `api.rs:970-971` — `(decisions 8, 22)` cited, alongside decision 22 (the identity gate, which
  does run mid-attach and supports the claim), `embarch-core`'s own decision 8 — the SoC-to-chip
  table, unrelated to the mid-attach identity check and not touched by `validate_role_timed`'s call
  path. Dropped the wrong number, kept 22.
- `api.rs:1424` (test comment) — `` `embarch-dev-bench` decision 26 `` is that repo's
  ESP32-C5-WROOM-1 board decision — unrelated. The actual claim (`base_address` only meaningful for
  `format = "bin"`) is `embarch-core`'s own decision 18 (`flashing.md`, "Format::Bin at the merge
  address"). Fixed to the correct repo (bare, this crate's own) and number.

**The three "known leads" in this task (`api.rs:970, 1110, 1126`) were false alarms**, exactly as
warned. `embarch-core` has its own decision 28 ("`POST /validate` and `GET /alerts`, reachable
without touching hardware", `enrollment.md`) which is precisely what all three sites describe —
bare is correct there. `embarch-topology`'s own, unrelated decision 28 was the coincidence that made
them look suspicious.

No decision bodies touched, no behavioural change. `cargo build`/`test`/`clippy --all-targets -- -D
warnings` all clean.

## Done when

- [x] Every bare `decision N` in `embarch-core/src/api.rs` has been resolved against its body and
      either left, attributed, or corrected — and the commit message says how many of each.
- [x] Any foreign citation names its repo **and** the number was re-derived in that repo.
- [x] Gate green (`../../../embarch-fleet/protocol.md` §10).
- [x] `changelog.d/core-*` fragment.
