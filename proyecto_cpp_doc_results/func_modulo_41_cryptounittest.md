The provided code snippets are unit tests for various cryptographic functions in the `aircrack-ng` project. These tests validate the correctness of cryptographic operations such as message digest computation, stream cipher encryption, and related functionalities. Below is a detailed explanation of each file and its functionality:

### FILE: test-crypto-wpa.c
This file contains unit tests for WPA (Wi-Fi Protected Access) cryptographic operations. Specifically, it tests the calculation of MIC (Message Integrity Code) using PMK (Pairwise Master Key), PTK (Pairwise Transient Key), and the ESSID (Extended Service Set Identifier). The tests are performed for both WPAv1 and WPAv2.

- **Structures and Variables:**
  - `struct wpa`: Defines the WPA structure with a `keyver` field indicating the WPA version.
  - `unsigned char pmk[32]`, `unsigned char ptk[80]`, `unsigned char mic[20]`: Arrays to store PMK, PTK, and MIC respectively.
  - `unsigned char essid[33]`: Array to store the ESSID.

- **Functions:**
  - `calc_mic`: A function that calculates the MIC using the provided PMK, PTK, and ESSID. This function is expected to be implemented elsewhere in the codebase.
  - `test`: A helper function to compare expected and actual values and count errors.

- **Test Execution:**
  - The tests initialize the `wpa` structure for WPAv1 and WPAv2, calculate the MIC, and then compare the results with the expected values using the `test` function.

### FILE: test-digest-sha1.c
This file contains unit tests for the SHA-1 (Secure Hash Algorithm 1) message digest computation. SHA-1 is a cryptographic hash function that produces a 160-bit (20-byte) hash value.

- **Test Vectors:**
  - `sha1_test_buf`: Input data for the SHA-1 function.
  - `sha1_test_buflen`: Lengths of the input data.
  - `sha1_test_sum`: Expected SHA-1 hash values for the input data.

- **Functions:**
  - `Digest_SHA1`: A function that computes the SHA-1 hash of the given input data.
  - `test`: A helper function to compare expected and actual values and count errors.

- **Test Execution:**
  - The tests compute the SHA-1 hash for the provided test vectors and compare the results with the expected values using the `test` function.

### FILE: test-cipher-arcfour.c
This file contains unit tests for the ARCFOUR stream cipher. ARCFOUR is a stream cipher that is considered weak and is not recommended for use in new systems due to vulnerabilities.

- **Test Vectors:**
  - `arc4_test_key`: Input keys for the ARCFOUR cipher.
  - `arc4_test_pt`: Input plaintexts for the ARCFOUR cipher.
  - `arc4_test_ct`: Expected ciphertexts for the input plaintexts.

- **Functions:**
  - `Cipher_RC4_set_key`: Sets up the key for the ARCFOUR cipher.
  - `Cipher_RC4`: Encrypts the plaintext using the ARCFOUR cipher.
  - `test`: A helper function to compare expected and actual values and count errors.

- **Test Execution:**
  - The tests encrypt the plaintexts using the provided keys and compare the results with the expected ciphertexts using the `test` function.

### Summary
These unit tests ensure the correctness of cryptographic operations in the `aircrack-ng` project. They validate the functionality of message digest computation, stream cipher encryption, and WPA cryptographic operations. Each test function compares the actual results with expected values and counts any discrepancies, providing a robust way to validate cryptographic implementations.