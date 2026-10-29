#!/usr/bin/env python3
"""Check that `embarch-api/interfaces/tools.md` lists every MCP tool, and no other.

That file is the tool index: its `## Sections` list names every tool the
`embarch-api` MCP server exposes, and an agent reads it first to decide what to
call. Nothing compared it with `src/tools.rs` until 2026-10-29
(tasks/doc/051). Two interface docs had disagreed for two days about three
retired aliases, and the wrong one was the index -- a stale name there is a
call that fails, not a sentence that reads oddly.

**What counts.** On the source side, every `async fn` that a
`#[tool(description` attribute precedes in `src/tools.rs` -- the same adjacency
`embarch-api`'s own `tests/tool_subcommand_parity.rs` reads. On the doc side,
only the leading run of each `## Sections` bullet: the comma-separated
backticked names right after its dash. Prose after the run is never read, which
is what makes the check tolerate it: a retired alias in a parenthetical, `test`
in "`run_study`'s `test`", `status` in "and what `status` now carries", and
everything outside the list (`doctor`, field names, crate names). A listed name
that is not a tool must be one the doc itself declares CLI-only, in its
"The CLI is a **superset**" sentence (`versions` today).

**Sets, not counts.** Two compensating errors pass a count. A tool missing from
the index and a listed name with no tool both fail, by name.

The source is the sibling checkout `../embarch-api`. Where there is none -- CI,
or a worktree without that link -- this SKIPS rather than fails, the same rule
`check-docs.py` applies to the framework repo.

Usage: scripts/check-tool-index.py
Exit status: 0 if the index and the source agree (or the source is absent).
"""
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(REPO_ROOT, '..', 'embarch-api', 'src', 'tools.rs')
INDEX = os.path.join(REPO_ROOT, 'embarch-api', 'interfaces', 'tools.md')

RUN = re.compile(r' — ((?:`[a-z_]+`(?:,\s*(?:and\s+)?|\s+and\s+)?)+)')
NAME = re.compile(r'`([a-z_]+)`')
SUPERSET = re.compile(r'The CLI is a \*\*superset\*\*:(.*?)have no tool')


def source_tools(text):
    """Every fn name a `#[tool(description` attribute precedes."""
    names, armed = set(), False
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('#[tool(description'):
            armed = True
        elif armed and line.startswith(('async fn ', 'pub async fn ')):
            names.add(re.match(r'(?:pub )?async fn (\w+)', line).group(1))
            armed = False
    return names


def index_names(text):
    """(listed, cli_only): names in the Sections bullets' leading runs, and
    the names the superset sentence says have no tool."""
    section = text.split('\n## Sections\n', 1)[1].split('\n## ', 1)[0]
    listed = set()
    for line in section.splitlines():
        m = RUN.search(line) if line.startswith('- [') else None
        if m:
            listed |= set(NAME.findall(m.group(1)))
    sup = SUPERSET.search(text)
    return listed, set(NAME.findall(sup.group(1))) if sup else set()


def main():
    if not os.path.exists(SOURCE):
        print('SKIP: no ../embarch-api beside this repo; nothing to compare.')
        return 0
    with open(SOURCE, encoding='utf-8') as fh:
        tools = source_tools(fh.read())
    with open(INDEX, encoding='utf-8') as fh:
        listed, cli_only = index_names(fh.read())
    missing = sorted(tools - listed)
    unknown = sorted(listed - tools - cli_only)
    rel = os.path.relpath(INDEX, REPO_ROOT)
    for name in missing:
        print(f'{rel}: MCP tool `{name}` is in src/tools.rs and in no section')
    for name in unknown:
        print(f'{rel}: `{name}` is listed as a tool; src/tools.rs has no '
              f'#[tool] fn {name}, and the superset sentence does not call it '
              f'CLI-only')
    if missing or unknown:
        return 1
    print(f'All {len(tools)} #[tool] fns in embarch-api/src/tools.rs are listed '
          f'in {rel}, and nothing else is ({len(listed & cli_only)} CLI-only: '
          f'{", ".join(sorted(listed & cli_only))}).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
