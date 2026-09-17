# 115 — `interfaces/tools-discovery.md`'s `list_targets` row does not know `build_dir_name` exists

**State:** open
**Filed by:** leg 139, 2026-09-17, at `api/109`'s fold, from that unit's reviewer — which found this
and **deliberately declined to file it as a reviewer finding**, on the reasoning that it contradicts
no numbered decision and would not justify reverting either commit. That judgement was right and the
gap is still real, so it becomes an ordinary queue entry rather than disappearing with the review.
**Source:** `embarch-reviewer` on landed unit `api/109` (`embarch-api@87f67df`, `embarch-doc@fffc419a`).
**Scope:** api
**Hardware:** none. Settled by reading one interface doc against one tool's live description.
**Owner:** no

## What

`api/109` added `build_dir_name` to every `zephyr-west` row that `list_targets` returns, and
documented the field's real limit **in the tool's own runtime description** in `src/tools.rs` — the
text an MCP caller actually reads:

> is the identity for this row's own default build only, not every snippet/extra_args combination
> that row could be built with

So `embarch-api` decision 44's "surface text is what a caller reads" is satisfied at the surface
that matters most. **What was not touched is the doc repo's canonical interface reference.**
`embarch-api/interfaces/tools-discovery.md`'s `list_targets` row still describes the return as
*every file-backing-validated tuple plus `snippets_by_app`, `default_snippets`,
`default_extra_args`* — **it does not mention `build_dir_name` at all**, so a reader working from
the interface docs rather than from a live tool call cannot learn the field exists, let alone that
it is `null` when the configured default snippet is unavailable.

That is `DOC-PROTOCOL.md` §4's "shipped feature or changed interface" trigger, unfired.

## Why now

Cheap, and it is the half of the documentation that outlives the running process. It is also the
exact shape this suite keeps paying for: a change documented where it was made and not where it is
looked up. `api/109` itself exists because `embarch-umbrella/open.md` described `embarch-api`'s
surface wrongly for eleven days — **the reviewer's own point 1 was that decision 26's premise named
a "study listing" that has never existed** — and a stale interface row is how the next such bullet
gets written.

## Done when

- [ ] `embarch-api/interfaces/tools-discovery.md`'s `list_targets` row names `build_dir_name`, says
      what it is, and carries the same limit the tool description carries: **default combination
      only**, `null` when the configured default snippet is not among the app's available ones.
- [ ] While you are in there, check whether the same row's other fields still match what
      `list_targets` returns today — a row that was stale in one field is worth re-reading whole.
- [ ] `changelog.d/` fragment only if the wording change is reader-facing beyond the fix itself.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).

## Not yours

- **Do not change `list_targets`' behaviour or its shape.** Decision 77 settled both; this is a
  documentation-currency task and nothing about it should reach `src/`.
- **Do not touch `embarch-umbrella`.** `tasks/umbrella/082` carries that side.
