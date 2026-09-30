# embarch-api: bootload tools

**Status:** active, 2026-09-30. Uploading a signed image through the DUT's own MCUboot serial-recovery bootloader, and declaring the two USB ports that takes — see [tools.md](tools.md) for the one-table premise and `P`.

| Tool / subcommand | Params | Behaviour |
|---|---|---|
| `bootload` | `project`, `P`, `image_path?` | Core `POST /bootload` with the resolved target's signed image, found sysbuild-aware ([decisions](../decisions/bootload.md) 81), or `image_path`. Does not build and resolves no chip. Sends the project's `[projects.bootload]` facts ([config.md](config.md)). Returns `bytes`, `requests`, `duration_ms`, `upload_ms`, `entered_via`, `bootloader_port`, `app_reappeared`, and a `warning` when that is `false` |
| `build_and_bootload` | `project`, `P` | Runs `build`, then bootloads only if it succeeded **and** wrote a signed image newer than its own start. Returns both sub-results. Refuses `image_path` |
| `declare_bootload_ports` | `bootloader`, `bootloader_interface?`, `app?`, `app_interface?` | Core `PUT /bootload/ports`. Each identity is `VID:PID[:SERIAL]` in hex; the interface narrows it. A pair one port could match both of is refused by Core. Replaces any earlier declaration |
| `show_bootload_ports` | — | Core `GET /bootload/ports`; `declared: null` when none |
| `clear_bootload_ports` | — | Core `DELETE /bootload/ports`; `removed: false`, not an error, when none |

**Nothing here has met a real bootloader** — see [../open.md](../open.md).
