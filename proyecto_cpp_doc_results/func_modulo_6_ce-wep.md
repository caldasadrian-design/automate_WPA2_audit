# MODULE: ce-wep

## 1. PURPOSE
This module provides functionality for detecting IV (Initialization Vector) uniqueness in WEP (Wired Equivalent Privacy) packets. It includes methods to initialize, mark, check, and wipe IV data structures, as well as a method to check for data cloaking based on IV and data content.

## 2. CORE COMPONENTS
- `unsigned char ** uniqueiv_init(void)`: Initializes the root structure for IV uniqueness detection.
- `int uniqueiv_mark(unsigned char ** uiv_root, unsigned char IV[3])`: Marks a new IV in the uniqueness structure.
- `int uniqueiv_check(unsigned char ** uiv_root, unsigned char IV[3])`: Checks if a given IV has been seen before.
- `void uniqueiv_wipe(unsigned char ** uiv_root)`: Unallocates the IV uniqueness structure.
- `unsigned char * data_init(void)`: Initializes a data structure for storing IV and data pairs.
- `int data_check(unsigned char * data_root, unsigned char IV[3], unsigned char data[2])`: Checks if the data associated with a given IV matches a previously seen data pattern.
- `void data_wipe(unsigned char * data)`: Unallocates the data structure.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `aircrack-ng/defs.h`: Used for various definitions and macros.
- `aircrack-ng/ce-wep/uniqueiv.h`: Header file for declarations of functions and data structures used within the module.

## 4. INCOMING DEPENDENCIES (Used By)
- Not explicitly listed in the provided code snippet.