# 046 — Compact embarch-core/decisions/auth.md

**State:** claimed by agent/core/046-compact-core, 2026-09-28 17:31
**Size debt due:** 2026-09-26 (two weeks out; re-check `api.rs`'s auth-sweep
churn rate then and either compact or extend).
**Source:** `scripts/check-doc-size.py`, run by task `core/045` (2026-09-12):
`embarch-core/decisions/auth.md` at 11356/12288 B (92.4%, 932 B left), no debt
filed.
**Scope:** core
**Hardware:** none
**Owner:** no

## What

**Compacts:** `embarch-core/decisions/auth.md`

Shorten `decisions/auth.md` (`DOC-COMPACTION.md`/`DOC-COMPACTION-PASS.md`)
without deleting a decision number or a distinct finding. The file crossed
90% of its reserve when decision 60 (the route-wiring cross-check, the other
half of decision 42's sweep) landed.

**In flux:** no — unparked at claim, 2026-09-28, two days past its clock, on the re-check this
task's own due line asks for. The prediction was that the next new HTTP route would land here, and
four have landed in `build_router` since (`.../load/spans` `4251af3`, `GET /studies` `d73a73a`,
`DELETE /probes/enrolled/{role}` `e50de6d`, `PUT /probes/enrolled/{role}/board` `f832043`) with **none**
touching this file, which is unchanged since `f6e23215` (2026-09-12). The old answer, kept as
history: *yes — decisions 42 and 46 both concern `build_router`'s own route-registration scan, and
decision 60 is a third mechanism reading the same source text a different way; the next new HTTP
route or the next gap found in this sweep family is likely to land here again rather than somewhere
quieter.*

**Must not delete:** decision 42's derivation rationale and its "residual is
one-sided" scan limitation; decision 46's cross-repo `include_str!` failure
mode and why `DOCUMENTED_ROUTE_COUNT` is a pinned literal instead; decision
53's directory-vs-file ACL distinction and the instruction not to narrow the
directory; decision 60's mutation-verification result and its stated "not
covered" limits (a route the scan's text pattern misses; a handler whose own
`// route:` comment is simply wrong).

## Why now

`check-doc-size.py` names this file with no filed debt; per protocol §5 item
5, that failure must be filed rather than left silent.

## Dispatch note (supervisor, 2026-09-28)

**Prefer a verbatim split; there is a seam.** The file carries two missions under one heading:
**5, 6, 11, 53** are auth, binding and configuration (the token, the bind address, `core.toml`,
the `%ProgramData%` ACL), and **42, 46, 60** are the route sweep — three mechanisms reading
`build_router`'s source to keep the routes, the auth coverage and `interfaces.md`'s count in step.
`decisions.md`'s row already calls the file "Auth, binding, and surface consistency". Moving 42, 46
and 60 byte-identical into a new `decisions/route-sweep.md` (or the seam you find better, said why)
restates nothing; every `Must not delete:` item above survives by construction. Check inbound
links to all seven numbers across the suite before cutting (`grep -rn` over `embarch-doc` and the
code repo — `api.rs`'s comments cite 42/46/60) and repoint any that name the file rather than a
bare number; a link in another sub-project's directory you cannot write goes in an `inbox/` drop
at `/home/gabriel/Github/embarch/embarch-doc/inbox/` (absolute path), and the supervisor repoints
it at the fold.

**Also in reserve in `core`, not yours to write:** `decisions/surfaces.md` 709 B left
(`tasks/core/091`, blocked). If your work pushes any other `core` file into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit.

## Done when

- [ ] `embarch-core/decisions/auth.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving.
- [ ] `scripts/check-doc-size.py` clean.
- [ ] Gate green.
