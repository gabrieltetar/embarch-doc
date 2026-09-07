# 011 — The firmware on the bench was built from a checkout whose history is gone, so nothing can say how stale it is

**State:** open
**Source:** `tasks/umbrella/034`'s bench run, leg 030, 2026-09-07 — `doctor` check 13's first real comparison
**Scope:** dev-bench
**Hardware:** bench — and the build half needs the `toolchain` hands (`tasks/README.md`): this repo's Zephyr tree is gitignored, so it builds in the **main checkout** and not in a worktree
**Owner:** no

## What

The dev-bench on the primary `wsl-host` bench reports `HelloAck.firmware_version` **`49958d34`**,
measured over `GET /dev-bench/hello` on 2026-09-07 (`{"schema_version":15,"compatible":true,
"firmware_version":"49958d34","hardware_id":"cb781b716fcddc36","link_identity":"match",
"probe_hardware_id":"6fcddc36cb781b71"}`).

**`49958d34` is not a commit in `embarch-dev-bench`.** Not among its 27 commits, not a tag, not in
any reflog; the repo's history begins 2026-07-30 and `main` is at `d599453`. So the flashed image
was built from a checkout whose history no longer exists — the 2026-09-04 client-name scrub is the
obvious candidate and is **not proven** here.

The consequence is not cosmetic. **Nobody can currently say what firmware is on the bench**, which
means nobody can say whether a study's result depends on a fix that is or is not in it. The bench
reports wire schema **v15** and Core accepts it, so it is not incompatible — it is unidentifiable.
And `main` has moved since: `d599453` regenerated two Core wire vectors that the same scrub had left
stale, which is exactly the class of change a stale bench would hide.

## Why now

`doctor` check 13 exists to catch this and only reached its comparison arm on 2026-09-07, after
`umbrella/030` fixed the handshake budget. Its answer is a `FAIL` and its fix line — rebuild and
reflash — is the only action that can clear it. Reflashing from current `main` replaces an
unidentifiable image with one whose id resolves, which is what makes every later check 13 run
meaningful rather than permanently red.

## What this needs, stated so nobody infers it

- **Board:** the dev bench is an **nRF54L15DK**; its link is **COM17 / VCOM1, interface 2** — the
  higher interface, not the lowest — enrolled with `link_port_interface=2`, probe `001057729826`,
  hardware id `6fcddc36cb781b71`. All re-validated live 2026-09-07 01:47 MDT.
- **The build is not a worktree job.** `workspaces/*/{zephyr,modules,.west}` are gitignored, so only
  the main checkout has a Zephyr tree. The fleet's own west is
  `/home/gabriel/Github/embarch/.west-venv/bin/west` — never a `west` from inside a client
  workspace, which would put a client's name in this repo.
- **Do not infer the board, the app, the snippet or the flash runner from source.** If the exact
  `west build` invocation for this bench is not written down where you can find it, stop and say so;
  an inferred hardware fact asserted as measured is the failure this suite has already paid for.

## Done when

- [ ] The bench runs firmware whose `git describe --always --dirty --abbrev=8` resolves in this
      repo, and the value is recorded.
- [ ] `doctor` check 13 with `EMBARCH_DEV_BENCH_REPO_PATH` set is a `PASS`, quoted.
- [ ] Whether anything behaved differently after the reflash is recorded — especially the two
      regenerated wire vectors from `d599453`.
- [ ] Gate green; `changelog.d/dev-bench-*` fragment.

## Related

`tasks/umbrella/037` is the other half: check 13 is silent by default because nothing configures
`dev_bench_repo_path`, and it cannot tell "an older commit" from "no such commit".
