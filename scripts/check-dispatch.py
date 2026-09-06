#!/usr/bin/env python3
"""Shim: the implementation lives in the embarch-fleet repo.

Written by `embarch-fleet/scripts/install.py`. Do not edit -- edit the framework
copy and re-run the installer. A shim rather than a copy because there must be
exactly one implementation: two that a checker holds equal is still two.

The framework is located at RUN TIME, not baked in. This file is committed to
the instance repo, so a second checkout on another machine would otherwise get a
path that exists only where the installer ran.
"""
import os, sys

NAME = 'check-dispatch.py'
HERE = os.path.dirname(os.path.abspath(__file__))
CANDIDATES = [
    os.path.join(os.environ["EMBARCH_FLEET_ROOT"], "embarch-fleet", "scripts", NAME)
    if os.environ.get("EMBARCH_FLEET_ROOT") else None,
    # the documented layout: the framework cloned beside the instance
    os.path.join(HERE, os.pardir, os.pardir, "embarch-fleet", "scripts", NAME),
    # where the installer ran, as a last resort
    '/home/gabriel/Github/embarch/embarch-fleet/scripts/check-dispatch.py',
]
for c in CANDIDATES:
    if c and os.path.exists(c):
        os.execv(sys.executable, [sys.executable, os.path.abspath(c)] + sys.argv[1:])
sys.exit("fleet framework missing; tried:\n  " +
         "\n  ".join(c for c in CANDIDATES if c) +
         "\nClone embarch-fleet beside this repo and re-run its scripts/install.py.")
