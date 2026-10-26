# embarch-ui decisions: The browser drive scripts

**Status:** active, 2026-10-26.

How `tests/browser/drive*.py` find geckodriver and the UI. How to run them: `tests/browser/README.md` in the code repo. Index: [../decisions.md](../decisions.md).

### 65 — Every drive script takes its two addresses from `addr.py`, and the old names are refused
Five scripts hardcoded 4444 and 4899 with no override, and others read one of `GECKO`/`UI`, `WEBDRIVER`, `EMBARCH_GECKO_PORT` or a per-script `*_UI_PORT`. On 2026-10-26 a worker passed scratch ports to scripts that read none and one opened a session on the owner's own geckodriver. Now `tests/browser/addr.py` is the only reader: `EMBARCH_GECKO_PORT` (default 4444) and `EMBARCH_UI_PORT` (default 4899, or the script's own where it starts the UI), each a bare port on 127.0.0.1. **Defaults stay the owner's interactive ports**, so his usage is unchanged; chosen over refusing to start without the variables because that would break every `README` recipe for the one person who runs them by hand, and the fleet's rule (never run unset) is already written in the dispatch brief and the README. **The retired names exit with an error instead of being ignored**, since a variable that does nothing is the failure being fixed. `tests/drive_addresses.rs` fails `cargo test` if a `drive*.py` lacks the `addr` calls or contains `127.0.0.1:4444`/`:4899`, and runs the helper with the variables set, unset and legacy, without a browser. Not measured: a drive script end to end against scratch ports (no geckodriver was started for this change).
