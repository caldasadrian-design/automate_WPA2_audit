The provided code snippets are unit tests for a cryptographic engine used in wireless network security tools, specifically for WPA-PSK authentication. These tests are written using the CMocka framework and cover both the calculation of the Pairwise Master Key (PMK) and the execution of the cryptographic engine for a specific type of challenge-response protocol (EAPOL).

### Key Components and Concepts:

1. **Cryptographic Engine Initialization**:
   - The cryptographic engine is initialized with the ESSID (Service Set Identifier) using `ac_crypto_engine_set_essid`.
   - The engine is configured to handle multiple threads for parallel computation using `ac_crypto_engine_thread_init`.

2. **Calculation of PMK**:
   - The `test_calc_one_pmk` function demonstrates how to calculate the PMK using a pre-defined key and ESSID. The PMK is then compared against an expected value.
   - The `test_calc_pmk` function sets up the engine, defines a key, and calculates the PMK. The result is verified against the expected PMK.

3. **Thread Management**:
   - The cryptographic engine supports multi-threading to improve performance, especially on systems with multiple CPU cores. Functions like `ac_crypto_engine_thread_init` and `ac_crypto_engine_thread_destroy` manage the threads.

4. **SIMD (Single Instruction, Multiple Data) Optimization**:
   - The tests support different SIMD instruction sets (e.g., AVX, AVX2, SSE2, NEON) to optimize performance on different hardware platforms.
   - The `group_setup` function determines the supported SIMD features and passes this information to the unit tests.

5. **Memory Management**:
   - Memory allocation and deallocation are handled carefully to ensure that the cryptographic operations are performed on properly initialized memory buffers.

### Detailed Code Analysis:

#### test-crypto-engine.c
- **Initialization and Setup**:
  ```c
  void perform_unit_testing(void ** state)
  {
      ac_crypto_engine_t engine;
      uint8_t bssid[6] = "\x00\x14\x6c\x7e\x40\x80";
      uint8_t essid[33] = "Harkonen";
      int nparallel = dso_ac_crypto_engine_simd_width();
  ```
  - The cryptographic engine is initialized and configured with the ESSID and BSSID.

- **Key Cracking**:
  ```c
  for (int i = 0; i < nparallel; ++i)
  {
      int rc;

      memset(key, 0, sizeof(key));

      strcpy((char *) (key[i].v), "12345678");
      key[i].length = 8;

      if ((rc = dso_ac_crypto_engine_wpa_crack(&engine,
                                               key,
                                               eapol,
                                               eapol_size,
                                               mic,
                                               2,
                                               expected_mic,
                                               nparallel,
                                               1))
          >= 0)
      {
          // does the returned SIMD lane equal where we placed the key?
          assert_int_equal(rc, i);
      }
      else
      {
          fail();
      }
  }
  ```
  - The engine is used to crack WPA keys using parallel threads. Each thread attempts a different key and checks if the calculated MIC (Message Integrity Code) matches the expected value.

#### test-calc-one-pmk.c
- **PMK Calculation**:
  ```c
  static void test_calc_one_pmk(void ** state)
  {
      uint8_t essid[] = "linksys";
      uint8_t key[] = "password";
      uint8_t pmk[PMK_LEN] = {0};
      uint8_t expected[PMK_LEN]
          = {0xec, 0xc9, 0x99, 0x1e, 0x3c, 0xfb, 0x1b, 0x11, 0x7b, 0xdb,
             0xbd, 0x0,  0xde, 0xb4, 0x7,  0xf0, 0x23, 0x29, 0x44, 0xb5,
             0x68, 0x21, 0x64, 0x7e, 0x23, 0x49, 0x13, 0x9d, 0x2,  0xfd,
             0x2b, 0xfb};

      ac_crypto_engine_calc_one_pmk(key, essid, strlen((char *) essid), pmk);

      assert_memory_equal(pmk, expected, sizeof(expected));
  }
  ```
  - The `ac_crypto_engine_calc_one_pmk` function is tested to ensure it correctly calculates the PMK for a given key and ESSID.

- **PMK Calculation with Engine**:
  ```c
  static void test_calc_pmk(void ** state)
  {
      uint8_t essid[33] = "linksys";
      wpapsk_password key[MAX_KEYS_PER_CRYPT_SUPPORTED];
      ac_crypto_engine_t engine;

      ac_crypto_engine_init(&engine);
      ac_crypto_engine_set_essid(&engine, &essid[0]);
      ac_crypto_engine_thread_init(&engine, 1);

      strcpy((char *) (key[0].v), "password");
      key[0].length = 8;

      ac_crypto_engine_calc_pmk(&engine, key, 1, 1);

      uint8_t expected[PMK_LEN]
          = {0xec, 0xc9, 0x99, 0x1e, 0x3c, 0xfb, 0x1b, 0x11, 0x7b, 0xdb,
             0xbd, 0x0,  0xde, 0xb4, 0x7,  0xf0, 0x23, 0x29, 0x44, 0xb5,
             0x68, 0x21, 0x64, 0x7e, 0x23, 0x49, 0x13, 0x9d, 0x2,  0xfd,
             0x2b, 0xfb};

      assert_memory_equal((unsigned char *) (engine.thread_data[1]->pmk),
                           expected,
                           sizeof(expected));
  }
  ```
  - The PMK is calculated using the cryptographic engine, and the result is verified against the expected PMK.

### Usage and Execution:

These tests are executed using the CMocka framework. They can be run by compiling the code and executing the resulting binary. The tests are designed to ensure that the cryptographic engine is functioning correctly and that parallel processing is utilized effectively on different hardware platforms.

### Conclusion:

The provided unit tests are crucial for validating the functionality of a cryptographic engine used in WPA-PSK authentication. They ensure that the engine correctly calculates the PMK and handles key cracking efficiently. The tests are designed to be portable across different hardware platforms, utilizing SIMD instructions where available to improve performance.