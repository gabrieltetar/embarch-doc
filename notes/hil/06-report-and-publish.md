# HIL notes: the report and publishing

**Status:** draft, 2026-11-15.

Shared by the Study and the Test: one publish mechanism, one zip shape, one audit appendix, one `verify`.

## Publish

- **An explicit step.** A finished run is a draft; **`publish <run id>`** (an MCP tool and a subcommand; renamed from `study_publish`, owner, review round 1) publishes it, a Study run or a Test run alike, a Test run as one zip for the whole run. **Choosing what to publish does not choose what the reader sees**: a report lists every run of the same test or study on the same unit, published or not, with its verdict (owner, review round 1), **read from Core's run log**, the repo's rows being its mirror, and grouped by DUT image and definition hash so a rebuild hides nothing ([03](03-test.md#the-report)) (review round 2, recommended). A pass after four failures shows the four failures.
- **Two interop exports in every zip** (owner, review round 1): **JUnit XML**, the de-facto CI summary, and **OCP Test & Validation v2.0 JSON Lines** (MIT, under JSON Schema), the structured one ([11](11-prior-art.md#classical-hil-frameworks-formats-and-report-tooling)). **Neither is lossless; EmbArch's own record is.** **No verdict but pass maps to a passing outcome**; `skipped` maps to JUnit's `<skipped>`, which is not a pass but which most CI does not fail on, so a gate that must fail on a skip reads its reason. A requirement's `not verified` is carried in each of its tests' properties, since JUnit and OCP T&V have no requirement level (review round 2, recommended):

  | Verdict | JUnit | OCP T&V status, result |
  |---|---|---|
  | pass | (no child) | COMPLETE, PASS |
  | fail | `<failure>` | COMPLETE, FAIL |
  | error | `<error>` | ERROR, NOT_APPLICABLE |
  | inconclusive | `<failure type="inconclusive">` | ERROR, NOT_APPLICABLE, verdict in metadata |
  | cancelled | `<error type="cancelled">` | ERROR, NOT_APPLICABLE, verdict in metadata |
  | skipped | `<skipped>` with the reason | SKIP, NOT_APPLICABLE |
- **One zip with everything**: the PDF report, the study file, `run.json` for a Test ([03](03-test.md#selecting-and-rerunning)), `events.json`, `measurements.json` ([02](02-study.md#measurements)), **Core's signed records of every test and study in it, and Core's signature over the manifest** ([12](12-prevention.md#what-core-then-guarantees-in-code)) (review round 2, recommended), the operator's notes, the hash manifest, and **every capture twice: the raw `.bin` (the evidence) and its CSV rendering (what a reader opens).** **It also carries `report.typ` and the Typst packages it used, so the PDF can be rebuilt from the zip alone**, with no repo and no network. **It is not for a repo.**
- **Written to a local folder set in embarch-api's configuration, with no default**: publish refuses until the folder is configured, and says how. Sending the zip anywhere else stays a human step.
- **Named `<date>-<slug>-<id8>.zip`**: the date, the study's slug (a Test run's suite name), the first 8 characters of the run ID.
- **The operator's notes come in as a `notes` parameter**: the agent asks the person and passes their words verbatim. A UI form comes later. **Notes passed with the agent's token read "relayed by the agent"; notes typed on the card with the person's token read as the person's** (review round 2, recommended).
- **A publish is never overwritten** (owner, review round 1; *replaces "republishing overwrites"*). `publish` of the same run again writes **`-r2`**, then `-r3`, each naming the revision it supersedes and that revision's manifest hash; the earlier zips stay. **The manifest's own hash is also recorded outside the zip**, **in Core's run log**, signed, so a zip edited after publish is detectable without trusting the zip (review round 2, recommended).

## Verify

**`embarch-api verify <zip>`** (owner, review round 1), open source like the rest, so a client runs it with no trust in the machine that produced the zip. Its checks, in order (review round 2, recommended):

0. **The signatures**: Core's signature over the manifest and over each test's and study's record verifies **against a key fingerprint the client got from the engineer out of band**, never against the one the report prints, which is shown only to compare by eye; every capture, `events.json`, `measurements.json` and `run.json` in the zip is a subject of a signed record. **Attested means the key matches a fingerprint from Core's elevated install**, which the engineer hands the client with the zip; any other key, a development Core's included, verifies the zip's integrity and says **"origin unattested"**, whatever its record claims about itself ([12](12-prevention.md#the-root-of-trust-core-under-its-own-account)).
1. **The manifest**: every file's SHA-256 matches.
2. **The measurements**: every step-time number re-parsed from the raw replies with `run.json`'s patterns, and every derived measurement recomputed from the raw captures, **with the shared crate's version the signed records name**, matches `measurements.json`; a zip from a crate version `verify` lacks is reported as not recomputed, never as matching.
3. **The verdicts**: every verdict recomputed from `run.json`, the step outcomes in `events.json` and the measurements matches the report, the requirement roll-up included.
4. **The PDF's text**: every number in the rendered PDF matches a signed measurement, is listed in the appendix (untagged, tagged or hardcoded), or sits in an exempt context ([02](02-study.md#the-report)). So the PDF, which embarch-api assembles, cannot carry a number the signed data does not.
5. **The labels**: the attestation line on the report's first page and each person's act's attribution match what the signed records say.

**What `verify` cannot recompute**: what Core read from the hardware, the identities, the image readback, an instrument's `*IDN?`, a bench board's reported version. For those it checks Core's signature, and the report says they rest on Core. It answers each check with what it compared, and names the embarch-api version that produced the zip and the one that verified it. **This is what lets a reader check the report without trusting the agent** ([09](09-trust-model.md)): measurements and verdicts are pure functions of files the zip carries, and the files are Core's.

## The report

- **Rendered by embarch-api, to PDF, with Typst built into the binary**: no external tool to install, plots drawn as SVG and embedded. The Typst version is recorded in the appendix, since output depends on it. **The stack** (owner, review round 1): the `typst` and `typst-pdf` crates (Apache-2.0) through `typst-as-lib` (MIT), packages vendored under a local root so no registry is contacted, **plots with lilaq (MIT), not cetz (LGPL-3.0)**, `PdfOptions.ident` and `timestamp` set for stable re-renders.
- **A plot over a large capture draws per-bin min and max, never an average**, as the UI's series route already does ([embarch-ui interfaces](../../embarch-ui/interfaces.md)); the raw file in the zip holds the detail.
- **A Study's body is its own `report.typ`**, free in shape, compiled against the run's measurements and files ([02-study.md](02-study.md#the-report)).
- **A Test's body is organised by requirement**: each verdict cites the run behind it; **every applicable test that did not run is listed, with why**; the standard's own coverage is counted; the unit and who is responsible are named; and **a fixed statement says it is pre-compliance evidence, not a certification and not an accredited test report** ([03-test.md](03-test.md#the-report)).
- **Each prose block names its author**, `agent (<model id>)` or a person, and **every untagged number in prose that matches no measurement is listed** in the appendix ([02](02-study.md#the-report)).

## The audit appendix

**Appended by embarch-api to every report; a study cannot leave it out.**

| Item | What it holds |
|---|---|
| **Observed by Core** | The DUT image's SHA-256 as Core flashed it, and **whether the chip holds it** by readback, or why that is a claim ([03](03-test.md#a-run)); each bench board's image against EmbArch's released firmware, and its reported version; the unit's and every board's identity; Core's build and key fingerprint; the shared crate's version |
| **Claimed by the build** | The git branch, commit and **whether the tree was dirty**, the toolchain, the build host: what embarch-api reports, in the agent's reach, so labelled a claim (review round 2, recommended) |
| **Pinned inputs** | The study file's hash, and for a Test `run.json`'s, the plan's and the suite's version and commit; embarch-api's build; the Typst version; the lease holder |
| **Attestation** | **Which held for the person's acts, as Core observed it**: "person-scoped token", "passkey" or "agent-scoped only"; the engineer's statement that the agent ran in a container, labelled as the engineer's statement, since Core sees a token's scope and not where the agent ran (review round 2, recommended) |
| **Definition files** | Each definition the run read (study, test, plan, bench) by its hash, since `embarch/` is untracked ([03](03-test.md#it-grows-out-of-the-ledger)) |
| **Instruments** | Each instrument's `*IDN?` reply, read at the smoke check, and its calibration due date and its uncertainty as the engineer declared them (**a person's act**, refused with the agent's token, and carried into Core's signed record (review round 2, recommended)), **checked against the run's date**: a verdict resting on a measurement from an instrument past its due date is **inconclusive**, reason "calibration expired"; an undeclared date is shown as undeclared beside every measurement it touches. Each bench board's characterisation, where it times or measures |
| **Measurements** | Every measurement: value, unit, resolution, uncertainty, `by`, the instrument or board and its `bench_image`, and the capture file and rows it came from |
| **Decision rule** | Simple acceptance or a guard band, per limit ([03](03-test.md#the-verdict)) |
| **Limits and losses** | Truncated captures, dropped records, overrides such as `--allow-version-mismatch`, inconclusive verdicts and why, and what is measured against what is assumed |
| **Inputs and their provenance** | For a Test, each DUT capability (`measured`, `decoded`, `confirmed`, `declared`), each hook mapping, and who confirmed each |
| **The study design** | The study as submitted, and a readable list of its steps, taps and checks; for a test copied from a premade one, its `derived_from` and every verdict-deciding field changed |
| **Every run** | Every run of the same test or study on the same unit, from Core's run log, grouped by image and definition hash, with its verdict and whether it was published |
| **Prose** | Each block and its author, and the token that entered it; every untagged, tagged and hardcoded number ([02](02-study.md#the-report)) |
| **Plots** | Each plot cites the file it was drawn from |
| **Operator and setup notes** | Who ran it, which bench, cables and fixtures, conditions: typed in by the person at publish time; each prompt's answer, its kind, and **the token's scope it came with** (person, or relayed by the agent) beside the surface (`ui`, `mcp`, `cli`) (review round 2, recommended) |
| **Hash manifest** | SHA-256 of every file in the zip, and the revision it supersedes |

**The DUT's firmware version is a claim unless it was read back**: without the readback, nothing reads it off a DUT, so it means "this run built and flashed this tree" ([studies guide §2](../../suite/studies-guide.md)). The appendix says which, in those words.

## Open

- **A zip's own size**: a long capture is in it twice, raw and rendered. No limit decided; measure on the first real Study.
- **How a plot drawn by EmbArch's helper is marked in the PDF**, so `verify` can tell its axis ticks from a number in the text.
- **Whether `typst-pdf` renders byte-identically** across machines; `verify` does not depend on it, since it checks the PDF's numbers, not its bytes.
