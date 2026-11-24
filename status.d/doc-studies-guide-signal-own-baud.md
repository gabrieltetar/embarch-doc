**Target:** suite/studies-guide.md §3 — the paragraph beginning "A third, rarer one"
**Was:** "A third, rarer one: **`EMBARCH_SIGNAL_BAUD`** sets the line rate when Core reads a DUT signal on its own serial port rather than through the bench. ..."
**Now:** the line rate of a DUT signal is set on the signal: declare it with its `baud` (Topology tab, `embarch-api declare-signal --baud`, or the `declare_signal` MCP tool's `baud`). Core opens the signal at its own `baud` when it declares one; `EMBARCH_SIGNAL_BAUD` is only the fallback for a signal that declares none (default 1000000), and as a service variable it needs the registry `Environment` edit and a restart. Keep the existing warning: the rate has to match what the DUT transmits, nothing checks it, and a mismatch fails every frame's CRC and looks like a firmware bug. Do not assert any DUT's rate; which rate a board needs is the owner's call. Drop the "its real value on this bench is 460800" claim and the "keeps two numbers in step by hand" sentence, or move them to the bench's own notes as the owner decides.

Replacement text, §3:

> A third, rarer one is the line rate of a DUT signal that Core reads on its own serial port rather than through the bench. **Set it on the signal, not in the environment:** declare the signal with its `baud` (`embarch-api declare-signal ... --baud <rate>`, or the `baud` field of the `declare_signal` MCP tool), and Core opens that signal at that rate. **`EMBARCH_SIGNAL_BAUD`** is only the fallback for a signal that declares no `baud`; its default is 1000000. **Whichever sets it, the rate has to match what the DUT actually transmits, and nothing can check that for you: if they disagree, every frame fails its CRC and the capture looks exactly like a firmware bug.**

Followed by the existing "On an installed Core these are not shell variables" paragraph, which still applies to the fallback.

---

**Target:** suite/studies-guide.md §4 step 1 — "Tell EmbArch where the wire goes."
**Was:** "give it a name (that is what a study taps it by) and pick a route."
**Now:** give it a name (that is what a study taps it by), pick a route, and, if the DUT's line is not at Core's 1000000 default, give its `baud`. A direct signal needs it to match the DUT's configured speed; a USB CDC ACM port ignores it. From a terminal: `declare-signal ... --baud <rate>`.
