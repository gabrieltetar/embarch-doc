# 007 — The permission-prompt alert fires for the owner's own sessions, and has never once fired for a leg

**State:** open
**Source:** owner's session, 2026-09-05 — found on the first read of `#embarch-fleet` after the connector resolved
**Scope:** doc
**Hardware:** none
**Owner:** required

**`Owner: required`** — the alert set is `embarch-fleet/ops.md` §3 and the hook
lives in `embarch-doc/.claude/settings.local.json`. The first is reserved
(`protocol.md` §3); the second is `.gitignore`d and belongs to the owner's window
(`ops.md` §5.1). A leg can write neither.

## What

`#embarch-fleet` contains 11 bot messages. **Nine are the identical alert**
`blocked on a permission prompt and cannot continue: AskUserQuestion`, between
2026-09-03 14:31 and 2026-09-05 00:08. The other two are the owner's own webhook
tests. There has never been a connector-posted message in the channel.

The alert comes from a `PermissionRequest` hook in
`embarch-doc/.claude/settings.local.json`, which shells `scripts/fleet-alert.py`
for **any** permission prompt in **any** session rooted at `embarch-doc` — the
owner's ordinary windows included.

**The handover framed this as "something under a leg is reaching for
`AskUserQuestion` and dying". It is not. Nothing under a leg has ever called it.**
All 194 `AskUserQuestion` calls across every transcript in
`~/.claude/projects/-home-gabriel-Github-embarch-embarch-doc/` carry
`isSidechain: false`, i.e. every one came from a main session and **none** from a
subagent. Each of the nine alerts matches a main-session call to within 3
seconds:

| Alert (MDT) | Matched call (UTC) | Δ | Sidechain | Session | Question |
|---|---|---|---|---|---|
| 2026-09-03 14:31:58 | 2026-09-03 20:31:58 | +0 s | no | `3a01c217` | Targets |
| 2026-09-03 14:36:38 | 2026-09-03 20:36:38 | +0 s | no | `3a01c217` | Watchdog |
| 2026-09-04 12:02:19 | 2026-09-04 18:02:18 | +0 s | no | `3a01c217` | Split |
| 2026-09-04 17:46:32 | 2026-09-04 23:46:30 | +1 s | no | `3a01c217` | Wedge |
| 2026-09-04 18:01:49 | 2026-09-05 00:01:46 | +2 s | no | `3a01c217` | History |
| 2026-09-04 18:05:21 | 2026-09-05 00:05:19 | +1 s | no | `3a01c217` | Naming |
| 2026-09-04 19:14:14 | 2026-09-05 01:14:11 | +3 s | no | `c27e462c` | Mechanism |
| 2026-09-04 21:53:09 | 2026-09-05 03:53:08 | +1 s | no | `c27e462c` | features.md |
| 2026-09-05 00:08:54 | 2026-09-05 06:08:51 | +2 s | no | `479584cc` | doc/005 |

Regenerate with the script in this task's git history, or by scanning those
transcripts for `tool_use` entries named `AskUserQuestion` and reading
`isSidechain`.

**Legs are already obeying the rule that covers this.** `ops.md` §3 says *never
ask a question mid-leg*; the evidence says they never have. So an
`AskUserQuestion` prompt is not a degraded-fleet signal at all — it is the owner
being asked a question in his own window, with his own terminal in front of him,
which is the one situation the alert exists **not** to cover: `fleet-alert.py`'s
header scopes it to *"a leg [that] runs unattended where a prompt stops it until
the owner happens to look."*

**Two further facts, both structural:**

- **The alert set in `ops.md` §3 is declared closed** — *leg blocked and stopped ·
  budget HOLD · a failed spawn · the same failure blocking two units · a dream · a
  parked `suite` task* — and **"a permission prompt" is not in it.** The hook is
  documented only in `fleet-alert.py`'s docstring. The set and the mechanism
  disagree, and the docstring is the only place that would tell you.
- **The hook is `.gitignore`d and not templated.** `.claude/settings.local.json`
  is matched by `.gitignore:12`, is not in `embarch-fleet/templates/.claude/`, and
  `install.py --check` therefore cannot see it. The fleet's only backstop for a
  suspended agent is unversioned, undeployable and unverifiable: a wiped or
  re-cloned settings file loses it silently, and nothing reports the loss. This is
  the same shape as the `CLAUDE.md`-pointing-at-`design.md` defect closed the same
  day — a load-bearing hook that no check can reach.

## Why now

`fleet-alert.py`'s own docstring says widening the alert set *"is how a
notification channel becomes a feed nobody reads"*. That has now happened, from a
single repeating cause, in a channel whose entire alert history is nine false
positives and two tests — a 0 % true-positive rate. The next genuine alert lands
in a feed the owner has been trained to ignore, and the webhook exists precisely
because it is the one thing that buzzes his phone.

## Done when

- [ ] The hook no longer alerts for `AskUserQuestion` — principled, not a
      denylist: `ops.md` §3 forbids a leg asking mid-leg, so the prompt cannot be
      the condition the hook is for. *(This is the light fix and it clears 9/9 of
      the observed noise.)*
- [ ] `ops.md` §3 either lists the permission-prompt alert in its closed set or
      says explicitly that the hook is out of band — the set may not stay silent
      about a live alert source.
- [ ] **Decided, not assumed:** whether the hook should gate on the caller being
      an agent at all (see below), or whether excluding one tool is enough.
- [ ] **Decided:** whether `.claude/settings.local.json`'s hook block moves into
      `embarch-fleet/templates/` so `deploy.py` ships it and `install.py --check`
      guards it — which means splitting the fleet hook out of a file that also
      holds machine-local permissions.

### The fork worth deciding rather than defaulting

**Light** — drop `AskUserQuestion` from the hook. One line, reversible, kills
every observed false positive. Leaves the hook firing for a Bash prompt in the
owner's own window; the channel shows only 2 such messages ever, both deliberate
tests, so the measured cost of that gap is ~0.

**Heavy** — gate the hook on the permission request coming from a subagent, so
the backstop keeps full coverage (including `AskUserQuestion`, if a leg ever does
break §3) and the owner's window is silent whatever it prompts for. The signal
exists — `isSidechain` on the transcript entry — but the hook would have to tail
`transcript_path` and read the last record, which is racy, undocumented, and
executing inside a hook that `fleet-alert.py` requires to stay async and
failure-swallowing. **Not obviously worth it against a defect whose entire
observed population is one tool.**
