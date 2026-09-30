# 077 — Restore "served by the binary" in spec.md's dev-bench-picker invariant

**State:** claimed by agent/ui/077-served-by-the-binary, 2026-09-29 22:14

Drained from `inbox/ui-075-dropped-served-by-binary.md` at step 0 of the leg after the recovery
leg, 2026-09-29. Body unchanged apart from this line and the number.
**Source:** embarch-reviewer, unit ui/075 (merge SHA embarch-doc 1fe6295b)
**Scope:** ui
**Hardware:** none — one phrase in `embarch-ui/spec.md`; re-checked at the drain.
**Owner:** no

## What

`embarch-ui/spec.md`'s invariants list, in the "role is a fixed slot" paragraph,
read before ui/075:

> "...the dev-bench picker is the suite's own supported pair, served by the binary."

After the squeeze:

> "...the dev-bench picker is the suite's own supported pair."

`served by the binary` was dropped, and it is not in the commit message's quoted
list of five squeezed hunks (`git show 1fe6295b`), so it was not accounted for
under `DOC-COMPACTION-PASS.md`'s quoting rule.

The phrase is load-bearing. `embarch-ui/decisions/topology-roles.md` states, of
the same picker: "the two board types `embarch-dev-bench`'s firmware supports,
**served from the binary like every other vocabulary**." That is the
vocabulary-is-served invariant the surrounding spec.md paragraph exists to state.

## Size

Restoring the phrase verbatim puts `embarch-ui/spec.md` about 13 B into its size
reserve (9031 B at the drain). Prefer a wording that restores the claim without
entering the reserve — e.g. trimming an equal number of bytes elsewhere in the
same paragraph without dropping another named claim, and quoting every hunk in
the commit message. If it does enter the reserve, file
`tasks/ui/<NNN>-compact-ui.md` in the same commit per `tasks/README.md`.
`embarch-ui/open.md` is already in reserve (253 B left, parked under
`tasks/ui/074`) — do not write to it.

## Done when

- [ ] `embarch-ui/spec.md`'s dev-bench-picker sentence restores "served by the
      binary" (or an equivalent phrase tying it to topology-roles.md's "served
      from the binary like every other vocabulary").
- [ ] Every hunk quoted in the commit message.
- [ ] `python3 scripts/check-docs.py` green.
