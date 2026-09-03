# embarch-outpost decisions: Naming what the wire reports

**Status:** active, 2026-09-02.

Turning a thread pointer and a vector number into a name, out of the build's own record — never a guess.

Index: [../decisions.md](../decisions.md). Current truth: [../spec.md](../spec.md).

### 7 — ISR identity: read the active vector number in the hook, emit it raw, resolve it to a handler name from the ELF

Engineer markers stay, **for spans *inside* a handler.**

**Both halves are facts, not inferences, and that is what makes this cheap.** **Reading the number is what Zephyr itself does, at the same instant** — the trace hook is called from inside the ISR wrapper, in exception context, and three lines later the wrapper computes the same expression from the same register. **Not a heuristic that usually works: the identical expression, guaranteed valid at that point, returning the number the wrapper is about to dispatch on.** The register still holds the same exception at the exit hook, **so the number is emitted on exit too, which makes nesting and tail-chaining trivial for a host instead of a stack it has to reconstruct.** And **resolving a number to a name is an ELF read**: the software ISR table is indexed by IRQ line, and the generator walks it at exactly the index the firmware will report. **Nothing is derived, nothing is matched heuristically, and the number on the wire stays raw whether or not a name was found.**

**So the honest split is not "number versus name" — it is "what the kernel dispatches" versus "what happens inside a handler."** The first is free and exact; **the second is what markers are for, and no vector number can substitute for it.** Both, not either.

**What this costs, stated rather than buried.** Reading that register is Cortex-M, so a Kconfig gates it — **on where the arch supports it, off elsewhere, degrading to the anonymous enter/exit records the hooks give regardless.** Four build variants defeat or degrade it and each is named rather than assumed equivalent: a **custom interrupt controller** substitutes a different read in the wrapper and is **explicitly unsupported**, with the symbol depending on its absence **so such a build degrades rather than reporting a plausible wrong number**; **dynamic interrupts** make the table runtime-filled, so ELF entries may still be placeholders and those IRQs render as bare numbers; **multi-level aggregators** put second-level IRQs at a table offset **the generator must honour or mislabel — named here because mislabelling is the one outcome decision 9 exists to prevent**; and **shared interrupts** put a dispatcher in the table position. **The stamp is wrapper-entry, not handler-entry** — a fixed prologue early, consistently, for every ISR.

**The table's handler field does not necessarily name anything useful, and on this target usually does not.** The vendor's glue **registers one shared trampoline per peripheral and passes the driver's real handler as the entry's argument**, so most populated entries resolve to the same useless name. **The fix is one field over and is the same kind of read:** resolve that argument against the symbol table too and take it **when it points at a function.** The manifest carries both.

### 8 — Thread names come from the manifest, by DWARF *type* joined to symbol-table *address*; anything not covered renders as a raw pointer

The switch-in hook takes no arguments, so **the hook reads the current thread pointer — a runtime address, four bytes on the wire, no name.** What turns it into a name is an address-to-name table generated into the manifest **at zero wire cost.**

**A naming convention over symbol prefixes is not enough, and the gap is most of what a quiet trace does.** Matching by name resolved **5 of 20** thread objects on a real image; the fifteen missed include the outpost's own drain thread, the BLE stack's work queues, the system work queue, and four application queues. **Four of them are not a thread struct at all** — a work-queue struct starts with one, **so a work queue's address *is* its thread's address, and that is the pointer the kernel was handed. No naming convention could have found any of them.**

**So the generator reads DWARF. DWARF says what a variable is; the symbol table says where it lives; neither is guessed**, and both are facts the build recorded — **the same standard every other table in the manifest is held to.** Two details are load-bearing rather than incidental:

- **Type from DWARF, address from the symbol table.** Only definition entries carry a location, and **the kernel's own objects appear in this image *only* as declarations: typed, with no address. Insisting on a DWARF location loses exactly the four objects a quiet trace spends most of its time in.** A name is enough to join on, and the join is exact.
- **First-member recursion stops at any non-zero offset**, because **then the outer object's address is not the thread's.**

An array of threads gets one entry per element at the element type's own recorded size, **which is what names the per-CPU idle threads.** The name match survives as **the fallback for an image linked without debug info**, which path ran is recorded in the manifest, and **a thread the type walk somehow missed is added from the name match with the disagreement reported rather than papered over.**

**What is still not covered:** an image with no DWARF resolves only what the name match finds, and **a thread struct embedded at a non-zero offset is not found — finding it would mean claiming an address the kernel was never handed.**

*Rejected: emitting runtime name-registration records.* Would cover every thread **and put strings back on the wire.**

**The equivalent gap on the ISR side closes the same way.** The software ISR table holds only vectors that dispatch through the wrapper; **a directly-connected line leaves its row empty. On this target exactly one line does that, and it is the radio — the single most interesting vector in a BLE trace.** The hardware vector table holds a function address, so **any entry that is not the wrapper is a direct handler, and comparing against the wrapper's own symbol is what makes that exact rather than a guess about which entries are interesting.**
