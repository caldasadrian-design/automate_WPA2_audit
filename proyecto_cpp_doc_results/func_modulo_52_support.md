The provided code snippet is a header file for a network scanning tool, likely part of a project like aircrack-ng. It defines data structures and constants related to wireless network detection and analysis. Here's a breakdown of the key components:

1. **WPS_info Structure**:
   - Holds information about the Wi-Fi Protected Setup (WPS) state and capabilities of an access point.

2. **n_channel_info and ac_channel_info Structures**:
   - `n_channel_info` holds details about 802.11n channel capabilities.
   - `ac_channel_info` holds details about 802.11ac channel capabilities.

3. **AP_info Structure**:
   - Represents an access point (AP) and contains detailed information about it.
   - Includes:
     - Channel information
     - Signal power statistics
     - Encryption and authentication methods
     - MAC address and ESSID
     - GPS coordinates
     - Statistics on captured beacons and packets
     - WPA handshake data
     - IV (Initialization Vector) data for WEP decryption
     - Probing data
     - Decloak detection status
     - Data packets

4. **ST_info Structure**:
   - Represents a client station connected to an AP.
   - Includes:
     - MAC address
     - Associated ESSID
     - Signal power and bitrate statistics
     - GPS coordinates
     - WPA handshake data

5. **Constants**:
   - `NB_PRB` and `NB_PWR` define the size of ring buffers for probed ESSIDs and signal power, respectively.

6. **Channel Width Enum**:
   - Defines possible channel widths supported by 802.11 standards.

This header file is crucial for the data structures that underpin the functionality of network scanning and analysis tools, allowing them to store and process information about wireless networks and their associated clients.