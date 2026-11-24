# 102 — The atlas design doc's head says what the doc is today

**State:** open
**Source:** the reviewer of `atlas/101` (supervisor log, 2026-11-23 15:04): "`embarch-atlas/design.md`'s head still calls the doc a placeholder awaiting resumed design work, which was stale before this unit"
**Scope:** atlas
**Hardware:** none
**Owner:** no

## What

The head of `embarch-doc/embarch-atlas/design.md` (its `**Status:**` line and
the paragraph after it) says the doc is a placeholder that "becomes the source
of truth once `embarch-atlas` design work resumes", that a landscape survey "is
being gathered" in `research/` (2026-09-22), and points at the roadmap's Later
bucket. The body below it is a working design with a dozen settled sections, and
atlas units land most days. When this is done, the head states what the doc is
now: which of it is the source of truth, what the repo's own `DESIGN.md` still
holds and whether "local, not yet published" is still true, whether `research/`
is still raw intake or has folded, and where the atlas sits in
`suite/roadmap.md` today. Check each claim against the repo and the roadmap
before writing it; keep what is still true.

If the roadmap or `embarch.md` is what is out of date rather than this doc, do
not edit them: drop a `status.d/` fragment naming the fact, and the supervisor
folds it.

## Why now

Filed by the supervisor from that reviewer's note, which the `atlas/101` leg
left as written. A reader opening the doc meets "placeholder" above sections
the atlas's code follows, which is the drift `DOC-PROTOCOL.md` §5 exists to
prevent.

**Doc headroom:** `embarch-atlas/design.md` is about 24,000 of its 25,600 B, so
the new head should be no longer than the old one.

## Done when

- [ ] The head of `embarch-atlas/design.md` says what the doc is today, with no
      claim the repo or the roadmap contradicts.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment dropped, `status.d/` fragment for anything
      suite-level it made false.
