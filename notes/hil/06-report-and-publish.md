# HIL notes: the report and publishing

**Status:** draft, 2026-11-15.

Shared by the Study and the Test: one publish mechanism, one zip shape, one audit appendix.

## Publish

- **An explicit step.** A finished run is a draft; `study_publish <id>` (an MCP tool and a subcommand) publishes it. Only the runs worth keeping are published. A Test run publishes the same way, as one zip for the whole run.
- **One zip with everything**: the PDF report, the study file, `events.json`, the operator's notes, the hash manifest, and **every capture twice: the raw `.bin` (the evidence) and its CSV rendering (what a reader opens).** **It also carries `report.typ` and the Typst packages it used, so the PDF can be rebuilt from the zip alone**, with no repo and no network. **It is not for a repo.**
- **Written to a local folder set in embarch-api's configuration, with no default**: publish refuses until the folder is configured, and says how. Sending the zip anywhere else stays a human step.
- **Named `<date>-<slug>-<id8>.zip`**: the date, the study's slug (a Test run's suite name), the first 8 characters of the run ID.
- **The operator's notes come in as a `notes` parameter**: the agent asks the person and passes their words verbatim. A UI form comes later.
- **Republishing overwrites.** `study_publish <id>` again replaces the zip, so a copy someone received earlier can differ from the current one; the hash manifest inside each copy is how two copies are told apart.

## The report

- **Rendered by embarch-api, to PDF, with Typst built into the binary**: no external tool to install, plots drawn as SVG and embedded.
- **A plot over a large capture draws per-bin min and max, never an average**, as the UI's series route already does ([embarch-ui interfaces](../../embarch-ui/interfaces.md)); the raw file in the zip holds the detail.
- **A Study's body is its own `report.typ`**, free in shape, compiled against the run's files ([02-study.md](02-study.md#the-report)).
- **A Test's body is organised by requirement**: each verdict cites the run behind it, and **every applicable test that did not run is listed, with why** ([03-test.md](03-test.md#the-report)).

## The audit appendix

**Appended by embarch-api to every report; a study cannot leave it out.**

| Item | What it holds |
|---|---|
| **Pinned inputs** | The study file's hash, the DUT image's SHA-256, the bench firmware's version (a measurement: the bench reports it), the git branch and commit, the Core version, the lease holder |
| **Traceable numbers** | Every number in the report points at the capture file and row it came from |
| **Limits and losses** | Truncated captures, dropped records, overrides such as `--allow-version-mismatch`, and what is measured against what is assumed |
| **The study design** | The study as submitted, and a readable list of its steps, taps and checks |
| **Plots** | Each plot cites the file it was drawn from |
| **Operator and setup notes** | Who ran it, which bench, cables and fixtures, conditions: typed in by the person at publish time |
| **Hash manifest** | SHA-256 of every file in the zip |

**The DUT's firmware version is a claim, not a measurement**: nothing reads it back off a DUT, so it means "this run built and flashed this tree" ([studies guide §2](../../suite/studies-guide.md)). The appendix says so in those words.

## Open

- **A zip's own size**: a long capture is in it twice, raw and rendered. No limit decided; measure on the first real Study.
