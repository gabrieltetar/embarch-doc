# 060 — `check-decision-refs.py` cannot see a `suite` decision's definition, so 877 references go unchecked

**State:** open
**Source:** `outpost/022`'s worker, 2026-09-14, which hit it while writing its own report and
**deliberately did not file it** — it judged a formatting quirk with no observed false negative not
worth a drop. Leg 114 verified the mechanism and disagrees about the size, so it is filed here rather
than left in a report nobody greps. Confirmed on `main` at the time of filing.
**Scope:** doc
**Hardware:** none — a regex in a gate script.
**Owner:** required — `scripts/check-decision-refs.py` is reserved by `../../embarch-fleet/protocol.md`
§2. No agent may write it.

## What

`scripts/check-decision-refs.py:78`:

```python
DEF_HEAD = re.compile(r'^#{3,4}\s+(\d+(?:\s*,\s*\d+)*)\s+[-—]\s')
```

It matches a decision **definition** heading at `###` or `####` only. Every sub-project's
`decisions/*.md` uses `###`, so this is right everywhere except one place: **`suite/decisions/*.md`
uses `##`.** Four `suite` decisions are defined that way today — `naming.md` (1), `placement.md` (1),
`tooling.md` (2) — and the resolver cannot see any of them as definitions.

The effect is not a failure. `python3 scripts/check-decision-refs.py` reports:

```
All 1995 decision references resolve. 877 ambiguous (--warnings to list), not an error.
```

**877 of 1,995 is 44% of the corpus**, and "ambiguous" is the bucket a reference lands in when the
script cannot decide which repo's decision N it means. A reference that unambiguously names a `suite`
decision — prose citing `suite/decisions.md` and `suite/decisions/tooling.md` near a bare
`decision 2` — cannot be resolved to the definition it names, because no definition was ever indexed
for it. So it is not checked at all, and nothing says so.

## Why it matters more than it looks

The suite's whole citation-sweep programme (`core/049`, `ui/040`, `dev-bench/020`, `outpost/021`,
`outpost/022`, `study-designer/048`, `api/095`, and the ~236 unswept hits behind
`tasks/dev-bench/021`–`026`) exists because **a wrong decision number that happens to resolve fails
no gate.** This is the same defect one level up: a *right* number that cannot resolve at all also
fails no gate, and the two are indistinguishable from the summary line. A `suite` decision is the
most cross-cutting kind there is — it is cited from every repo — so it is the worst class to have
outside the resolver's sight.

## Watch for

- **The fix may not be the regex.** Widening `DEF_HEAD` to `#{2,4}` is one line, but `##` is also the
  section-heading level in ordinary docs, so a looser pattern may start matching prose headings that
  merely begin with a number. The alternative is to make `suite/decisions/*.md` use `###` like every
  other topic file — a doc change, not a script change, and `DOC-CONVENTIONS.md` is the place that
  would have to say so.
- `tasks/doc/044` (a verbatim split is the one move `check-decision-refs.py` cannot see) and
  `tasks/doc/056` (a cross-repo decision link whose text is the repo name is invisible to both
  resolvers) are the two neighbouring gaps in the same script. Whoever takes this should read all
  three together — they may share a fix.

## Done when

- [ ] A reference that names a `suite` decision resolves to its definition, or the reason it cannot
      is written down where the next sweeper will find it.
- [ ] The `ambiguous` count is either brought down or explained — 877 unchecked references reported
      as "not an error" is the part that hides the problem.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
