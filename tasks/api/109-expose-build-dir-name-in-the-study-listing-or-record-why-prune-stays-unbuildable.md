# 109 — Expose `build_dir_name` in the study listing, or record why `embarch-umbrella`'s `--prune` stays unbuildable

**State:** done — leg 139, 2026-09-17, branch `agent/api/109-build-dir-name`

**Resolution:** the umbrella bullet's framing was wrong on two counts, corrected in writing
(`embarch-api` decision 77, `decisions/target-json.md`, and the inbox drop below): the field
decision 26 actually names belongs to `list-targets` (the target menu), not a "study listing" —
this crate has no listing of multiple studies at all, and nothing in `StudyResult` or
`study_results/<study_id>/` (keyed by `study_id`) ever named a build directory. The 803 MiB
`study_results/` figure the bullet cited is a separate, already count-bounded gap (Core's
`sweep_study_results`), unrelated to `build_dir_name`. The real gap — `list-targets`'s JSON
carrying the tuple but not `build_dir_name` — was real and **entirely this crate's own call**: no
`embarch-core` wire change needed, since `build_dir_name` is `zephyr::Target::build_dir_name`,
computed locally. Shipped additively: every `zephyr-west` `list-targets` row now carries
`build_dir_name`, resolved against the project's configured `default_snippets`/`default_extra_args`
(the identity a bare `build` for that row writes to today), `null` when the app's available
snippets don't cover `default_snippets`. Three unit tests cover the default case, the null
fallback, and a real default-snippet fold. Known, documented residual: this names only the default
combination — a non-default snippet/`extra_args` build is exactly as current per decision 26 and
gets no name here, needing `target.json` (decision 69) instead; recorded as a Structural-limits
bullet in `open.md` so a future `--prune` design does not rediscover it.
`embarch-umbrella/open.md`'s stale bullet is filed for correction, not edited directly:
`/home/gabriel/Github/embarch/embarch-doc/inbox/umbrella-build-dir-name-shipped-in-api-list-targets.md`.
`embarch-api/open.md`'s new bullet pushed it into reserve; compaction debt filed as `tasks/api/112`.
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

## Dispatch note — leg 139, 2026-09-17

**Two `api` files are in reserve and neither is likely to be yours; the third-largest is the one to
watch.** Measured at dispatch, against a 12,288 B cap for `decisions/*.md` and 10,240 B for
`spec.md`:

- `embarch-api/decisions/failure-reporting.md` — **11,578 B, 710 B left** (`tasks/api/111`,
  blocked). Do not put a study-listing decision here; it is not the topic and there is no room.
- `embarch-api/spec.md` — **9,089 B, 1,151 B left** (`tasks/api/083`, blocked). A one-line spec
  amendment fits; a paragraph does not.
- `embarch-api/decisions/client-crate.md` — **10,947 B, 1,341 B left (89.1%)**, *not* in reserve and
  therefore **invisible to `check-doc-size.py`** — this is exactly the "a paragraph from the line"
  case `embarch-api/open.md`'s last bullet warns about. If your decision belongs here, it will very
  likely push the file into reserve, and then you file `tasks/api/<next free NNN>-compact-api.md` in
  the same commit per `tasks/README.md`.

**On current reading, `embarch-api/decisions/study-reads.md` (6,313 B) is the topic-appropriate home
for a decision about what the study listing carries, and it has ~6 KB of room.** That is a
suggestion, not an instruction: pick the file whose topic it is. If nothing fits the topic, say so
and propose a new file rather than filing it somewhere with room.

**Outcome 3 in `## What` is the one to take seriously.** "This stays deferred, and here is the cost"
is a complete unit — the 803 MiB figure argues for the feature but nobody has argued `--prune` is
worth its failure modes, and you are not obliged to win that argument by default. Equally, if
box 1's re-derivation shows the umbrella bullet is simply **wrong**, saying so in writing is the
best possible outcome of this unit and you should not manufacture a change to avoid it.

**Ownership is checked on both your branches.** `embarch-umbrella/**` and `embarch-core/**` are not
yours in any form. Drops go to `/home/gabriel/Github/embarch/embarch-doc/inbox/` by **absolute**
path — a relative one is written inside your worktree and is deleted with it.

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

- [x] Re-derived from source whether the study listing carries a build-directory identity today, and
      the umbrella bullet's claim confirmed or corrected in writing.
- [x] Either the field is exposed (additive, with a test), or a numbered decision in the right
      `embarch-api/decisions/*.md` records why it is not and what would change that.
- [x] If the answer needs `embarch-core` to serve something new, that half is dropped in `inbox/` in
      full task format and **not implemented here**. (Not needed: closed entirely within this crate.)
- [x] `embarch-api/open.md` gains or loses a bullet to match, and the `embarch-umbrella/open.md`
      bullet's claim about this repo is either confirmed or filed for correction — **do not edit
      `embarch-umbrella/open.md` yourself**, it is another sub-project's doc.
- [x] A `changelog.d/` fragment.
- [x] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D
      warnings` in `embarch-api`; `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

- **Do not change `embarch-umbrella`** — not its code, not its docs, not `decisions/schema-skew.md`,
  not its `open.md`. Its `--prune` is its own to build once this half is answered.
- **Do not build `--prune`.**
- **Do not implement a wire change to `embarch-core`.** File it.
