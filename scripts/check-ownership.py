#!/usr/bin/env python3
"""Shim: the implementation lives in the embarch-fleet repo.

Written by `embarch-fleet/scripts/install.py`. Do not edit -- edit the framework
copy and re-run the installer. A shim rather than a copy because there must be
exactly one implementation: two that a checker holds equal is still two.
"""
import os, sys
TARGET = '/home/gabriel/Github/embarch/embarch-fleet/scripts/check-ownership.py'
if not os.path.exists(TARGET):
    sys.exit(f"fleet framework missing: {TARGET}\n"
             "Clone embarch-fleet beside this repo and re-run its scripts/install.py.")
os.execv(sys.executable, [sys.executable, TARGET] + sys.argv[1:])
