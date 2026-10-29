# MODULE: ce-wep

## 1. PURPOSE
This module is part of a software that attempts to crack WEP and WPA-PSK keys. It manages unique initialization vectors (IVs) and related data structures to facilitate the cracking process.

## 2. CORE COMPONENTS
- `unsigned char ** uniqueiv_init(void)`: Initializes the unique IV data structure.
- `int uniqueiv_mark(unsigned char ** uiv_root, unsigned char IV[3])`: Marks an IV as present in the unique IV data structure.
- `int uniqueiv_check(unsigned char ** uiv_root, unsigned char IV[3])`: Checks if a given IV is present in the unique IV data structure.
- `void uniqueiv_wipe(unsigned char ** uiv_root)`: Frees the memory allocated for the unique IV data structure.
- `unsigned char * data_init(void)`: Initializes the data structure for storing data.
- `int data_check(unsigned char * data_root, unsigned char IV[3], unsigned char data[2])`: Checks if a given data block is present in the data structure.
- `void data_wipe(unsigned char * data)`: Frees the memory allocated for the data structure.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `No external dependencies mentioned in the code`

## 4. INCOMING DEPENDENCIES (Used By)
- `No external dependencies mentioned in the code`