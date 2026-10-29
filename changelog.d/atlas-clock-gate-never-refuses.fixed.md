atlas reg_read: the clock-gate word no longer tips a read past its limits into refusal (reads without it, says clock unknown); only RCC *ENR registers (not SMENR/LPENR) can name the gate.
