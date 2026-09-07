# 011 — The firmware on the bench was built from a checkout whose history is gone, so nothing can say how stale it is

**State:** claimed
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

- [x] The bench runs firmware whose `git describe --always --dirty --abbrev=8` resolves in this
      repo, and the value is recorded. — **`d599453d`**, see the run record below.
- [x] `doctor` check 13 with `EMBARCH_DEV_BENCH_REPO_PATH` set is a `PASS`, quoted. — below.
- [x] Whether anything behaved differently after the reflash is recorded — especially the two
      regenerated wire vectors from `d599453`. — below; nothing behaved differently, and the check
      that would have shown it is named rather than assumed.
- [x] Gate green; `changelog.d/dev-bench-*` fragment.

## Run record — supervisor, leg 034, 2026-09-07

**Both roles validated live before anything was built or flashed, and both matched their enrolled
identities exactly** [measured 2026-09-07]: `dev-bench` `6fcddc36cb781b71` on probe `001057729826`,
`dut` `834f2559f10a6cdf` on probe `000852006107`, both `nRF54L15`, `ok: true`. No mismatch either
side.

**The build invocation was read from `embarch-dev-bench/README.md`, not inferred** — its
*Building: nordic (nRF54L15DK)* section gives `west build -b nrf54l15dk/nrf54l15/cpuapp app` from
`workspaces/nordic`, which is the board this bench is enrolled as. Run with the fleet's own west
(`/home/gabriel/Github/embarch/.west-venv/bin/west`) in the main checkout, since
`workspaces/*/{zephyr,modules,.west}` are gitignored and only it has a Zephyr tree. The workspace
was already `west init`'d and `west update`d; **neither was re-run**, so the NCS pin this README
warns about was not moved.

**Built `-p always` (pristine) deliberately.** `APP_FIRMWARE_VERSION` comes from
`app/CMakeLists.txt`'s `execute_process(COMMAND git describe --always --dirty --abbrev=8)`, and
that file's own comments record that a cached configure can leave a stale value baked in. A
pristine build removes the question. Exit 0, `FLASH: 295968 B / 1524 KB (18.97%)`,
`RAM: 153536 B / 256 KB (58.57%)`. `strings` on the resulting `zephyr.elf` carries **`d599453d`**
and no `49958d34`, confirming the stamp before anything was written to the board.

**Flashed through Core, not `west flash`** — `flash_dev_bench` with an explicit `firmware_path` of
the artifact just built, so Core picked the board's declared vendor runner (jlink for this chip
family) under its own `hw_lock`, and no probe had to be selected by hand with two J-Links attached.
Then `reset_dev_bench`, since flashing halts the core rather than starting it running.

**`doctor` check 13 is now a `PASS`**, quoted verbatim, with `EMBARCH_DEV_BENCH_REPO_PATH` set:

```
[13] PASS dev-bench firmware matches the local checkout — firmware_version 'd599453d' matches /home/gabriel/Github/embarch/embarch-dev-bench
```

**Check 11 also still passes and is the more interesting one**, because it is the check that would
have caught a wire regression: `study-designer schema versions agree — host type: Core serves v17,
the located embarch-api was built against v17; this embarch agrees at v17; dev-bench wire: bench
reports v15, and Core accepts it`. The bench's wire schema is **unchanged at v15** across the
reflash, so `d599453`'s two regenerated vectors did not move the wire — consistent with that
commit's own message, which describes them as *captured* `StudyStart` payloads whose committed
bytes had drifted from the generator, not a schema change.

**What behaved differently after the reflash: nothing observable, and here is the check rather than
the assertion.** `d599453` regenerated `core_study_start_frame` and
`core_study_start_with_security_frame` — both `DevBenchMessage::StudyStart` payloads, and the
drifted field was step 0's `target_name`. So the behaviour at risk is *decoding a `StudyStart` that
carries a `target_name`*, and that is what was exercised: a one-step `BleConnect` with
`target_name` set to a name no device could have, which is the documented census
(`suite/studies-guide.md` §3a). Study **`c434bdc1a847690b9063672a9fd27289`**, 20 s, `reflash` at its
`none` default. It failed as intended and the bench reported what was on the air:

```
dev-bench stopped the study early: step 'census' failed (no name match; on air: 'pod-36e017c', 'pod-5678212')
```

**The `target_name` round-tripped and the census path works on the reflashed firmware.** That is
the whole of what this run establishes about the vectors — it does not prove the two arrays are
byte-correct, only that the message they capture still decodes and drives the right behaviour.

**One incidental measurement, recorded because it bears on four other bench tasks and not on this
one.** Two named advertisers, `'pod-36e017c'` and `'pod-5678212'`. The 2026-09-06 censuses saw
`'GABRIEL'` and `'pod-36e017c'` — so **the set of named advertisers on this bench changes between
sittings**, and `'GABRIEL'` was absent this time. That is one more reason the DUT cannot be
attributed by name here, and it changes nothing about `tasks/api/029`'s open question: nothing in
EmbArch joins a BLE advertiser to an enrolled probe, and **no DUT fact was inferred from this run.**

**What this task does not settle.** It clears check 13 on *this* bench, once. It does not make
check 13 fire by default — `dev_bench_repo_path` is still unset in saved state and only the
environment variable produced a comparison, which is `tasks/umbrella/037` and stays open. And
`49958d34`'s provenance is still unknown: replacing the image removed the *consequence* of an
unidentifiable build without establishing where it came from. The 2026-09-04 client-name scrub
remains the obvious candidate and is **still not proven**.

## Related

`tasks/umbrella/037` is the other half: check 13 is silent by default because nothing configures
`dev_bench_repo_path`, and it cannot tell "an older commit" from "no such commit".
