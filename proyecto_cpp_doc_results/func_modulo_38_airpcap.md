# MODULE: airpcap

## 1. PURPOSE
The `airpcap` module provides a interface for network packet capture and injection on Windows systems, using Airpcap drivers, with a focus on handling 802.11 network frames.

## 2. CORE COMPONENTS
- `int cygwin_init(char *param)`: Initializes the Airpcap adapter with the specified parameters.
- `int cygwin_set_chan(int chan)`: Sets the wireless channel for capturing or injecting packets.
- `int cygwin_sniff(void *buf, int len, struct rx_info *ri)`: Captures a packet and stores it in the provided buffer.
- `int cygwin_inject(void *buf, int len, struct tx_info *ti)`: Injects a packet into the network.
- `void cygwin_close(void)`: Closes the Airpcap handle and cleans up resources.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `AirpcapOpen()`: Called to open the Airpcap adapter.
- `AirpcapRead()`: Called to read a packet.
- `AirpcapWrite()`: Called to write a packet.
- `AirpcapSetFcsPresence()`: Called to set the FCS presence.
- `AirpcapSetLinkType()`: Called to set the link type.
- `AirpcapSetFcsValidation()`: Called to set the FCS validation.
- `AirpcapSetMinToCopy()`: Called to set the minimum number of bytes to copy.
- `AirpcapSetDeviceChannel()`: Called to set the device channel.
- `AirpcapClose()`: Called to close the Airpcap handle.
- `fprintf(stderr, ...)`: Used for error messages.

## 4. INCOMING DEPENDENCIES (Used By)
- `main.cpp init()`: The module is initialized by the `init()` function in `main.cpp`.
- Any application that needs to capture or inject network packets on a Windows system using Airpcap drivers.