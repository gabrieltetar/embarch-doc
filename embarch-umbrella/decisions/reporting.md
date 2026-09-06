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

**Unverified live.** A healthy run here should print `study_results/ at /mnt/c/ProgramData/embarch/study_results: 50 entries, …`, with the same string under `--json`'s `checks[15].path`.
