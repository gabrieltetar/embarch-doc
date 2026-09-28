# 046 — Compact embarch-core/decisions/auth.md

**State:** done by agent/core/046-compact-core, 2026-09-28
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

- [x] `embarch-core/decisions/auth.md` back under reserve (under 90% of
      12288 B), same decision numbers still resolving.
- [x] `scripts/check-doc-size.py` clean.
- [x] Gate green.

## Closed 2026-09-28

Took the dispatch note's split. Decisions 42, 46 and 60 (the route sweep — three
mechanisms reading `build_router`'s own source) moved byte-identical into a new
`embarch-core/decisions/route-sweep.md`; 5, 6, 11 and 53 (auth, binding,
`core.toml`, the ACL) stay in `auth.md`. One sentence that topically belongs to
decision 53 (`**What this decision does not claim**...`) sat, in the old file,
*after* decision 60's block rather than after 53's own two paragraphs — an
existing misplacement, not something I introduced — and moved with 53 back to
its own paragraph in `auth.md`, verbatim, no wording changed.

`embarch-core/decisions.md`'s index row split into two rows. `platform.md`'s
one-line pointer to `auth.md` updated to name both files. `src/api.rs:1712`'s
comment named the old path (`` `embarch-doc/embarch-core/decisions/auth.md`
decision 42 ``) and was repointed to `route-sweep.md`; the two *bare* `decision
42`/`decision 46` code comments (api.rs:1795, 1896, no file named) were left as
is, per the dispatch note. `main.rs`'s "decision 46" references are
`embarch-study-designer`'s own decision 46, unrelated, not touched.

Byte counts: `auth.md` 11,356 B -> 3,799 B (30.9% of 12,288 B cap).
`route-sweep.md` (new) 8,468 B (68.9% of cap) — not in reserve. Confirmed via
`check-doc-size.py --pressure`: `auth.md`'s ledger item now reads PAID, closing
this task; the only other `core` file near reserve is `decisions/surfaces.md`
(94.2%, already filed and blocked under `tasks/core/091`, not touched here —
this task's own work did not push it there).

**DOC-COMPACTION-PASS.md's human question — "Can `spec.md` alone answer what
someone needs to work on this component today?"** — not applicable in the
usual sense: this was a verbatim split, not a spec.md rewrite, and `spec.md`
was untouched. Answered for the two split files instead: yes for each — a
reader who needs auth/binding/`core.toml` opens `auth.md` and gets only that;
a reader chasing the route-sweep family opens `route-sweep.md` and gets only
that, with `decisions.md`'s index row pointing at whichever mission the reader
is there for. Nothing was deleted, summarized or reworded to make this fit;
`DOC-COMPACTION-PASS.md` §"A split needs none of this" applies — no quoted-cut
list is owed because nothing was cut.

Gate: `check-docs.py` (11/11 green), `check-decision-refs.py` (3140 refs
resolve), `check-doc-size.py` (clean, no unfiled reserve), `check-ownership.py
--scope core` (doc worktree) and `--scope core --code-repo` (code worktree,
both OK), `check-client-names.py --repo <code worktree>` (clean against 8
denylist entries), `cargo build`/`test` (245 passed, 0 failed)/`clippy
--all-targets -- -D warnings` (clean) in the code repo.

Pushed: `embarch-doc` and `embarch-core`, both `agent/core/046-compact-core`.
