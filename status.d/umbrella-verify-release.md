**Target:** embarch-release-signing-proposal.md — "Order" step 3, and the `embarch verify-release` bullets under "The design in one screen" and the `embarch-umbrella` row of "The work"
**Was:** "`embarch verify-release`: about a day. Its spike passed on 2026-11-16"; the verb described as proposed
**Now:** Step 3 is built (EMB-192, `tasks/umbrella/097`): the verb, its identity policy and its offline trust root live in `embarch-umbrella`'s docs (`spec.md`, `interfaces/verify-release.md`). Fold the step out of the proposal. The aarch64 `aws-lc-sys` check is `build-check.yml`'s.
