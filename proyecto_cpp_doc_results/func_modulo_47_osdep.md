The provided code snippets are from the `aircrack-ng` project, specifically focusing on the OS-dependent modules for interfacing with network interfaces and managing wireless operations. Here's a breakdown of each file and its contents:

### FILE: osdep.h
This header file defines the OS-dependent structures and functions required by the aircrack-ng project. It includes structures for wireless interface (`wif`) and tap interface (`tif`), as well as common types and functions.

- **Structures:**
  - `struct rx_info`: Contains information about received packets, including RSSI, signal strength, etc.
  - `struct tx_info`: Contains information about transmitted packets, including transmission rate, etc.
  - `struct wif`: Represents a wireless interface, with function pointers for various operations like reading, writing, setting channel, frequency, etc.
  - `struct tif`: Represents a tap interface, with function pointers for reading, writing, setting MTU, IP, and MAC address, etc.

- **Functions:**
  - `wi_open`: Opens a wireless interface.
  - `wi_read`, `wi_write`: Read and write packets on the wireless interface.
  - `wi_set_channel`, `wi_set_freq`: Set the wireless channel and frequency.
  - `wi_get_channel`, `wi_get_freq`: Get the current wireless channel and frequency.
  - `wi_close`: Close the wireless interface.
  - `wi_fd`: Get the file descriptor for the wireless interface.
  - `wi_get_mac`, `wi_set_mac`: Get and set the MAC address of the wireless interface.
  - `wi_get_rate`, `wi_set_rate`: Get and set the transmission rate of the wireless interface.
  - `wi_get_monitor`: Check if the interface is in monitor mode.
  - `wi_get_mtu`, `wi_set_mtu`: Get and set the Maximum Transmission Unit (MTU) of the interface.
  - `wi_open_osdep`: OS-dependent function to open a wireless interface.
  - `wi_fd`: Get the file descriptor for the wireless interface.
  - `wi_alloc`, `wi_priv`: Helper functions for allocating and accessing private data in the `wif` structure.
  - `get_battery_state`: Get the battery state (OS-dependent).
  - `ti_open`: Open a tap interface.
  - `ti_read`, `ti_write`: Read and write data on the tap interface.
  - `ti_fd`: Get the file descriptor for the tap interface.
  - `ti_name`: Get the name of the tap interface.
  - `ti_set_mtu`, `ti_get_mtu`: Get and set the MTU of the tap interface.
  - `ti_set_ip`, `ti_set_mac`: Set the IP and MAC address of the tap interface.
  - `ti_close`: Close the tap interface.
  - `ti_alloc`, `ti_priv`: Helper functions for allocating and accessing private data in the `tif` structure.

### FILE: common.h
This header file defines common functions and macros that can be used across different parts of the aircrack-ng project. It includes:

- **Macros:**
  - `EXPORT`, `IMPORT`: Used for defining exported and imported functions, which depend on the compiler being used.
  - `HIGHEST_CHANNEL`, `LOWEST_CHANNEL`: Define the range of valid wireless channels.

- **Functions:**
  - `getFrequencyFromChannel`, `getChannelFromFrequency`: Convert between frequency and channel numbers.

### FILE: channel.h
This header file defines constants and macros related to wireless channel management. It includes:

- **Macros:**
  - `CHANNEL_NO_HT`, `CHANNEL_HT20`, `CHANNEL_HT40_PLUS`, `CHANNEL_HT40_MINUS`: Define the different types of wireless channels (non-HT, HT20, HT40+/-).

These files provide a framework for interacting with wireless interfaces and tap interfaces in a platform-independent manner, allowing the aircrack-ng project to be compiled and run on various operating systems.