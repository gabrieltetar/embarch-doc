# embarch-api decisions: The client crate's types follow Core's additions

**Status:** active, 2026-11-27.

How `embarch-core-client`'s request and response types take on fields Core added: a Test run prompt's kind, outputs and answer value (137), `/status`'s `mode` and `keyid` (139) and its one `host_type_schema_version` read from either key (150). The rule they apply, that a field an older Core may not send is an `Option<T>` with `#[serde(default)]` (58), stays in [client-crate.md](client-crate.md). Split out of it on 2026-11-27 (`api/222`), a verbatim move along a topical seam.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md). The crate's runtime stack, extraction, older-Core parsing rule, WSL2 predicate, topology types and token scopes: [client-crate.md](client-crate.md); its funnel and home: [client-crate-funnel.md](client-crate-funnel.md).

### 137 — The client's prompt types carry a Test run prompt's kind, outputs and answer value, additively

`PendingPrompt` gains `kind` (`embarch_study_designer`'s `PromptKind`), `observation` and `switched_on` (a new `SwitchedOn {target, line, step}`), each `#[serde(default)]` and skipped when absent or empty, so a host study's prompt reads and writes the bytes it did; `PromptAnswerRequest` gains `value`, skipped when `None`. `observation` is a `serde_json::Value`: Core's shape is the designer's (`{name, answers?, number?}`) and a surface only reads it. `value` is a string (a declared choice) or a number, `confirmed` only ([core 138](../../embarch-core/decisions/host-prompt.md)).

**On the event it is `prompt_kind`** ([core 151](../../embarch-core/decisions/host-prompt.md); the stream's tag is `kind`): `StudyEvent::PromptPending` carries it, optional, and `as_pending_prompt` and `prompt_pending` pass it both ways (`suite/065`). A Core older than 151 writes two `kind` keys, still refused as a duplicate field.

**Source-breaking for struct literals:** `value: None` in a `PromptAnswerRequest` (three here), `prompt_kind: None` in a `PromptPending` (`embarch-ui`'s test helper `prompt_event`, fixed in the same pass).

**Measured:** `tests/prompt_types.rs`: a host prompt and answer byte for byte, a Test run's prompt and event round trips with a kind, a host study's event with none. **Not run:** against a live Core's Test run.

### 139 — The client's `StatusResponse` carries Core's `mode` and `keyid`

`StatusResponse` gains `mode` (`"service"` or `"development"`) and `keyid` (the sealing key's fingerprint), each `Option<String>` with `#[serde(default)]`: Core already sends both ([core 129](../../embarch-core/decisions/)), and the client dropped them, so a surface could only infer the mode from the attestation's match result and read a development Core whose key was recorded as the installed one as `service`. `None` is a Core that predates them: unknown, never `service`. **Source-breaking for struct literals:** none exists in `embarch-api`, `embarch-ui` or `embarch-umbrella` (checked 2026-11-26). The UI switching its identity line to the reported mode is ui's follow-up.

**Measured:** a unit test parses a body with both and one with neither. **Not run:** against a live Core.

### 150 — `/status` exposes one `host_type_schema_version`, read from either key
The suite settled on `host_type_schema_version` as the one name; Core served it as `study_designer_schema_version` and `embarch-core` adds the new key **beside** the old. `StatusResponse` now has the one field `host_type_schema_version: Option<u32>` (rule 58 unchanged), filled from the new key and, failing that, the old, so the same value reads from a Core before and after. It deserializes through a private `StatusWire` carrying both keys as two `#[serde(default)]` fields: `#[serde(alias)]` on one field fails a body with both keys as a duplicate field, which is exactly what the new Core serves. If the two ever disagree the new key wins. `Serialize` emits only the new key. **Source-breaking for field reads and struct literals:** none exists in `embarch-api`, `embarch-ui` or `embarch-umbrella` at `origin/main` (checked 2026-11-27; `embarch doctor` parses `/status` itself). **Measured:** a unit test parses old-only, new-only, both, neither and a disagreeing body. **Not run:** against a live Core.
