These are header files for cryptographic operations used in the aircrack-ng suite, which is a popular suite of tools for wireless security testing. Let's break down the key parts of each file:

### FILE: aircrack-ng/crypto-engine.h

This file defines the interface for a cryptographic engine used for various wireless security operations, particularly for WPA/WPA2 cracking. Here are the key components:

1. **Initialization and Destruction Functions:**
   - `ac_crypto_engine_thread_init`: Initializes the cryptographic engine for a specific thread.
   - `ac_crypto_engine_thread_destroy`: Cleans up the cryptographic engine for a specific thread.

2. **SIMD Width Query:**
   - `ac_crypto_engine_simd_width`: Returns the width of the SIMD (Single Instruction, Multiple Data) instructions supported by the engine.

3. **Cryptographic Operations:**
   - `ac_crypto_engine_calc_pmk`: Calculates the Pairwise Master Key (PMK) for a given password.
   - `ac_crypto_engine_calc_ptk`: Calculates the Pairwise Transient Key (PTK) for a given vector index.
   - `ac_crypto_engine_calc_mic`: Calculates the Message Integrity Code (MIC) for a given EAPOL frame.
   - `ac_crypto_engine_wpa_crack`: Attempts to crack the WPA key using a given EAPOL frame and MIC.
   - `ac_crypto_engine_wpa_pmkid_crack`: Attempts to crack the WPA key using a given PMKID.

4. **Utility Functions:**
   - `ac_crypto_engine_calc_one_pmk`: Calculates a single PMK for a given password and ESSID.

### FILE: johnswap.h

This file provides functions for byte swapping, which is essential for cryptographic operations on different architectures. Here are the key components:

1. **Conditional Compilation:**
   - The file uses conditional compilation to detect the target architecture and include the appropriate functions for byte swapping.

2. **Byte Swapping Functions:**
   - `JOHNSWAP` and `JOHNSWAP64`: Macros that perform 32-bit and 64-bit byte swapping, respectively. These macros use built-in compiler intrinsics (`__builtin_bswap32`, `__builtin_bswap64`) if available, or fall back to platform-specific functions if not.

3. **Fallback Functions:**
   - `john_bswap_32` and `john_bswap_64`: Inline functions that provide byte swapping for architectures where compiler intrinsics are not available. These functions use bitwise operations to perform the swap.

4. **Rotation Functions:**
   - `ROTATE_LEFT` and `ROTATE_LEFT64`: Macros that perform left rotations on 32-bit and 64-bit integers, respectively. These are used in the byte swapping functions.

These header files provide a robust framework for cryptographic operations in a multi-threaded, SIMD-optimized environment, suitable for wireless security testing tools like aircrack-ng.