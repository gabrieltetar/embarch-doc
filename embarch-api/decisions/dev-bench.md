# embarch-api decisions: The dev-bench pipeline

**Status:** active, 2026-09-02.

Why the bench is not a `[[projects]]` entry, and why its board stopped being a constant.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 32 — A dedicated pipeline outside `[[projects]]`
*Rejected: adding dev-bench as an ordinary Zephyr-discovery project entry*, which would have cost zero new code. Declined on the repo owner's explicit call: `[[projects]]` is for **DUT firmware a firmware engineer or an agent configures per repo**, and mixing in EmbArch's own fixed test rig conflates two different kinds of thing. So a separate config table, and three tools mirroring build/flash/build-and-flash **minus every selection param** — the same "no project param when the concept genuinely isn't project-shaped" precedent already set elsewhere.

The resolution turns that config into the **exact same shape** a real project's resolution produces, so the build and flash machinery is reused verbatim with zero new code paths.

**Two real, previously-undetected gaps found the first time this ran against real hardware, neither specific to dev-bench.** `base_address` had never actually been exposed by this crate's flash tools — a known open item from the moment Core gained it, closed only once a real `bin` build needed it through this path. And **`probe_serial` was designed in Core, never threaded through from this side, and — found the same session — never actually implemented in Core either**, despite that doc claiming otherwise. The first real need for it, since exercising a DUT's probe and the bench's simultaneously was new.

### 45 — "There is exactly one dev-bench board" was a premise, and it has been falsified twice
Decision 32 was right that the bench is not a DUT anyone configures per repo. But it drew a second conclusion from that — *therefore* its board, chip, format and offset are facts the suite already knows, so they belong in Rust as constants rather than config. The bench has since been an nRF54L15DK, then an ESP32-C5 when the DK broke, then an nRF54L15DK again.

**The two boards agree about none of the four, plus a fifth nobody had noticed was a variable at all:**

| | nRF54L15DK | ESP32-C5-DevKitC |
|---|---|---|
| board | `nrf54l15dk/nrf54l15/cpuapp` | `esp32c5_devkitc/esp32c5/hpcore` |
| chip | `nRF54L15` | `esp32c5` |
| format | `hex` | `bin` |
| base address | — (a hex carries its own) | `0x2000` |
| artifact path | `build/app/zephyr/zephyr.hex` | `build/zephyr/zephyr.bin` |

**The artifact path is the one a change that only made "board" configurable would have missed.** It differs because **NCS turns sysbuild on by default and vanilla Zephyr does not**, which puts the image a directory deeper. That is not a property of the board, the chip, or the format — it is a property of which SDK the workspace pulls, and no rule over the other four predicts it. Read off a real build rather than reasoned about.

So all five move to config, and **none is defaulted**. A default would have to pick one of the two boards, and picking wrong means building the wrong image and handing it to Core to flash through the wrong debug interface at the wrong chip — the class of silent-wrong-answer this suite refuses elsewhere on principle. **A missing field is a startup error naming it, which is cheap; a wrong default is not.**

**What stays a constant, legitimately:** the app directory name, which is dev-bench's own repo layout and identical for every vendor family, not a property of any board. And the build lock key stays fixed: *which* board it is now varies, but the bench is still one at a time.
