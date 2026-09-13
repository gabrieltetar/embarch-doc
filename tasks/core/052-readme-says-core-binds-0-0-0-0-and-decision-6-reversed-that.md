# 052 — `embarch-core/README.md` says Core binds `0.0.0.0` by default and that loopback was rejected; decision 6 reversed exactly that

**State:** claimed — leg 108, unit 3, 2026-09-13, branch `agent/core/052-readme-bind-and-stale-claims`.
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

- [ ] `README.md:135-138` states the loopback default, decision 6's reason for it, and the real
      widening remedy — and no longer asserts the reversed rationale.
- [ ] Each ride-along taken is verified against the source first, and each one left is named in the
      report with why.
- [ ] `cargo build` / `test` / `clippy --all-targets -- -D warnings` green.
- [ ] `changelog.d/` fragment.
