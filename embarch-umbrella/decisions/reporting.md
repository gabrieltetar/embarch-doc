# embarch-umbrella decisions: What `doctor` reports

**Status:** active, 2026-09-06.

**Split out of [doctor.md](doctor.md) on 2026-09-05, entries moved verbatim.** That file's mission is *what is checked*; these three are *what a consumer reads back*, which is a different reader and a different contract — a UI breaks on this group and a bench engineer on that one.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md), whose check table owns which checks carry which field.

### 11 — `doctor` and `status` are split by cost, and both carry `--json`

`status` is one Core call — **cheap enough for a UI or a shell prompt to poll.** `doctor` is the full chain including filesystem checks and a build-command resolution, **far too heavy to poll.** The JSON shape on both is the contract a UI consumes, **and it exists in v1 specifically so the UI does not arrive and find only human-formatted text to scrape.**

### 37 — A check may carry a machine-readable `code`, because `status` cannot hold every state a check distinguishes

Decision 23 asks check 10 to report success, failure and timeout **distinctly**, and decision 11 makes `--json` the contract a UI consumes. Those two together do not fit in three statuses: registered-but-broken and registered-but-hanging are both Fail, and the only thing separating them was an English sentence in `detail`.

So `Check` grows an optional `code` — a short stable identifier, `null` for every check that has nothing to add. **Never derived from `detail`**, which is written for a human and is free to be rephrased; a consumer that had to match on it would break on a wording change.

**Which checks carry one is [../spec.md](../spec.md)'s table's job, not this entry's.** The roster that used to sit here went stale within a day of check 5 landing, and correcting it only restarts that clock. The durable half is the *test* a check has to meet, which is why checks 5 and 22 were named the obvious next ones — both exist to split states that share a status. **More states than statuses earns a code**; everything else stays `null`.

**A code's referent is as much of the contract as its spelling.** Renaming one breaks a consumer loudly. Keeping the name and moving what it means breaks the same consumer silently — the one that did exactly what this decision asked and matched on the code — and no check in the gate can see it. So a code kept for a state that *replaced* the old one is recorded as a deliberate reuse in the decision that moved it. **Two so far:** check 10's `no-cli` ([decision 40](mcp.md)), and check 17's `bind-too-narrow`, kept for the strictly narrower state left when the loopback hit stopped counting as evidence ([decision 22](bind.md)).

**And the test is the decision's written referent, not the set of machines that happened to match.** Asked because 2026-09-06 applied this entry two ways in one commit: `bind-too-narrow` was recorded as a reuse for narrowing, while `bound-narrow` and `bind-too-narrow` *both* narrowed again in the same commit — the `remote` sub-case guarded out from under them ([decision 22](bind.md)'s `bind-elsewhere`) — and neither was. **The settled reading: a record is owed where a code keeps its spelling for a state that *replaced* the one its decision described, and is not owed where a fix stops it firing on states that decision never described.** The first moves the referent and breaks a matching consumer silently; the second restores it. `bind-too-narrow`'s narrowing was the first — the loopback hit *was* the state the check shipped with and deliberately stopped being. The `remote` guard was the second: check 17 compared what this topology needs against evidence about **this** machine's Core from the day it shipped, and a `remote` machine's Core is another computer's, so `remote` was never inside either code's referent — the predicate merely had no guard saying so. **The mechanical form: if closing the change means rewriting the entry's description of what the code names, it is a reuse; if the description already excluded what you removed, it is a bug fix.** Under it the count above stays two. A change to a check's `fix` text is never a reuse at all — `fix` is prose for a human, and nothing is contracted to match on it.

**Check 10's seven**, the set that forced this: `handshake-ok`, `handshake-failed`, `handshake-timeout`, `no-handshake` (the handshake was never attempted — reported as itself rather than defaulting to a pass), `not-registered`, `unreadable-entry`, `no-cli`.

**Additive on the wire**: the key is always present, so nothing has to tell "absent" apart from "no code", and every existing consumer of `--json` keeps working.

### 39 — A check that resolves a directory prints which one, in `detail` and as a `path` field

Check 16 reported `study_results/: 50 entries, 809.0 MiB` and **named no directory**, while its own build-directory half printed every root it counted. So the one check whose job is to resolve a machine-wide data directory was the one you could not tell had resolved the right one: confirming it on the primary topology took a live run plus a hand `du`, and the answer went nowhere afterwards.

The path goes **both** places, for two readers. `detail` reads `study_results/ at <path>: …`. `--json` gets a `path` field beside `code` — `null` elsewhere, always present, never derived from `detail`, for decision 37's reasons. **One path, not every path a check mentions:** check 16's per-project build roots are several and already in `detail`, and a field that is sometimes a list is one a consumer must branch on.

**The `%ProgramData%` caveat surfaces only when the directory is absent.** `setup::data_dir_for` hardcodes `/mnt/c/ProgramData/embarch` for `wsl-host` — a *stronger* assumption than [../../embarch-token.md](../../embarch-token.md) §5's last gap records, whose stated mitigation is resolving the real value from the Windows side, which token discovery does and this does not. A relocated `ProgramData` therefore reads as "nothing yet at …", indistinguishable from a machine that never ran a study, so that arm says the path is assumed. Where the directory exists and holds runs it is self-evidently right, and the sentence would be noise on every healthy run.

**Verified live** [measured 2026-09-06, `embarch doctor` and `embarch doctor --json` on the primary `wsl-host` bench]: `detail` read `study_results/ at /mnt/c/ProgramData/embarch/study_results: 50 entries, 802.9 MiB`, and `checks[15].path` carried that same path as its own field. Both **placements** hold on a real machine. The `%ProgramData%` caveat above was not exercised — the directory existed and held 50 runs.

### 43 — The one-line message rule is a runtime property, and the guard only sees text this module authored

Every `detail` and `fix` is **one line with no run of two or more spaces.** The rule exists because of what Rust does to a long string literal wrapped without a trailing `\`: the continuation's indentation stays *inside* the sentence, so the defect renders as a run of spaces mid-word and compiles, tests and ships. A `contains` assertion reading one side of the wrap does not catch it, which is how check 14 shipped it twice.

`no_check_renders_a_run_of_two_or_more_spaces` holds every verdict the **pure judges** emit to a fixture corpus, and pins its exemption at exactly one check — check 6, whose `{e:#}` of a `toml` parse error is foreign text with a caret diagram whose layout is not ours to police.

**The pinned exemption is a statement about the fixtures, not about the program**, and on 2026-09-06 a live run showed the difference. Check 1 renders foreign text too: `binary_version` interpolates `embarch-core --version`'s **stdout** into `detail` verbatim, and the deployed Core prints a multi-line `Caused by:` chain there when it cannot open its log directory. The rendered `detail` carried newlines, multi-space runs **and raw ANSI escape sequences**, in `--json`, while the guard was green — because the corpus hands check 1 a version string that is a version string.

So the durable statement is not "check 6 is the only check that renders foreign text". It is: **any check that interpolates another program's output can break this rule at runtime with the guard green.** And the exemption is narrower than even that comment claims: the guard pushes to `verbatim` only when the text contains a **newline**, so what it actually exempts is *checks whose fixtures contain a newline* — **foreign text carrying a multi-space run and no newline is an offender today**, exempted by nothing and caught by nothing. Closing the gap is a normalisation at the point of interpolation — one line, escapes stripped — not a wider exemption; a wider exemption is how a green test comes to be believed to cover more than it does. Filed as `tasks/umbrella/031`; the stdout half is `embarch-core`'s and is `tasks/core/015`.

**`open.md`'s previous statement of this gap named checks 4 and 12** — the two `async` checks with no pure judge — and that remains true and is a *different* gap: those checks' text is never tested at all, where check 1's is tested against text it does not carry in the field.

### 46 — `status` authenticates for the probe count spec.md promises; no-token is its own state

`spec.md`'s `status` row always promised "how many probes," but the binary never asked: it made only `embarch-topology`'s unauthenticated `GET /status`, which classifies `200`/`401` and reads no body, and printed a static `auth: not checked` line citing a `milestone-6.md` that no longer exists. `--json` carried `reachable`/`base_url`/`topology`/`authorized`/`attempts` and nothing about probes.

**Chosen: make `status` do what the row says.** It now makes one more authenticated `GET /status` at the winning candidate — `token::resolve_token`, then the `probes` array's length, exactly as `doctor` checks 4/5 already do. `doctor.rs`'s `authed_get`/`DEVICE_SCAN_GET_TIMEOUT` move to `pub(crate)` for that reuse; `doctor` itself is unchanged. **Rejected: shrinking the row instead** — a poll-friendly `--json` (decision 11) that can never carry a count is the worse contract, and the fix is one proven call, not new infrastructure.

**Six states, not a wider zero:** `ok` (a count), `unreachable` (no candidate was Core), `no-token` (resolution failed), `unauthorized` (`401`), `request-failed` (the call itself didn't return — timeout, drop, or a non-`200`/`401` status), `bad-response` (the call *did* return `200`, but the body carried no `probes` array). `--json`'s new `probes` field is always `{state, count, reason}`, `count` non-null only for `ok` — so a real zero and "wasn't allowed to look" never share a value. Human `status` prints the same distinction.

`status` has no `--config`, so it resolves with `token::resolve_token(None, None)` — no `[core].token`/`token_env` override, the same gap `doctor`'s own config-less callers already have.

**Amendment (task 039): `bad-response` split out of `request-failed`.** The original fold (`5c92ea0`) fixed the `Count(0)` collapse but folded the malformed-`200` case into `request-failed`'s label. That label is what a `--json` consumer switches on to decide whether to retry, and retrying a `200` that Core keeps answering the same way is exactly wrong — the request didn't fail, Core answered and said something unexpected. `bad-response` is now its own state; `request-failed` keeps its narrower meaning: the call itself didn't come back with an answer to read.
