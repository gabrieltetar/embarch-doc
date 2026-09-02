#!/usr/bin/env python3
"""Flag suite-level status text that looks stale next to the doc it summarizes.

This automates half of DOC-PROTOCOL.md §4's pre-close staleness-check rule
("grep the suite-level docs... for a status word the step you're closing
just made false"). Two independent, heuristic checks:

  A. Project-level: for each row of embarch.md §3's table, classify its
     maturity tier from the row text and from the linked sub-project's
     spec.md "**Status:**" line, using the keyword tiers below (highest
     matching keyword anywhere in the text wins — these status blurbs are
     already written as prose summaries, not single status words, so this
     matches how they actually read). Flags any row whose tier disagrees
     with its spec.md.

  B. Feature-level: for each row of suite/features.md still carrying a
     stale-tier word (Todo/Proposed/Planned/design-only/Paused), greps that
     sub-project's spec.md for the feature's own backticked identifiers.
     spec.md is "what is true now", so a name appearing there while the
     inventory still says Todo is exactly the disagreement §4 asks about.

     Both halves read spec.md because both used to read design.md, and
     design.md stopped existing when each sub-project migrated to the
     four-file shape (DOC-COMPACTION.md §3). Half B additionally grepped a
     "## Changelog" section that no doc has any more, so it had been a
     silent no-op -- reporting "no disagreements found" while reading
     nothing at all. Anchor a check to a filename and it dies quietly when
     the filename moves.

Both are heuristics, not proof: a flagged row deserves a human read, not a
blind edit, and a clean run doesn't mean every doc agrees — it means these
two specific cross-checks found nothing. Deliberately NOT covered:
embarch-roadmap.md, whose per-milestone prose has no per-sub-project status
field to diff against; that one stays a manual §4 grep for now.

Exit status: 0 if nothing flagged, 1 otherwise.
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Ordered low -> high maturity. The highest tier with a keyword found anywhere
# in the text wins, not the first — see module docstring.
TIERS = [
    (1, ["planned", "paused", "no repo yet", "not started", "no code yet"]),
    (2, ["design-only", "design only", "proposed", "scoping in progress", "placeholder"]),
    (3, ["in progress", "partial", " wip", "scoped and"]),
    (4, ["shipped", "implement", " ship", "verified end-to-end", "closing out"]),
]
TIER_NAMES = {1: "Planned/Paused", 2: "Design-only/Proposed", 3: "In progress", 4: "Shipped/Implemented"}

STALE_FEATURE_WORDS = ["todo", "proposed", "planned", "design-only", "design only", "paused"]
SHIPPED_CHANGELOG_WORDS = ["implement", "shipped", "ships", "done", "closing out"]

# embarch.md §3's row names its sub-project either bare-backticked or as a
# markdown link to its spec, and carries either three or four cells. Both
# shapes have existed; matching only one is how half A silently died twice.
ROW_RE = re.compile(
    r'^\|\s*(?:\[)?`([\w-]+)`(?:\]\([^)]*\))?\s*\|(.*)\|(.*?)(?:\|(.*))?\|\s*$'
)
STATUS_LINE_RE = re.compile(r'\*\*Status:\*\*(.*?)(?:\n\n|\Z)', re.DOTALL)


def classify(text):
    text_l = text.lower()
    best = None
    for tier, keywords in TIERS:
        if any(kw in text_l for kw in keywords):
            best = tier
    return best


def read(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def check_project_level():
    """embarch.md §3 table vs. each sub-project's spec.md Status line."""
    findings = []
    embarch_md_path = os.path.join(REPO_ROOT, 'embarch.md')
    for line in read(embarch_md_path).splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        sub_project, _purpose, status_cell, doc_cell = m.groups()
        doc_cell = doc_cell or ''
        # The status line to diff against is the sub-project's own spec.md.
        # Fall back to a decisions.md or design.md the row happens to link,
        # for a sub-project that has not migrated to the four-file shape.
        spec_path = os.path.join(REPO_ROOT, sub_project, 'spec.md')
        if os.path.exists(spec_path):
            design_path, linked = spec_path, f'{sub_project}/spec.md'
        else:
            doc_match = re.search(
                r'\((%s/(?:decisions|design)\.md)\)' % re.escape(sub_project),
                doc_cell + _purpose)
            if not doc_match:
                continue  # e.g. embarch-doc's own row names no sub-project doc
            linked = doc_match.group(1)
            design_path = os.path.join(REPO_ROOT, linked)
        if not os.path.exists(design_path):
            continue
        design_status_m = STATUS_LINE_RE.search(read(design_path))
        if not design_status_m:
            continue
        row_tier = classify(status_cell)
        design_tier = classify(design_status_m.group(1))
        if row_tier is None or design_tier is None or row_tier == design_tier:
            continue
        findings.append(
            f"embarch.md §3 row for `{sub_project}` reads as "
            f"{TIER_NAMES[row_tier]}, but {linked}'s own Status "
            f"line reads as {TIER_NAMES[design_tier]}."
        )
    return findings


def check_feature_level():
    """suite/features.md rows vs. their sub-project's spec.md."""
    findings = []
    features_path = os.path.join(REPO_ROOT, 'suite', 'features.md')
    if not os.path.exists(features_path):
        return findings
    sub_project = None
    for line in read(features_path).splitlines():
        heading = re.match(r'^##\s+(embarch-[\w-]+)\s*$', line)
        if heading:
            sub_project = heading.group(1)
            continue
        if not sub_project or not line.startswith('| '):
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        feature_cell, status_cell = cells[0], cells[1]
        if not any(w in status_cell.lower() for w in STALE_FEATURE_WORDS):
            continue
        spec_path = os.path.join(REPO_ROOT, sub_project, 'spec.md')
        if not os.path.exists(spec_path):
            continue
        spec = read(spec_path)
        for name in re.findall(r'`([\w./{}-]{4,})`', feature_cell):
            if name in spec:
                findings.append(
                    f"suite/features.md row for `{name}` ({sub_project}) is still "
                    f"marked '{status_cell}', but {sub_project}/spec.md -- which is "
                    f"what is true now -- already names it."
                )
                break
    return findings


def main():
    findings = check_project_level() + check_feature_level()
    if findings:
        print(f"Found {len(findings)} possibly-stale status mention(s):\n")
        for f in findings:
            print(f"  - {f}")
        print("\nEach is a heuristic match, not certain drift — read the row and "
              "the linked doc, then either update the stale one or, if it's a "
              "false positive, leave it (this check isn't a formal proof).")
        return 1

    print("No project-level or feature-level status disagreements found.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
