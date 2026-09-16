# embarch-topology decisions: The chip classifier behind the identity gate

**Status:** active, 2026-09-11.

Which register pair (or eFuse) a chip name resolves to for the self-reported-ID comparison, and the one classifier both `read` and `is_nordic_deviceid_chip` share. What the comparison itself asserts, and what it cannot, is [validation.md](validation.md) decision 21 — this file exists because a second question (coverage: which chips this arm even applies to) grew past that one's room.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 25 — `read` and `is_nordic_deviceid_chip` share one chip classifier; unlisted nRF54L/nRF54H and STM32 names are refused, not guessed

Decision 21's arm rests on `read` and `is_nordic_deviceid_chip` agreeing on exactly which chips get the `FICR.INFO.DEVICEID` pair. They were two separate matches instead: `read` listed four exact nRF54L names then fell through to `c.starts_with("nRF5")`, and `is_nordic_deviceid_chip` duplicated the list. `"nRF54"` starts with `"nRF5"`, so any nRF54L/nRF54H spelling **not** one of the four — e.g. `nRF54L47` — matched the classic guard first and never reached the newer pair, in both functions, silently.

**The fix is one function, `classify_chip`, that both call.** It checks lowercased `nrf54l` before the classic `nrf5`/`nrf9` prefix, so the newer family can no longer lose to the broader prefix that contains it. `read` matches on the result to pick a register pair or bail with a named error; `is_nordic_deviceid_chip` reduces to whether it classified as either Nordic family — so the two cannot disagree.

**Why lowercase, when decision 21's four names were exact-case.** `embarch-core`'s `flash_backend.rs` already treats a lowercased `starts_with("nrf54l")` the same way, accepting unlisted parts like `nRF54L47` — this file matches that existing rule rather than proposing a shared dependency.

**nRF54H is checked first and returns `None`.** Decision 21's evidence for `0x00FF_C304`/`0x00FF_C308` is entirely nRF54L — three nRF54L15s over JTAG, one HAL cross-check — nothing establishes the Haltium family's FICR layout. Checking `nrf54h` before the classic `nrf5` prefix is load-bearing: that prefix would otherwise swallow it. An unrecognized chip is a named error, never a guess; when an nRF54H is enrolled, the way in is a register read on real silicon.

**What this does not change:** the register addresses themselves (still decision 21's, unverified past three nRF54L15s and the one confirmed `INFO.DEVICEID` pair), and the fallback-register exposure decision 21 already accepted — a chip whose device ID is truly inaccessible still comes back *mismatch*, not *undeclared*, on either classification.

**`requires_vendor_tool` (`embarch-core`) stays unrelated to this classifier, on purpose** — declined independently by `embarch-core` decision 49. It answers a different question (is probe-rs's flat-NVM erase/write safe) with a different codomain (bool vs. three-way). `None` here is an abstention; `requires_vendor_tool`'s `true` is a positive refusal — reading the second as agreement with the first is how a future change unifies them by mistake.

**One inconsistency left deliberately.** `esp32c5` is matched case-**sensitively**, before the lowercasing — `ESP32C5`/`esp32-c5` reach the named error rather than the Espressif arm. Safe direction, no other spelling has appeared in this suite, but it breaks the narrowest-verified-match rule above, unargued rather than argued.

**`classify_chip` gained an ST arm 2026-09-11:** enrolling a NUCLEO-G0B1RE hit the named error until `Stm32G0Uid` was added for `stm32g0`, read as three words at `UID_BASE` (`0x1FFF_7590`/`4`/`8`). Evidence: `hal_stm32`'s `stm32g0*xx.h` headers and Zephyr's `hwinfo_stm32.c` agree, and a real board enrolled off it.

**`stm32g0`, not `stm32`, is the arm's whole design.** `UID_BASE` moves between STM32 families (F4 `0x1FFF_7A10`, H7 `0x1FF1_E800`), so a vendor-wide prefix would read whatever sits at the G0 address on an unrelated part and return a plausible-looking string. `STM32F407VG`, H7 and L4 are tested to confirm they still miss this arm.

**96 bits needed a third word: `read_two_words` became `read_words` over a slice.** A two-word slice is byte-identical to the old output, so every `hardware_id` in `enrollment.toml` still compares equal — the alternative would have silently invalidated both enrolled Nordic boards. `is_nordic_deviceid_chip` is untouched: STM32 parts get `Undeclared`, already specified as not a match.
