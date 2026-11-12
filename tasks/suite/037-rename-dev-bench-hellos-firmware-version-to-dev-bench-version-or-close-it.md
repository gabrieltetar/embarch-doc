# 037 — Rename `GET /dev-bench/hello`'s `firmware_version` to `dev_bench_version`, or close the question for good

**State:** done — 2026-11-10, the rename shipped on `agent/suite/037-rename-dev-bench-hellos-firmware-version-to-dev-bench-version-or-close-it`
in `embarch-core`, `embarch-api`, `embarch-ui`, `embarch-umbrella` and `embarch-doc`, pushed and not
landed. Gated on a native Windows build of `embarch-core` in a scratch copy; **nothing was deployed.**
Landing, and the deploy after it, are the owner's.
**Owner's word:** given by the owner in his interactive session on 2026-11-10 and relayed in the
dispatch of this run — take this task's first path: a native Windows build of `embarch-core` in this
run, **build only, no deploy**, in a scratch copy on the Windows side, then the rename gated on that
build. That is the "native build … and takes this task in that same sitting" the park named, with
the deploy step of `embarch-dev-workflow.md` §4a left out on purpose. The installed Core service and
its Windows-side source copy were not touched.
**Owner's word, 2026-11-11, given directly in his interactive session:** (1) embarch-umbrella lands with core, api and ui. (2) When Core sends no `dev_bench_version`, the reflash gate **always refuses** a study that pins a bench version, and `allow_version_mismatch` does **not** let it through; the only way to run such a study against an old Core is a bench requirement of `any`. This replaces the override behaviour first built on this branch. (3) After landing, Core is deployed per `embarch-dev-workflow.md` §4a and the API is rebuilt.
**Source:** split out of `suite/036` by leg 105, 2026-09-13, when that task's documentation half
landed (`embarch-doc` `6f369d3`, `embarch-api` `72e8b12` + `265c8ff`). **This is the half it could
not take**, because leg 105's announcement window covered documenting the field and this is a
breaking change to a served field.
**Scope:** suite
**Hardware:** none — an HTTP response field, its client types and its consumers. Nothing reaches a
board. (But see "The old-Core half" — the Core *running* on this machine matters here even though
no board does.)
**Owner:** no
**Announced:** `#embarch-fleet` `ts` `1789326123.058939`, leg 107, 2026-09-13 — the 30-minute
window under `ops.md` §4 ran and closed with no objection (leg 108 read the thread). It named three
repos; this run also changed a fourth, `embarch-umbrella`, whose doctor check 13 reads the same field
(see "Consumers").

**The gate: a native Windows build in a scratch copy, and no deploy.** Why it was needed: this task's
fourth `Done when` item and `.claude/leg.md` both require a native Windows build wherever
`embarch-core` is involved, and no leg can run one, which is what parked this task from leg 107 to
2026-11-10. How it ran, `embarch-dev-workflow.md` §4a steps 1–2 only: the four crates were copied
with `rsync -a --exclude '/target/' --exclude '/.git'` into
`C:\Users\tmp12\source\repos\_wt\core-suite-037\` — `embarch-study-designer` `f6cca94`,
`embarch-topology` `b905523`, `embarch-smp` `4b23bc2` (each clean, at `origin/main`) and
`embarch-core` at this branch's `c0d2a7e` — then, from that copy's `embarch-core`,
`/mnt/c/Users/tmp12/.cargo/bin/cargo.exe build --release`. **Exit 0, `Finished release` in 3 m 07 s,
no warnings**, a cold cache [measured 2026-11-10]. Steps 3–4 (install, verify) were not run.

## The argument, stated here in full

`suite/036`'s file was retired by its own fold, as every completed task is, so this does not point
at it: the long form is in `embarch-doc` commit **`6f369d3`** and in `supervisor-log.md`'s
`suite/036` entry. Everything load-bearing is below.

- **The defect.** `GET /dev-bench/hello` serves the **bench's** build as `firmware_version`. The
  `Study` field it corresponds to is `requires.dev_bench_version`. The identically named
  `requires.firmware_version` on the same struct is the **DUT's**. A caller matching name to name
  pins a DUT requirement to the bench's build, and `embarch-core` only *compares*
  `requires.firmware_version` when a run supplies `flashed_firmware_version` — so in the normal
  no-reflash case the wrong value is accepted and recorded as `Declared`.
- **The precedent.** `embarch-core` decision 47 made exactly this rename on exactly this route
  (`hardware_id` → `self_reported_hardware_id`) for exactly this defect class.
- **The count does not change, so a "third spelling" is not a reason to refuse.** `036` first
  argued that it would; leg 105 corrected that, and its reviewer re-derived the enumeration from
  `embarch-study-designer/src/protocol.rs:67`, `embarch-core/src/study.rs:621`,
  `embarch-study-designer/src/study.rs:280-281` and `src/result.rs:44,49`, confirming `Provenance`
  reuses the same two spellings and adds no third:

| | wire (`HelloAck`) | HTTP (`/dev-bench/hello`) | study (`Requirements`) | distinct |
|---|---|---|---|---|
| today | `firmware_version` | `firmware_version` | `dev_bench_version` | **2** |
| renamed | `firmware_version` | `dev_bench_version` | `dev_bench_version` | **2** |

- **What the rename actually moves is where the crossing happens, and it cuts *for* the rename.**
  Today the crossing is in the caller's hands, at the exact point where the HTTP name collides with
  a field on the same struct holding a different board's version. After the rename the crossing is
  inside Core, where Core composes the response and no caller crosses anything.

## The old-Core half, which is the actual work

**This is not a mechanical field rename.** `embarch-api` decision 58 is the crate-wide rule that
every response field Core may not yet send is `Option<T>` with `#[serde(default)]`; decision 60 is
that rule applied to `dev_bench_hello`'s three identity fields, precisely because decision 47's
rename meant an older Core does not send them. `firmware_version` is a plain `String` on
`embarch-core-client` today (`crates/embarch-core-client/src/client.rs`), and `embarch-api`'s
reflash gate **compares** it (`src/reflash.rs:259-270`).

So a renamed Core plus an un-tolerant client gives a silent empty string where a version check
should be — **a real check turned vacuous, which is worse than the collision this task exists to
fix.** And this is not hypothetical: the Core running on this machine is the Windows service, which
is behind `main` by `core/015`'s outstanding native build, so "an older Core" is the bench.

## Consumers

- **`embarch-core`** — the response type for `GET /dev-bench/hello` (`src/study.rs`'s
  `HelloAckInfo`), and `interfaces/studies.md`'s row, which already documents the collision and
  would document the rename instead.
- **`embarch-api`** — `embarch-core-client`'s response struct and its doc comment,
  `src/reflash.rs`'s use, `src/cli.rs`'s `--json` key, `render_hello_ack`'s human line, the
  `dev_bench_hello` MCP tool's output, and `interfaces/tools-dev-bench.md`.
- **`embarch-ui`** — **two lines only.** It already spells the value `dev_bench` on its own
  surface (`src/study_designer.rs:1581`, `:1645`); what changes is the field it deserializes. No
  rendering changes and no `embarch-ui` doc mentions the field.
- **`embarch-umbrella`** — **missing from this list until this run.** `doctor` check 13 parses the
  route's raw JSON for `firmware_version` (`src/doctor.rs`, `fetch_dev_bench_hello`), so the rename
  alone would have turned its stale-bench `Fail` into a permanent "unexpected response" `Warn`.
  Found by grepping every repo for the route, not by reading this list.
- **Neither suite guide mentions it** — checked, leg 105, and again in this run.

## Done when

- [x] **Announced in `#embarch-fleet` with its own 30-minute window**, naming the three repos and
      the breaking-change half. `suite/036`'s window does not cover this.
- [x] Either the rename lands across every consumer above **with the old-Core tolerance answered**
      — `Option` + `#[serde(default)]` under decision 58, and an explicit decision about what the
      reflash gate does when the field is absent, which must not be "treat it as matching" — **or**
      this task is closed and the answer recorded as a numbered decision in `embarch-core`, since
      it owns the route. *The rename, on branches: `embarch-core` decision 108 for the route,
      `embarch-api` decision 105 for the tolerance and the gate.*
- [x] Whichever way it goes, `embarch-study-designer` decision 74 gains a sentence pointing at the
      answer. 74 deliberately left this open and says so; it should not stay open in 74 after it is
      closed here.
- [x] Gate green in every repo touched, **including a native Windows build where `embarch-core` is
      involved**; `changelog.d/` fragments for each. *The Windows build was in a scratch copy, with
      no deploy (the header has the record).*

## Do not

**Do not rename `HelloAck.firmware_version` on the wire.** `embarch-study-designer` decision 74
rejected that on cost — it is a schema bump that reflashes every bench and redeploys Core in one
sitting — and its reversal condition is the next wire bump taken for another reason. Taking it here
would be reversing a decision one day old for a reason it already weighed.

## Shipped

All on `agent/suite/037-rename-dev-bench-hellos-firmware-version-to-dev-bench-version-or-close-it`,
pushed, none landed:

- **`embarch-core` `c0d2a7e`** — `HelloAckInfo.firmware_version` → `dev_bench_version`, so the
  route, the gate and `Provenance` read one name; the wire `HelloAck` is untouched. A test pins the
  response's key set. Decision 108.
- **`embarch-api` `8067c4f`** (on `origin/main` `d36be9e`, which carries api/126 and api/127) —
  `HelloAckResponse.dev_bench_version: Option<String>`, `#[serde(default)]`, no alias;
  `render_hello_ack`, `dev-bench-hello --json` and `run_study`'s gate follow it. Decision 105.
- **`embarch-ui` `2e16164`** — one helper feeds both bench-state reads; absence is a reason, shown
  as unavailable. Builds only against the `embarch-api` branch.
- **`embarch-umbrella` `47feb0f`** — check 13 reads `dev_bench_version`; absence is a `Warn` naming
  the rename.
- **`embarch-doc`** — decisions core 108 and api 105; study-designer 74's open paragraph closed;
  umbrella 19, the doctor-chain row and the message-rendering reference; the Core and api interface
  rows; a Core `open.md` bullet for the undeployed rename, which put that file in reserve, so `tasks/core/126` files the debt; five `changelog.d/` fragments.

**The absent-field decision (api 105): an unreported bench version satisfies nothing but `any`.** A
pinned `requires.dev_bench_version` is refused before the DUT is built or flashed;
`allow_version_mismatch` lets it through as it does a mismatch, recording `dev_bench_version: null`,
because Core still gates the bench from its own handshake on submit.

**Gate** [2026-11-10]: `cargo build`, `cargo test`, `cargo clippy --all-targets -- -D warnings` green
in `embarch-core`, `embarch-api` (after the rebase onto `d36be9e`), `embarch-ui` and
`embarch-umbrella`, the last two built against the `embarch-api` branch through a symlink farm in
`/tmp`; `check-client-names.py --repo` clean on all four; `scripts/check-docs.py` all 12 green on this branch [2026-11-11]. Nothing on any `origin/main` moved between the build and the doc commit, so the Windows build still matches the SHAs above.
Native Windows build: the header.

**Land in this order**, shared crate before its consumer: `embarch-core`, `embarch-api`,
`embarch-ui`, `embarch-umbrella`, then `embarch-doc`. **Deploy Core first, then rebuild the API,
`embarch-ui` and `embarch`.** Both skews refuse rather than pass: a new client against the installed
Core reports the bench's build as unknown, and the old API against a new Core fails
`dev_bench_hello` outright on the missing required `firmware_version` until it is rebuilt.
