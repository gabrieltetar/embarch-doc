**Target:** suite/hil-guide.md, Study, "6. Verify it in a clean folder"
**Was:** the step runs `curl -s -X POST <core>/auth/challenge` with a fixed nonce and reads `public_key` from the JSON
**Now:** the step names `embarch-api core-key`, which checks Core's signature over a fresh nonce before printing the key. Copy `embarch-api`'s `guide/hil-guide.md` over `suite/hil-guide.md` so the two match again (the drift guard `the_pinned_copy_matches_the_suite_guide_where_one_is_reachable` is red until then).
