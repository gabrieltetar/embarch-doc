# 022 — `crate.md`'s 2026-09-08 qualification names a mirror that was retired hours later

**State:** open
**Source:** `embarch-reviewer` on unit `umbrella/036`, 2026-09-08 (leg 051). Not a
contradiction introduced by that unit — a true sentence that its own landing made false.
**Scope:** topology
**Hardware:** none
**Owner:** no

## What

`embarch-topology/decisions/crate.md`'s **Qualified 2026-09-08** paragraphs — written by
`topology/020` one leg earlier — cite `embarch-umbrella/src/token.rs` as a **live** mirror of
the crate's own logic and name `tasks/umbrella/036` as the unit that would remove it. That was
accurate when written. `umbrella/036` landed the same evening (code `e1a5e7c`, doc `444f84d`):
`src/token.rs` is deleted and `embarch-umbrella` now calls
`embarch_core_client::token_discovery::resolve_token` directly.

So the qualification's *argument* is still exactly right — linking a shared crate stops a
mirrored copy of the crate's own logic, and cannot stop a caller writing an unrelated second
predicate beside a call it never makes — but the **example it hangs that argument on no longer
exists**, and the file reads as though a live mirror is sitting in `embarch-umbrella` today.

The other instance the qualification cites, `api/038`'s, is genuinely closed and already
described as such. After this unit there is **no known live mirror left**, which is itself the
fact worth writing down: the point of the qualification was never that a mirror exists, it was
that nothing can cheaply *detect the next one* — and `embarch-topology/open.md`'s bullet, also
from `topology/020`, already says that and stays true either way.

## Why now

This is the exact shape `embarch-decision-reversals.md` calls the worse variant of shape 1 —
a decisions file describing a state of the world that has moved — and it has the short half-life
that makes it cheap to fix now and expensive later: the next reader who goes looking for
`embarch-umbrella/src/token.rs` on the strength of this paragraph will not find it and will not
know whether the file moved, was renamed, or the claim was wrong.

## Done when

- [ ] `embarch-topology/decisions/crate.md`'s qualification no longer describes
      `embarch-umbrella/src/token.rs` as live; it names it as the second mirror **since closed**,
      with the date and the unit, and keeps the argument intact.
- [ ] The qualification still makes its point without a live example — the claim is about what
      cannot be detected, not about a count of open mirrors.
- [ ] `embarch-topology/open.md`'s detection bullet is re-read and either left alone or narrowed
      to match; it is expected to be left alone.
- [ ] Gate green; `changelog.d/` fragment only if a reader-visible fact changed.

**Do not** re-open the question `topology/020` settled, and do not turn this into a sweep for
other mirrors — `umbrella/036`'s own state note already names the config mirrors (`CoreConfig`,
`ProjectConfig`) that are still copies, and they are `umbrella`'s, not `topology`'s.

**Reserve note:** `embarch-topology/decisions/crate.md` is at 11,290/12,288 B (998 B left, in
reserve) and `open.md` at 4,841/5,120 B, both filed against `tasks/topology/021-compact-topology.md`
and `tasks/topology/014-compact-topology.md` respectively. This edit should be net-neutral or
smaller; if it is not, record the spend against those tasks rather than filing a new one.
