# 024 — The contract fixes build step 5's shapes and forks

**State:** claimed by agent/promptu/024-the-contract-fixes-build-step-5s-shapes-and-forks, 2026-11-25 00:11
**Source:** EMB-403 — Promptu's contract says nothing of build step 5's reads and shapes
**Issue:** EMB-403
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

`embarch-promptu` decision 3 (`embarch-doc/embarch-promptu/decisions/what.md`)
builds every step against its contract, written first, each open choice a fork
in `docs/forks.md` on its most reversible default. Build step 5 (decision 16,
`decisions/chat.md`: the chat's 💡 linker gains datasheet and spec sections,
instruments, captures and traces, Linear projects and documents, branches and
worktrees, Kconfig symbols and devicetree nodes) has neither. When this is
done:

- **`docs/contract.md` has §15, "The linker's kinds (build step 5)"**, with:
  - **the reference entry** the chat's linker holds per line: `kind` (`issue`,
    `pr`, `project`, `document`, `branch`, `worktree`, `section`, `symbol`,
    `node`, `instrument`, `capture`, `trace`), a key unique within its kind, the
    words it is matched on, the exact names a draft may use for it, the line the
    block shows, and the text that replaces a phrase;
  - **one table, one row per kind**: source, refresh, cue words, written form,
    cap. The block is `<references>`, 12 lines and 3,600 characters, at most 4
    lines per kind before the best of the rest fill it; a high-volume kind
    (sections, symbols, nodes, branches, Linear documents) is offered only on an
    exact name or one of its cue words; issues and PRs keep `embarch-chat`
    decision 88's word match;
  - **the three read surfaces' JSON**, each built later by its own unit:
    - `embarch-atlas refs --json`: `{"atlas_refs": 1, "atlas_dir", "atlas":
      "<target>@<commit12>"|null, "commit", "stale": [...], "sections": [{"doc",
      "kind", "part", "id", "title", "level", "page"}], "symbols": [{"name",
      "prompt", "type"}], "nodes": [{"path", "labels", "compats", "status",
      "aliases"}]}`;
    - `embarch-api --json list-studies [--limit N]`: `{"success": true, "keep",
      "studies": [{"study_id", "study_name", "status", "started_utc_ms",
      "ended_utc_ms", "taps": [{"name", "encoding", "encoding_kind",
      "rendered"}]|null, "note"}]}`, newest first;
    - the desk's `GET /refs` gains `"projects": [{"id", "name", "state", "url",
      "team_keys"}]` and `"documents": [{"id", "title", "url", "project_id",
      "project_name", "updated_ms"}]`; an older desk omits both and a reader
      takes them as empty.
- **§11 gains "From step 5"**: nothing in §0 to §14 changes; §15's shapes are
  fixed once built and may grow by §0's rules. §0 names §15 wherever it lists
  the sections.
- **`docs/forks.md` gains "Step 5: the 💡 linker's kinds"** after W24, one fork
  per numbered choice of the step 5 plan, numbered `L<choice>`, each "open,
  built on its recommendation" with its alternative, ranked by consequence as
  W1 to W24 are, the riskiest five first: the cue-word gate (11), Core through
  the `embarch-api` CLI (5), the atlas verb (3), the block's size (10), the
  contract first (2).
- **Promptu's docs say step 5 is under way**: the status line of
  `embarch-doc/embarch-promptu/spec.md` and `spec/status.md`, and a step 5
  table in `interfaces.md` pointing at contract §15.

**Where the plan's choices come from.** The plan itself is not in any repo.
Its choices are stated, each with its recommendation, in the bodies of the
step 5 issues (EMB-404 to EMB-415), and the leg hands the worker a copy of
those bodies. They state choices 2 to 17, 20 and 22: 2 the contract first;
3 the atlas verb; 4 atlas only (a repo with no built atlas offers no symbols or
nodes); 5 Core through the `embarch-api` CLI in the chat's folder; 6 a signal's
live capture is not a kind; 7 `list-studies --limit 20`; 8 which Linear
projects and documents the desk indexes; 9 branches from the chat folder's main
clone; 10 the block's size; 11 the cue-word gate; 12 each kind's written form;
13 one References submenu; 14 no prose links beyond decision 16's; 15 when each
source refreshes; 16 at most 4 lines per kind; 17 `list-studies` is not an MCP
tool; 20 the instrument words; 22 real Haiku fixtures left to the review unit.
**Choices 1, 18, 19 and 21 are stated nowhere the leg could find.** Write L1,
L18, L19 and L21 as entries saying the plan's choice is not recorded in any
filed issue and is the owner's to state, and add one `open.md` bullet saying
the same; do not invent their content.

## Why now

EMB-403: every other step 5 unit (EMB-404 to EMB-415) codes against §15, and
Linear holds those issues until this one is Done.

**Burndown leg: no new numbered decision.** The issue says so itself: the
forks hold the choices until the owner picks. Promptu's decisions 3 and 16 may
gain a pointer to §15, amended in place; `embarch-chat`'s decisions 88 and 97
are another sub-project's, so leave them to the chat's own step 5 units.

## Done when

- [ ] `docs/contract.md` has §15 with the reference entry, the kinds table and
      the three read surfaces' JSON, and §11 says what step 5 fixes.
- [ ] `docs/forks.md` has L1 to L22, each with its default and alternative,
      L1, L18, L19 and L21 saying their choice is unrecorded.
- [ ] Promptu's spec, status and interfaces say step 5 is under way and point
      at §15; `open.md` names the four unrecorded choices.
- [ ] Gate green (`../../embarch-fleet/gate.md`), `changelog.d/` fragment
      dropped.
