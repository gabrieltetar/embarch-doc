# 092 — `dispatch` stamps "(request timeout Ns)" on failures that were never timeouts

**State:** open
**Source:** `embarch-reviewer`, reviewing landed unit `api/088` (code
`be04f9e8a6410bf9aedd36fad3a7a541566c4540`, doc `6ef2131809969c4606e4816ab2a3c01f6d5b0a05`).
Finding accepted by the leg of 2026-09-13 19:4x and filed rather than fixed in the fold — see
"Why this is a task and not a one-line repair" below.
**Scope:** api
**Hardware:** none — error-message wording and a decision amendment. No board, no live Core.
**Owner:** no

## What

`CoreClient::dispatch` (`crates/embarch-core-client/src/client.rs`, ~1084–1098) now wraps **every**
`send()` failure that had a configured timeout with:

```rust
format!("request to embarch-core failed (request timeout {}s)", timeout.as_secs())
```

— unconditionally, whenever `timeout: Option<Duration>` is `Some`, which is nearly every route
through decision 55's funnel. `reqwest::Error` exposes `.is_timeout()`; `dispatch` never calls it.
**A connection-refused, a DNS failure, a TLS error and an actual timeout all now read the same.**

And this is not confined to human-readable output: `src/cli.rs`'s `error_result`/`finish` puts the
whole `anyhow` chain (`format!("{e:#}")`) into the `--json` object's `"error"` field, so the
parenthetical lands in the one machine-readable surface a scripted caller reads on every failure.

## Why it matters — decisions 16 and 50

Decision 50 (`decisions/surface.md`) refused to build *any* failure-kind signal into this crate's
error surface, **even one derived from an HTTP status code Core actually sent**, because a coarse
derived signal invites a scripted caller to treat it as real classification — *"the cheap substitute
is a trap, and this is the entry that says so."* Decision 16 says a caller branches on `success`
plus the exit code, and the finer signal waits on Core.

`api/088` put that shape of signal back, and in a form **coarser than the one decision 50
rejected**: it is not derived from an observed fact at all, but from "a timeout duration happened to
be configured for this call." That is the inverse of the rule decisions 71 and 73 apply to `kind` —
never derive a client-side classification you have not confirmed; read the field or say `unknown`.
Here a confident-sounding classification is stamped on failures nobody checked.

**Nothing matches this string today.** The reviewer grepped `embarch-api`, `embarch-ui` and
`embarch-umbrella` and found no caller keying on `"request to embarch-core failed"`, so the hazard
is latent rather than live. That is why this is a task and not a revert.

## Why this is a task and not a one-line repair

The code fix is one conditional. **The doc half is not**, and that is the whole reason this was not
done in `api/088`'s fold: **decision 74's own closing sentence says the timeout is named "on every
failure."** So correcting the code makes decision 74's text false, and the amendment has to land
with it — into `decisions/tests.md`, which decision 74 itself pushed to **12,201/12,288 B, 87 bytes
left**. There is no room for the amendment, so this unit is gated on headroom.

**Do `tasks/api/090-compact-api.md` first, or in the same unit.** `090` is `open`, `In flux: no`,
and proposes the natural split of `tests.md` (smoke-harness tier vs. mocked unit-test
infrastructure). Whoever takes this task should expect to pay `090` as part of it. Do **not** file
the amendment into a roomier decisions file to dodge that — `embarch-api` did exactly that once
before (2026-09-05, `zephyr.md`, 96 B left) and it is the failure `DOC-COMPACTION.md` §2 names.

## What to do

1. Gate the parenthetical on `reqwest::Error::is_timeout()`. A real timeout keeps the bound and the
   number — that is the genuinely useful half of `api/088`, and it should survive. Anything else
   says what it actually was, or says nothing extra.
2. Amend decision 74 with a dated note: the "on every failure" clause was wrong, why (decisions
   16/50), and what it says now. **Amend, do not rewrite** — `api/068` is the protection for that.
3. Decide, and say so explicitly, whether naming a real bound on a real timeout reopens decision 50
   at all. The honest reading is that it does not — a measured duration is not a *kind* — but that
   argument has to be made rather than assumed, because `api/088` made the change without
   mentioning 16 or 50 anywhere.

## Done when

- [ ] `dispatch` names the timeout only when the failure was one.
- [ ] Decision 74 carries a dated amendment saying so, in `decisions/tests.md`, with the headroom to
      hold it — which means `tasks/api/090` is paid first or alongside.
- [ ] The decision-50 question above is answered in writing, either way.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment.

## Reserve, for planning

`embarch-api/decisions/tests.md` is **12,201/12,288 B — 87 B left, 99.3%**, the highest pressure in
the suite, filed against `tasks/api/090` (`open`). `embarch-api/spec.md` is 9,102/10,240 B (88.9%),
filed against blocked `tasks/api/083`. Read the note above: this unit's doc half cannot land without
paying the first of those.
