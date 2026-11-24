Edit set for EMB-316 (doc/101), applied at the fold; no guide was edited by the worker, and `suite/hil-guide.md` is untouched. One block per edit, in file order. Each `Was` is the exact current text (a unique match in its file); each `Now` is the replacement verbatim. Applying all of them takes `studies-guide.md` from 23,029 B to 21,421 B, `user-guide.md` from 22,948 B to 22,984 B and `agent-guide.md` from 4,399 B to 4,792 B.

**Where the lore lives after these edits.** Reflash and `--reflash none` semantics, the no-`git checkout` rule and `--allow-version-mismatch`: `hil-guide.md` Study 2 and "What you never do". Truncation: `hil-guide.md` Study 4 step 1. Address byte order, most significant first: `hil-guide.md` Study 1, with the code locations that enforce it kept in `studies-guide.md` 3b. Census by a failed `BleConnect`: `hil-guide.md` Study 1, with the bench's own measurements (the 64-byte `fail_reason`, nameless advertisers, `dev-bench.log`) kept in `studies-guide.md` 3a. Kept in `studies-guide.md` because `hil-guide.md` does not state them: `--reflash both` and the reason `none` is the default, the DUT-version-is-a-claim limit (`git describe`), the UI Build card, `--raw`, and the retired per-channel commands.

**Two notes for the fold.** (1) The task and the audit say "`user-guide.md` §9", and the "Testing against a second board?" sentence is there, as the last paragraph of §9 "The token"; the edit replaces that paragraph in place. (2) Other docs link `studies-guide.md` §1 and §2 by number (`notes/hil/02-study.md`, `06-report-and-publish.md`, `09-trust-model.md`); the headings are unchanged, and the facts those links cite (truncation reported per capture, no `git checkout`, bench version measured and DUT version claimed) are all still stated, in `hil-guide.md` or §2.

---

**Target:** suite/agent-guide.md — §1, new paragraph before the "### 1.1" heading
**Was:**

```text
### 1.1 Which operations should need your approval
```

**Now:**

```text
**For hardware work, read the HIL guide first.** `embarch-api guide hil` prints what every mode shares (what you are trusted with and never do, choosing Live, Study or Test, what comes before any hardware), and `embarch-api guide hil study` prints the Study walkthrough, from writing a study to publishing it. The same text is [hil-guide.md](hil-guide.md). Live and Test are not written yet.

### 1.1 Which operations should need your approval
```

---

**Target:** suite/user-guide.md — §9 (the last paragraph before "## 10"), replace the whole paragraph
**Was:**

```text
**Testing against a second board?** Studies, the dev bench, and capturing a DUT trace are their own guide: [studies-guide.md](studies-guide.md).
```

**Now:**

```text
**Testing against a second board?** Start with `embarch-api guide hil study` ([hil-guide.md](hil-guide.md)), then the bench and trace notes in [studies-guide.md](studies-guide.md).
```

---

**Target:** suite/studies-guide.md — §1, the "Partly usable" quote
**Was:**

```text
> **Partly usable.** The endpoints and CLI are implemented and have run against a real bench and a real DUT. **What is missing is hardware**: power-sampling hardware (deferred by decision), GPIO and analog stimulus, and any physical DUT connector. Read this as "how the parts that exist work", not a tutorial you can follow end to end.
```

**Now:**

```text
> **Partly usable.** The endpoints and CLI are implemented and have run against a real bench and a real DUT. **What is missing is hardware**: power-sampling hardware (deferred by decision), GPIO and analog stimulus, and any physical DUT connector. Read this as "how the parts that exist work"; the tutorial is the HIL guide's Study section, which §1 points at.
```

---

**Target:** suite/studies-guide.md — §1, from "Start from the worked example" through the truncation paragraph (the sh block included); the "Add `--raw`" paragraph after it stays
**Was:**

```text
**Start from the worked example, not from the type tables.** `embarch-api/tests/fixtures/self_test_study.json` is a complete, currently-valid study — the §3a self-test — and a test deserializes it on every run, so it cannot go stale. The one shape a `serde` reading will not predict is that **`action` is externally tagged**: one key, the variant name, its value the fields (`{"BleAdvertise": {…}}`). Field by field: [embarch-study-designer/interfaces/types.md](../embarch-study-designer/interfaces/types.md).

```sh
embarch-api run-study --study-file my-study.json     # returns a study_id
embarch-api study-status <study_id>                  # pending | running | completed | failed
embarch-api list-study-streams <study_id>            # what it captured, and whether anything was lost
embarch-api study-stream-data <study_id> --name <tap> --out capture.csv
```

**Read `list-study-streams` before you read a capture.** It lists every capture the study declared, how many bytes each wrote, and — **the column that matters** — whether it was **truncated**. A truncated capture is a short one: either retention rotation deleted an older segment, or the bench reported dropping records. **Nothing else in the suite will tell you, and a short capture read as a complete one is the failure this whole area is built to prevent.** A capture listed with 0 bytes was declared and produced nothing, **which is a different problem from one that was never declared.**
```

**Now:**

```text
**The walkthrough is in the HIL guide, not here.** Writing a study, running it, reading its losses and publishing it are the Study section: `embarch-api guide hil study` ([hil-guide.md](hil-guide.md)), with a complete worked study (`embarch-api/tests/fixtures/ble_gatt_rate_study.json`) and the truncation, reflash and address rules, each stated there once. Field by field: [embarch-study-designer/interfaces/types.md](../embarch-study-designer/interfaces/types.md). This guide keeps what that one leaves out: this bench's measured behaviour (§3 to §3b) and DUT traces (§4).
```

---

**Target:** suite/studies-guide.md — §2, from "A study declares the bench and DUT builds" through the `--allow-version-mismatch` paragraph; "One limit worth knowing" stays
**Was:**

```text
A study declares the bench and DUT builds it is meant to run against, and **`"any"` is a legal, explicit answer for either.** Core checks the bench's declaration against what the bench actually reports and **refuses the study before any step runs** if they disagree, naming both strings.

`--reflash` says what to do about a disagreement:

```sh
embarch-api run-study --study-file my-study.json --reflash dev-bench
embarch-api run-study --study-file my-study.json --reflash dut --project my-firmware
```

`none`, the default, means **"run against what is already on the boards"** — flashing is the destructive half, and **a study that just observes a board you flashed by hand should not quietly overwrite it.** The others rebuild and reflash **from your working tree exactly as it stands right now.**

**EmbArch will not run `git checkout` for you, ever.** If your tree is not at the revision the study asks for, **the run fails, names both revisions, and stops before touching the board. Moving your tree is your call, not a test harness's.**

`--allow-version-mismatch` runs anyway, **and the override is written into the result** naming what was required and what actually ran — **so a result that was waved through never looks like one that met its requirements.**
```

**Now:**

```text
What a study's `requires` and `--reflash` do, that EmbArch never runs `git checkout`, and what `--allow-version-mismatch` writes into the result are the HIL guide's Study section 2 (`embarch-api guide hil study`). Two things it leaves out: `--reflash` takes `none` (the default), `dev-bench`, `dut` or `both`; and `none` is the default because flashing is the destructive half, so a study that observes a board you flashed by hand does not overwrite it.
```

---

**Target:** suite/studies-guide.md — §3a, first paragraph (one phrase; the paragraph is quoted whole so it can be found)
**Was:**

```text
**One study has been run end to end by the fleet against the real bench** [measured 2026-09-06, `dev-bench` probe `001057729826`, hardware ID `6fcddc36cb781b71`, both roles validated live first]. It is the two-step `BleAdvertise` self-test — **`embarch-api/tests/fixtures/self_test_study.json`**, the file §1 points at — submitted with `reflash` at its `none` default — **nothing was built and nothing was flashed** — and it passed 2 of 2 steps. Its provenance came back `dev_bench_source: ReportedByDevBench, dev_bench_version: 49958d34` against a `Declared` firmware version of `any`, which is §2's asymmetry showing up in a real result: the bench's version is a measurement and the DUT's is a claim.
```

**Now:**

```text
**One study has been run end to end by the fleet against the real bench** [measured 2026-09-06, `dev-bench` probe `001057729826`, hardware ID `6fcddc36cb781b71`, both roles validated live first]. It is the two-step `BleAdvertise` self-test — **`embarch-api/tests/fixtures/self_test_study.json`**, the file in `embarch-api/tests/fixtures/` — submitted with `reflash` at its `none` default — **nothing was built and nothing was flashed** — and it passed 2 of 2 steps. Its provenance came back `dev_bench_source: ReportedByDevBench, dev_bench_version: 49958d34` against a `Declared` firmware version of `any`, which is §2's asymmetry showing up in a real result: the bench's version is a measurement and the DUT's is a claim.
```

---

**Target:** suite/studies-guide.md — §3a, the "How to find out" paragraph
**Was:**

```text
**How to find out what to put there: run a `BleConnect` whose `target_name` no device could have.** A failed name match does not return a bare timeout — the bench reports what *was* on the air, in the step's own `fail_reason`. That is the scan, and it is why there is no separate scan action. A blank name means "no filter", so the nonsense name is the whole trick.
```

**Now:**

```text
**How to find out what to put there is the HIL guide's** (run a `BleConnect` whose `target_name` nothing has, and read the census). What it leaves out: a failed name match does not return a bare timeout, it reports what *was* on the air in the step's own `fail_reason`. That is the scan, which is why there is no separate scan action; a blank name means "no filter", so the nonsense name is the whole trick.
```

---

**Target:** suite/studies-guide.md — §3b, the "bytes go in display order" paragraph
**Was:**

```text
**The bytes go in display order, most significant first.** `C4:82:E1:42:B1:26` is `[196, 130, 225, 66, 177, 38]` with `kind: "Public"`, exactly as `bt_addr_le_to_str` prints it in the census log — verified by connecting with it, above. **It is written down in three places, and the type is one of them**: `embarch-study-designer/src/ids.rs` states it on `BleAddress` itself (both `BleAddressKind`s, never reversed in that crate); `embarch-study-designer/interfaces/types.md` states it in prose; and `ble_bridge_real.c`'s `to_bt_addr` reverses it for Zephyr with a comment saying so. A wrong guess still fails *silently* — the step simply never matches — which is why the type saying it matters (`embarch-dev-bench` decision 23).
```

**Now:**

```text
**The byte order is the HIL guide's rule, and it has been checked on the air.** `C4:82:E1:42:B1:26` is `[196, 130, 225, 66, 177, 38]` with `kind: "Public"`, exactly as `bt_addr_le_to_str` prints it in the census log, verified by connecting with it, above. **It is written down in three places, and the type is one of them**: `embarch-study-designer/src/ids.rs` states it on `BleAddress` itself (both `BleAddressKind`s, never reversed in that crate); `embarch-study-designer/interfaces/types.md` states it in prose; and `ble_bridge_real.c`'s `to_bt_addr` reverses it for Zephyr with a comment saying so. A wrong guess still fails *silently* — the step simply never matches — which is why the type saying it matters (`embarch-dev-bench` decision 23).
```
