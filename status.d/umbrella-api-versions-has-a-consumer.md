**Target:** suite/features.md — the `embarch-api` `versions` row
**Was:** "`versions` — the compiled study-designer host type schema version, readable with no config and no live Core | Shipped — **nothing reads it yet** | unit | 52"
**Now:** `embarch doctor`'s check 11 reads it, as of 2026-09-04 (`embarch-umbrella` decision 35). The "nothing reads it yet" qualifier is false; the row's Verified column stays `unit` — no `doctor` run against an installed `embarch-api` has happened.

`embarch-api/open.md`'s "Nothing reads `versions` yet" bullet closes with the same fact; that file is another sub-project's and was deliberately not edited here.
