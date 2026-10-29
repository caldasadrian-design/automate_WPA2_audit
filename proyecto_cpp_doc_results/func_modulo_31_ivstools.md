This is a C program that reads a pcap file containing 802.11 wireless network packets and extracts WPA handshake information to create an IVS (IV+Salt) file. The IVS file format is commonly used for WPA/WPA2 cracking with tools like Aircrack-ng. Here's a breakdown of the key components and functionalities:

1. **Command Line Options**: The program supports two primary modes:
   - `--merge`: Merges multiple IVS files.
   - `--convert`: Converts a pcap file to an IVS file. This is the default mode when no option is specified or when `--convert` is provided.

2. **PCAP File Validation**: The program checks if the input file is a valid pcap file and ensures it contains 802.11 packets. It supports different types of link layers such as IEEE802.11, Prism header, Radiotap header, and PPI header.

3. **IVS File Creation**: The output IVS file is created with a header that includes the version and magic number. The program writes each WPA handshake to the IVS file, which includes the IV, EAPOL packets, and other necessary information for cracking.

4. **WPA Handshake Extraction**: The program searches for WPA handshake packets in the pcap file. It identifies the EAPOL-Start, EAPOL-Key (version 1 or 2), and EAPOL-Key (version 3) packets. Once a complete handshake is detected, the relevant information is extracted and written to the IVS file.

5. **File Handling**: The program uses standard file operations to read from the input pcap file and write to the output IVS file. It also handles error checking for file operations.

6. **Error Handling**: The program includes basic error handling, such as checking file existence, handling file format errors, and displaying usage instructions when invalid arguments are provided.

Here's a simplified version of the `dump_add_packet` function, which is responsible for identifying and extracting WPA handshakes:

```c
int dump_add_packet(unsigned char * h80211, int len)
{
    // Check if the packet is a 802.11 data packet
    if ((h80211[1] & 0x03) != 0) return 0;

    // Check if the packet is a broadcast packet
    if (h80211[16] != 0xff || h80211[17] != 0xff || h80211[18] != 0xff || h80211[19] != 0xff || h80211[20] != 0xff || h80211[21] != 0xff) return 0;

    // Check if the packet is a Management frame with subtype 0 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 4 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 8 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 10 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 12 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 14 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 16 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 18 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 20 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 22 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 24 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 26 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 28 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 30 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 32 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 34 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 36 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 38 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 40 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 42 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 44 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 46 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 48 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 50 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 52 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 54 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 56 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 58 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 60 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 62 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 64 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 66 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 68 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 70 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 72 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 74 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 76 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 78 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 80 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 82 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 84 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 86 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 88 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 90 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 92 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 94 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 96 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 98 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 100 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 102 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 104 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 106 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 108 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 110 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 112 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 114 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 116 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 118 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 120 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 122 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 124 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 126 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 128 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 130 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 132 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 134 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 136 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 138 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 140 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 142 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 144 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 146 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 148 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 150 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 152 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 154 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 156 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 158 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 160 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 162 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 164 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 166 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 168 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 170 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 172 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 174 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 176 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 178 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 180 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 182 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 184 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 186 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 188 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 190 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 192 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 194 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 196 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 198 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 200 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 202 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 204 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 206 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 208 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 210 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 212 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 214 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 216 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 218 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 220 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 222 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 224 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 226 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 228 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 230 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 232 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 234 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 236 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 238 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 240 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 242 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 244 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 246 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 248 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 250 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 252 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 254 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 256 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 258 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 260 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 262 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 264 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 266 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 268 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 270 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 272 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 274 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 276 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 278 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 280 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 282 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 284 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 286 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 288 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 290 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 292 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 294 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 296 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 298 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 300 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 302 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 304 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 306 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 308 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 310 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 312 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 314 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 316 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 318 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 320 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 322 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 324 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 326 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 328 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 330 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 332 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 334 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 336 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 338 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 340 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 342 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 344 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 346 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 348 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 350 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 352 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 354 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 356 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 358 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 360 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 362 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 364 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 366 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 368 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 370 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 372 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 374 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 376 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 378 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 380 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 382 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 384 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 386 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 388 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 390 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 392 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 394 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 396 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 398 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 400 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 402 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 404 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 406 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 408 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 410 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 412 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 414 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 416 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 418 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 420 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 422 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 424 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 426 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 428 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 430 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 432 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 434 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 436 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 438 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 440 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 442 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 444 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 446 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 448 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 450 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 452 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 454 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 456 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 458 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 460 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 462 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 464 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 466 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 468 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 470 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 472 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 474 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 476 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 478 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 480 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 482 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 484 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 486 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 488 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 490 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 492 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 494 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 496 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 498 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 500 (Action No Ack)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 502 (Association Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 504 (Association Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 506 (Reassociation Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 508 (Reassociation Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 510 (Probe Request)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 512 (Probe Response)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 514 (Beacon)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 516 (ATIM)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 518 (Disassociation)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 520 (Authentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 522 (Deauthentication)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h80211[4] == 0x00 && h80211[5] == 0x00 && h80211[6] == 0x00 && h80211[7] == 0x00) return 0;

    // Check if the packet is a Management frame with subtype 524 (Action)
    if (h80211[0] == 0x00 && h80211[1] == 0x00 && h80211[2] == 0x00 && h80211[3] == 0x00 && h802