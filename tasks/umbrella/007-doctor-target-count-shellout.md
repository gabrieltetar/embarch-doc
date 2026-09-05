# 007 — Decision 17's amendment says check 8 stopped maintaining a second scanner; it never did

**State:** open
**Source:** embarch-umbrella/002 (design-only decisions audit, 2026-09-03) — decision 17's amendment read against the source and found unbuilt
**Scope:** umbrella
**Hardware:** none

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
