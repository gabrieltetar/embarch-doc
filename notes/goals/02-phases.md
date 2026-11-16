# Goals notes: the phases

**Status:** draft, 2026-11-16.

Where EmbArch is now, and the order it grows in. Every answer here is the owner's, 2026-11-16, unless it sits under Open.

## 1. Build: now

**New features, and existing ones improved a lot.** The owner: "right now we are developing new features and enhancing present features a lot". **Hardware-in-the-loop and the atlas above all**: "I still want to improve the HIL process and the Atlas a lot". The two designs in flight: [embarch-hil-proposal.md](../../embarch-hil-proposal.md) with [embarch-hil-evidence-proposal.md](../../embarch-hil-evidence-proposal.md), and [embarch-atlas-planes-proposal.md](../../embarch-atlas-planes-proposal.md).

## 2. Stabilise: the owner's call

**No named bar.** The phase ends when the owner is happy with the toolset: "once it's stabilized and we are happy with the toolset we can work on scaling the features rather than working on the features themselves".

## 3. Scale: still inside the trinity

**Scaling the features, not adding them.** Two goals offered for now were moved here by the owner:

- **A short first hour**: one download, then a first study on a common Zephyr dev kit, with no atlas and no suite to write.
- **Nothing tied to the owner**: no step depends on the owner's machine, setup or client work.

**A remote Core, on a Raspberry Pi first, comes before the trinity is broken** (owner). Today a Pi over the LAN is detected and verified, and the token is carried across machines by hand ([roadmap](../../suite/roadmap.md), "Later").

## 4. Beyond the trinity

**More than one engineer or more than one Core**, only after scaling, and only when the owner decides the suite has reached "a real impressive milestone". No goal of the build phase plans for it.

## Open

- **Whether a remote Core breaks "one machine".** Recommended reading: Core on a Pi beside the bench is the first step past one machine, kept within one engineer and one Core; the trinity's wording in [00-goals.md](00-goals.md) then reads "one machine, or one machine and its bench Pi". Not asked.
- **Whether the scaling-phase goals get a status line now**, like the ten goals in [03-status.md](03-status.md).
- **What a contributor does in the build phase**: whether outside contributions are welcome before the stabilise phase, and to which parts.
