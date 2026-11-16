# HIL notes: the report and publishing

**Status:** draft, 2026-11-15.

Shared by the Study and the Test: one publish mechanism, one zip shape, one audit appendix, one `verify`.

## Publish

- **An explicit step.** A finished run is a draft; **`publish <run id>`** (an MCP tool and a subcommand; renamed from `study_publish`, owner, review round 1) publishes it, a Study run or a Test run alike, a Test run as one zip for the whole run. **Choosing what to publish does not choose what the reader sees**: a report lists every run of the same test or study on the same DUT image, published or not, with its verdict, from the ledger's append-only rows (owner, review round 1). A pass after four failures shows the four failures.
- **Two interop exports in every zip** (owner, review round 1): **JUnit XML**, the de-facto CI summary, and **OCP Test & Validation v2.0 JSON Lines** (MIT, under JSON Schema), the lossless one; the six verdicts map onto its status and result, inconclusive and cancelled through its metadata ([11](11-prior-art.md#classical-hil-frameworks-formats-and-report-tooling)).
- **One zip with everything**: the PDF report, the study file, `run.json` for a Test ([03](03-test.md#selecting-and-rerunning)), `events.json`, `measurements.json` ([02](02-study.md#measurements)), the operator's notes, the hash manifest, and **every capture twice: the raw `.bin` (the evidence) and its CSV rendering (what a reader opens).** **It also carries `report.typ` and the Typst packages it used, so the PDF can be rebuilt from the zip alone**, with no repo and no network. **It is not for a repo.**
- **Written to a local folder set in embarch-api's configuration, with no default**: publish refuses until the folder is configured, and says how. Sending the zip anywhere else stays a human step.
- **Named `<date>-<slug>-<id8>.zip`**: the date, the study's slug (a Test run's suite name), the first 8 characters of the run ID.
- **The operator's notes come in as a `notes` parameter**: the agent asks the person and passes their words verbatim. A UI form comes later.
- **A publish is never overwritten** (owner, review round 1; *replaces "republishing overwrites"*). `publish` of the same run again writes **`-r2`**, then `-r3`, each naming the revision it supersedes and that revision's manifest hash; the earlier zips stay. **The manifest's own hash is also recorded outside the zip**, in the run's ledger row, so a zip edited after publish is detectable without trusting the zip.

## Verify

**`embarch-api verify <zip>`** (owner, review round 1), open source like the rest, so a client runs it with no trust in the machine that produced the zip:

1. **The manifest**: every file's SHA-256 matches.
2. **The measurements**: every derived measurement recomputed from the raw captures with the built-in reducers ([02](02-study.md#measurements)) matches `measurements.json`.
3. **The verdicts**: every verdict recomputed from `run.json` and the measurements matches the report.
4. **The prose**: the untagged numbers that match no measurement are the ones the appendix lists.

It answers each check with what it compared, and names the embarch-api version that produced the zip and the one that verified it. **This is what lets a reader check the report without trusting the agent** ([09](09-trust-model.md)): measurements and verdicts are pure functions of files the zip carries.

## The report

- **Rendered by embarch-api, to PDF, with Typst built into the binary**: no external tool to install, plots drawn as SVG and embedded. The Typst version is recorded in the appendix, since output depends on it. **The stack** (owner, review round 1): the `typst` and `typst-pdf` crates (Apache-2.0) through `typst-as-lib` (MIT), packages vendored under a local root so no registry is contacted, **plots with lilaq (MIT), not cetz (LGPL-3.0)**, `PdfOptions.ident` and `timestamp` set for stable re-renders.
- **A plot over a large capture draws per-bin min and max, never an average**, as the UI's series route already does ([embarch-ui interfaces](../../embarch-ui/interfaces.md)); the raw file in the zip holds the detail.
- **A Study's body is its own `report.typ`**, free in shape, compiled against the run's measurements and files ([02-study.md](02-study.md#the-report)).
- **A Test's body is organised by requirement**: each verdict cites the run behind it; **every applicable test that did not run is listed, with why**; the standard's own coverage is counted; and **a fixed sentence says it is pre-compliance evidence, not a certification by any standards body** ([03-test.md](03-test.md#the-report)).
- **Each prose block names its author**, `agent (<model id>)` or a person, and **every untagged number in prose that matches no measurement is listed** in the appendix ([02](02-study.md#the-report)).

## The audit appendix

**Appended by embarch-api to every report; a study cannot leave it out.**

| Item | What it holds |
|---|---|
| **Pinned inputs** | The study file's hash, and for a Test `run.json`'s, the plan's and the suite's commit; the DUT image's SHA-256 and **whether it was verified by readback** or is a claim, with why ([03](03-test.md#a-run)); the git branch, commit and **whether the tree was dirty**; each bench board's version (a measurement: the board reports it); embarch-api's and Core's builds; the Typst version; the lease holder |
| **Definition files** | Each definition the run read (study, test, plan, bench) by its hash, since `embarch/` is untracked ([03](03-test.md#it-grows-out-of-the-ledger)) |
| **Instruments** | Each instrument's `*IDN?` reply, read at the smoke check, and its calibration due date as the engineer declared it |
| **Measurements** | Every measurement: value, unit, resolution, and the capture file and rows it came from |
| **Decision rule** | Simple acceptance or a guard band, per limit ([03](03-test.md#the-verdict)) |
| **Limits and losses** | Truncated captures, dropped records, overrides such as `--allow-version-mismatch`, inconclusive verdicts and why, and what is measured against what is assumed |
| **Inputs and their provenance** | For a Test, each DUT capability (`measured`, `decoded`, `confirmed`, `declared`), each hook mapping, and who confirmed each |
| **The study design** | The study as submitted, and a readable list of its steps, taps and checks; for a test copied from a premade one, its `derived_from` and every verdict-deciding field changed |
| **Every run** | Every run of the same test or study on the same image, with its verdict and whether it was published |
| **Prose** | Each block and its author; every untagged number that matches no measurement |
| **Plots** | Each plot cites the file it was drawn from |
| **Operator and setup notes** | Who ran it, which bench, cables and fixtures, conditions: typed in by the person at publish time; each prompt's answer and the surface it came through (`ui`, `mcp`, `cli`) |
| **Hash manifest** | SHA-256 of every file in the zip, and the revision it supersedes |

**The DUT's firmware version is a claim unless it was read back**: without the readback, nothing reads it off a DUT, so it means "this run built and flashed this tree" ([studies guide §2](../../suite/studies-guide.md)). The appendix says which, in those words.

## Open

- **A zip's own size**: a long capture is in it twice, raw and rendered. No limit decided; measure on the first real Study.
- **Signing the manifest** with a key per installation, so a zip's origin is checkable, not only its integrity. The prior-art survey looks at what exists ([09](09-trust-model.md#open)).
