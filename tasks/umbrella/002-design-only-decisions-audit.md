# 002 — Six decisions are recorded as designs, and nobody has checked which shipped

**State:** claimed by agent/umbrella/002-design-only-decisions-audit, 2026-09-03 12:26
**Source:** embarch-umbrella/open.md — "Several later decisions are recorded as designs with no implementation note, and whether each shipped is not established here. … Reading the code is the way to close this, not reading this repo."
**Scope:** umbrella
**Hardware:** none

## What

`embarch-umbrella`'s docs carry a set of decisions whose implementation status is
unknown *to the docs*: `setup --dry-run` (21), the firewall and disk checks (22b,
22c), the MCP-handshake spawn (23), `doctor --prune` (26), the release version
assertion (27/29), and check 16, the bind-address-versus-topology check, which
`spec.md` marks design-only.

**Close each one against the source, one at a time**, and make the docs say what
the code does. For each: shipped, not shipped, or shipped differently from what
the decision describes — that third outcome is the valuable one and is the reason
this is worth a task rather than a skim.

This is exactly the drift `open.md` names, and it just bit for real: the same
bullet said "check 14 (bind address versus topology) is explicitly design-only"
while decision 31's flashing-backend check had **shipped as 14** in code, so two
different checks answered to one number until `umbrella/001` renumbered the
unbuilt ones to 16–19 on 2026-09-03. Assume more of that, not less.

**Read `embarch-umbrella/spec.md` and `decisions/` fresh** — several of its files
moved this morning under `umbrella/001`, and a stale copy in your head will send
you looking for the wrong numbers.

## Why now

Every one of these is a claim the suite's own docs make about a shipped binary,
and the numbering collision above shows the claims have already drifted from the
code at least once. It is entirely a reading task: no build to design, no
hardware, no wire.

## Done when

- [ ] Each of the seven items above has a stated, evidenced answer — name the
      function or the absence, not "appears to".
- [ ] `spec.md` describes what the binary does, with any design-only marker that
      is now false removed and any that is still true kept.
- [ ] `decisions/` gains an implementation note wherever a decision shipped
      differently from what it describes. **Do not rewrite the decision** — the
      record of what was decided stays; the note says what was built.
- [ ] `open.md`'s "Several later decisions…" bullet is rewritten to whatever is
      genuinely still unestablished, or removed if nothing is.
- [ ] A `status.d/` fragment for anything in `suite/features.md` this makes
      false — the `embarch doctor` row and its neighbours are the likely ones.
- [ ] **Build nothing.** If an item turns out to be unshipped, that is a finding
      to record, and a task for it belongs in `inbox/` — not work to do here.
      A doc-only branch is the expected shape of this task.
- [ ] Gate green (`embarch-parallel-agents.md` §10).
- [ ] `changelog.d/` fragment dropped.

## Watch for

If you find that a *number* is wrong somewhere — a check, a decision reference —
say so loudly in your report. `umbrella/001` found one collision already, and a
second would mean the numbering needs a rule rather than another repair.
