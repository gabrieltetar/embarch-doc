# 076 — Three more `embarch-umbrella` doc-versus-code contradictions, from the same census that produced 075

**State:** done — 2026-09-17. All three items resolved — item 1 as a code change (`src/doctor.rs`,
decision 53), item 2 as a doc correction (`open.md`), item 3 as a code change across `deploy.rs` and
`setup.rs`'s `up`/`down`/`uninstall`/`apply_plan`. `open.md` crossed into doc-size reserve while
fixing item 2; filed as `tasks/umbrella/077-compact-docs.md` (open, not blocking).
**Source:** leg 132's own refill census of `embarch-umbrella`'s docs against its source — the same
pass that produced `tasks/umbrella/075`. **Filed so they survive**: they existed only in a
supervisor's report, and `supervisor-log.md` folds daily and rolls into `log-archive/`, so anything
living there alone is on a timer. Nothing dispatches from a log entry.
**Scope:** umbrella
**Hardware:** none for items 1 and 3 — reading Rust and correcting prose. **Item 2 is settled by
reading code too**, not by running `doctor`: the point is what the code *would* do under mirrored
networking, not an observation of it. No board, no probe, no live Core, no deploy.
**Owner:** no

**Doc-size reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` is **11,533/12,288 B
(755 B left)**, filed as `tasks/umbrella/009` and blocked. Everything else of umbrella's has room.
Run `python3 scripts/check-doc-size.py --pressure` before and after; if you push a file into the
band, file `tasks/umbrella/<NNN>-compact-docs.md` in the same commit.

**Every coordinate below came from a census pass and has not been re-read.** Verify each before
acting on it, and correct the record in your report where it has drifted. The *shapes* are what this
task asserts; the line numbers are a starting point. **Any of the three may turn out not to hold —
reporting that is the correct outcome.**

## 1 — Check 5's USB scan is gated on check 3's winner *class*, not on which machine Core is on

`doctor.rs` (reported ~3262) does `let usb_scan = usb_scan_for(core_probe.winner_class);`, and
`usb_scan_for` (reported ~862–872) scans `/sys/bus/usb/devices` whenever the winner is `Local`.

`decisions/doctor.md` 18 grounds that gate in *"Core must be enumerating on **this** machine"*. But
`decisions/topology.md` 30 records that under WSL2 mirrored networking **a Windows-hosted Core and a
WSL2-guest-hosted Core both answer at loopback, so a `local` classification does not say *where*
Core is.** Nothing guards that case — even though the driver already computes `core_belongs_to(...)`
a couple of statements earlier (reported ~3249) for exactly this reason, for checks 1 and 14.

Consequence on a mirrored-networking bench: the guest's bus is scanned on Core's behalf and check 5
emits `no-probe-found` — *"genuinely nothing plugged in"* — a **confident verdict about the wrong
machine**, which is the thing decisions 18 and 31 say the check refuses to do.

**This is the strongest of the three and also the one with a real judgement in it.** Mirrored mode is
unexercised (`open.md` says so), so the honest fix may be a documented limitation rather than a code
change. Decide which, and say why. If you change code, the obvious move is reusing the
`core_belongs_to` answer the driver already has — but check whether that answer is meaningful under
mirrored networking at all before you lean on it, because decision 30's whole point is that
loopback discriminates nothing there.

## 2 — `open.md`'s check-5 settling protocol names a code the protocol cannot reach

`embarch-umbrella/open.md`'s check-5 bullet says: *"a Linux box running Core natively, probe
attached, udev rules removed — Fail `probe-not-permitted`, then **`no-probe-found` with them
back**."*

With the rules back, Core enumerates the probe, so `check_probes` returns Pass `probes-present`
(reported ~920–925). `no-probe-found` requires a zero probe count **and** no known VID on the bus,
which cannot happen with a permitted, attached, known-VID probe. So the second half of the protocol
asks for an outcome that is unreachable by construction.

This matters more than a typo: that bullet is the written plan for settling a check nobody has ever
exercised, and whoever finally has the Linux box would follow it and conclude something was wrong.
Fix the protocol to name the code the second step actually produces.

## 3 — `deploy-core` and `uninstall` print failures on stdout where `spec.md` promises stderr

`spec.md`'s Command surface section ends: *"`1` failure with the message on stderr (or folded into
the JSON object under `--json`)"*.

`deploy.rs` prints every failure with `println!` and returns 1 — reported at ~523 (*"deploy-core:
FAILED. No transcript at {} — the elevated child never started…"*), ~538–545 (the failed-to-land
message), ~452 and ~458. `setup::uninstall` and `refuse_if_remote` are reported as doing the same.

**A script that redirects stderr to capture the reason gets nothing.** Either the code should use
`eprintln!` for failure paths or `spec.md` should stop promising stderr; **this one is genuinely a
code-or-doc fork and the code side is small and safe.** Note that `deploy-core` already has a
`[deploy-core lies about landing]` history in this suite, so a caller not seeing its failure text on
the stream it expects is not a hypothetical concern. Whichever way you resolve it, resolve it for
*all* the sites, not the first one — a half-converted convention is worse than either side.

## Done when

- [x] Each of the three is either **fixed** or **reported as not holding**, with the evidence, one
      by one. Partial is acceptable and expected: if you run out of budget, fix the ones you
      reached and **file a follow-up task naming exactly which of the three remain**, the way this
      task names them. (All three fixed; no follow-up on the census items themselves needed.)
- [x] Nothing is "fixed" on the strength of this task's own description. Every change rests on a
      line you read.
- [x] Item 1's outcome states explicitly whether it landed as a code change or a documented
      limitation, and why. (Code change — see report below and decision 53.)
- [x] A `changelog.d/` fragment. (Three: `umbrella-usb-scan-wsl2-ambiguity.fixed.md`,
      `umbrella-open-check5-protocol.fixed.md`, `umbrella-deploy-setup-stderr.fixed.md`.)
- [x] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` in
      `embarch-umbrella`, and `python3 scripts/check-docs.py` in `embarch-doc`. All green, plus
      `check-ownership.py` (both repos) and `check-client-names.py`.

## Outcome, item by item

**Item 1 — fixed as a code change (decision 53), coordinates held near-exact.** `usb_scan_for` (was
line 862, holds) gated purely on `winner_class`; `core_belongs_to` (line 216, comment confirms it is
"only ever consulted when no binary could be located at all") is *not* a safe drop-in for check 5,
because it is oblivious to whether a real local `embarch-core` binary was actually found — under WSL2
with no explicit `--host` it always resolves `WslHost` regardless, so gating check 5 on it directly
would silently disable the scan on every WSL2 machine, including one with a genuine native-Linux
Core reachable via `usbipd`. Fix: `usb_scan_for` now also takes the located binary and `under_wsl2`,
and scans when `winner_class == Local` **and** (not under WSL2, **or** the located binary is a native
Linux exe rather than a Windows one reached through interop). No located binary reduces to the same
"assume the Windows host" call `core_belongs_to` already makes, for the same reason. Four new/updated
unit tests, all against synthetic `Located` values — unexercised on real hardware, matching the rest
of this check's fail branch (`open.md`).

**Item 2 — fixed as a doc correction, no code change.** `check_probes` (line 913, holds) confirmed:
with the probe permitted again, `a.probes` is non-empty and the function returns Pass
`probes-present` before the USB scan is ever consulted — `no-probe-found` needs a zero count *and*
nothing on the bus, unreachable with a permitted known-VID probe. `open.md`'s settling protocol
corrected to name the reachable code.

**Item 3 — fixed as a code change, swept for all failure-exit sites in the named scope.**
`deploy_core` (line 319, holds): every `println!` immediately preceding `return EXIT_FAILURE`
converted to `eprintln!` (11 sites); progress/success prints (plan render, "syncing …", the transcript
dump, "landed and running") stay on stdout. `setup::uninstall`: its three failure-language messages
converted, even though the function always returns 0 (best-effort cleanup) — matched to the task's
own framing of this site, not to the stricter exit-code rule used elsewhere. `refuse_if_remote`'s two
call sites (`up`/`down`) and the adjacent `defer_to_windows_service`/`Deferral` mechanism: split so the
`satisfied: true` (exit 0) message stays on stdout and the `satisfied: false` (exit 1) message moves
to stderr — the two outcomes previously shared one `println!`. Also swept, same file, same shape:
`apply_plan`'s `(_, None)` arm (`Can't continue without embarch-core`, exit 1). **Not swept:**
`install_this_platform` and `apply_plan`'s other advisory messages (`Could not install the service`,
`Could not save state`) — these are printed under branches that still return 0 by explicit design
(`install_this_platform`'s own doc comment: "shouldn't silently abort the rest of `setup`"), so
`spec.md`'s exit-code-1 promise does not govern them; converting them would blur that distinction, not
fix it. Also not audited: `init.rs`, `main.rs::status`, `doctor.rs::doctor` — outside the task's named
scope (`deploy.rs`, `setup::uninstall`, `refuse_if_remote`).

## Coordinate drift

`usb_scan_for` def: reported ~862, actual 862 (exact). `usb_scan_for` call site: reported ~3262,
actual 3261 (drift 1). `core_belongs_to` call: reported ~3249, actual 3247 (drift 2). `check_probes`:
reported ~920–925 for the Pass arm, actual 920–925 (exact). `deploy.rs` failure sites: reported ~523,
~538–545, ~452, ~458; actual 520–526, 539–546, 452–453, 458–459 (drift 0–3, all within a line or two).
Every shape held; only line numbers drifted, consistent with `umbrella/075`'s finding.

## Not yours

**Do not touch `tasks/umbrella/075`'s defect** — the `setup`-confirms-discovery sentence in
`spec.md`'s Token handling section. It is a separate unit and may be in flight.

**Do not add a `doctor` check, and do not renumber one.** The check set and its numbering are a
surface other repos and the user guide cite by number.

**Do not run `doctor` against a live machine**, and do not conclude anything about mirrored
networking from an observation — there is no mirrored-mode bench and `open.md` is right that it is
unexercised. Item 1 is answerable by reading the driver.

### Claims the same census checked and found the code honours — do not re-sweep these

Recorded so the next unit in this repo does not spend its budget re-deriving them. **Second-hand,
so do not cite them as verified either** — they are "nobody found a problem here", not "this was
proven correct": check 5's nine vendor IDs and the deliberate absence of `0403`, and its five codes;
check 10's seven codes, 10 s handshake, `~/.claude.json` `projects.<cwd>.mcpServers` path,
local-before-user scope and three-way `file_stem` identity; the 500 ms / 10 s budget ladder,
`authed_get`'s budget-as-parameter and `request_failure_verb`'s "timed out after N ms" precedence;
check 17's full code set including `bind-elsewhere`'s `remote` guard and the exhaustive
`setup_would_infer` match; check 13's `not-configured`/`stale`/`unresolvable`; check 11's four
numbers with the own-constant arm unable to fail; `code`/`path` always present with `with_path` only
on check 16; 17 checks emitted in order with no 18; `locate_api`'s four-source ranking and
`locate_core`'s PATH-then-service-registration order; decision 51's `apply_plan` clearing of
`saved.host`; decision 50's SHA-256 `landed`, transcript-before-digest ordering and absent
`--verify-only`; `SYNC_CRATES` order; `SUITE_BINARIES` = three; `.bashrc`/`.zshrc` only;
`flash_format` required with `retired_targets`/`soc_chip_overrides` refused by name; `CoreConfig`
re-exported; `artifact_path_for_core` gone from `init`/`ProjectConfig`/check 9; the `verify-version`
job gating the release matrix; and `doctor` writing or deleting nothing outside `#[cfg(test)]`.
