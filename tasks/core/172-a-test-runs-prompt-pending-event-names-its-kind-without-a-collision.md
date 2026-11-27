# 172 — A Test run's PromptPending event names its prompt's kind without a collision

**State:** open
**Source:** EMB-577 — the PromptPending event's flattened prompt kind collides with the event tag
**Issue:** EMB-577
**Scope:** core
**Hardware:** none
**Owner:** no

## What

`StudyEvent` is `#[serde(tag = "kind")]`, and `PromptPending` flattens
`host_study::PendingPrompt`, which carries its own `kind` in a Test run (core
decision 138). The serialized event therefore has `"kind":"PromptPending"` and
`"kind":"observation"` on one JSON object. `serde_json::to_value` keeps only the
last, so the tag is lost; `embarch-core-client` refuses the event as a duplicate
field, so its event carries no prompt kind and the client reads the kind from
`GET /study/{id}`'s `pending_prompt` instead (api decision 137). When this is
done:

- **A Test run's `PromptPending` event names its prompt's kind under a key other
  than `kind`.** Choose the key and record it.
- **The event's own tag is `PromptPending`** on every reader: typed, `Value`, and
  a JSON parser that keeps the last duplicate key.
- **`GET /study/{id}`'s `pending_prompt` keeps `kind`**: the client reads it there
  today (api decision 137). Do not change that shape.
- **A host study's prompt event is unchanged**, byte for byte, if it carries no
  prompt kind today. Check this, and say what you found.
- **An event test pins the shape**: for a Test run's prompt, the tag, the new key,
  and no second `kind`.

Before you change the event, list every reader of a `PromptPending` event that you
can find in the suite, typed or raw, and say in the decision what each one sees
after the change. Core is the only repo you write. If the client should read the
new key, the client change is api's, a follow-up: file it with
`scripts/fleet-linear.py file --from worker --project embarch-api`.

## Where to look

- `src/study.rs`: `StudyEvent::PromptPending`, and its uses
- `src/host_study.rs`: `PendingPrompt`, its `kind`
- `embarch-doc/embarch-core/decisions/host-prompt.md` (138)
- `embarch-doc/embarch-core/interfaces/`: the study event stream and
  `test-runs.md`
- `embarch-api/crates/embarch-core-client/src/`: `StudyEvent`, read only

## Where the doc goes

A new core decision beside 138, or 138 amended if it stays under its size limit
(`scripts/check-doc-size.py --pressure`). The interface doc that lists the event
says which key carries the prompt's kind. **`embarch-core/open.md` is in reserve**
(893 B left; its compaction `tasks/core/171` is blocked, In flux: yes): do not
write it. If you must, carry `core/171`'s compaction in the same commit and keep
its `Must not delete:` items.

## Done when

- [ ] A Test run's `PromptPending` event carries the prompt's kind under the new
      key, with one `kind`, the tag; an event test pins it.
- [ ] A host study's prompt event is unchanged, or the decision says how it
      changed and why.
- [ ] The interface doc names the key.
- [ ] Gate green (`cargo build`, `test`, `clippy --all-targets -- -D warnings`).
