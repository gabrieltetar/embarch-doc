# 018 — check 17's fix line can green its own check, and its `bind-too-narrow` evidence cannot discriminate

**State:** open
**Source:** `umbrella/017`'s reviewer, 2026-09-06, reviewing merge `80f4cb8` / `cbe8a5d`.
Reported as observations rather than contradictions — decision 22(a) was rewritten in the same
diff — and filed here by the supervisor, who merged 017 knowing about both.
**Scope:** umbrella
**Hardware:** none to fix; the underlying verification debt stays hardware-owed either way
**Owner:** no

## What

`doctor` check 17 (bind address versus topology) shipped in `umbrella/017` with two Fail arms
on different evidence. **The `bound-narrow` arm is sound. The `bind-too-narrow` arm has two
defects, and they compound.**

**1. Its fix line can silence the check instead of fixing anything.** The fix offers *"or
re-run `embarch setup`, which passes it for you."* But `bind-too-narrow` fires **only when a
candidate answered** — and that is precisely the condition `setup.rs:80` treats as
`already_running`, so `setup.rs:260` prints *"embarch-core is already running — nothing to
install"* and never touches the bind. Worse: `setup.rs:343` then writes
`topology: Some(plan.class.as_str())` **unconditionally**, and on that path `plan.class` is the
*winner's* class — `local`. So a user who follows the second half of the fix rewrites the
recorded class, after which **check 17 reports Pass `bind-matches` having changed nothing.**

A fix that makes a check green without fixing the condition is worse than no fix, and this one
also destroys the single piece of independent evidence the check was built around (the class
`setup` recorded). The same string is used for `bound-narrow`, **where it is correct** —
nothing answered there, so `setup` really does install.

**2. Its evidence does not discriminate, and `open.md`'s plan for retiring its debt cannot
retire it.** `candidates()` (`embarch-topology/src/software.rs:122`) always pushes
`Local @ 127.0.0.1` first and `resolve` stops at the first responder — so **a Core bound
`0.0.0.0` on the same machine wins at loopback exactly as one bound `127.0.0.1` does.**
`embarch-umbrella/open.md`'s new bullet says settling the debt means a `doctor` run from the
Windows side "which still reaches loopback"; that arm emits `bind-too-narrow` **either way**,
so running it proves nothing. The detail string's word "only" — *"reached at {url} … only"* —
is unearned for the same reason: the probe never tried the others.

## What to do, and the shape of the choice

**Do not simply delete `bind-too-narrow`.** It is the arm that catches a genuinely reachable
Core whose recorded class disagrees, which is a real state. Three shapes, and one of them has
to be argued for in the decision entry:

- **Give it evidence.** Read the service registration on this arm too, the way `bound-narrow`
  does, and fail only when the registration *and* the recorded class disagree. Costs a second
  `sc.exe` call on a path that already succeeded.
- **Demote it to a warn** and say plainly that a reachable Core is not evidence of a narrow
  bind. Cheapest, and honest; the cost is that the one state it uniquely catches stops failing.
- **Probe the other candidates before concluding.** Most faithful to what the detail string
  already claims, most expensive, and it changes `embarch-topology`'s resolve contract — which
  is **another sub-project and therefore not yours**. If this is the right answer, say so and
  stop; do not reach into `embarch-topology`.

**The fix line is separable and must be fixed whichever shape wins**: `bind-too-narrow` should
not offer `embarch setup` at all, or must say it only helps when nothing is running.

**And correct `open.md`'s verification plan in the same pass** — as written it describes an
experiment whose outcome is fixed in advance. Only the `bound-narrow` half of that debt is
settled by the session it describes.

## Why now

Check 17 is live and its fix text is what an operator reads at the moment they are stuck. The
`setup`-rewrites-the-recorded-class path is the sharper half: it is silent, it looks like the
problem was solved, and it destroys the evidence that would show otherwise.

## Reserve

`embarch-umbrella/open.md` is **in reserve at 4,840 / 5,120 B — 94.5%, 280 B left**, filed
against `tasks/umbrella/009-compact-docs.md` (`blocked`, `In flux: yes`). You are editing that
file, so under [DOC-COMPACTION.md](../../DOC-COMPACTION.md) §2 **the ride-along is yours**:
bring it below 90% in your own commit and tick `009`'s `open.md` item, carrying `009`'s
`Must not delete:` list. `009` also records **eighteen rows / one unbuilt decision** for
`spec.md`'s doctor table — refresh that if you change it. `embarch-umbrella/spec.md` is at
8,966 B (87.6%) with room.

## Done when

- [ ] `bind-too-narrow` either has evidence that discriminates, or is a warn that does not
      claim more than it saw — with the two rejected shapes argued against in the decision
      entry, not merely listed.
- [ ] Its fix line can no longer green the check without changing anything, and the detail
      string does not say "only" about candidates never tried.
- [ ] `embarch-umbrella/open.md`'s check-17 verification plan describes an experiment that can
      fail, and says which half of the debt each arm settles.
- [ ] `embarch-umbrella/open.md` is out of reserve and `tasks/umbrella/009` is updated.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/umbrella-*` fragment
      dropped.
