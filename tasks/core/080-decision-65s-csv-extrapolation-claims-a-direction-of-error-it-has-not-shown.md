# 080 — Decision 65's CSV-size extrapolation names one source of bias and omits a larger one

**State:** done — leg 138 unit 3, 2026-09-17, `agent/core/080-decision-65-extrapolation-direction`.
Drained from `inbox/core-decision-65-size-extrapolation.md` by leg 138 at `core/076`'s fold,
2026-09-17; body unchanged apart from this line, the number and the notes below.

**Supervisor dispatch note 1 — this is prose, and the code is fine.** `core/076` landed 90 minutes
ago (code `ef60321` in `embarch-core`, doc `e0d54e6`) with a green gate I re-ran myself. The reviewer
that raised this checked the route, its tests and the `/load`-unchanged property explicitly and found
them sound. **Expect your code branch to carry zero commits** and push it anyway so I have it to
land; that is the right instinct, not a failure.

**Supervisor dispatch note 2 — I am not telling you which way to resolve it.** The `Done when` list
offers two routes (drop the directional claim, or back it with an argument that addresses the
lane/name-mix gap) and both are legitimate. A third is open to you: re-measure something that closes
the gap — if a second fixture or a renderable capture with a different lane/name profile exists in
this repo, measuring it would turn an argument into evidence. **Do not manufacture one**, and do not
touch hardware. Say what you chose and why.

**Supervisor dispatch note 3 — doc-size reserve for `core`.** The file you are editing,
`embarch-core/decisions/stream-index.md`, is **10,941/12,288 B (1,347 B left)** — not in reserve but
close, and decision 65 is already the longest entry in it, so prefer rewriting its existing sentence
over appending a qualifying one. Two `core` files *are* in reserve and neither is yours to touch
here: `decisions/surfaces.md` 11,253/12,288 B (1,035 B left, filed as the blocked
`tasks/core/079-compact-core.md`) and `decisions/auth.md` 11,356/12,288 B (932 B left, filed as the
blocked `tasks/core/046-compact-core.md`). If your work pushes a file into the reserve, or leaves one
there that nothing has filed, file `tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** embarch-reviewer on `core/076` (code merge `ef603210f88a407efdf68b215e89349656ec69b7`, doc merge `e0d54e642ff144c08fae1f13b4b8e860b9fc6305`) — directed check from the reviewing supervisor, re-deriving decision 65's fixture measurement
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`embarch-core/decisions/stream-index.md` decision 65 measures the checked-in
real-firmware fixture at 43,573 B / 831 rows = 52.367 B/row, extrapolates
linearly to the reference capture's 225,627 rows to get ≈11.8 MB, and calls
this "likely-low ... understating a populated capture's row width" because
the fixture's `rx_utc_ms` column is empty throughout. The reviewer re-rendered
the same fixture (`tests/fixtures/outpost-native-sim.bin` +
`outpost-native-sim-manifest.json`) via a scratch test and reproduced the
headline numbers: 43,573 B / 831 rows, 52.434 B/row (the decision's 52.367
looks like an off-by-one denominator, immaterial). `rx_utc_ms` is confirmed
empty in all 831 rows.

Two things the decision's text does not surface, both bigger than the
`rx_utc_ms` gap it names:

- **Row width is not constant even within the sampled fixture** — line
  lengths (excluding the header) range from 22 to 67 bytes around a 51.4-byte
  mean, a ~3x spread. Linear extrapolation from one average implicitly
  assumes the *mix* of row kinds/name lengths generalizes to the target
  profile, which is a much stronger assumption than "row width is roughly
  constant."
- **The fixture and the reference profile are structurally different
  captures, not just different lengths.** The fixture is a 4-lane
  native-sim scenario (`kind_counts`: gap 3, idle 75, isr_enter 75,
  isr_exit 74, marker 155, thread_create 6, thread_name 2, thread_switch_in
  220, thread_switch_out 221; only 7 distinct names total — `main`, `idle`,
  `outpost_ping`, `outpost_pong`, `BURST`, `WORK_BEGIN`, `WORK_END`) versus
  the reference's 26 lanes / 112,804 spans (decision 18,
  `embarch-ui/decisions/trace-transfer.md`). A capture with ~6x the lane
  count plausibly has a different mix of event kinds and materially
  different (very possibly longer) name strings, which can move average
  bytes/row in either direction by more than the `rx_utc_ms` column would.

So "likely-low" asserts a specific direction for the estimate's error while
naming only the smaller, one-directional cause and leaving the larger,
direction-unknown one (lane/name-mix mismatch between a 4-lane synthetic
fixture and a claimed 26-lane real capture) unacknowledged. This doesn't
necessarily flip the conclusion — 11.8 MB and 12.6 MB are close enough that
even a 2-3x correction either way stays "same order of magnitude," so
decision 64's underlying call (serve the spans) is probably still fine — but
the specific evidentiary claim in decision 65 ("likely-low ... understating")
is not established by what's in the fixture, and reads as more certain than
the measurement supports.

## Why now

Decision 64's whole cost argument rests on the spans being "the same order
of magnitude" as the CSV that already crosses the Core↔`embarch-ui` call;
decision 65 was written specifically to source that number, since nobody had
before. If its own sourcing overclaims a direction it hasn't shown, that
weakens the one number this two-decision chain rests on for anyone who reads
decision 65 as confirmation rather than as a rough sanity check.

## Done when

- [x] `embarch-core/decisions/stream-index.md` decision 65's "likely-low"
      language either drops the directional claim (state the estimate as
      "order-of-magnitude, direction of error not established" rather than
      "likely-low") or is backed with an argument that addresses the
      lane/name-mix gap between the fixture and the reference profile, not
      only `rx_utc_ms`. **Chose the drop-the-claim route** (dispatch note 2's
      first option): no second fixture with a different lane/name profile
      exists in this repo to measure instead (only
      `tests/fixtures/outpost-native-sim.bin`, the same one already used),
      and dispatch note 2 explicitly rules out manufacturing one. The
      replacement sentence states the estimate as order-of-magnitude with
      direction of error not established, and names all three factors: the
      `rx_utc_ms` gap the old text already had, the ~3x row-width spread
      within the fixture itself (22–67 B around a 51.4 B mean), and the
      4-lane/7-name vs 26-lane/112,804-span structural mismatch with the
      reference profile. The "holds: same order of magnitude" conclusion
      (decision 64 unaffected) is unchanged.
- [x] No code change implied — `core/076`'s route, tests and the `/load`
      byte-for-byte-unchanged property are all fine as landed; this is a
      documentation-precision fix only. Code worktree carries zero commits,
      as expected, and is pushed anyway.
- [x] Gate green (`../../embarch-fleet/protocol.md` §10). The edit pushed
      `stream-index.md` from 10,941 B into reserve (11,172/12,288 B, 90.9%)
      because the honest replacement needed more words than the false one it
      replaced — filed as `tasks/core/082-compact-core.md` in this same
      commit, per protocol §5 item 5. **Filed by the worker as `081` and
      renumbered to `082` by leg 138 at the fold**, because the supervisor's
      own refill sweep had taken `081` in the same twenty minutes; see that
      file's header.
