Atlas build directory is keyed on the build arguments too, so changing a target's extra_args (sysbuild or not) no longer fails in CMake on a stale cache.
