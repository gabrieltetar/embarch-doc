# embarch-api: `publish`, and the zip it writes

**Status:** active, 2026-11-22 (`tasks/api/167` and `168`, HIL M1.10). Why: [decisions 112 to 114](../decisions/publish.md) and [115 to 117](../decisions/publish-revisions.md). Core's side: [embarch-core/interfaces/publish.md](../../embarch-core/interfaces/publish.md). Source: `notes/hil/06-report-and-publish.md`. A reader builds `verify` (M1.11) from this file and those two, not from this crate's source. `verify`'s own surface is [verify.md](verify.md); why: [decisions 118 to 121](../decisions/verify.md).

## The tool and the subcommand

`publish` (MCP) and `publish <run_id>` (CLI) over `embarch_api::publish::run`, behind the `pdf` feature (a build without it refuses by name).

| Param | Meaning |
|---|---|
| `run_id` | A finished **Study** run's id. A Test run does not exist in milestone 1 |
| `notes` / `--notes` | Optional. The person's words **verbatim**; adopted through Core, which records the token's scope and the text's hash (a note passed here reads "relayed by the agent") |
| `prose` / `--prose <path>` (repeatable), `--prose-author`, `--prose-reviewed-by` | Optional. Prose files the agent wrote for the run: adopted as `prose/<name>`, carried in the zip, scanned for numbers. `author` is the model id (an agent's block) or a name; `reviewed_by` the person who adopted an agent's block. Core records the token's scope, not the names ([decision 116](../decisions/publish-revisions.md)) |
| `report` / `--report` | Optional path to the study's `report.typ`. Absent, the zip carries a data section this crate generates. Nothing finds a study's folder on the caller's behalf |

**The publish folder** is `[publish] folder = "<path>"` in the config, **with no default**. With none, `publish` refuses before it asks Core anything, and the message prints the table to add. The folder is created if its parent exists. A `report.typ` that sets its own page footer, or draws a picture (`image`, `svg`; not `image()` of a `streams/` capture), is refused, also before Core is asked.

**Result** (`--json`, the MCP result): `{success, zip, zip_sha256, revision, manifest_sha256, report_source, files, embarch_api_files [{name, sha256}], supersedes {revision, manifest_sha256, from_zip} or null, warnings}`. A non-empty `warnings` is `success: false`, exit 1 and an MCP error: **the zip is written and is less than a complete report**, so the caller says so. Core's refusals (`404`, `409`) are relayed as text.

## The zip

Named `<date>-<slug>-<id8>.zip`: the UTC date of the publish, the study name slugged (lowercase letters and digits, runs of the rest one `-`, `study` if none), the first 8 characters of the run id; `-r<N>` from revision 2. **Never overwritten** (`create_new`). **A revision is built from the earlier zip** in the folder: its `measurements.json` and `streams/*` renderings are read from it, so a run whose captures are swept is republished from it. If Core answers `report-data` with `409` (the run swept), publish hands Core the earlier zip's manifest and then every Core file it names (`PUT /study/{id}/restore/{name}`, `embarch-core` decision 120), asks again, and continues; with no earlier zip it refuses, naming the folder and the file name it looked for, and writes nothing ([decision 126](../decisions/publish-revisions.md)). The appendix names the revision superseded and that zip's manifest hash. Entries are in name order with a fixed time, so the same entries are the same bytes.

**Core's files**, byte for byte as Core served them, each checked against the manifest's digest: `manifest.dsse.json` (signed), `report-data.json`, `report-data.dsse.json`, `run-log-segment.jsonl`, `call-log-segment.jsonl` (a manifest subject Core writes with each revision, never restored), and every subject of the manifest: `study.json`, `events.json`, `measurements.json` (when the study declares any), `record.dsse.json`, `streams/*` (each tap's `.bin`, and its rendering, `.csv` or `.txt`, **as Core made it**: a `Raw` tap has none, and none is invented).

**embarch-api's files**, all listed in the manifest's `embarch_api_files` with the hashes sent at publish and never its subjects:

| Name | What |
|---|---|
| `report.pdf` | `report.typ` then `appendix.typ` under the compile's page-number footer ([report-pdf.md](report-pdf.md)); Typst root = the staged files; `ident` `<run id>-r<N>`, time = the publish's |
| `report.typ` | The study's own, or the generated data section: the run status, each capture with its row count, each measurement |
| `appendix.typ` | The fixed audit appendix, generated from `report-data.json` and `measurements.json` as Typst string literals: observed by Core, claimed by the build, pinned inputs (embarch-api's and Typst's versions), attestation, measurements, the study's steps, adopted notes and prose (each with its author, attribution, token scope and hash), **the numeric-oracle listing** (every number of the prose files and `report.typ` as cited, cited-but-mismatched, tagged, unbound, untagged or hardcoded, with file and line: [decision 115](../decisions/publish-revisions.md)), the notes, limits and losses (including what milestone 1 does not carry), the manifest |
| `exports/junit.xml` | One `<testsuite>`, a `<testcase>` per step; `<error type="step_failed"\|"step_timed_out">`, never `<failure>` or `<skipped>`; properties `run_status`, `attestation`, `qualifiers`, `measurement.<name>` and its `.by`, `.bench_image`, `.u_source`, `.declared_by` |
| `exports/ocp-tv.jsonl` | OCP T&V v2.0 JSON Lines: run start, a start and end per step (`status` COMPLETE or ERROR, `result` NOT_APPLICABLE, outcome in metadata), a measurement record each, run end (COMPLETE for `completed`). Never PASS or FAIL |
| `notes/operator-notes.txt` | The notes, when given; the name Core adopted them under, so check 5 hashes it against `report-data.json`'s `adopted` |
| `prose/<name>` | Each prose file, as adopted, so check 5 hashes it against `report-data.json`'s `adopted` |
| `typst-packages/<namespace>/<name>/<version>/…` | **Every embedded package file**, when the study brought its own `report.typ`; none for the generated one, which imports nothing |

**Both exports are pure functions** of `report-data.json`, `measurements.json` and the step outcomes (`publish_export::{junit_xml, ocp_jsonl}`), with no clock beyond the signed stamps, so `verify` regenerates and compares bytes. **The PDF rebuilds byte for byte from the zip alone**: unpack, stage `report.typ`, `appendix.typ`, `report-data.json`, `measurements.json` and `streams/*.csv|txt` under one root, render with `ident` and the time the publish used (a test does it).

**What the PDF read is what Core signed**: `publish` compares each file it staged (`report-data.json`, `measurements.json`, the renderings) with the one the manifest names, and writes nothing on a difference.

## What publish reads of Core before the manifest exists

Moved verbatim to [publish-pending-reads.md](publish-pending-reads.md).

## verify

Moved verbatim to [verify.md](verify.md).
