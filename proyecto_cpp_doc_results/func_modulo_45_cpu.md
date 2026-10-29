# MODULE: cpu

## 1. PURPOSE
The `cpu` module provides functionality to retrieve and manage information about the CPU, including its SIMD support, core details, and frequency.

## 2. CORE COMPONENTS
- `cpuid_simdsize(int)`: Retrieves the number of 32-bit integers that can be packed into a single vector register.
- `cpuid_getinfo(void)`: Populates the `cpuinfo` structure with detailed information about the running machine.
- `ac_cpuset_new(void)`: Allocates a new cpuset module handle.
- `ac_cpuset_free(ac_cpuset_t * cset)`: Deallocates a cpuset module handle.
- `ac_cpuset_init(ac_cpuset_t * cset)`: Initializes the cpuset module handle.
- `ac_cpuset_destroy(ac_cpuset_t * cset)`: Destroys the cpuset module handle.
- `ac_cpuset_distribute(ac_cpuset_t * cset, size_t count)`: Distributes a specified number of threads over all available CPUs.
- `ac_cpuset_bind_thread_at(ac_cpuset_t * cset, pthread_t tid, size_t idx)`: Binds a thread to a CPU at a specified index position.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `cpuid.h`: Calls `cpuid_getinfo()` to populate the `cpuinfo` structure.
- `cpuset.h`: No direct calls, but used for managing CPU sets for thread affinity.

## 4. INCOMING DEPENDENCIES (Used By)
- `trampoline.h`: No direct uses, but could be used by other modules that require CPU information or SIMD support.