# 109 — Expose `build_dir_name` in the study listing, or record why `embarch-umbrella`'s `--prune` stays unbuildable

**State:** open
**Source:** refill sweep, leg 137, 2026-09-17, from
[`embarch-umbrella/open.md`](../../embarch-umbrella/open.md)'s standing bullet: *"Decision 26's
`--prune` is the last designed-and-unbuilt piece here, deferred by choice — it needs
`build_dir_name` in `embarch-api`'s listing. **Check 16 argues for it:** `study_results/` is 803 MiB
across 50 entries [measured 2026-09-06]; the sweep bounds the count, not the size."* That bullet has
named `embarch-api` as the blocking half for eleven days and **nothing has ever been filed against
this repo for it**, so the prerequisite has no owner and the deferral has no way to end.
**Scope:** api
**Hardware:** none. Settled by reading this crate's study-listing type and its Core client, plus the
`decisions/` tree. **Do not flash anything, do not run a live Core, and do not run a study** — the
question is what a listing carries, not an observation of one.
**Owner:** no

**Doc-size reserve for `api`, read at filing:** `embarch-api/spec.md` is **9,089/10,240 B (1,151 B
left)**, filed as `tasks/api/083` and blocked — plan around it. Every `embarch-api/decisions/*.md`
has room, but [`open.md`](../../embarch-api/open.md)'s own last bullet warns this corpus *"runs
narrow across `api`"*: several decision files sit a paragraph from the line and are invisible to
`check-doc-size.py` until they cross. **The right file for a new entry is the one whose topic it is,
not whichever has room** — that is the exact mistake leg 015 made with 96 bytes to spare.

## What

`embarch-umbrella` decision 26 designed a `--prune` for `study_results/` and did not build it,
because pruning safely needs to know **which build directory a study result belongs to**, and
`embarch-api`'s study listing does not carry that. The field the umbrella side names is
`build_dir_name`.

Answer, from this crate's side only:

1. **Does this crate's study listing actually lack it today?** Re-derive it — read the listing type
   and the Core response it is built from rather than trusting this task's summary. It is possible
   the field exists under another name, or that the information is recoverable from what is already
   listed, in which case the umbrella bullet is wrong and the correct output of this task is saying
   so and correcting it.
2. **If it genuinely is missing:** is adding it this crate's call alone, or does it need
   `embarch-core` to serve something it does not serve today? If Core already has it, adding it here
   is a small additive change. **If Core does not, this is a wire change and you do not make it** —
   name it and drop the `embarch-core` half in `/home/gabriel/Github/embarch/embarch-doc/inbox/` in
   full task format, absolute path.
3. **Either way, record the answer as a numbered decision** in the topic-appropriate
   `embarch-api/decisions/*.md`, so the next person reading the umbrella bullet finds a resolved
   dependency rather than a second dead end. **"This stays deferred, and here is the cost" is a
   first-class outcome** — the 803 MiB number argues for the feature, but nobody has argued that
   `--prune` is worth its own failure modes, and that argument is not yours to win by default.

## Why now

Not urgent, and it is not a defect: `--prune` is deferred deliberately and the existing sweep still
bounds the entry *count*. What makes it worth a unit is that the deferral is **parked on a
prerequisite in a repo that has never been told about it**. That is the shape that sits forever —
each side reading the other as the blocker — and it costs one unit to end, in either direction.

`embarch-api`'s queue is also the thinnest in the suite: `tasks/api/108` is the only other open task
and **cannot be closed by anything in this environment** (it needs a Windows machine to execute a
process-tree kill), so `api` has had no closeable work for several legs.

## Done when

- [ ] Re-derived from source whether the study listing carries a build-directory identity today, and
      the umbrella bullet's claim confirmed or corrected in writing.
- [ ] Either the field is exposed (additive, with a test), or a numbered decision in the right
      `embarch-api/decisions/*.md` records why it is not and what would change that.
- [ ] If the answer needs `embarch-core` to serve something new, that half is dropped in `inbox/` in
      full task format and **not implemented here**.
- [ ] `embarch-api/open.md` gains or loses a bullet to match, and the `embarch-umbrella/open.md`
      bullet's claim about this repo is either confirmed or filed for correction — **do not edit
      `embarch-umbrella/open.md` yourself**, it is another sub-project's doc.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-api`; `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

- **Do not change `embarch-umbrella`** — not its code, not its docs, not `decisions/schema-skew.md`,
  not its `open.md`. Its `--prune` is its own to build once this half is answered.
- **Do not build `--prune`.**
- **Do not implement a wire change to `embarch-core`.** File it.
