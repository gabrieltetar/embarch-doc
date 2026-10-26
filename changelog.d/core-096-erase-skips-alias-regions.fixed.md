`POST /flash` with `erase: true` skips alias and non-writable NVM (STM32 option bytes), checks all ranges first, and answers `erased` ranges. [decision 84](../embarch-core/decisions/flashing.md)
