pd-bench's carried USB PD R3.2 patch makes `usbc_pd.h` include `<zephyr/toolchain.h>`, so a file that includes it first compiles; `pd_logic.h` drops its workaround include (EMB-147).
