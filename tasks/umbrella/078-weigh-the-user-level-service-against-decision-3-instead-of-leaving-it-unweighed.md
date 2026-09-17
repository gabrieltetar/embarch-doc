# 078 — Weigh the user-level service against decision 3, instead of leaving it "not weighed"

**State:** done
**Source:** `embarch-umbrella/open.md`, swept by leg 134's refill. The bullet is one sentence and
ends by saying nobody has done the work: *"A user-level service needs no elevation on Linux or macOS
(systemd `--user`, a launch agent) **but would not start before login, defeating decision 3.** Not
weighed."*
**Scope:** umbrella
**Hardware:** none, and **do not try to make it hardware**. This is a design question settled by
reading decision 3, the install path, and the two platforms' own documented service semantics. Do
not install a service, do not run `setup`, do not touch a live Core, do not deploy anything.
**Owner:** no

## What

Every other bullet in `embarch-umbrella/open.md` is either a hardware debt waiting for a bench or a
question explicitly deferred with a reason. This one is neither: it is a real trade-off with both
sides already identified, marked **not weighed**, and nothing about it needs a machine. It is the
only host-side unweighed design question left in that file.

The trade-off as the bullet states it:

- **For a user-level service** (`systemd --user`, a launchd launch agent): no elevation needed, so
  the install stops asking for a privilege escalation on Linux and macOS.
- **Against:** it would not start before login, which defeats decision 3 — the reason the service
  exists at the system level in the first place.

## What "weighed" has to mean here

Not a preference. Establish, from decision 3 and the install path:

- **What decision 3 actually requires**, quoted rather than paraphrased — specifically whether
  "starts before login" is the property it depends on, or whether it depends on something weaker
  that a user-level service would still satisfy.
- **Who the before-login start is for.** If nothing in the suite's real usage depends on Core
  running before a login, the objection is weaker than the bullet implies and that is the finding.
  If something does, name it — that closes the question in the other direction, permanently.
- **Whether a mixed answer exists**: a user-level service on macOS and a system one on Linux, or
  either as an opt-in install mode. Say why not, if not.

Then record the outcome as a numbered `embarch-umbrella` decision per `DOC-CONVENTIONS.md`, and
rewrite the `open.md` bullet to match. **A decision that the system-level service stands is a
perfectly good outcome** — what is not acceptable is leaving the bullet saying "not weighed" after
this task runs. If the honest conclusion is that it cannot be weighed without something the suite
does not have, say exactly what that is; that is a narrower open question than the one there now,
and narrowing it is a result.

**Do not build anything.** No new install mode, no new flag, no service file. If the decision
concludes something should be built, that is a follow-up task filed in `tasks/umbrella/`, not this
unit's work.

## Doc-size reserve for umbrella

`embarch-umbrella/open.md` is at **4,127/5,120 B (993 B left)** and in reserve, filed as
`tasks/umbrella/077-compact-docs.md` and blocked. This task *shortens* that bullet if it does its
job, so it should relieve pressure rather than add it — but re-check with
`python3 scripts/check-doc-size.py --pressure` before and after, and if a decision file crosses into
reserve, file a compaction task for it in the same commit.

**Supervisor dispatch note, leg 136 — the second umbrella file in reserve, which this task's own
reserve paragraph does not mention.** `embarch-umbrella/decisions/bind.md` is at **11,533/12,288 B
(755 B left)**, filed against `tasks/umbrella/009-compact-docs.md` and blocked. **Do not write your
new decision into `bind.md`.** Put it wherever umbrella's `DOC-CONVENTIONS.md` routing actually
sends a service/install decision, and check that file's headroom first — if the only correct home is
`bind.md` and the entry will not fit in 755 B, say so in your report and file
`tasks/umbrella/<NNN>-compact-docs.md` in the same commit rather than squeezing the entry.
Nothing else of umbrella's is in reserve.

## Done when

- [x] Decision 3 is quoted, not paraphrased, and what it depends on is stated exactly.
- [x] One numbered `embarch-umbrella` decision records the outcome, with a reversal condition.
- [x] `open.md`'s bullet no longer says "not weighed" — it either states the answer or states a
      narrower question with what is missing.
- [x] A `changelog.d/` fragment; a `status.d/` fragment for any suite-level fact this made false.
- [x] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`,
      `check-docs.py`, `check-ownership.py --scope umbrella`,
      `check-client-names.py --repo <code worktree>`.

## What shipped

Decision 3, quoted exactly (`decisions/install.md`): *"if Core autostarts at boot **there is nothing
for a human to start, ever**"*. Read closely, that guarantee is independent of any login event, not
merely "already running by the time a logged-in human tries it" — and every consumer this suite
documents (a human's own shell, an MCP client spawned inside that human's editor session) already
implies a login has happened, so for them a user-level service is equivalent in practice. The case
the guarantee actually protects and the open.md bullet never named: a machine dedicated to running
Core where nobody ever completes an interactive login. There, a macOS launch agent never starts (no
lingering-session equivalent) and a `systemd --user` unit needs `loginctl enable-linger`, which
`setup` does not run and cannot assume. No platform split survives it either — macOS has nothing to
switch to, so a Linux-only user-level mode would help only the platform that isn't the problem.

Recorded as **embarch-umbrella decision 54** in `decisions/install.md` (the file decisions 3, 4, 5,
14, 21, 25, 28 already live in — the correct home per `decisions.md`'s own routing), with a stated
reversal condition: a documented consumer needing Core running with zero logins since boot, which
nothing in `spec.md` currently describes. The `open.md` bullet is deleted outright rather than
reworded to "resolved" — `DOC-CONVENTIONS.md` states every top-level `open.md` bullet is an open
question, and this one no longer is; the decision and its reversal condition are the durable record.

Built nothing: no install mode, no flag, no service file. Ran no `setup`, touched no live Core.

**Doc-size reserve, both checked before and after (`check-doc-size.py --pressure`):** `open.md`
shrank 4,127 → 3,954 B (80.6% → 77.2%), relieving rather than adding pressure, and stays filed under
the existing `tasks/umbrella/077-compact-docs.md` (blocked, unchanged). `decisions/install.md` had
no slack to add a target-sized decision entry without crossing its own reserve line: 11,009 → 12,071 B
(89.6% → 98.2% of its 12,288 B cap, 217 B left, still under the hard cap). Filed
`tasks/umbrella/079-compact-docs.md` in this same commit, per protocol, rather than squeezing decision
54 to fit — `decisions/bind.md` (755 B left, filed against `009`) was left untouched, decision 54 was
not written there.

Gate: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green in the
`embarch-umbrella` worktree (no source touched, doc-only unit — see report for exact commands and
whether the crate had any code changes). `check-docs.py`, `check-doc-size.py`,
`check-ownership.py --scope umbrella`, `check-client-names.py --repo <code worktree>` all green in
the `embarch-doc` worktree.
