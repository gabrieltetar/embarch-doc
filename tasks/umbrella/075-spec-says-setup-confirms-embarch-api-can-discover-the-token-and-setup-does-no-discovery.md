# 075 — `spec.md` says `setup` "confirms `embarch-api` can discover" the token; `setup` does an existence check and its own code comment says so

**State:** claimed by agent/umbrella/075-setup-token-discovery, 2026-09-17 00:51 (leg 132 unit 4)
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

> Umbrella invents no token mechanism — [embarch-token.md](../embarch-token.md) is the source of
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

- [ ] You have independently verified, and reported, each of these: the `spec.md` sentence's current
      wording and location; that `setup`'s token step is an existence check; that nothing in
      `setup.rs` resolves a token or spawns `embarch-api`; and that the `wsl-host` arm prints rather
      than starts. **Say plainly if any of them does not hold** — a task built on a census can be
      wrong, and reporting that is the correct outcome, not a failure.
- [ ] `embarch-umbrella/spec.md`'s Token handling section says what `setup` actually does: which
      topologies it starts Core on, that the token step is an existence check at a conventional
      path, and that discovery is verified by `doctor` check 4 / `status` rather than by `setup`.
      **Do not overcorrect either** — the "writes no token value into any config file" clause and
      the cross-machine clause were checked and are true; leave them.
- [ ] Whether §5 and §6 now agree is stated. If a cross-reference from the Token handling section to
      the `doctor` chain is the honest fix for that, make it.
- [ ] A judgement call, reported with its reasoning: **is this a plain doc correction, or does it
      warrant a numbered `umbrella` decision?** Read how this repo has handled comparable
      corrections before deciding — a correction that only restates what the code always did is
      usually not a decision. If you do write one, it goes in the `decisions/` file whose topic it
      is, never in whichever file has room.
- [ ] A `changelog.d/` fragment.
- [ ] Gate green: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` in
      `embarch-umbrella`, and `python3 scripts/check-docs.py` in `embarch-doc`.

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
