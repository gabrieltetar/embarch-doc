# 007 — Decision 17's amendment says check 8 stopped maintaining a second scanner; it never did

**State:** open
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 17's amendment read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none

**Compacts:** embarch-umbrella/spec.md, embarch-umbrella/open.md
**In flux:** yes — by this task, which is the point: `tasks/umbrella/009-compact-docs.md` is `blocked` on exactly
that, and a blocked compaction task parks the pass, not the reserve (`DOC-COMPACTION.md`
§2). You are the unit that rewrites a row of `spec.md`'s doctor table, so **compact both as part of this
commit**, honour `tasks/umbrella/009-compact-docs.md`'s `Must not delete:` list, and close only their item there.
**Headroom: `spec.md` 151 B of 10,240, `open.md` 69 B of 5,120.** Neither can absorb your
edit, and neither can be split — 10 KB and 5 KB are role caps on single files
(`DOC-COMPACTION.md` §2–3), so shortening is the only move here. `Must not delete:`, from
009: the doctor table's per-row **designed-and-unbuilt** distinction, which lives nowhere
else, and `open.md`'s note that check 15 is not a hash comparison. Refresh 009's counts if
you change the table's shape — a `Must not delete:` clause that protects a table *by a
count* is worse than useless once the count is stale.

## What

`embarch-umbrella` decision 17's amendment says the zephyr-west target-count
check "now shells out to `embarch-api`'s own listing instead of maintaining a
second scanner", on the argument that by the time check 8 runs there is no
bootstrapping problem — `init` has already run and a real config exists.

**Check 8 still calls this crate's own `zephyr::count_valid_targets`.** Its code
comment still records the deliberate approximation the amendment describes as
replaced: a revision counts as backed if *any* revision-suffixed file in the
board directory names it, which can overcount relative to `embarch-api`'s
per-tuple check. The crate's one mention of `list-targets` is a fix line telling
a human to run it.

Either build the shell-out, or retire the amendment paragraph and keep the
scanner with its overcount stated as intended behaviour. **Both are defensible**
— the amendment's own argument is sound, but the approximation only ever feeds a
pass/fail signal, and shelling out adds a subprocess to a check that currently
needs none.

## Why now

Everything else in decision 17 shipped and was verified as real cross-repo
interop, so this one paragraph is the only part of the entry that does not
describe the binary. The lightweight *shape* detection the amendment preserves is
genuinely still there, which is what makes the drift easy to miss.

## Done when

- [ ] Check 8's zephyr-west branch either shells out to `embarch-api`'s listing,
      or the amendment is retired per `DOC-CONVENTIONS.md` and the local scanner
      is documented as the intended answer.
- [ ] Decision 17's implementation note updated to match whichever was chosen.
- [ ] `status.d/` fragment for `suite/features.md`'s live-target-discovery row.
- [ ] Gate green; `changelog.d/` fragment dropped.
