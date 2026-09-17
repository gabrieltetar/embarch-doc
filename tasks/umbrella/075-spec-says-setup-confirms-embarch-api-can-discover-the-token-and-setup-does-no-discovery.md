# 075 — `spec.md` says `setup` "confirms `embarch-api` can discover" the token; `setup` does an existence check and its own code comment says so

**State:** done — leg 132 unit 4, 2026-09-17, `agent/umbrella/075-setup-token-discovery`
**Source:** leg 132's own refill census of `embarch-umbrella`'s docs against its source. **Not from
a worker's report and not a citation defect** — a documented behaviour checked against the code that
is supposed to perform it.
**Scope:** umbrella
**Hardware:** none — reading Rust and correcting prose. Nothing is built for a board, no probe, no
live Core, no deploy, no `setup` run. **The `wsl-host` half below is settled by reading
`setup.rs`, not by running anything.**
**Owner:** no

**Doc-size reserve for `umbrella`:** `embarch-umbrella/decisions/bind.md` is **11,533/12,288 B
(755 B left)**, filed as `tasks/umbrella/009` and blocked. **`embarch-umbrella/spec.md` — the file
this task edits — is *not* in reserve**, so you have room; do not spend it carelessly, and if your
edit pushes `spec.md` into the band, file `tasks/umbrella/<NNN>-compact-docs.md` in the same commit
per `tasks/README.md`. Run `python3 scripts/check-doc-size.py --pressure` before and after and
report both numbers.

## What

**Every line number and quotation below was taken by a census pass, not by this task's author
reading the file a second time. Verify each one yourself before you act on it** — if a line has
moved or a quotation is off, correct it in your report and work from what is actually there. The
*shape* of the defect is what this task asserts; the coordinates are a starting point.

`embarch-doc/embarch-umbrella/spec.md`, in the **Token handling** section (reported at line 71):

> Umbrella invents no token mechanism — [embarch-token.md](../../embarch-token.md) is the source of
> truth — and **writes no token value into any config file.** On a same-machine topology `setup`
> starts Core once so the machine-wide token file exists, **then confirms `embarch-api` can discover
> it.** Across machines there is no shared filesystem and no solution: it prints the export line for
> a value the human reads off the Core machine.

**Two clauses of that sentence are false, and they fail in different ways.**

### (a) `setup` performs no token discovery, and its own helper says so

`embarch-umbrella/src/setup.rs` (reported at lines 320–333) is the *entire* token step: a bare
`Path::exists()` on a path computed by string convention, printing one of two lines —

```
Token file: {} (present)
Token file: {} (not yet — embarch-core creates it the first time it starts)
```

— and the doc comment on the function that produces that path (reported at lines 22–24) states the
limit outright:

> This is an existence check only, not token discovery — reading and validating the value is
> `doctor`'s job (embarch-umbrella spec.md §5), and needs the discovery logic `embarch-api` already
> has.

The census reports that nothing in `setup.rs` resolves a token or invokes `embarch-api` at all: the
only real callers of `embarch_core_client::token_discovery::resolve_token` are `doctor`'s check 4 and
`status` (decision 46), and `setup.rs`'s only `Command::new` is its generic `run()` helper, used for
`embarch-core install`/`start`/`uninstall`. **Confirm that yourself with a grep** — it is the load-
bearing claim of this task, and a single missed call site would change the answer.

So **§6 and §5 of the same document disagree about who verifies discovery, and the code sides with
§5** — which is also what the code comment cites.

### (b) "starts Core once" is false on the primary topology

On `local`, `setup` really does run `embarch-core install --bind …` and print `"Installed and
started."` (reported at `setup.rs:291`). On **`wsl-host`** — which `spec.md` itself calls today's
primary topology, and which *is* a same-machine topology — `setup` only **prints** the elevated
Windows command for the human to run (reported at `setup.rs:271–279`) and starts nothing. So on the
topology this suite actually uses, `setup` finishes with the token file **absent**, and correctly
says so with the "not yet" line. `remote` is properly excluded already, by `token_path_for`
returning `None`.

## Why it matters

The sentence promises that a clean `setup` has already proven the API half of the token chain
works. An operator — or an agent reading the doc — takes a clean `setup` as evidence that
`embarch-api` will authenticate. What actually happened is that a file was found (or not found) at a
hardcoded conventional path, **assumed rather than resolved**; the first thing that tests discovery
for real is `doctor` check 4, which `spec.md` says `setup` does not run.

That is the same failure shape this suite's `[measured]`/`[assumed]` provenance tagging exists to
prevent, in the one document a new operator reads first.

## Done when

- [x] You have independently verified, and reported, each of these: the `spec.md` sentence's current
      wording and location; that `setup`'s token step is an existence check; that nothing in
      `setup.rs` resolves a token or spawns `embarch-api`; and that the `wsl-host` arm prints rather
      than starts. **Say plainly if any of them does not hold** — a task built on a census can be
      wrong, and reporting that is the correct outcome, not a failure.

      **Verification (all claims held; two coordinates were off by a couple of lines from the
      census, shape unchanged):** the sentence is still at `spec.md:71`, wording unchanged from the
      quote. `setup.rs`'s token step (lines 320–332, not 320–333) is exactly the bare
      `token.exists()` branch quoted in the task. The doc comment naming the existence-check limit
      is at lines 22–24, exact match. `grep -n "Command::new\|resolve_token\|embarch_api" src/*.rs`
      confirms the only `Command::new` in `setup.rs` is the generic `run()` helper (line 117), used
      only for `embarch-core install/start/uninstall`; the only real callers of
      `token_discovery`/`resolve_token` are `doctor` (decision 46 confirms checks 4/5) and `status`.
      `local`'s install-and-start path is at lines 290–302 (not 291 — 291 is the "Installing..."
      print; "Installed and started." is line 293). The `wsl-host` arm that only prints is at lines
      272–282 (not 271–279 — off by one at each end), and it genuinely starts nothing; `remote`'s
      arm (264–271) likewise only prints. `token_path_for` returning `None` for `Remote` is
      confirmed at `setup.rs:57`. **Everything the task asserted about the shape of the defect held;
      only line-range citations drifted by 1–2 lines, which is what "second-hand" predicts.**
- [x] `embarch-umbrella/spec.md`'s Token handling section says what `setup` actually does: which
      topologies it starts Core on, that the token step is an existence check at a conventional
      path, and that discovery is verified by `doctor` check 4 / `status` rather than by `setup`.
      **Do not overcorrect either** — the "writes no token value into any config file" clause and
      the cross-machine clause were checked and are true; leave them.

      Done — rewrote the second and third sentences of `spec.md`'s Token handling section (still
      §6). The "writes no token value" clause and the cross-machine export-line clause are
      untouched, word for word.
- [x] Whether §5 and §6 now agree is stated. If a cross-reference from the Token handling section to
      the `doctor` chain is the honest fix for that, make it.

      They now agree: §6 states plainly that confirming `embarch-api` can read the token is the
      doctor chain's job (check 4) and `status`'s (decision 46), and that `setup` is not among the
      real callers of token discovery — matching what §5 already implies by listing check 4 as
      "token resolves and matches." Added the cross-reference by name ("the doctor chain's job:
      check 4 and `status` (decision 46)") rather than a markdown anchor — this file has no existing
      `#anchor` convention for internal section links (checked: none in `spec.md`, or in any other
      `embarch-umbrella/*.md`), only the `(decision N)` / bare cross-repo-file-link forms already in
      use, so I matched those instead of inventing a new pattern for one link.
- [x] A judgement call, reported with its reasoning: **is this a plain doc correction, or does it
      warrant a numbered `umbrella` decision?** Read how this repo has handled comparable
      corrections before deciding — a correction that only restates what the code always did is
      usually not a decision. If you do write one, it goes in the `decisions/` file whose topic it
      is, never in whichever file has room.

      **Plain doc correction, no decision.** Checked three directly comparable prior commits, all
      the same shape (spec.md asserting a behaviour the code doesn't have, code unchanged, doc
      brought into line): `44b203a` (umbrella/054, doctor check count 18→17 — "interfaces/doctor-
      chain.md already had this right"), `5b854be` (umbrella/055, setup/init rows stop asserting a
      doctor chain — "Correct the doc, not the code"), and `4f2c8bc` (the "no hardware knowledge"
      boundary claim, decision-46-era). None of the three touched `decisions/`, and none is itself
      numbered as a decision — a correction restating existing code behaviour isn't a decision by
      this repo's own precedent, since nothing was *chosen*: no design ambiguity was resolved, no
      trade-off was made, no future case turns on remembering *why*. This task is the same shape: the
      fix says what `setup` and `doctor` already did before this task existed. No decision written.
- [x] A `changelog.d/` fragment.

      `changelog.d/umbrella-setup-token-discovery-doc.fixed.md`, 184 bytes.
- [x] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` in
      `embarch-umbrella`, and `python3 scripts/check-docs.py` in `embarch-doc`.

      `embarch-umbrella`: build clean, 225 tests pass, clippy clean (no code changed — this task's
      whole fix is `spec.md` prose; "Not yours" is honoured, `setup.rs` untouched). `embarch-doc`
      `check-docs.py`: 11/11 green (`check-links.py` was RED before any of my edits, on a pre-
      existing broken relative link in *this task file itself*, `../embarch-token.md` from
      `tasks/umbrella/` — one `../` short; fixed to `../../embarch-token.md` since I was editing
      this file anyway). `check-ownership.py --scope umbrella` (doc worktree): OK, 1 path.
      `check-ownership.py --code-repo --scope umbrella` (code worktree): OK, 0 paths changed.
      `check-client-names.py --repo <code worktree>`: OK, clean against 7 denylist entries.
      `check-doc-size.py --pressure`: `embarch-umbrella/spec.md` not listed before or after (well
      under its reserve band both times) — before 6384 B, after 6911 B (of a 10240 B cap, ~67%);
      `embarch-umbrella/decisions/bind.md` unchanged at 11533/12288 B (755 B left), still the only
      umbrella file in the PARKED band, untouched by this task as instructed.

## Not yours

**Do not change what `setup` does.** Making `setup` perform real token discovery means giving it the
discovery logic `embarch-api` has — a dependency and a behaviour change that decision 46 already
routed elsewhere on purpose, and the code comment names `doctor` as the owner of that job. The
defect here is that the document describes a `setup` that does not exist, and the fix is in the
document. If you conclude `setup` genuinely *should* verify discovery, **file that as a task** in
`tasks/umbrella/` with the cost named, and say so in your report.

Also not yours: three further doc-versus-code contradictions the same census turned up in this repo
— check 5's USB scan gated on a class rather than on which machine Core is on, `open.md`'s check-5
settling protocol naming an unreachable code, and `deploy-core`/`uninstall` printing failures on
stdout where `spec.md` promises stderr. They are filed separately as `tasks/umbrella/076`. **Do not
touch them here**, even if you pass one; one task, one defect.
