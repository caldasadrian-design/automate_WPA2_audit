# MODULE: test

## 1. PURPOSE
This module is a simple command-line tool that converts a hexadecimal string into an array of bytes and prints the result. It is used for testing purposes to ensure that hexadecimal strings are correctly converted and displayed.

## 2. CORE COMPONENTS
- `int main(int nbarg, char * argv[])`: The entry point of the program. It takes a hexadecimal string as an argument, converts it to an array of bytes using `hexStringToArray`, and then prints the array.
- `int hexStringToArray(const char *hex, size_t len, unsigned char *out, size_t out_len)`: Converts a hexadecimal string to an array of bytes.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `aircrack-ng/support/common.h`: Used for the `hexStringToArray` function.
- Standard C libraries: Used for string handling and printing.

## 4. INCOMING DEPENDENCIES (Used By)
- None. It is a standalone executable that can be run from the command line.