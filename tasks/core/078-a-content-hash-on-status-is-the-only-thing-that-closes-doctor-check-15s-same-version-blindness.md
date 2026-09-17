# 078 — A content hash on `/status` is the only thing that closes `doctor` check 15's same-version blindness, and it is this repo's call

**State:** claimed by agent/core/078-status-content-identity, 2026-09-17 17:46
**Source:** refill sweep, leg 137, 2026-09-17, from
[`embarch-umbrella/open.md`](../../embarch-umbrella/open.md)'s standing bullet: *"**Check 15 is not
a hash comparison and must not be read as one.** It catches a *cross-version* stale deploy and is
blind to a same-version one: `core_version` is `CARGO_PKG_VERSION`, so a rebuild and failed deploy
at one version reads as a match ([decision 34](../../embarch-umbrella/decisions/schema-skew.md)). A
content hash on `/status` would close it, `embarch-core`'s call."* The bullet has named this repo as
the deciding one and **nothing has ever been filed here**, so the call has no owner.
**Scope:** core
**Hardware:** none — this is a decision about what `/status` carries, answered by reading
`src/api.rs`'s status handler, `decisions/surfaces.md` and the build. **Do not deploy, do not run a
live Core, do not flash anything.**
**Owner:** no

**Doc-size reserve, re-read at dispatch (leg 141, 2026-09-17) — this supersedes the filing-time
reading below, and it changes what you owe.** `embarch-core/decisions/surfaces.md` — the file this
task's `Done when` names as the likely home for your decision — is **11,253/12,288 B (91.6%), IN
RESERVE, 1,035 B left**. Its compaction task `tasks/core/079-compact-core.md` is **`blocked` on
`In flux: yes`**, and `.claude/leg.md` is explicit that a blocked compaction task parks the *pass*,
not the reserve: **if you write into `surfaces.md`, you compact `surfaces.md` as part of this unit**,
carrying `tasks/core/079`'s `Must not delete:` list verbatim (read that file first — it names
decision 12's scope/trigger paragraph, decision 59's original resolution, `core/074`'s correction and
`core/077`'s settlement) and bringing the file back under 90%. You are the actor making the flux, so
you are the only one who can shorten what you are rewriting without writing a clean statement of
something about to be wrong. Do **not** close `tasks/core/079` — say in your report what you paid and
leave the task for the supervisor to settle.

**If the topic-correct home for your decision turns out not to be `surfaces.md`, none of the above
applies** — say which file you chose and why, and check its headroom instead. What you must not do
is pick a file by where there is room; `embarch-api` filed a decision in the wrong topic file on
2026-09-05 for exactly that reason, with 96 B left, and nothing failed.

**Doc-size reserve for `core`, read at filing:** `embarch-core/decisions/auth.md` is
**11,356/12,288 B (932 B left)**, filed as `tasks/core/046` and blocked — do not write into it.
`decisions/surfaces.md` and `interfaces.md` have room. Run `python3 scripts/check-doc-size.py
--pressure` before and after; if your edits push another file into the band, file
`tasks/core/<NNN>-compact-core.md` in the same commit.

## What

`embarch-umbrella`'s `doctor` check 15 compares the `core_version` a running Core reports against
the version the umbrella expects. `core_version` is `CARGO_PKG_VERSION`, so it answers *"is the
running binary from a different release"* and cannot answer *"is the running binary the one I just
built"*. **The failure it misses is the common one on this bench**: a rebuild at the same version
whose deploy silently did not land. `deploy-core` is already recorded elsewhere in this suite as
something that reports "landed" when nothing installed, which is exactly the case check 15 reads as
a match.

Decide, for `embarch-core` and only `embarch-core`:

1. **Should `/status` carry a content identity** — a hash of the running binary, a build fingerprint,
   a git SHA baked at compile time, or nothing — and if so, which? Weigh what each actually proves:
   a `git` SHA baked in at build time proves *what source was compiled*, which is not the same as
   *what bytes are running*, and a self-hash of the running executable is the only one that answers
   the second. Say which question is worth answering, not just which is easy.
2. **What it costs.** A self-hash means reading the executable's own file at startup or on request;
   on Windows that is the installed service binary. Say plainly whether that is acceptable and
   whether it is done once at start or per request.
3. **Whether the answer is "no".** It legitimately might be: this is a diagnostic for one consumer,
   the failure is already visible by other means, and adding a field to `/status` is a wire surface
   three consumers read. **Recording a considered "no" with the reasoning is a complete outcome** and
   is the cheaper one. What it must not stay is unanswered in another repo's `open.md`.

## Why now

Not urgent and not a defect — nothing is broken, a capability is missing. It is worth a unit because
it is a **decision parked in the wrong repo's `open.md`**: `embarch-umbrella` cannot make it,
correctly says so, and has said so since decision 34 landed. Nothing was ever filed here, so the
sentence *"`embarch-core`'s call"* has been true and unactioned the whole time. One unit ends it
either way.

## Done when

- [ ] Re-derived from `src/api.rs` (or wherever the status handler now lives) exactly what `/status`
      carries today, rather than trusting this task's summary of it.
- [ ] A numbered decision in `embarch-core/decisions/surfaces.md` (or the topic-correct file — **not
      `auth.md`**) recording either the field, its shape and what it proves, or the reasoned refusal
      and the trigger that would reverse it. This suite's posture is not to build machinery first, so
      a refusal with a named trigger is in keeping with it.
- [ ] If the answer is yes and it changes `/status`'s response shape, **that is a wire-schema bump
      and you do not land it** — the supervisor must announce it first (`ops.md` §4). Make the
      decision, file the implementation as a separate task, and say so in your report.
- [ ] `embarch-core/interfaces.md` (or `interfaces/*.md`) updated to match whatever `/status` is
      documented to carry, held to the same "one consistent account" bar `core/074` and `core/077`
      used.
- [ ] `embarch-core/open.md` gains the open question or loses nothing, as appropriate.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-core`; `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

- **Do not change `embarch-umbrella`** — not check 15, not `decisions/schema-skew.md`, not its
  `open.md`. Once this decision exists, the umbrella side can consume it on its own unit.
- **Do not implement the wire change** if you decide in favour. Decide, then file.
- **Do not touch `deploy-core` or anything under `scripts/`.**
