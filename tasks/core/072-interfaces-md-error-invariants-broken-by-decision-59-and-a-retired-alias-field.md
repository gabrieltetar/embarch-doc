# 072 — `interfaces.md`'s two error invariants were broken by decision 59, and `result-layout.md` still lists a retired `alias` field

**State:** claimed by agent/core/072-interfaces-error-invariants, 2026-09-17 01:50
**Source:** leg 133's refill census of `embarch-core`, findings 3 and 4 of four —
`tasks/core/071` carries the other two. **Filed so they survive**: they existed only in a census
report, and `supervisor-log.md` folds daily and rolls into `log-archive/`.
**Scope:** core
**Hardware:** none. Both are settled by reading Rust. **Do not run a live Core, do not attach a
probe, do not issue an HTTP request to anything** — item 1 is about which handler constructs which
body, not an observation of a response.
**Owner:** no

**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` is **11,356/12,288 B (932 B left)**,
filed as `tasks/core/046` and blocked — **do not write into it.** Nothing else of core's is in
reserve. Check `python3 scripts/check-doc-size.py --pressure` before and after; if you push a file
into the band, file `tasks/core/<NNN>-compact-core.md` in the same commit.

**Every coordinate below came from a census pass.** Re-derive each line you act on and correct the
record in your report where it has drifted. **"This does not hold" is a correct outcome.**

## 1 — Following `interfaces.md` reproduces exactly the mis-routing decision 59 was written to stop

Three doc sentences:

- `embarch-core/interfaces.md` (reported line 10): *"**Errors are plain text, not JSON**, on every
  non-2xx: the full `anyhow` chain … **Parse JSON only on 2xx.** … so an error's *kind* is available
  only as its HTTP status, and the status codes above are the whole vocabulary a caller can branch
  on."*
- `embarch-core/interfaces.md` (reported line 13): *"**`503` means `hw_lock` was contended and the
  wait timed out** (decision 14, built `tasks/core/013`)"*.
- `embarch-core/spec.md` (reported line 35) carries the first one too: *"**Errors are plain text on
  every non-2xx**, so an error's *kind* is only its HTTP status."*

**The code ships a JSON body on a non-2xx from one route.** `src/api.rs`'s `validate_handler`
(reported 1090–1108) returns, on a `TopologyMismatch`,
`Ok((status, Json(ValidateMismatchResponse { ok, kind, … })).into_response())` — **JSON on a 409 and
on a 503**. The status comes from `classify_topology_mismatch` (reported 1043–1051):
`if m.live_hardware_id.is_none() { (StatusCode::SERVICE_UNAVAILABLE, "not_attached", None) } else {
(StatusCode::CONFLICT, "mismatch", …) }`. A second plain-text 503 with the same *"not attached"*
meaning comes from `describe_topology_error` (reported 201–208), used by `/flash`, `/reset` and
`study.rs`'s handshake gate. The handler's own comment (reported 1083–1089) states the exception
plainly: *"with the full structured fields as its JSON body, never collapsed into plain-text `500`
prose the way an unrelated I/O error still is below."*

**What it costs a reader — and it is the precise failure decision 59 exists to prevent.** A client
written to `interfaces.md` (a) does not parse the body of a non-2xx, so never sees `kind`, and (b)
reads `503` as *lock contention, retry shortly*. Point it at a bench with the board unplugged and it
**retries forever against a condition whose whole meaning is "go plug in a cable"** — while
`interfaces/topology.md` (reported line 15) in the same directory instructs the opposite:
*"decision 59: distinguished by `kind`, never by parsing `reason`"*. Two docs a caller is equally
likely to open give contradictory integration instructions, and the older, more prominent one — the
index's own status vocabulary — wins by default. `interfaces.md` line 10's parenthetical is also
false on its face: it asserts the status codes are *"the whole vocabulary a caller can branch on"* at
the same moment `/validate` ships a `kind` field for the express purpose of being branched on.

**Do not assume `tasks/core/041` already covered this.** `041` (done) fixed the *rendered sentence*'s
leading clause and added `kind`; the census reports it did not touch `interfaces.md`'s status
vocabulary or the plain-text invariant, and `041`'s own text does not mention either line. **Verify
that before you write anything** — if `041` did cover it, this item does not hold and saying so is
the right outcome. `tasks/core/037` / decision 55 settled that no `code` enum exists, which is
orthogonal.

**Resolve it for all three doc sites or none** — `interfaces.md` 10, `interfaces.md` 13, and
`spec.md` 35. A half-corrected invariant is worse than either side, and `spec.md` is the file a
reader is told to trust absolutely.

## 2 — `result-layout.md` lists `alias` as a field of `streams/index.json`; the code retired it with the routes that needed it

`embarch-core/interfaces/result-layout.md` (reported line 14):

> `index.json`       per tap: id, name, files, encoding, **alias**, rendered, note, named, timed,
> self_excluded, source_deferred

`src/stream_store.rs`'s `pub struct StreamIndexEntry` (reported 164–245) carries `id`, `name`,
`raw_file`, `rendered_file`, `arrival_file`, `encoding`, `note`, `named`, `timed`, `self_excluded`,
`source_deferred` — **no `alias`.** The same file says why (reported 147–149, `StreamIndex`'s doc
comment): *"It was originally motivated by a second job as well — resolving the three fixed-channel
aliases (`/power-data`, `/waveform-data`, `/gatt-data`) to whichever tap answered each. **Those
routes are retired, and the `alias` field with them**"*. `grep -n alias stream_store.rs study.rs` is
reported to return only that retirement note, one comment about a vanished `alias_for` import
(reported ~873), and `study.rs` (reported ~5074, *"The aliases are gone"*).
`StreamIndexEntryResponse` (reported 2897–2935) is reported clean and matching
`interfaces/studies.md`.

**What it costs a reader.** This is the only doc describing the on-disk index, and `index.json` is a
file a person opens by hand when a trace rendered wrong. The list is what tells them whether a field
they *don't* see is missing or was never there; `alias` sends them looking for a field removed
deliberately, and it is the one entry on the line that corresponds to nothing.

**This is the residue of a fix, not a duplicate of one.** `tasks/core/043` (done) rewrote this exact
line — it added `named`/`timed`/`self_excluded`/`source_deferred` and left `alias` standing.
Lower value than item 1 because nothing branches on it.

## Done when

- [ ] Item 1 is **fixed across all three doc sites** or **reported as not holding**, with `041`'s
      actual diff checked rather than assumed.
- [ ] Item 1's wording says what is true of *both* shapes: which routes return plain text and which
      single route returns a structured body, and that `503` now carries two distinct meanings
      (`hw_lock` contention, and `/validate`'s `not_attached`). **Do not "fix" it by deleting the
      plain-text guidance** — it is correct for every other route and a caller needs it.
- [ ] Item 2's line is corrected or reported as holding.
- [ ] Nothing is "fixed" on the strength of this task's own description. Every change rests on a line
      you read.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build --all-targets`, `cargo test`, `cargo clippy --all-targets -- -D warnings`
      in `embarch-core`, and `python3 scripts/check-docs.py` in `embarch-doc`.

## Not yours

**Do not change any handler, status code, response shape or error rendering.** Both items are doc
corrections restating what the code already does. Making `/validate` plain text, or making every
route structured, is a wire-surface change with consumers in `embarch-api`, `embarch-ui` and the user
guide — out of scope, and a supervisor-announced change even for the fleet. If you conclude the code
is what should move, drop it in `inbox/` (absolute path
`/home/gabriel/Github/embarch/embarch-doc/inbox/`).

**Do not write a new numbered decision, and do not amend decision 12 or 59.** These are corrections
restating shipped behaviour, so they record no choice. The census did note that decisions 12 and 59
sit in one file without cross-referencing each other; **if you think one needs a pointer to the
other, that is a legitimate small edit** — say so explicitly in your report and keep it to a
cross-reference, not a restated rationale.

**Do not touch `decisions/auth.md`** — in reserve, parked under `tasks/core/046`.

**Do not do `tasks/core/071`'s two items** — decision 32's rejected-versus-shipped sector erase and
`hardware::flash`'s chip-erase doc comment. Separate unit, may be in flight.
