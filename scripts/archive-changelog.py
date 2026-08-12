#!/usr/bin/env python3
"""Move old Changelog entries out of a doc's body into a sibling archive file.

DOC-PROTOCOL.md §5 treats a doc's numbered sections as "a living description
of current reality, not an append-only log" — but the `## Changelog` section
at the bottom of every doc *is* meant to be append-only, and left alone it
grows without bound (embarch.md §7 is past 20 dated entries as of writing).
This keeps the live section short while losing no history.

For every Markdown file with a `## ... Changelog` heading, keeps the
KEEP_MIN_ENTRIES most recent dated bullets (ranked by their own YYYY-MM-DD,
not by position) and moves the rest into `<name-without-ext>.changelog-archive.md`
next to the source file, each preserving the original doc's own relative
ordering — prepending each run's newly-archived batch above whatever an
earlier run already archived.

Ranking by date rather than position is deliberate: docs in this repo don't
agree on a direction — embarch.md prepends new entries at the top, but
embarch-core/design.md appends them at the bottom — so a position-based
top-N cut would silently archive the *newest* entries on a doc using the
latter convention. (A pure age-based cutoff was tried and dropped too — on a
doc this young, any window generous enough to be safe kept everything; a
fixed entry count doesn't have that problem.) Entries are matched as
`^- YYYY-MM-DD — ...` blocks (a dated top-level bullet plus any indented
continuation lines that follow it, e.g. sub-bullets).

Idempotent: re-running with nothing new to archive changes nothing. Intended
to run unattended (see .github/workflows/changelog-archive.yml, which runs
this weekly and opens a PR rather than pushing straight to main) — this script
itself never pushes or commits anything, only rewrites files on disk.

Usage: scripts/archive-changelog.py [--dry-run]
Exit status: 0 always (informational) unless it hits an actual I/O error;
--dry-run reports what would move without writing anything.
"""
import os
import re
import sys
from datetime import date

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KEEP_MIN_ENTRIES = 8

HEADING_RE = re.compile(r'^(#{1,6})\s+(?:\d+\.\s*)?Changelog\s*$', re.MULTILINE)
ENTRY_START_RE = re.compile(r'^- (\d{4}-\d{2}-\d{2}) [—-] ', re.MULTILINE)
ARCHIVE_NOTE_RE = re.compile(r'\n?\*Older entries.*?changelog-archive\.md\).*?\*\n', re.DOTALL)

ARCHIVE_HEADER_TEMPLATE = """# {basename}: changelog archive

Entries beyond the {keep_min} most recent, moved here from [{basename}]({basename})
by `scripts/archive-changelog.py`, per `DOC-PROTOCOL.md` §5. Newest-first,
same as the live doc's own Changelog.
"""


def find_md_files(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != '.git']
        for name in filenames:
            if name.endswith('.md') and not name.endswith('.changelog-archive.md'):
                yield os.path.join(dirpath, name)


def split_entries(section_body):
    """Return list of (date, entry_text) for each dated top-level bullet, in order found."""
    starts = [(m.start(), m.group(1)) for m in ENTRY_START_RE.finditer(section_body)]
    entries = []
    for i, (pos, date_str) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(section_body)
        entries.append((date_str, section_body[pos:end].rstrip('\n')))
    return entries


def process_file(path, dry_run):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    heading_m = HEADING_RE.search(content)
    if not heading_m:
        return None
    level = heading_m.group(1)
    section_start = heading_m.end()
    # Find the next heading of the same or higher level (fewer-or-equal '#'), or EOF.
    next_heading_re = re.compile(r'^#{1,%d}\s' % len(level), re.MULTILINE)
    m2 = next_heading_re.search(content, section_start)
    section_end = m2.start() if m2 else len(content)

    section_body = content[section_start:section_end]
    section_body = ARCHIVE_NOTE_RE.sub('\n', section_body, count=1)

    entries = split_entries(section_body)
    if len(entries) <= KEEP_MIN_ENTRIES:
        return None

    # Rank by actual date, not by position: some docs here prepend newest-first
    # (embarch.md), others append oldest-first (embarch-core/design.md) — a
    # position-based top-N cut would silently archive the wrong end on the
    # latter. Ties (same-day entries) keep their original relative order.
    by_recency = sorted(
        range(len(entries)),
        key=lambda i: (_parse(entries[i][0]), i),
        reverse=True,
    )
    kept_indices = set(by_recency[:KEEP_MIN_ENTRIES])
    kept = [entries[i] for i in range(len(entries)) if i in kept_indices]
    archived = [entries[i] for i in range(len(entries)) if i not in kept_indices]

    if not _is_prefix_or_suffix(kept_indices, len(entries)):
        print(f"  WARN {os.path.relpath(path, REPO_ROOT)}: kept entries aren't a clean prefix/suffix of the "
              f"section (some out-of-order dates near the cut point) — archiving anyway, worth a human glance.")

    basename = os.path.basename(path)
    stem, _ext = os.path.splitext(basename)
    archive_name = f"{stem}.changelog-archive.md"
    archive_path = os.path.join(os.path.dirname(path), archive_name)

    if dry_run:
        print(f"  {os.path.relpath(path, REPO_ROOT)}: would archive {len(archived)} of {len(entries)} entries "
              f"-> {os.path.relpath(archive_path, REPO_ROOT)}")
        return len(archived)

    # Rewrite the live doc: heading, archive-note, kept entries.
    note = f"\n*Older entries archived to [{archive_name}]({archive_name}).*\n"
    new_section_body = note + "\n" + "\n".join(text for _, text in kept) + "\n\n"
    new_content = content[:section_start] + new_section_body + content[section_end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # Prepend the newly-archived batch to the archive file (creating it if needed).
    if os.path.exists(archive_path):
        with open(archive_path, encoding='utf-8') as f:
            existing = f.read()
        header_end = existing.index('\n\n') + 2 if '\n\n' in existing else len(existing)
        archive_header, archive_rest = existing[:header_end], existing[header_end:]
    else:
        archive_header = ARCHIVE_HEADER_TEMPLATE.format(
            basename=basename, keep_min=KEEP_MIN_ENTRIES,
        ) + "\n"
        archive_rest = ""

    new_archive = archive_header + "\n".join(text for _, text in archived) + "\n\n" + archive_rest
    with open(archive_path, 'w', encoding='utf-8') as f:
        f.write(new_archive.rstrip('\n') + '\n')

    print(f"  {os.path.relpath(path, REPO_ROOT)}: archived {len(archived)} of {len(entries)} entries "
          f"-> {os.path.relpath(archive_path, REPO_ROOT)}")
    return len(archived)


def _parse(date_str):
    y, m, d = (int(x) for x in date_str.split('-'))
    return date(y, m, d)


def _is_prefix_or_suffix(indices, total):
    ordered = sorted(indices)
    return ordered == list(range(len(ordered))) or ordered == list(range(total - len(ordered), total))


def main():
    dry_run = '--dry-run' in sys.argv
    print(f"Scanning for Changelog sections ({'dry run' if dry_run else 'archiving'})...")
    total = 0
    touched = 0
    for path in sorted(find_md_files(REPO_ROOT)):
        result = process_file(path, dry_run)
        if result:
            total += result
            touched += 1
    if touched:
        print(f"\n{'Would archive' if dry_run else 'Archived'} {total} entries across {touched} file(s).")
    else:
        print("\nNothing to archive.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
