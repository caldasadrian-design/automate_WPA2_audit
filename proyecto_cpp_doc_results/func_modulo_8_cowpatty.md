# MODULE: cowpatty

## 1. PURPOSE
The `cowpatty` module is responsible for handling the opening, reading, and closing of hash database files used in the aircrack-ng suite. It provides functions to open a hash database file, read the next record from the file, and properly close and free the associated resources.

## 2. CORE COMPONENTS
- `struct cowpatty_file * open_cowpatty_hashdb(const char * filename, const char * mode)`: Opens a cowpatty hash database file and initializes the `cowpatty_file` structure.
- `struct hashdb_rec * read_next_cowpatty_record(struct cowpatty_file * cf)`: Reads the next record from the open cowpatty hash database file.
- `void close_free_cowpatty_hashdb(struct cowpatty_file * cf)`: Closes and frees the resources associated with the `cowpatty_file` structure.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `aircrack-ng/defs.h`: Used for macro definitions and common utility functions.
- `aircrack-ng/cowpatty/cowpatty.h`: Header file for declarations of functions and structures used within the cowpatty module.

## 4. INCOMING DEPENDENCIES (Used By)
- `aircrack-ng/cowpatty/cowpatty.c`: Contains the implementation of the cowpatty module functions.