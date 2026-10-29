# MODULE: peek

## 1. PURPOSE
This module provides an interface to a wireless network adapter, allowing for capturing packets, sending packets, and changing the channel.

## 2. CORE COMPONENTS
- `struct pstate`: Manages the state of the network adapter and its associated functions.
- `CYGWIN_DLL_INIT(char *param)`: Initializes the network adapter with the specified device.
- `CYGWIN_DLL_SET_CHAN(int chan)`: Sets the wireless channel.
- `CYGWIN_DLL_INJECT(void* buf, int len, struct tx_info* ti)`: Injects a packet into the network.
- `CYGWIN_DLL_SNIFF(void *buf, int len, struct rx_info* ri)`: Captures a packet from the network.
- `CYGWIN_DLL_GET_MAC(unsigned char* mac)`: Retrieves the MAC address (currently unimplemented).
- `CYGWIN_DLL_SET_MAC(unsigned char* mac)`: Sets the MAC address (currently unimplemented).
- `CYGWIN_DLL_CLOSE(void)`: Closes the network adapter.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `network.h`: Calls `verifyssid()` to verify the SSID.
- `Peek.dll`: Calls various functions (`PeekOpenAdapter`, `PeekStartCapture`, etc.) to interact with the network adapter.

## 4. INCOMING DEPENDENCIES (Used By)
- `main.cpp init()`: Calls `CYGWIN_DLL_INIT(char *param)` to initialize the network adapter.
- `main.cpp start_sniffing()`: Calls `CYGWIN_DLL_SNIFF(void *buf, int len, struct rx_info* ri)` to capture packets.
- `main.cpp stop_sniffing()`: Calls `CYGWIN_DLL_CLOSE(void)` to close the network adapter.
- `main.cpp send_packet()`: Calls `CYGWIN_DLL_INJECT(void* buf, int len, struct tx_info* ti)` to inject packets.
- `main.cpp change_channel()`: Calls `CYGWIN_DLL_SET_CHAN(int chan)` to change the wireless channel.