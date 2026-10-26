The `alloc`-only test cell compiles again: host_study's tests import `alloc::vec`, so CI's `cargo test --features alloc` step is green.
