# 062 — "decisions 34/36/54/55 were each opened by" is still imprecise after `ui/061` fixed one member

**State:** open
**Source:** `ui/061`'s reviewer, 2026-09-16. `ui/061` corrected one wrong member of a four-member
citation (53 → 55); the reviewer then checked the other three and found the claim still does not
hold for all of them. Filed by the supervisor at that unit's fold. The reviewer deliberately did
**not** file it, on the grounds that the imprecision predates `ui/061`'s diff and its own
compaction-residue check is bounded to the diff under review — which is right for a reviewer and is
not a reason for the queue to lose it.
**Scope:** ui
**Hardware:** none — one sentence, written identically at two sites in one Rust source file.
Nothing is built for a board, the UI is not launched, no probe, no live Core.
**Owner:** no

## What

`embarch-ui/src/study_designer.rs` says, at **~line 536** (in `build_taps`) and again at **~line
2371** (in `a_gatt_tap_nothing_subscribes_to_is_refused_at_authoring_time`):

> "A tap whose characteristic no step subscribes captures nothing, passes, and looks fine — which is
> the exact failure `embarch-study-designer` decisions 34/36/54/55 were each opened by."

**"Each opened by" is a strong claim and only decision 55 makes it literally.** Decision 55's own
closing paragraph is near-verbatim the source of that sentence. Of the other three, read at
`embarch-study-designer/decisions/`:

- **34** (`authoring.md`) — a real monitor-everything run came back empty because nothing was
  *written*, not because no step subscribed.
- **36** (`gatt.md`) — a timing/ordering gap: a capture window that did not outlive its own step.
- **54** (`removed.md`) — a capped in-memory field, and it names the broader *"nothing captured, no
  error"* family these all belong to.

So the three are genuine members of the family decision 54 names, and none of them was opened by
*this* mechanism. Either narrow the sentence to 55 and cite 54 as the family, or reword it so it
claims family membership rather than an identical origin. Both sites say it identically and must
keep saying it identically.

## The history worth reading before deciding

The reviewer traced this, and it changes what "fix" means. Decision 54's **original** text
(`embarch-study-designer/decisions/removed.md`, commits `d0b7608` / `04b63cf` / `ed899d8`)
explicitly enumerated the four as *"decisions 34, 36, 53, and this one"* — the sub-project once
locked in **53**, which `ui/061` has just established is the wrong member, since 53 is about link
flooding and shares no wording with this failure. A compaction at **`7affd84`** dropped that
enumeration, and the current decision 54 names no members at all.

**Do not restore the old enumeration.** It was an authoring error; `ui/061`'s 53 → 55 correction is
right and reverting toward 53 would reintroduce a wrong reference. What the history tells you is
that the *sentence in `embarch-ui`* has been carrying a list nobody has re-derived since decision 54
stopped stating one — which is why this is worth a unit rather than a shrug.

## Why now

This chain's standing doubt, recorded across several supervisor-log entries, is whether its
zero-defect sweeps mean the corpus is clean or the census is blind. This is a third shape of answer:
a citation whose numbers all resolve, whose sentence reads fluently, and which is still wrong about
the relationship it asserts between them. No grep pattern finds that, and `ui/061` did not either —
its reviewer did, and only because it was asked to test all four members rather than the one under
repair.

## Done when

- [ ] Both sites say something true about the relationship between that failure and the decisions
      they cite, and say it identically.
- [ ] Whatever is decided is checked against decision 54's current text, since it is the one that
      names the family.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10) — `cargo build --all-targets`, `cargo test`,
      `cargo clippy --all-targets -- -D warnings` in `embarch-ui`, and `check-docs.py` in
      `embarch-doc`.
- [ ] `changelog.d/` fragment dropped. No `embarch-study-designer` doc is touched — that repo is not
      this task's scope, and decision 54 is not wrong, only silent about its members.
