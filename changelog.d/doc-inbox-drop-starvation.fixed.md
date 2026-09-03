An `inbox/` drop no longer starves itself: the leg drains `inbox/` every leg and counts with `--tasks-only`, so a drop cannot suppress the refill that files it.
