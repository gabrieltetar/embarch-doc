`cargo test` no longer aborts: the crate sets a 64 MiB harness stack for the allocator-free shape it tests (decision 63).
