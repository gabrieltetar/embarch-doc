# 076 — Three more `embarch-umbrella` doc-versus-code contradictions, from the same census that produced 075

**State:** claimed by agent/umbrella/076-three-more-contradictions, 2026-09-17 01:04
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

- [ ] Each of the three is either **fixed** or **reported as not holding**, with the evidence, one
      by one. Partial is acceptable and expected: if you run out of budget, fix the ones you
      reached and **file a follow-up task naming exactly which of the three remain**, the way this
      task names them.
- [ ] Nothing is "fixed" on the strength of this task's own description. Every change rests on a
      line you read.
- [ ] Item 1's outcome states explicitly whether it landed as a code change or a documented
      limitation, and why.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` in
      `embarch-umbrella`, and `python3 scripts/check-docs.py` in `embarch-doc`.

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
