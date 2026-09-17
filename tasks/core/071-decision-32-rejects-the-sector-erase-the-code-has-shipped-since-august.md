# 071 — Decision 32 records sector-erasing the NVM regions as *rejected*, and it is what `hardware.rs` has shipped since 2026-08-25

**State:** claimed by agent/core/071-sector-erase-decision-32, 2026-09-17 01:25
**Source:** leg 133's refill census of `embarch-core`'s docs against its source. **Filed so it
survives**: it existed only in a census report, and `supervisor-log.md` folds daily and rolls into
`log-archive/`, so anything living there alone is on a timer. Nothing dispatches from a log entry.
**Scope:** core
**Hardware:** none. Everything below is settled by reading Rust and git history. **Do not flash
anything, do not attach a probe, and do not run a live Core** — the subject is what the code does,
not an observation of it, and the one family this could brick is the family decision 36 routes away
from this code path.
**Owner:** no

**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` is **11,356/12,288 B (932 B left)**,
filed as `tasks/core/046` and blocked. Nothing else of core's is in reserve. `decisions/flashing.md`
— which you will be writing into — has room; check `python3 scripts/check-doc-size.py --pressure`
before and after, and if you push a file into the band, file
`tasks/core/<NNN>-compact-core.md` in the same commit.

**Every coordinate below came from a census pass.** The census read the code and quoted it, but
**you re-derive each line you act on** and correct the record in your report where it has drifted.
The *shapes* are what this task asserts. **"This does not hold" is a correct and welcome outcome.**

## 1 — The decision and the code say opposite things, and the code is the older of the two

`embarch-core/decisions/flashing.md` (reported line 23) records, as the rejected alternative:

> *"Rejected, and it was the option already written and compiling:* sector-erasing the declared NVM
> regions — **another EmbArch-authored guess about what a Nordic part needs erased, the same class of
> guess that produced the brick.**"

`src/hardware.rs`'s `pub fn flash(...)`, the `if erase { … }` block (reported 205–251), collects
every `MemoryRegion::Nvm` range from `session.target().memory_map` and loops
`flashing::erase(&mut session, &mut progress, start, end, false)` over each. Its own comment
(reported 222) argues *for* the rejected option:

> *"Sector-erasing the declared NVM regions gives the semantics anyone actually wants from `--erase`
> … without going near `pc_erase_all`."*

**The provenance is the load-bearing part and the census checked it**: `git log -L 205,251:src/hardware.rs`
gives one commit, `62ef241` (2026-08-25, *"core: stream pipeline in study.rs, sector-erase in
hardware.rs"*) — the same date decision 32 cites for its own measurement — added, never reverted. On
the doc side `git log -S` on the "Rejected" sentence first hits `c767f8d` (2026-09-02, the four-file
migration), so **the sentence was written a week after the code it denies landed.** It was wrong from
birth rather than overtaken. `grep -rn 'sector-eras'` across `embarch-core/`'s docs returns only that
line — nothing retracts it. **Re-run both history commands yourself**; if either disagrees with the
above, that changes which side is stale and you should say so instead of proceeding.

**What it costs a reader.** Decision 32 is what someone opens to answer *"is `erase=true` safe on a
new part?"* It currently answers *"EmbArch does not erase sectors itself; that guess was rejected"* —
when EmbArch does exactly that on every probe-rs-backed family. The thing that narrows the blast
radius is `decisions/flash-backend.md` 36 routing nRF54L/nRF54H to a vendor tool, so the bricking
family never reaches this block — **and that is not written anywhere as the reason sector-erase became
acceptable**, so a reader cannot recover the real posture from the docs at all.

**The judgement is yours and I want the reasoning, not just the verdict.** Amending decision 32 to
record sector-erase as *adopted, confined by decision 36* is the likely answer, but establish it:
read decision 36's body and `flash_backend.rs`'s `requires_vendor_tool` (reported ~100–145) and
confirm **no probe-rs-backed family in `SOC_TO_CHIP` has the RRAM shape** before you write that the
confinement holds. If one does, the finding is larger than a doc correction and you should stop and
say so rather than widen the change yourself.

## 2 — `hardware::flash`'s own doc comment says `erase` is a full chip erase, and `api.rs` cites that sentence as its authority

`src/hardware.rs` (reported 152–154):

> *"`erase` requests a **full chip erase** before writing, rather than erasing only the sectors the
> image covers (probe-rs's default, and what `download_file` alone does)."*

Fifty lines down, the same function says the opposite — `hardware.rs:206`, *"Deliberately NOT
`DownloadOptions::do_chip_erase` (nor `flashing::erase_all`, which routes to the same place)"*, and
`hardware.rs:240`, the bail when no NVM region is declared, *"refusing to fall back to a chip erase,
which is what bricks some targets"*. A test pins the code's side: `flash_backend.rs` (reported
656–666) `no_backend_maps_erase_to_a_full_chip_erase` asserts `!script.contains("erase_chip")`, and
the vendor path maps `erase` to `chip_erase_mode=ERASE_RANGES_TOUCHED_BY_FIRMWARE` (reported ~392–395)
under a comment calling it *"deliberately never a full chip erase"* (reported ~359).

**It has already propagated into the HTTP surface.** `api.rs` (reported 295–297), the `erase` field on
the `/flash` request struct, repeats the claim *and points at the stale sentence as its explanation*:

> *"Full chip erase before writing, rather than erasing only the sectors the image covers
> (`hardware::flash`'s own doc comment has why that distinction matters). The equivalent of
> `west flash --erase`."*

**What it costs a reader.** These two doc comments are the only API-level description of what
`erase: true` does, and they promise a strictly larger operation than the code performs. The
difference is observable: a region probe-rs's target description does not declare as NVM **survives**
a `POST /flash {erase: true}`, and on a target declaring no NVM region at all the call is **refused**
rather than performed. Someone debugging *"I set `erase` and stale state survived"* reads the doc
comment, concludes the erase failed or the probe lied, and goes looking at the board.

**One thing to get right rather than tidy.** `interfaces/hardware.md` (reported line 10) is already
correct on the behaviour — *"`erase` never becomes a chip erase in any backend (decision 32)"* — **but
it cites decision 32 for a claim decision 32 does not make.** Decision 32 rejected *both* arms of the
feature as written; it did not conclude "sector, not chip". Fix the citation as part of this item;
do not leave a correct sentence resting on a wrong reference because the sentence reads fine.

## Done when

- [ ] Item 1 is resolved with its history re-derived, and the outcome states **explicitly** whether
      decision 32 was amended (and to say what) or whether the census's reading of the history was
      wrong.
- [ ] Item 1's write-up says whether decision 36's confinement was **verified against
      `SOC_TO_CHIP`** or merely assumed. If you could not verify it, say so and do not assert it.
- [ ] Item 2's three sites — `hardware.rs`'s doc comment, `api.rs`'s `erase` field comment, and
      `interfaces/hardware.md`'s decision-32 citation — are each corrected or each reported as
      holding. **All three or none**: a half-converted description is worse than either side, and
      `api.rs` explicitly delegates its explanation to the other one.
- [ ] Nothing is "fixed" on the strength of this task's own description. Every change rests on a
      line you read.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      in `embarch-core`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

**Do not change what `flash` does.** No new erase mode, no removal of the sector-erase block, no
touching `flash_backend.rs`'s vendor arm. If the honest conclusion is that the *code* is what should
move, that is a finding for `inbox/` and a follow-up task, not a change to make here — it is a
flashing behaviour on hardware nobody in this fleet can exercise, and `decisions/flashing.md`'s whole
subject is a part that was once bricked by a guess.

**Do not write a new numbered decision for item 2.** It is a correction restating what the code always
did, which records no choice. Item 1 may need decision 32 *amended*; amending an existing decision to
match shipped behaviour is in scope, authoring a new numbered decision is not — if you conclude one is
genuinely needed, drop it in `inbox/` with your reasoning instead.

**Do not touch `decisions/auth.md`** — it is in reserve and parked under `tasks/core/046`.

### Also found by the same census, filed separately — do not do these here

`tasks/core/072` carries two more findings from this pass (`interfaces.md`'s plain-text-errors and
`503`-means-contention invariants versus decision 59's structured `/validate` body, and a retired
`alias` field still listed in `interfaces/result-layout.md`). Leave both alone.

### Claims the same census checked and found the code honours — do not re-sweep these

Recorded so this unit does not re-spend budget. **Second-hand, so do not cite them as verified
either** — they are "nobody found a problem here", not "proven correct": `build_router`'s 23 route
registrations against all six `interfaces/*.md` tables; `StatusResponse`'s field set against
`interfaces/hardware.md`; `spec.md`'s CLI subcommand list against `main.rs`'s `enum Command` (11 for
11); every value in `interfaces/constants.md` against its constant (`HW_LOCK_WAIT_MS` 500,
`WATCHDOG_GRACE_MS` 10_000, `RESET_PULSE_MS` 50, `MAX_DURATION_MS` 10_000, `DEFAULT_MAX_BYTES` 1 MiB,
`DEFAULT_STREAM_MAX_BYTES` 32 MiB, `DEFAULT_STUDY_RESULTS_KEEP` 50, `MAX_UNDECODABLE_FRAMES` 10, both
baud rates 1 Mbaud, `max_log_files(7)` in both places); the *"`400` checked before `hw_lock` is
taken"* claim on `/serial-log`; and decision 14's 503-with-holder, which `decisions/platform.md` 32
correctly records as built.
