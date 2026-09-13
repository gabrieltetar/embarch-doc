# 052 — `embarch-core/README.md` says Core binds `0.0.0.0` by default and that loopback was rejected; decision 6 reversed exactly that

**State:** done — leg 108, unit 3, 2026-09-13, branch `agent/core/052-readme-bind-and-stale-claims`.
**Doc-size reserve for `core`:** `embarch-core/decisions/auth.md` 11356/12288 B (**932 B left**,
filed as blocked `tasks/core/046`). **That is the file decision 6 lives in**, so if you conclude a
decision body needs amending, read `DOC-COMPACTION.md` §2 first and compact in-unit if your edit
will not fit, carrying `tasks/core/046`'s `Must not delete:` list and closing only that file's item.
**You probably need no doc edit at all** — this is a README correction, and `spec.md` §2 and
`decisions/auth.md` already say the right thing. If you push any `core` doc into reserve, file
`tasks/core/<NNN>-compact-core.md` in the same commit.
**Source:** a read-only hunter pass over `embarch-core`, leg 108, 2026-09-13. Every line and quote
below was read on both sides by that pass; **re-derive them anyway** — a citation you did not check
yourself is the defect this task exists to close.
**Scope:** core
**Hardware:** none — README prose and source comments. Nothing runs, no Core, no board, no deploy.
**Owner:** no

## The defect

`README.md:135-138` says:

> Binds to `0.0.0.0:4884` by default — deliberately not `127.0.0.1`, since the point of this service
> is to be reachable from WSL2 (if Core runs native on Windows) or the LAN (if Core moves to a Pi).
> Override with `--bind` / `--port`.

Three sources say the opposite, and they agree with each other:

- `src/main.rs:32` — `pub(crate) const DEFAULT_BIND: &str = "127.0.0.1";`, whose own doc comment
  cites "decision 6's amendment, 2026-08-15".
- `embarch-doc/embarch-core/decisions/auth.md:14-15` — the bind default "was originally `0.0.0.0`
  … **Reversed**", because `0.0.0.0` plus no TLS plus a static token plus `/flash` reading an
  arbitrary local path, in a process that may run as `LocalSystem`, is a posture nobody had assessed
  as a whole.
- `embarch-doc/embarch-core/spec.md` §2 — "**Default bind is `127.0.0.1`.** Widening is
  `embarch-umbrella setup`'s job, per detected topology."

**This is worse than a stale value.** The sentence asserts the *rationale* that decision 6 recorded
as reversed, so a reader following it concludes no `--bind` is needed for the WSL2→Windows
topology — which is the one topology that does need it.

## Two fixes that read well and are wrong

- **Changing the code to match the doc.** `DEFAULT_BIND = "0.0.0.0"` would "make them agree" and
  reverse a security decision taken after composing four separate weaknesses. **The doc is the wrong
  side.** Do not touch `src/main.rs:32`.
- **Writing "run `embarch setup` to widen it."** A half-truth. Per
  `embarch-doc/embarch-umbrella/decisions/bind.md:23`, `setup` run natively on the Windows side
  infers `local`, reinstalls `--bind 127.0.0.1` and rewrites the recorded class — greening `doctor`
  check 17 with the bind untouched. The offer is correct only from the WSL2 guest, and a README
  cannot carry that guard. Name the command instead: `embarch-core install --bind 0.0.0.0`, run
  elevated, which is what `suite/user-guide.md` already prescribes for `bound-narrow`. **Verify that
  against the current `user-guide.md` rather than trusting this paragraph.**

## Ride-alongs in the same file — take them if they still hold, and re-verify each

Same README, same sitting, each independently evidenced by the hunter pass. **Re-grep and re-check
every one before changing it**; report any that turn out correct rather than editing it anyway.

- `README.md:5` — "five bearer-token-authed HTTP endpoints". There are 22 `.route(` registrations,
  and `src/api.rs:1569` carries `DOCUMENTED_ROUTE_COUNT = 22`. Use the constant, not a hand count.
- `README.md:35` — lists `src/dev_bench.rs`, which does not exist; detection moved to
  `embarch_topology::hardware`, as the same README says about 40 lines later.
- `README.md:158` — "`open_first_probe()` in `hardware.rs` takes the first probe-rs finds". That
  function is gone; `resolve_probe` (`src/hardware.rs:79`) replaced it and **errors loudly on
  ambiguity**, which is the opposite behaviour. `src/hardware.rs:61-66` already records the old doc
  comment as a drift found and fixed.

## Not in scope

- Anything requiring a board, a running Core, or a deploy.
- The `src/hardware.rs:74` stale `board_gate.rs` justification the hunter also found — real, but a
  different subsystem; if you want it fixed, drop it to `/home/gabriel/Github/embarch/embarch-doc/inbox/`
  rather than folding it in.
- Amending decision 6 itself. It is correct; the README disagrees with it.

## Done when

- [x] `README.md:135-138` states the loopback default, decision 6's reason for it, and the real
      widening remedy — and no longer asserts the reversed rationale.
- [x] Each ride-along taken is verified against the source first, and each one left is named in the
      report with why.
- [x] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [x] `changelog.d/` fragment.

## Closing notes

**Re-derivation of the task's own citations** — all confirmed correct except one line-number nit:
`src/main.rs:32` (`DEFAULT_BIND = "127.0.0.1"`) — exact. `decisions/auth.md` — the "was originally
`0.0.0.0` … Reversed" text is real, but lives on line 15 as one long paragraph, not "14-15" as two
lines — a citation slip, not a wrong quote. `spec.md` §2's "Default bind is `127.0.0.1`" — exact, at
line 36. `embarch-umbrella/decisions/bind.md`'s claim about `setup` inferring `local` when run
natively on Windows and reinstalling the narrow bind — read and confirmed (2026-09-06 amendment).
`suite/user-guide.md:226`'s `bound-narrow` row — confirmed, prescribes `embarch-core install --bind
0.0.0.0` run elevated, exactly as the task states.

**Fix applied** (`README.md:135-145`, in the `## Running` section): loopback default restated,
decision 6's actual rationale (composed weaknesses, not "reachability is the point"), and the real
widening remedy named as a command (`embarch-core install --bind 0.0.0.0`, elevated) with the
`embarch setup`-only-from-the-guest caveat. `src/main.rs:32` untouched, per the task's own
instruction — the doc was the wrong side.

**Ride-alongs — all three taken, all three re-verified first:**
- `README.md:5` ("five... endpoints") — confirmed wrong; `DOCUMENTED_ROUTE_COUNT = 22` at
  `src/api.rs:1569`, and `cargo test` passes the test that pins it against `interfaces.md`. Changed
  to "22", pointed at `embarch-doc/embarch-core/interfaces.md` for the full list rather than
  hand-listing all 22 in the README (table below still shows the same 5 core routes it always did,
  now explicitly labeled a subset).
- `README.md:35` (`src/dev_bench.rs` in the Layout tree) — confirmed the file does not exist
  (`ls` fails); removed the stale entry. Did not replace it with a new tree line for
  `embarch_topology::hardware`, since that's a different crate's module and the README already says
  so ~30 lines below (`README.md:63-66` as edited, formerly ~64-67).
- `README.md:158` (`open_first_probe()` claim) — confirmed gone from `hardware.rs`; `resolve_probe`
  (line 79) is the real function and **errors loudly on ambiguity**, the opposite of what the README
  said. The whole bullet was a "what's not here yet" gap that's now closed (decision 9 /
  `hardware.rs:61-66`'s own doc comment records the fix), so removed rather than reworded in place.

**Left alone (verified correct, not touched):** nothing else in the file — the three ride-alongs
above were the only ones the task named, and no other line was found wrong during the read-through
of the whole file (done in full before editing).

**Dropped to inbox, not fixed here (both out of this task's scope):**
- `/home/gabriel/Github/embarch/embarch-doc/inbox/core-hardware-rs-stale-board-gate-comment.md` —
  the task's own named `src/hardware.rs:74` stale `board_gate.rs` reference (confirmed real:
  `board_gate.rs` doesn't exist in this crate; `hardware.rs:116`'s doc comment already has the
  corrected story, `hardware.rs:74`'s doesn't).
- `/home/gabriel/Github/embarch/embarch-doc/inbox/doc-check-task-state-title-substring-false-positive.md`
  — found while gating, not part of this task: `scripts/check-task-state.py`'s Rule 6 title scan
  flags this very task's title as naming `embarch-doc`'s reserved root `README.md`, because it does
  a raw substring match with no path boundary and this task's title contains the substring
  `README.md` inside `embarch-core/README.md` — a different file in a different repo, one `core`
  legitimately owns. See `## Gate results` below.

**Windows build debt.** Per the fleet's standing debt (§7 in `protocol.md`, `embarch-core`'s native
Windows target): this unit did not attempt or verify a Windows build. Nothing here touches
platform-conditional code (`README.md` prose only), so the risk this adds is minimal, but it is
still an addition to that standing debt per this fleet's own accounting rule, and is recorded here
so the supervisor logs it.

## Gate results

- `cargo build` / `cargo test` / `cargo clippy --all-targets -- -D warnings` (code worktree): **all
  green**. 197 tests passed (2 ignored), including `registered_route_count_matches_the_count_
  documented_in_interfaces_md`, which is what makes "22" a verified-live number rather than a
  hand count.
- `python3 scripts/check-docs.py` (doc worktree): **RED on one sub-check**,
  `check-task-state.py`, and it is a false positive — see the inbox drop above. Every other
  sub-check (`check-links.py`, `check-staleness.py`, `check-decision-refs.py`,
  `check-doc-conventions.py`, `check-doc-size.py`, `check-task-numbers.py`,
  `build_changelog.py --check`, `build_features.py --check`, `install.py --verify`,
  `check-client-names.py`) passed.
- `scripts/check-client-names.py --repo <code worktree>`: **green** — "clean against 7 denylist
  entries."
- `scripts/check-ownership.py --scope core` (doc worktree): **green** — "all 1 changed path(s) owned
  by the 'core' worker" (base `37a9198f67a3`).
- `scripts/check-ownership.py --scope core --code-repo` (code worktree): **green** — "worker for
  'core' owns the whole tree" (base `f852fa8d2908`).
