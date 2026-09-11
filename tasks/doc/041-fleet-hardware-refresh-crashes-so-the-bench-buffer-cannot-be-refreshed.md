# 041 — `fleet-hardware.py --refresh` crashes, so the bench buffer has been 79 hours stale and no leg can refresh it

**State:** open
**Source:** leg 081, 2026-09-11 — hit at step 0 while sizing the one `bench` task in the queue
**Scope:** doc
**Hardware:** none to fix. **Confirming the fix needs Core reachable and at least one board
attached**, which was true when this was found (`Core: reachable`, both roles `attached: yes`).
**Owner:** required — `scripts/` is owner-reserved (`check-ownership.py --supervisor`), so no
agent may make this edit.

## What

`embarch-fleet/scripts/fleet-hardware.py --refresh` raises and writes nothing:

```
  File ".../fleet-hardware.py", line 214, in measure
    hwid = (dut or {}).get("measured", {}).get("hardware_id") if dut else None
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'get'
```

The guard is on the wrong level. `(dut or {})` protects against `dut` being absent, and the
trailing `if dut else None` protects against it again — but neither protects against `dut` being a
dict whose `measured` key is **present and null**, or absent with a `None` default reaching
`.get`. `.get("measured", {})` returns the stored `None` rather than the `{}` default whenever the
key exists and holds null, which is what Core answered here.

The plain form still works and prints the buffer; only `--refresh` is broken. So the failure is
**silent in the way that matters**: `fleet-hardware.py` prints a complete, confident topology and
one trailing line saying `buffer is 4767 min old -- STALE, run --refresh`, and running `--refresh`
does nothing but traceback. A leg that does not read the traceback carefully has a plausible
hardware view that is **79 hours old**, containing `attached: yes` for two boards that may have
been unplugged three days ago.

## Why it is the owner's and not the supervisor's

`scripts/` is reserved. A supervisor that can repair the script it is measured by has no
constraint — this is the same reasoning that keeps `protocol.md` and `.claude/` off the fleet's
hands, and it holds even though the fix is one line and obvious.

## Why now

`leg.md` makes the buffer load-bearing for *selecting* bench work: *"selecting bench work costs no
hardware attach at all — which is the point, since `validate` takes Core's `hw_lock`"*. A buffer
that cannot be refreshed inverts that: the cheap planning surface becomes the untrustworthy one,
and the only way to learn the truth is the expensive attach the buffer exists to avoid. Every leg
since the last successful refresh has been planning bench work against a three-day-old reading.

This leg took no bench unit, so nothing was decided on the stale data — but that was for an
unrelated reason (the bench queue is parked by commit `d0cf9a0`), not because the staleness was
caught in time.

## Done when

- [ ] `fleet-hardware.py --refresh` completes against the current bench and rewrites
      `/home/gabriel/Github/embarch/.fleet/hardware.json`.
- [ ] A `measured` key that is absent **or null** is handled at every site that reads one, not only
      this line — grep the file for `.get("measured"` before calling it fixed.
- [ ] Consider whether a `--refresh` that fails should make the **plain** form refuse to print a
      confident topology, or at minimum say "last refresh FAILED at <when>" rather than only
      "STALE". A stale buffer that knows it is stale is safe; one that cannot say why is the shape
      that misleads.
