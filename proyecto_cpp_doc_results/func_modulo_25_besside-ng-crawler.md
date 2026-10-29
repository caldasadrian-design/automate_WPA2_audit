# MODULE: besside-ng-crawler

## 1. PURPOSE
The `besside-ng-crawler` module is a tool designed to recursively search through a directory of packet capture files (PCAP files) and extract specific network traffic data, specifically focusing on EAPOL frames associated with WPA networks. It saves beacon frames and EAPOL frames from identified WPA networks to a specified output file.

## 2. CORE COMPONENTS
- `get_eapol_bssids(pcap_t * handle)`: Identifies BSSIDs with EAPOL frames in a PCAP file.
- `process_eapol_networks(pcap_t * handle, struct bsslist * bsl)`: Filters and saves beacon and EAPOL frames for identified WPA networks.
- `process_file(const char * file)`: Processes individual PCAP files by identifying and saving relevant frames.
- `process_directory(const char * dir, time_t begin)`: Recursively processes files and directories, filtering based on modification time.
- `main(int argc, char * argv[])`: Entry point of the program, initializes resources, and orchestrates the processing of directories and files.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `pcap_next()`: Calls the `pcap_next()` function from the PCAP library to read packets from a PCAP file.
- `malloc()` and `free()`: Memory management functions to allocate and deallocate memory for BSSIDs and other data structures.
- `printf()`: Standard output function for logging and error messages.
- `pcap_open_offline()`: Opens a PCAP file for reading.
- `pcap_datalink()`: Retrieves the data link type of the PCAP file.
- `pcap_dump_open()`: Opens a file for writing packet data.
- `pcap_dump()`: Writes packet data to a file.
- `pcap_close()`: Closes a PCAP file handle.
- `opendir()`, `readdir()`, and `closedir()`: Directory manipulation functions for traversing directories.
- `stat()`: Retrieves file status information.
- `perror()`: Prints an error message.
- `strlcpy()` and `strlcat()`: Safe string manipulation functions for constructing file paths.

## 4. INCOMING DEPENDENCIES (Used By)
- None noted in the provided code. The module is self-contained and does not directly call or depend on external modules/files outside of the standard PCAP library and basic C library functions.