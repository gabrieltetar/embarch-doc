# 078 — Weigh the user-level service against decision 3, instead of leaving it "not weighed"

**State:** open
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

## Done when

- [ ] Decision 3 is quoted, not paraphrased, and what it depends on is stated exactly.
- [ ] One numbered `embarch-umbrella` decision records the outcome, with a reversal condition.
- [ ] `open.md`'s bullet no longer says "not weighed" — it either states the answer or states a
      narrower question with what is missing.
- [ ] A `changelog.d/` fragment; a `status.d/` fragment for any suite-level fact this made false.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings`,
      `check-docs.py`, `check-ownership.py --scope umbrella`,
      `check-client-names.py --repo <code worktree>`.
