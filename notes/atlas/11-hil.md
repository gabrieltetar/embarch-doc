# Atlas notes: what the HIL proposal needs, plane by plane

**Status:** draft, 2026-11-15.

[The HIL notes](../hil/04-premade-suites.md#what-the-hil-side-needs-from-the-atlas-rework) list what the Test runner and Live mode need from this rework, and leave the shape to it. Where each lands:

| HIL need | Plane | Today |
|---|---|---|
| A requirement ID stable across revisions of one standard | Specifications | `rid` exists; its stability across revisions does not |
| The join from a suite's test to its requirement record (the suite itself is plain data shipped with EmbArch and runs with no atlas, HIL review round 1) | Specifications | Not built |
| The suite's bench descriptions | None: saved-bench files ([embarch-ui decision 73](../../embarch-ui/decisions/saved-benches.md)), shipped in the suite | Not built |
| Applicability: which tests apply to a role and its capabilities | Specifications | The `applies` lookup is built |
| The capabilities the atlas decodes from a build | Firmware × specifications, and the firmware side of external interfaces | `fw_check` reads the devicetree and Kconfig; no capability list |
| A write-back verb for a Live finding, marked `via: live` and answered as development evidence (HIL review round 1) | Measured | Not built ([08](08-measured.md)) |
| **Added here**: the hardware a measurement or a Test report ran on | Hardware (units) | Not built ([02](02-hardware.md#units)) |

## Open

- **The order.** The HIL proposal puts this rework first and its Live phase third; Live waits on the write-back verb. This rework starts with design × hardware ([the proposal](../../embarch-atlas-planes-proposal.md#order)), so the write-back lands after it. Recommended: the write-back right after design × hardware, before the other planes.
