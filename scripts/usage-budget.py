#!/usr/bin/env python3
"""Answer "may the supervisor dispatch more workers right now?" from the real
Claude.ai rate-limit numbers.

Why this file exists: the supervisor's whole point is to keep the seat busy
(embarch-parallel-agents.md §1), and the only way to do that safely is to know
how close to the ceiling it already is. Claude Code publishes exactly that --
``rate_limits.five_hour.used_percentage`` and ``rate_limits.seven_day.*`` -- but
ONLY on the JSON it hands a status line command. Nothing else, local or remote,
exposes it: quota state arrives over the wire, so a tool that reads only files
can say what was consumed and never what is left.

So ``~/.claude/statusline-usage.py`` runs as the status line, caches those
numbers to ``~/.claude/usage-cache.json``, and this script reads that cache.

Two thresholds, deliberately different, both overridable:

* ``--seven-day-max`` (default 70) -- the weekly cap is the actual budget. This
  is the number the owner asked for.
* ``--five-hour-max`` (default 85) -- the 5-hour window is not a budget, it is a
  lockout. Burning it to 100% stops the OWNER working, not just the fleet, so it
  gets a higher ceiling but is still a stop: the window refills on its own in
  hours, and a batch that waits loses nothing.

Exit status is the whole interface:
  0  PROCEED -- headroom on both windows; ``--suggest`` prints a wave size
  1  HOLD    -- a threshold is reached; stop dispatching, finish landing
  2  UNKNOWN -- no cache, stale cache, or no rate_limits (not a Pro/Max seat,
                or no API response yet this session). Treated as HOLD by the
                supervisor: never dispatch a wide wave on numbers you don't have.

Usage:
  scripts/usage-budget.py                       check, human-readable
  scripts/usage-budget.py --suggest             also print a worker count
  scripts/usage-budget.py --json                machine-readable
  scripts/usage-budget.py --seven-day-max 55    tighter weekly budget
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

CACHE = os.path.expanduser("~/.claude/usage-cache.json")
MAX_WORKERS = 6  # embarch-parallel-agents.md §13's cap.


def read_cache(path: str, max_age: int):
    """(payload, None) or (None, reason-it-is-unusable)."""
    if not os.path.exists(path):
        return None, (f"no cache at {path} -- is statusline-usage.py wired up "
                      "as statusLine in ~/.claude/settings.json?")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        return None, f"cache unreadable: {e}"

    age = int(time.time()) - int(data.get("cached_at", 0))
    if age > max_age:
        return None, (f"cache is {age}s old (limit {max_age}s) -- the status "
                      "line has not run recently; set statusLine.refreshInterval")
    if not isinstance(data.get("rate_limits"), dict):
        return None, "cache has no rate_limits (not a Pro/Max seat, or no API response yet)"
    data["_age"] = age
    return data, None


def window(limits: dict, key: str):
    """(used_percentage, resets_at) for a window, or (None, None). A window is
    dropped by Claude Code once its resets_at passes, so absence is normal and
    means 'this window is not currently constraining'."""
    node = limits.get(key)
    if not isinstance(node, dict):
        return None, None
    used = node.get("used_percentage")
    if not isinstance(used, (int, float)):
        return None, None
    return float(used), node.get("resets_at")


def human_reset(ts) -> str:
    if not isinstance(ts, (int, float)):
        return "unknown"
    delta = int(ts) - int(time.time())
    if delta <= 0:
        return "now"
    h, m = divmod(delta // 60, 60)
    return f"{h}h{m:02d}m" if h else f"{m}m"


def suggest(five: float | None, seven: float | None,
            five_max: float, seven_max: float, taper: float) -> int:
    """A wave size from the tighter of the two headrooms.

    Full width until the tighter window is inside its taper band, then linear
    down to one worker. Running at full width is the POINT -- the fleet exists
    because the seat is under-used (§1), so a curve that tapers from zero would
    defeat it. The taper only exists so the last workers of a batch don't slam
    into the threshold six-in-flight.

    Still a heuristic over a number nobody has calibrated. The digest records
    actual per-batch burn (§11); once a few batches exist, replace this with
    cost-per-worker arithmetic against the measured headroom.
    """
    fracs = []
    for used, cap in ((five, five_max), (seven, seven_max)):
        if used is None or cap <= 0:
            continue
        band = taper * cap                      # width of the slow-down zone
        headroom = max(0.0, cap - used)
        fracs.append(1.0 if band <= 0 else min(1.0, headroom / band))
    if not fracs:
        return 0
    return max(1, min(MAX_WORKERS, round(MAX_WORKERS * min(fracs))))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--five-hour-max", type=float, default=85.0,
                    help="stop dispatching at this %% of the 5-hour window (default 85)")
    ap.add_argument("--seven-day-max", type=float, default=70.0,
                    help="stop dispatching at this %% of the weekly window (default 70)")
    ap.add_argument("--max-age", type=int, default=300,
                    help="reject a cache older than this many seconds (default 300)")
    ap.add_argument("--cache", default=CACHE)
    ap.add_argument("--taper", type=float, default=0.25,
                    help="fraction of a cap within which the wave narrows "
                         "toward 1 worker; below it, run full width (default 0.25)")
    ap.add_argument("--suggest", action="store_true", help="print a suggested wave size")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    data, why = read_cache(args.cache, args.max_age)
    if why:
        if args.as_json:
            print(json.dumps({"verdict": "UNKNOWN", "reason": why, "workers": 0}))
        else:
            print(f"UNKNOWN -- {why}")
            print("Treat as HOLD: do not dispatch a wave on numbers you do not have.")
        return 2

    limits = data["rate_limits"]
    five, five_reset = window(limits, "five_hour")
    seven, seven_reset = window(limits, "seven_day")

    blocking = []
    if five is not None and five >= args.five_hour_max:
        blocking.append(f"5-hour at {five:.1f}% (max {args.five_hour_max:g}%), "
                        f"resets in {human_reset(five_reset)}")
    if seven is not None and seven >= args.seven_day_max:
        blocking.append(f"weekly at {seven:.1f}% (max {args.seven_day_max:g}%), "
                        f"resets in {human_reset(seven_reset)}")

    workers = 0 if blocking else suggest(five, seven, args.five_hour_max,
                                         args.seven_day_max, args.taper)
    verdict = "HOLD" if blocking else "PROCEED"

    if args.as_json:
        print(json.dumps({
            "verdict": verdict,
            "workers": workers,
            "five_hour": five, "five_hour_resets_at": five_reset,
            "seven_day": seven, "seven_day_resets_at": seven_reset,
            "blocking": blocking,
            "cache_age_s": data["_age"],
        }))
        return 1 if blocking else 0

    def fmt(label, used, reset, cap):
        if used is None:
            return f"  {label}: not reported (window inactive)"
        bar = "#" * int(used / 5) + "." * (20 - int(used / 5))
        return f"  {label}: {used:5.1f}% [{bar}] cap {cap:g}%, resets in {human_reset(reset)}"

    print(f"{verdict}  (cache {data['_age']}s old)")
    print(fmt("5-hour", five, five_reset, args.five_hour_max))
    print(fmt("weekly", seven, seven_reset, args.seven_day_max))
    for b in blocking:
        print(f"  BLOCKING: {b}")
    if args.suggest and not blocking:
        print(f"  suggested wave: {workers} worker(s)")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main())
