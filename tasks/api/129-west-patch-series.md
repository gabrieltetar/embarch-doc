# 129 — Round-trip a west manifest's Zephyr patch series through one scratch tree

**State:** open
**Source:** field use on a USB PD charger board, 2026-09-09 to 2026-10-20 — 32 scratch Zephyr worktrees (18 in one session), 8 hand-written regen, renumber and message scripts; about 20 manifest "Fix:" commits each split across 2–6 patch commits at curation; a 22→6 regroup by topic; patch regeneration 2.3 % of review-loop cost and 6 % in the manifest sessions
**Scope:** api
**Hardware:** none
**Owner:** no

## What

Add an `embarch-api patches` command family for a west manifest that carries module patches (`patches.yml` plus patch files applied by `west patch`). **`patches export`** creates, or reuses, one scratch checkout of the module at the manifest's base revision. It holds one commit per patch file in `patches.yml` order, with the message taken from the patch header. **`patches import`** writes the patch files back from that commit range: stable headers, author and date kept, each entry's sha256 in `patches.yml` updated, and a list of which files changed. A fix made as a commit on top of the series is split by the patch each hunk belongs to and folded into that patch's commit, so a "Fix: correct patches 0013 and 0015" commit never needs splitting by hand at curation. **`patches regroup --map`** merges and renumbers patches (by topic, or upstream versus local directories). It proves that the applied module tree is byte-identical before and after, and rewrites patch-number references in commit messages, listing any it cannot rewrite. One scratch tree serves a whole review loop instead of one per round.

## Why now

Every review round that touched the carried Zephyr stack paid this cost again in the field. Each round made a new scratch tree, regenerated the patches with a hand-written script, and added a "Fix:" commit that later had to be split across the patch commits it touched. The engineer then asked for fewer patches, grouped by topic, and that regroup and its proof of tree identity were done by hand. The suite is about to become a second user: `dev-bench-pd-bench-own-west-manifest` (a sibling draft) gives pd-bench its own `west patch` set.

## Done when

- [ ] On an unchanged 3-patch fixture series, an export/import round trip produces byte-identical patch files.
- [ ] `patches.yml` sha256 fields are updated, and applying the series to a clean base gives the expected tree.
- [ ] A fix commit touching two patches folds into both patch commits, and import rewrites both files.
- [ ] `regroup` proves tree identity, renumbers files and `patches.yml`, and reports the message references it rewrote or could not rewrite.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `spec.md`/`decisions.md`/`open.md` updated, `changelog.d/` fragment dropped.
