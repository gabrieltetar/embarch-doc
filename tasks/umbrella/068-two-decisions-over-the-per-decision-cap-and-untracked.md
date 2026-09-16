# 068 — `embarch-umbrella` has two decisions over the per-decision cap, both untracked

**State:** done
**Reserve (leg 118):** `embarch-umbrella/decisions/bind.md` is at 93.9% — 755 B left of 12288 — and
is already filed against `tasks/umbrella/009-compact-docs.md`, which is **blocked**. Neither
decision in this unit lives in `bind.md`; do not write into it. If your work spends reserve anywhere
in `embarch-umbrella`, file `tasks/umbrella/<NNN>-compact-umbrella.md` in the same commit.
**Source:** leg 117, 2026-09-16. `core/063` closed this gap for `embarch-core` decision 30 and named
the real finding as *"nothing is watching it."* I ran the census that implied: **five** decisions
suite-wide are over [`DOC-BUDGET.md`](../../DOC-BUDGET.md)'s **4,096 B per-decision cap** with no pin
in `scripts/decision-size-baseline.json`, so nothing reports them and no ledger gives them a clock.
`core/063` fixed one, `core/064` files another, `topology/047` files the largest. **Two of the five
are here**, which is more than any other sub-project.
**Scope:** umbrella
**Hardware:** none — doc prose only. No board, no probe, no live Core, no `doctor` run.
**Owner:** no
**Compacts:** `embarch-umbrella/decisions/probe-vendors.md`, `embarch-umbrella/decisions/locate-api.md`
**In flux:** no, both — and the distinction matters, so read it rather than trusting the word.
Decision 49's **routing half is settled**: [`open.md`](../../embarch-umbrella/open.md) records
in as many words that *"the list stays here"* and moves only if something other than `doctor`'s own
message ever consumes it. What is unmeasured there is *whether the nine vendor IDs are the right
nine* — a question about the list's **contents**, not about this decision's text or its home.
Decision 42 was settled by `umbrella/059`, which split `locate-api.md` out as its own file. Neither
entry is being rewritten by anything in flight.

## What

Two entries, both over cap, neither pinned:

```
6,962 B  embarch-umbrella/decisions/probe-vendors.md#49   (+2,866 B, 170% of cap)
5,157 B  embarch-umbrella/decisions/locate-api.md#42      (+1,061 B, 126% of cap)
```

For each, the same fork `core/063` faced:

- **One decision that has accreted several arguments** → split it into two numbered decisions and
  update `embarch-umbrella/decisions.md`'s index — number list **and** size column, same commit.
- **One decision stated at length** → compact under 4,096 B without losing the "why not",
  [`DOC-COMPACTION-PASS.md`](../../DOC-COMPACTION-PASS.md) in full, including quoting every cut hunk
  verbatim rather than naming categories.

**Read each before choosing, and answer the fork separately for the two.** They are not the same
shape: decision 49's own opening is *"The question, as it was asked"* — an entry that narrates a
question and then answers it, which is the profile that compacts well. Decision 42's opening
sentence says `open.md` *"recorded [it] from three directions and never as its own item"*, which is
the profile that sometimes really is two decisions.

**A new decision number is the most expensive thing in this suite to reverse**, so the burden of
proof is on splitting: you have to name two claims a citation could want to point at *separately*.

## Why now

**Because the per-decision cap has no ledger and no clock.** The file-level ledger has both — a leg
spends its first unit on the oldest overdue entry, and `check-doc-size.py --pressure` lists every
file in reserve with the task that owns its debt. A decision that was never pinned is invisible to
all of it: `--decisions` prints only its top 20 by size, which is how `embarch-core` decision 30 sat
over cap until a reviewer opened the baseline file while checking something unrelated. Whether that
gap should be closed mechanically is the owner's call under `scripts/`
([`tasks/doc/052`](../doc/052-a-verbatim-split-silently-drops-the-decision-size-pin-of-every-decision-it-moves.md)
records the adjacent defect). **This task is only about the two entries that are actually over.**

## Watch for

- **Do not add pins to `scripts/decision-size-baseline.json` to make the numbers go away.**
  `scripts/` is owner-reserved, and pinning an over-cap decision is the papering-over move.
- **Decision 49 is cited from outside `embarch-umbrella`** — it is the vendor-ID routing decision
  and `doctor` check 5's behaviour hangs off it. Grep the whole doc repo for inbound `decision 49`
  and `decision 42` citations before renumbering anything, and remember a bare `decision 49` in
  another repo's file means *that* repo's 49.
- **Keep the "why not".** Decision 49's whole point is *why the list is not in `embarch-topology`* —
  that it is not the same fact that crate holds. That argument is the entry's reason for existing
  and a compaction that loses it invites the move being re-proposed. Cut narrative and single-machine
  measurements, not the reasoning.
- **If you only have budget for one**, do decision 49 — it is the larger breach and the one with
  cross-repo citations — and leave decision 42 with its remainder filed as its own task, the way the
  `study-designer` sweep chain does.
- **Report before/after byte counts and the margin left** for each entry you touch.

## Done when

- [x] `embarch-umbrella` decision 49 is at or under 4,096 B, or split, with the branch justified.
- [x] `embarch-umbrella` decision 42 likewise, **or** left untouched with a follow-up task filed
      naming it.
- [x] `embarch-umbrella/decisions.md`'s index table matches — numbers and size column.
- [x] Every inbound citation to a touched decision still resolves to the claim it was citing.
- [x] If compacted: every cut hunk quoted verbatim in the task file, per `DOC-COMPACTION-PASS.md`.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10).

## What shipped

**Both compacted, neither split.** Both fit the fork's "compacts well" profile once read: decision 49
narrates a question and answers it (no separable second claim — the routing answer and its costs are
one argument), and decision 42's "three sources, ranking is the decision" is one ranking decision with
supporting evidence, not two arguments a citation would want to point at separately. The burden of
proof for a new decision number was not met for either, so no split, no `decisions.md` renumbering —
its index table already carries no size column and its number list is unchanged (49 and 42 still
resolve to the same files), so no edit was needed there.

**Decision 49** (`embarch-umbrella/decisions/probe-vendors.md`): **6,962 B → 3,956 B**, margin 140 B
(3.4%). Kept intact: the "no shared fact to route" premise, the wrong-machine argument (marked as the
load-bearing cost), the general rule ("a fact whose wrongness produces a wrong diagnostic message
belongs where the diagnostic lives..."), the trigger condition that `open.md` line 17 relies on, and —
per the task's
explicit instruction — **"whether the nine vendor IDs are the right nine" as an unmeasured, live open
question**, verbatim in substance: "**whether the nine vendor IDs are the right nine** — unmeasured,
and a question about the list's *contents*, not its *home*". All three `*Rejected:*` alternatives kept.

**Decision 42** (`embarch-umbrella/decisions/locate-api.md`): **5,157 B → 4,019 B**, margin 77 B
(1.9%). Kept intact: the defect evidence, the three-source ranking and why (c) is last, the contested
(a)-ahead-of-`PATH` argument in full (including the two-binaries-same-`--version` evidence and the
"reading, not a guess" framing), both `*Rejected:*` alternatives, the residual note, and the fact that
"neither check 8 nor check 11 has run inside a live `doctor` yet" (cited by `suite/features.md` /
`features.d/umbrella-030-...md` alongside decision 17). The bulk of the cut is a paragraph of
single-sitting CLI measurements (clap arg order, `host_type_schema_version`, `list-targets` JSON
shapes) that duplicated `embarch-umbrella/decisions/schema-skew.md#35`, which records the same
measurement independently — confirmed by reading that file before cutting.

**Citations checked**, whole `embarch-doc` repo, before touching anything: every other `decision 49`
and `decision 42` hit is a *different* repo's own same-numbered decision (`embarch-core`,
`embarch-study-designer`) — not this one — per the task's own warning. The only inbound citations to
*this* sub-project's 49 and 42 are `history/umbrella.md` (two one-line entries, unaffected — decision
numbers and claims unchanged), `embarch-umbrella/open.md`'s line 17 (decision 49's routing-settled
claim, still holds verbatim), and `suite/features.md`/`features.d/umbrella-030-...md` (decision 42,
"the check has not run inside `doctor`" — kept).

### Cut hunks — decision 49 (verbatim, complete)

Every hunk below is the exact original text, in a fenced quote so nested backticks and bracket/paren
sequences are not parsed as markdown links.

1. Dropped from the opening framing paragraph (the "shape of a drift bug" claim survives without the
   illustration):
   ```
   an engineer whose probe is misidentified has to guess which repo to fix, and the one that does not
   get fixed silently falls out of step
   ```
2. Whole table row dropped. The nine umbrella names are recorded verbatim elsewhere in the same
   sub-project, `embarch-umbrella/decisions/doctor.md`'s decision 18 ("The list is SEGGER, CMSIS-DAP,
   ST-Link, LPC-Link2, EDBG, Raspberry Pi Debug Probe, Black Magic, XDS110, ULINK."), confirmed by
   reading it before cutting:
   ```
   | **Contents** | SEGGER, CMSIS-DAP, ST-Link, LPC-Link2, EDBG, RPi Debug Probe, Black Magic, XDS110, ULINK | `SEGGER_VID`, `ESPRESSIF_VID`, `SILABS_VID` |
   ```
3. Table cell wording only, no claim lost (`a bench that flashes, boots, runs and times out` → `a
   bench that flashes and times out`):
   ```
   , boots, runs
   ```
4. Second example dropped; the SILABS_VID example that precedes it already carries the point:
   ```
   and why `ESPRESSIF_VID` is there while being explicitly **not** a link candidate.
   ```
5. Corroborating cross-reference to a different decision, dropped as narrative, not load-bearing for
   this decision's own argument:
   ```
   `links-port.md` decision 24 is the same crate being careful about precisely this: it added a
   fourth `detected_by` constant because labelling a result `vid-match` when the VID gate never ran
   named a rule that did not happen.
   ```
6. Dropped as redundant with the sentence that follows it (`no shared fact to route, and no drift to
   prevent:`):
   ```
   and no drift to prevent
   ```
7. Dropped from the "What routing... would cost" heading:
   ```
   , taken on its merits
   ```
8. Whole bullet, dropped as a bullet and folded into one sentence of prose. Its surviving claim ("Core's
   own probe surface... is the same enumeration check 5 exists to catch the gap in, so a Core endpoint
   would inherit it") is restated in compact form in the new text; the sysfs-permission mechanism
   detail, the "second parallel sysfs reader" option, and the explicit non-load-bearing hedge are cut:
   ```
   **The natural way for Core to answer it is the under-reporting way, though not the only way.**
   Check 5 exists because probe enumeration *silently under-reports* a probe nobody has permission to
   open; its whole mechanism is that sysfs attributes are world-readable while `/dev/bus/usb/...` is
   the node a udev rule grants ([decision 18](doctor.md)). Core's existing probe surface is
   `probe_rs`'s `Lister` — exactly the enumeration whose gap this check was built to expose — so a
   Core endpoint answering "which probe vendors do you see" over that surface would inherit the blind
   spot. **This is a statement about the path of least resistance, not a structural impossibility**:
   `/sys/bus/usb/devices` is as readable from Core's process as from umbrella's, and Core could carry
   a second, parallel sysfs reader. That option is rejected on its own terms — it is the same fifty
   lines relocated, for no architectural gain, into a process on a machine the operator may not be
   sitting at. **The argument below about the wrong machine is the load-bearing one; this bullet is
   a cost, not a proof.**
   ```
9. Dropped from the wrong-machine bullet; a supporting citation, not the argument itself (which is
   kept):
   ```
   and [decision 31](doctor.md) names it as check 14's mistake with a different peripheral
   ```
10. Bolded header of the third bullet dropped; its claim survives unbolded, folded into the "secondary
    cost" sentence:
    ```
    **The permission question is about the user running `doctor`, not about Core.**
    ```
11. Dropped from `a udev rule for *this* user`:
    ```
    for *this* user
    ```
12. Dropped from the "what makes keeping it safe" paragraph; the general rule and the two consequences
    (which port / which prose sentence) survive without this specific-instance example:
    ```
    and nothing else — a wrong entry makes `doctor` say "no probe found" where it could have said
    "attached but not permitted", which is the warn the check already replaced and not a regression
    past it.
    ```
13. Whole sentence dropped; a subsidiary reassurance against a layering objection, not part of the
    routing argument itself:
    ```
    `spec.md`'s "never links `probe-rs` or `serialport`" boundary is intact either way: check 5 reads
    a text file.
    ```
14. Dropped from `(which would make them one fact, and one fact belongs in one place)`; redundant
    restatement within the same parenthetical:
    ```
    , and one fact belongs in one place
    ```
15. Whole paragraph dropped — a meta-summary restating the argument's own priority order (already
    implied by structure) plus review-process narrative; no new claim:
    ```
    **What carries this decision, stated plainly so a later reader does not lean on the wrong leg.**
    The *sufficient* argument is the first one: **there is no shared fact to route.** Everything after
    it is cost, and the strongest of those costs is the wrong-machine hazard, not the blind-spot one —
    which a reviewer correctly cut down to size before this was committed.
    ```
16. Dropped from `*Rejected: move it to `embarch-core` and have check 5 call it.*`:
    ```
    and have check 5 call it
    ```
17. Dropped parenthetical; restates the already-established premise:
    ```
    (the two lists are different facts)
    ```
18. Dropped from `*Rejected: leave it undecided and keep the `open.md` caveat.*`:
    ```
    and keep the `open.md` caveat
    ```
19. Trailing clause dropped; the sentence now ends at "replaces.":
    ```
    a routing question nobody has answered gets re-asked by the next reader of either file
    ```

### Cut hunks — decision 42 (verbatim, complete)

1. Shortened to "and"; `embarch-api`'s install location relative to `embarch` is not load-bearing for
   the defect evidence:
   ```
   beside `embarch` itself, and
   ```
2. Dropped, `turned on whether the shell that ran `doctor` happened to be interactive` → `turned on
   whether the shell that ran `doctor` was interactive`; wording only:
   ```
   therefore
   ```
   ```
   happened to be
   ```
3. Whole paragraph, replaced by a one-clause pointer. The quoted description of what `topology.md`
   answers, and the "no topology class, no WSL2 boundary, no elevation" enumeration, are dropped; the
   surviving sentence keeps only "which `embarch-api` checks 8, 10 and 11 are statements about":
   ```
   **Filed here rather than beside 38**, which is the same question for `embarch-core`: `topology.md`
   answers "where is Core, and what may be done to it from here", and this involves no topology class,
   no WSL2 boundary and no elevation. What it settles is which `embarch-api` checks 8, 10 and 11 are
   statements *about* — the check chain's own subject.
   ```
4. Dropped from the (a)-ahead-of-PATH paragraph; replaced by the shorter `not a guess (decision 38's
   rule)`. The `sc.exe qc` analogy and the exact quoted phrase "a reading beats a guess" are cut; the
   claim (registration is a reading, per decision 38's rule) survives:
   ```
   the way `sc.exe qc` is for Core, and decision 38's "a reading beats a guess" is the same rule
   ```
5. Dropped from the rejected-alternatives paragraph; the same point (the divergence is printed, not
   hidden) already appears earlier in the entry, in the (a)-ahead-of-PATH paragraph's closing clause,
   so this is a cut redundancy rather than a lost claim:
   ```
   check 1 names the divergence in its detail rather than choosing silently
   ```
6. The bulk of the "what the same sitting measured" paragraph, cut. Verified before cutting that this
   duplicates `embarch-umbrella/decisions/schema-skew.md`'s own decision 35 ("`--json` goes before the
   subcommand... `embarch-api versions --json` exits 2 [verified 2026-09-04]... The *installed* binary
   answers with `host_type_schema_version` v17, debug and release alike... check 11 read all three and
   agreed [measured 2026-09-05, owner's machine]"), which records the identical measurement
   independently. The surviving fact this paragraph existed to establish — "neither check has run
   inside a live `doctor` yet" — is kept, now pointing at decision 35 for the measurement instead of
   repeating it:
   ```
   `--json` and `--config` are top-level and must precede the subcommand — clap exits **2** otherwise,
   which is what [check 11](schema-skew.md) reports as an `embarch-api` too old to know `versions`;
   `versions` answered `host_type_schema_version` **17**, Core's own number, from both binaries;
   `list-targets` answered `{success: true, targets: [...]}` on exit 0 and `{success: false, error}`
   on exit 1, both on **stdout**, with its own log line on stderr. Every shape checks 8 and 11 had
   only read off `embarch-api`'s source is therefore observed.
   ```
7. Shortened to `not this one, so it is recorded rather than fixed here`; the "locator is now correct
   either way" clause is dropped, the pointer to `install.rs` owning the fix is kept:
   ```
   the locator is now correct either way, which is why it is recorded here rather than changed
   ```

## Inbox drop filed

**`embarch-umbrella/decisions/mirrors.md#16` is also over the 4,096 B per-decision cap (4,347 B,
unpinned)** — found while re-running `scripts/check-doc-size.py --decisions` after closing 49 and 42.
It was already over cap as of 2026-09-13 (`git show 91e75f5^`, 4,330 B), well before this task's own
`Source:` census (leg 117, 2026-09-16, which said "two of the five" over-cap decisions are in
`embarch-umbrella`). Out of scope for `umbrella/068` — its task file named exactly decisions 49 and
42 — so filed at
`/home/gabriel/Github/embarch/embarch-doc/inbox/umbrella-mirrors-decision-16-over-cap.md` per protocol
§ "found something outside your task", by absolute path per the worktree-drop rule.

## Gate results

- `scripts/check-docs.py` (embarch-doc worktree): **all 11 checks green**.
- `scripts/check-doc-size.py --decisions`: neither `probe-vendors.md#49` nor `locate-api.md#42`
  appears in the over-cap/pin list any more. (`mirrors.md#16` does — pre-existing, unrelated, filed
  to inbox above.)
- `scripts/check-ownership.py --scope umbrella` (doc worktree): `OK: all 2 changed path(s) owned by
  the 'umbrella' worker.`
- `scripts/check-ownership.py --scope umbrella --repo <code worktree> --code-repo`: `OK: code repo,
  worker for 'umbrella' owns the whole tree (0 path(s) changed, not path-checked)` — this unit is
  doc-only, the `embarch-umbrella` code worktree has no changes.
- `scripts/check-client-names.py --repo <code worktree>`: `OK: clean against 7 denylist entries.`
- No `cargo build`/`test`/`clippy` run: no code changed in `embarch-umbrella`, nothing to build.

## Left undone

Nothing from this task's own scope. `mirrors.md#16` (a third umbrella decision over the same cap) is
real remaining work, filed to `inbox/` rather than picked up here, per the task's explicit two-decision
scope and the worker-ownership rule against reaching past an assigned task.
