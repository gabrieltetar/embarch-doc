# Atlas notes: the platform plane

**Status:** draft, 2026-11-15.

## What it holds

**Versions, patches and known issues.** The platform is the code the firmware is built on and does not own: Zephyr, the vendor SDK and HAL, the toolchain, and the patches the project applies to them. **It changes on a `west update` or a manifest move, not on a firmware commit**, which is why it is a plane of its own and not part of the firmware's.

- **Version key**: every west project's path and revision, which the stamp already records (`embarch-atlas` repo, `DESIGN.md`, "The stamp"), plus the patch set: `patches.yml` and each patch file's hash.
- **Documents**: upstream release notes and known-issues lists, and the MCU's errata, as specification-plane documents tied to a platform version. The engineer supplies them; the atlas fetches nothing from the internet. The `errata` kind exists already (same doc, "Kinds").
- **Updated by** `update`, which already stops when the west workspace is not at the manifest's revisions (`update.workspace_drift`).

## Checks it enables

- **A backport the new base already carries.** A backport's `patches.yml` entry names its upstream merge commit; when that commit is an ancestor of the module's new revision, the patch is due for deletion. Deterministic.
- **An erratum whose workaround the HAL at this revision lacks.** Vendors name workaround code after the erratum; a search of the HAL's sources at the pinned revision says whether it is there. Deterministic once the naming is known per vendor.
- **A firmware call into an API the new platform version deprecates.** From the build's own warnings.

## Open

- **The erratum-to-workaround match per vendor.** Checked on the first two families the suite uses before it is trusted.
- **The toolchain version's source.** Recommended: the build's `build_info.yml`, which every atlas already copies; not checked that it holds the toolchain version for every SDK.
- **Whether the platform is shared across firmware repos of one product.** Each repo may pin its own; recommended per repo.
