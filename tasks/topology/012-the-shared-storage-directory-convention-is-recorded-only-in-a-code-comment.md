# 012 — The shared machine-wide storage directory is a real convention with `embarch-core`, recorded nowhere but a code comment

**State:** claimed
**Source:** `embarch-reviewer` on `tasks/topology/005`, leg 033, 2026-09-07 — found while checking a
citation the supervisor had *already* corrected once, and correctly said the second citation was no
better than the first
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology` stores enrollment under `/var/lib/embarch/topology` on Linux/macOS and
`%ProgramData%\embarch\topology` on Windows — **the same machine-wide, admin-owned directory
`embarch-core`'s token file already uses, deliberately and for a stated reason.** That is a
cross-repo convention: two crates agreeing on a location, one of them a Windows service running as
a different user than the CLI that reads it.

**Nothing in any doc records it.** The reviewer searched every `embarch-topology` decision file and
`spec.md` for the directory, `ProgramData`, and the token-file continuity together and found
nothing. `spec.md`'s *Storage and roles* is about role uniqueness and `guessed_among`; the one
sentence that comes close — *"Storage is one file under a machine-wide directory this crate owns"* —
sits in the unheaded tail of *The declared facts*, and does not mention `embarch-core` at all.

**The convention lives in `src/hardware/paths.rs`'s own comment and nowhere else.**

## Why now

`topology/005` walked into this twice in one unit. The worker rewrote `README.md`'s citation from
the deleted `design.md §5's storage-location decision` to `decision 3's continuity with that same
directory` — and decision 3 is *"live, in-process, on every call — no write-ahead file"*, which
says nothing about a directory. The supervisor caught that and repointed it at `spec.md`'s *Storage
and roles* — **which does not settle it either**, and the reviewer caught *that*. Two actors, both
looking, both reached for the nearest plausible pointer rather than concluding the fact is
undocumented. **A fact with no home attracts wrong citations**, and it will keep attracting them:
`README.md` now says in as many words that there is no citation because there is nothing to cite,
which is honest and is not a fix.

The stakes are not cosmetic. The directory choice is what makes an admin-owned Windows service and
an unprivileged CLI see the same enrollment, and `embarch-topology decision 21`'s whole safety
property assumes the store is where it is. A convention nobody wrote down is one a later change can
break without contradicting anything.

## Done when

- [ ] The shared-directory convention is a numbered `embarch-topology` decision, or a named section
      of `spec.md` — **whichever the unit argues for**, and it says why in `decisions.md`.
- [ ] It states the actual paths, that `embarch-core`'s token file uses the same location, and
      **why** (machine-wide and admin-owned, so a service and a CLI agree).
- [ ] `src/hardware/paths.rs`'s comment cites it by bare decision number instead of being the
      record.
- [ ] `README.md`'s "no decision or spec section records that convention" sentence is replaced by
      the citation it says does not exist.
- [ ] Check whether `embarch-core`'s own docs state the other half; if they do not, that is
      **`embarch-core`'s task, not yours** — file it in `inbox/`, do not reach across.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment only if something
      user-visible changed, and say which and why.
