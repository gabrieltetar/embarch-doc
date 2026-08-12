#!/usr/bin/env python3
"""Flag suite-level status text that looks stale next to the doc it summarizes.

This automates half of DOC-PROTOCOL.md §4's pre-close staleness-check rule
("grep the suite-level docs... for a status word the step you're closing
just made false"). Two independent, heuristic checks:

  A. Project-level: for each row of embarch.md §3's table, classify its
     maturity tier from the row text and from the linked sub-project's
     design.md "**Status:**" line, using the keyword tiers below (highest
     matching keyword anywhere in the text wins — these status blurbs are
     already written as prose summaries, not single status words, so this
     matches how they actually read). Flags any row whose tier disagrees
     with its design.md.

  B. Feature-level: for each row of embarch-features.md still carrying a
     stale-tier word (Todo/Proposed/Planned/design-only/Paused), greps that
     row's sub-project's design.md Changelog for the feature's own
     backticked name next to shipped-language. Flags any row whose own
     sub-project's changelog already says that feature shipped.

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

ROW_RE = re.compile(r'^\|\s*`([\w-]+)`\s*\|(.*)\|(.*)\|(.*)\|\s*$')
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
    """embarch.md §3 table vs. each sub-project's design.md Status line."""
    findings = []
    embarch_md_path = os.path.join(REPO_ROOT, 'embarch.md')
    for line in read(embarch_md_path).splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        sub_project, _purpose, status_cell, doc_cell = m.groups()
        design_match = re.search(r'\((%s/design\.md)\)' % re.escape(sub_project), doc_cell)
        if not design_match:
            continue  # e.g. embarch-doc's own row links to DOC-PROTOCOL.md, not a design.md
        design_path = os.path.join(REPO_ROOT, design_match.group(1))
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
            f"{TIER_NAMES[row_tier]}, but {sub_project}/design.md's own Status "
            f"line reads as {TIER_NAMES[design_tier]}."
        )
    return findings


def check_feature_level():
    """embarch-features.md rows vs. their sub-project's design.md changelog."""
    findings = []
    features_path = os.path.join(REPO_ROOT, 'embarch-features.md')
    for line in read(features_path).splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        feature_cell, sub_project_cell, status_cell, _notes = m.groups()
        status_l = status_cell.lower()
        if not any(w in status_l for w in STALE_FEATURE_WORDS):
            continue
        sub_project = sub_project_cell.strip().strip('`').split('/')[0].strip()
        design_path = os.path.join(REPO_ROOT, sub_project, 'design.md')
        if not os.path.exists(design_path):
            continue
        feature_names = re.findall(r'`([\w./-]+)`', feature_cell)
        if not feature_names:
            continue
        content = read(design_path)
        changelog_m = re.search(r'^## .*Changelog.*$', content, re.MULTILINE)
        changelog_text = content[changelog_m.start():] if changelog_m else content
        for name in feature_names:
            escaped = re.escape(name)
            for shipped_word in SHIPPED_CHANGELOG_WORDS:
                pattern = re.compile(
                    rf'`{escaped}`[^\n]{{0,80}}{shipped_word}|{shipped_word}[^\n]{{0,80}}`{escaped}`',
                    re.IGNORECASE,
                )
                if pattern.search(changelog_text):
                    findings.append(
                        f"embarch-features.md row for `{name}` ({sub_project}) is still "
                        f"marked '{status_cell.strip()}', but {sub_project}/design.md's "
                        f"changelog already reads as shipped (matched near \"{shipped_word.strip()}\")."
                    )
                    break
            else:
                continue
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
