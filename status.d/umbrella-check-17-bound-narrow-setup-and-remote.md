**Target:** suite/user-guide.md — the "Core bound where you cannot reach it" row of the `doctor` troubleshooting table
**Was:** "`bound-narrow`'s `setup` advice above stays correct, because nothing is running on that path"
**Now:** `bound-narrow`'s `setup` half is correct only where a re-run of `setup` from *here* would infer a class needing the wide bind. Run natively on the Windows side of a `wsl-host` machine it infers `local`, installs `--bind 127.0.0.1` again and rewrites the recorded class, after which check 17 passes `bind-matches` with the bind untouched — so the check now withdraws the offer there and prints the reinstall alone. The fix line says which it is; follow it rather than the guide's summary.

Also new in that row: a sixth code, `bind-elsewhere`. On a machine set up as `remote` the Core whose bind matters is another computer's, and the registration readable here is this host's own service, so neither Fail arm may fire off it — it Warns and points at running `embarch doctor` on the machine that runs Core. A `remote` Core reached at its declared host still passes `bind-matches`.

Why: [embarch-umbrella decision 22](../embarch-umbrella/decisions/bind.md), whose two 2026-09-06 amendments are the reasoning. That entry moved out of `decisions/doctor.md` into `decisions/bind.md` in the same commit, so the guide's link target changes if it links there.
