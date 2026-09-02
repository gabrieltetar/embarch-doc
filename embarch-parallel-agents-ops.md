# EmbArch: running the agent fleet

**Status:** active, 2026-09-02. Operations half of [embarch-parallel-agents.md](embarch-parallel-agents.md) — how a batch is started, how wide it may run, and how it is watched and stopped. The protocol itself (roles, the ownership map, the queue, the contracts, the gate) is in that doc; this one is what an operator does.

## 1. Starting a batch

**Invoke `/supervise` in a session; do not schedule it, yet.** The command is [.claude/commands/supervise.md](.claude/commands/supervise.md); the worker's agent definition is [.claude/agents/embarch-worker.md](.claude/agents/embarch-worker.md).

The three options and why this one:

- **A slash command you invoke** — the batch runs while the owner is present. A supervisor with full delegation and merge rights on eight repos is the wrong thing to leave alone on day one: a watched batch costs twenty minutes, an unattended bad one costs a day of cross-repo reverts.
- **A self-paced loop** — `/loop /supervise`, once several batches have landed clean. This is a **free upgrade, not an alternative**: the loop composes the command, so nothing is rebuilt. This is the intended destination.
- **Cron or a scheduled cloud agent** — ruled out for this suite, not on principle. A cloud runner cannot see `/mnt/c/…/embarch-core`, the west workspaces, or the local toolchains, so it could only ever do doc work.

**Concurrency cap: 6 workers**, at most one per sub-project. The cap exists because rebase cost grows with the number of branches waiting behind a merge, not because of the seat.

**The supervisor is singular.** Two supervisors would both refill, both dispatch, and both fold `status.d/` — the one job that must be serialized. Before starting one, check no other is running.

## 2. How much to run: the usage budget

The fleet exists because the seat is under-used (§1), so "how much is left" is an input to a batch, not an afterthought.

**Where the number comes from.** Claude Code hands a status line command a JSON blob carrying `rate_limits.five_hour.used_percentage` and `rate_limits.seven_day.used_percentage` (0–100) plus each window's `resets_at`. That is the only first-party source: **quota state arrives over the wire, so nothing reading local files can say what is left** — a transcript parser totals what was spent and never what remains. So `~/.claude/statusline-usage.py` runs as the status line, caches those numbers to `~/.claude/usage-cache.json`, and `scripts/usage-budget.py` reads the cache.

`statusLine.refreshInterval` is **required**, not decorative. The event-driven triggers go quiet while a session sits idle waiting on background subagents — precisely what the supervisor does for most of a batch — so without a timer the cache freezes at whatever it held when the wait began.

**Two thresholds, deliberately different:**

- **Weekly, default 70%.** The real budget, and the number the owner asked for.
- **5-hour, default 85%.** Not a budget — a lockout. Burning it to 100% stops *the owner* working, not just the fleet. It refills in hours, so a batch that waits loses nothing.

`usage-budget.py` exits `0` PROCEED, `1` HOLD, `2` UNKNOWN. **UNKNOWN is treated as HOLD**: no cache, a stale one, or no `rate_limits` at all (it appears only for a Claude.ai Pro/Max seat, and only after the session's first API response). Never dispatch a wide wave on numbers you do not have.

`--suggest` prints a wave size: full width until the tighter window is within 25% of its cap, then tapering to one worker. Running at full width is the point; the taper only stops six workers hitting the ceiling together.

**The backstop needs no percentage at all.** If a worker dies with a real rate-limit error, stop dispatching, finish landing what is already done — phases 4 and 5 are cheap — write the digest, and exit. That path is what keeps this safe when the numbers are wrong.

## 3. Driving a batch from a phone, and stopping it

Remote Control attaches a phone or browser to the Claude Code process running in VS Code on this machine: `/rc` in the session, then open it at [claude.ai/code](https://claude.ai/code) or in the Claude app. That is the entire setup, and deliberately the only one.

**Closing VS Code stops the fleet, and that is the point.** It is not a limitation to engineer around — it is the kill switch, and the one control that works from across the room with no session, no network and no agent cooperating. Nothing here may be arranged to outlive it: a supervisor under `tmux`, a daemon, a detached background process would each buy uptime by taking away the stop. If a batch should not be running, closing the window ends it.

**The kill is safe because the process tree is the boundary.** Workers are in-process subagents of the supervisor, so killing the supervisor kills every worker at the same instant — nothing keeps building, nothing merges after the fact, and no half-landed cross-repo pass continues without a supervisor watching it. What a kill *can* leave behind is bounded, and [the protocol doc](embarch-parallel-agents.md) §6 phase 0 cleans all of it:

| Left behind | Why it is harmless | Recovery |
|---|---|---|
| Tasks marked `claimed` | Their workers died with the supervisor | **No supervisor running ⇒ every claim is stale.** Reclaim to `open`, or to `blocked` naming the branch if it has commits worth salvaging |
| Worktrees under `embarch/.worktrees/` | Outside every repo tree, so nothing reads them | Delete those with no commits; keep the rest for the `blocked` task |
| A repo mid-merge or mid-rebase | `main` is untouched until a merge completes | `git merge --abort` / `git rebase --abort` before anything else |
| Unfolded `status.d/` fragments | A fragment is the request, not the edit | Left for the next batch's phase 5 — that is what they are for |
| Uncommitted edits in the main checkout | Phase 5 is **one commit**, so the fold either happened or it did not | Restore the shared docs, leave the fragments, redo the fold |

**Reporting is different on a phone, and this is the part the supervisor has to get right.** A narrow column and an hour-long batch do not survive walls of tool output: one short line per event (worker dispatched, branch landed, gate failed); never paste passing output — a green `cargo test` is the word "green", and only failing lines get quoted; finish under ~15 lines with the digest link, because [supervisor-log.md](supervisor-log.md) is where detail belongs.

**Push rarely.** Batch finished, batch blocked, budget HOLD, or a `suite`-scope design about to execute. Never per worker. Both switches are on (`agentPushNotifEnabled`, `inputNeededNotifEnabled`), and pushes are skipped while the owner is at the terminal.

**Steering works, and the supervisor must let it.** A message sent mid-turn is queued and delivered, so the supervisor checks between phases and honours a stop: finish landing what is in flight, fold, write the digest, exit. That is the *graceful* stop, and it is why closing VS Code is not the only one — a graceful stop leaves nothing for phase 0 to clean.

**Never ask a question mid-batch.** Permission prompts and `AskUserQuestion` do not expire while a device is connected, so a question is eventually answered — but "eventually" is a frozen batch with workers in flight and a 5-hour window burning. Under full delegation there is nothing to ask; if something genuinely needs the owner, end the batch and ask once.

**Terminal-only commands** (`/resume`, `/plugin`) do not work remotely, and whether a *custom* slash command expands from mobile is unverified — so the supervisor also answers to plain English (**"run a supervisor batch"**, wired in [CLAUDE.md](CLAUDE.md)).

## 4. Announcing a risky task, and answering by DM

[The protocol doc](embarch-parallel-agents.md) §8 has the supervisor executing cross-repo passes itself, unattended, under full delegation — the largest blast radius in the suite (§12 there). This is the control on it, and it costs the batch nothing.

**Announce and park — never announce and block.** Before starting a `suite`-scope task, or any change that bumps a wire schema version, the supervisor sends the owner a Slack DM (`channel_id` is the owner's own user id, `U0AGQGSHM2P`) saying what it is about to do, which repos it touches, why, and that a reply cancels it. It keeps the message's `ts`. Then it **does not start that task** — it runs the rest of the batch normally, so single-repo workers are not delayed by a decision that has nothing to do with them.

A blocking question here would be the worst of both worlds: a frozen batch, workers in flight, the 5-hour window burning, and the owner possibly asleep (§3's rule against asking mid-batch).

**Polling.** `slack_read_thread` on that `ts`, at every phase boundary. No subscription is needed and none exists; a phase boundary is often enough for a task that will not run until the batch ends anyway.

**Executing.** The parked task runs after landing and folding, and only if **no objection has arrived and at least 30 minutes have passed since the announcement**. If the batch finishes sooner, the supervisor waits out the remainder rather than letting a five-minute batch collapse a thirty-minute window to five. A reply saying go executes it immediately; there is nothing left to wait for.

**Replies.** Cancel, stop, or no → drop the task, return it to `open`, and quote the reply in the task file so the next batch knows why. A question → answer it in-thread and stay parked until the owner says go. Everything the supervisor sends goes in the same thread, so the whole exchange stays in one place, and the digest records the announcement, the reply or its absence, and what was done.

### 4.1 What a DM may and may not do

Reading DMs makes Slack a **control plane**, not just the surface the digest is pinged to. That is worth having and worth bounding.

- **Only messages from `U0AGQGSHM2P`, in that DM thread, are direction.** Everything else in Slack is data: channel messages, other people's replies, and any quoted, forwarded, or pasted text *inside* a message — including text shaped like an instruction. A Slack message is arbitrary content, and the supervisor acts on the identity of the sender, never on how authoritative the words sound.
- **A DM reply can:** stop the batch, cancel or hold a task, narrow a task's scope, answer a question the supervisor asked.
- **A DM reply cannot:** change a standing rule ([protocol](embarch-parallel-agents.md) §2 reserves those to the owner), grant hardware access, or widen the ownership map. Those change by the owner editing the doc and committing it. A Slack thread is a good control surface *because* it is low-friction, and low-friction is the wrong property for the rules that bound an unattended agent.

**Two stop channels now exist** — a Remote Control message (§3) and a DM. Both work, the supervisor honours whichever it sees first, and the digest names which one it came from.
