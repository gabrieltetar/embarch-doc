# 001 — A header-less `MEMORY.md` tells the writer it may add the first domain header

**State:** open
**Source:** Linear issue EMB-20, filed by a session
**Issue:** EMB-20
**Scope:** promptu
**Hardware:** none
**Owner:** no

## What

When a write touches a `MEMORY.md` that has no `## <domain>` header yet, check I2's message says the write may add one. Headers are free until the index has one (`embarch-promptu` decision 21), and only after that does I3 refuse a new one; the message should say so instead of telling the writer to put the line under a header that does not exist.

Today, on a write to a header-less `MEMORY.md`, I2 fails each touched index line with ``put this index line under the `## <domain>` header it belongs to``. With no headers there is nothing to put it under, and the `hint` is empty when `domains` is empty. A user rule that forbids adding a header unasked then makes the first memory in any new project break one rule or the other.

## Why now

Every new project's first memory hits it.

## Where to look

- `src/checks.rs` `index` — the I2 message and the `hint` that is empty when `domains` is empty
- `src/checks.rs` test `headers_are_free_until_the_index_has_some` — the rule as built
- `src/hook.rs` — the PreToolUse hook that reports it
- `embarch-doc/embarch-promptu/decisions/memory.md` decisions 4 and 21

To reproduce: write a line to a `MEMORY.md` with no `## ` header, through the Write tool in an auto-memory folder.

## Dispatch notes

- This is a message change, not a rule change: decision 21 stands as written. Amend it only if its text says something this makes false.
- No `embarch-promptu` doc is in reserve at the split.

## Done when

- [ ] I2 on an index with no header tells the writer it may add a first `## <domain>` header in the same write.
- [ ] A test covers the message for a header-less index.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10); `changelog.d/` fragment dropped.
