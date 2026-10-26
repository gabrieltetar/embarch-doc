# embarch-ui: verification technique

**Status:** active, 2026-10-26.

Split verbatim from [../spec.md](../spec.md) (`tasks/ui/078`); nothing below is reworded.

**"Tested in Rust, never looked at" is how this UI's worst defects hid**, so `tests/browser/` is the one to reach for: a headless-Firefox harness driving the **running binary** through geckodriver against a stub embarch-core. The assets are `include_str!`-embedded, so the deployed artifact is the only thing that can be checked, and a state a bench will not produce on demand is testable. `drive.py` covers Live Study, `drive_build.py` the Build card and builds source, `drive_topology.py` the diagram, `drive_fonts.py` every page; `tests/browser/README.md` has the shape. **`tests/element_ids.rs`** (24) is the static half, catching the one shape a text scan can: no id declared twice, no id lookup dangling.
