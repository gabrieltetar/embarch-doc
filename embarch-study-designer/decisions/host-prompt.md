# embarch-study-designer decisions: A prompt that names a bench configuration

**Status:** active, 2026-11-01.

A field on host-run studies, additive to decision 80 (in [study.md](study.md)). Who resolves it: `embarch-ui` decisions 98 and 99.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 88 — `Prompt.bench_config`: a step names the bench configuration it wants, and nothing here resolves it

`HostAction::Prompt { text, bench_config: Option<String> }` (owner, 2026-11-01). A name only: what the bench must look like, never which cables (`embarch-ui` decision 10's indirection). **Whoever shows the prompt resolves it**, against the bench live there; Core forwards it unchanged (`embarch-core` decision 107). A name the bench lacks is never refused: a config is resolved when a study needs it, not checked at rename.

- **Shape only.** Refused: blank (absent is how a step names none), over `MAX_HOST_NAME_LEN`, a control character, U+2028/2029, a bidi format character or edge whitespace (it prints on one line and is looked up by exact name); in steps, teardown and a `Repeat` alike.
- **Skipped when `None`**: a study written before it serializes byte for byte as it did (test-pinned).
- **`HOST_TYPE_SCHEMA_VERSION` 20 to 21**, wire still 15. It moves though old studies load (decision 12): a v20 Core's `422` names the field, not the version. The gate is a strict match both ways, so Core, the API (MCP server restarted) and the UI deploy together; rebuild `embarch-umbrella` too, or `embarch doctor` check 11 warns.
- *Rejected:* a name convention inside `text`, which a typo breaks silently; a lookup here, with no bench to look in.
