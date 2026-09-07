# 013 — `Cargo.toml` still says `embarch-ui` never depends on `embarch-topology` at all

**State:** open
**Source:** reviewer of `ui/012`, leg 026, 2026-09-06 — found while verifying that unit's own
correction, reproduced against `embarch-ui` at `fa3b7b6`
**Scope:** ui
**Hardware:** none
**Owner:** no

## What

`ui/012` corrected `embarch-ui/spec.md`, which said the UI `does NOT link embarch-topology, at all,
deliberately`. It does link it — transitively, `embarch-topology → embarch-core-client →
embarch-ui`, features `default,software` — and what is actually true is the narrower claim
`decisions/wiring.md` decision 5 makes: **never the `hardware` feature.**

**`embarch-ui/Cargo.toml` lines 23–24 carry the same overstated sentence, and cite decision 5 for
it:**

```
embarch-ui / never depends on embarch-topology or its hardware feature at all
```

Decision 5 says only the hardware-feature half. So the manifest comment attributes to a decision a
claim that decision does not make — the identical defect `ui/012` fixed, one file over.

**`ui/012` could not fix it**: it was a doc-only unit and the comment is in the code repo, so
changing it would have made its "the code is right and unchanged" claim false. That was the correct
call and this is the follow-up.

## Why it is worth a task rather than a shrug

It is a **comment in a manifest**, which is the file a reader opens precisely when they want to know
what this crate links — and it is the one place the wrong version now survives after `spec.md` and
`embarch.md` §5 both state the transitive shape correctly. A reader who trusts it concludes the
dependency does not exist and reasons from that.

## Watch for

- **The measurement, so it need not be re-derived:** `cargo tree -e normal -i embarch-topology -f
  "{p} FEATURES={f}"` gives `embarch-topology FEATURES=default,software → embarch-core-client →
  embarch-ui`; `embarch-topology`'s `default = ["software"]` and `hardware = ["dep:probe-rs",
  "dep:serialport", …]`; and the count of `probe-rs|serialport` in `cargo tree -e normal` is **0**,
  and still 0 with dev-dependencies [measured 2026-09-06, twice — by `ui/012`'s worker and
  independently by its reviewer].
- **The invariant that is actually being protected is the `probe-rs`/`serialport` count, not the
  absence of the crate.** `embarch-ui/spec.md`'s Invariants section already measures it correctly.
  Whatever the comment ends up saying should point at that rather than restate it.
- Check whether any *other* manifest in the suite carries the same sentence before concluding this
  is one line.

## Done when

- [ ] `embarch-ui/Cargo.toml`'s comment states what is true and what decision 5 actually says.
- [ ] Gate green (`../../embarch-fleet/protocol.md` §10).
- [ ] `changelog.d/` fragment if anything user-visible changed — a manifest comment alone may not
      warrant one; say which and why.
