The provided code snippet includes various structures and defines for network protocols and constants. Below, I'll provide a detailed explanation of each part:

### Structures

1. **Ethernet Frame Header (`struct ether_frame`)**
   - Defines the structure of an Ethernet frame header.
   - `ether_type`: Indicates the type of protocol following the Ethernet header (e.g., 0x0800 for IP).

2. **IP Header (`struct ip_frame`)**
   - Defines the structure of an IP packet header.
   - `version`: IP version (usually 4 for IPv4).
   - `hlen`: Header length in 32-bit words.
   - `tos`: Type of service.
   - `tot_len`: Total length of the IP packet.
   - `id`: Unique identifier for fragments.
   - `frag_off`: Fragment offset and flags.
   - `ttl`: Time to live.
   - `protocol`: Protocol number (e.g., 6 for TCP, 17 for UDP).
   - `check`: Header checksum.
   - `saddr`: Source IP address.
   - `daddr`: Destination IP address.

3. **TCP Header (`struct tcp_frame`)**
   - Defines the structure of a TCP segment header.
   - `sport`: Source port.
   - `dport`: Destination port.
   - `seq`: Sequence number.
   - `ack_seq`: Acknowledgment number.
   - `flags`: Control flags (e.g., SYN, ACK, FIN).
   - `window`: Receive window.
   - `checksum`: Header checksum.
   - `urg_ptr`: Urgent pointer.

4. **ICMP Header (`struct icmp`)**
   - Defines the structure of an ICMP message.
   - `icmp_type`: Type of ICMP message.
   - `icmp_code`: Subcode for ICMP message.
   - `icmp_cksum`: Checksum of the ICMP header.
   - `icmp_hun`: Union for different ICMP message types.
     - `icmp_pptr`: Pointer to next header.
     - `icmp_gwaddr`: Gateway address.
     - `icmp_id`: ID for echo request/reply.
     - `icmp_seq`: Sequence number for echo request/reply.
     - `icmp_void`: Unused field.
     - `icmp_pmvoid`: Unused field for PMTU discovery.
     - `icmp_nextmtu`: Next MTU size for PMTU discovery.
     - `icmp_num_addrs`: Number of addresses in router advertisement.
     - `icmp_wpa`: WPA preference.
     - `icmp_lifetime`: Lifetime of router advertisement.
   - `icmp_dun`: Union for different ICMP data types.
     - `icmp_otime`: Origin time for timestamp request/reply.
     - `icmp_rtime`: Received time for timestamp request/reply.
     - `icmp_ttime`: Transmitted time for timestamp request/reply.
     - `icmp_ip`: Encapsulated IP packet for ICMP echo.
     - `icmp_radv`: Router advertisement data.
     - `icmp_mask`: Subnet mask for IP address.
     - `icmp_data`: User data.

5. **DNS Query Header (`struct dns_query`)**
   - Defines the structure of a DNS query.
   - `tid`: Transaction ID.
   - `flags`: Query flags (e.g., recursion desired, query type).
   - `questions`: Number of questions.
   - `rrs`: Number of answer resource records.
   - `arrs`: Number of authority resource records.
   - `xrrs`: Number of additional resource records.
   - `qdata`: Query data (variable length).

6. **802.1X EAP Header (`struct dot1x_hdr`)**
   - Defines the structure of a 802.1X EAP header.
   - `code`: EAP code (e.g., request, response).
   - `idtype`: EAP identifier type.
   - `length`: Length of the EAP packet.

7. **RADIUS Header (`struct radius_hdr`)**
   - Defines the structure of a RADIUS packet.
   - `code`: RADIUS code (e.g., access request, response).
   - `flags`: Flags (e.g., key, request).
   - `length`: Length of the RADIUS packet.
   - `replaycnt`: Replay counter.
   - `wpa_nonce`: WPA nonce.
   - `wpa_key_iv`: WPA key IV.
   - `wpa_key_rsc`: WPA key RSC.
   - `wpa_key_id`: WPA key ID.
   - `wpa_key_mic`: WPA key MIC.
   - `wpa_key_len`: Length of the WPA key.
   - `wpa_key_datap`: Pointer to the start of the key data.

### Defines

- **Ethernet Protocol Types**: Defines constants for common Ethernet protocol types (e.g., `ETHTYPE_IP` for IP).
- **IP Protocol Numbers**: Defines constants for common IP protocol numbers (e.g., `PROTO_TCP` for TCP).
- **ICMP Types**: Defines constants for common ICMP message types.
- **Boolean Values**: Defines constants for `TRUE` and `FALSE`.

### Macros

- **MAC Address Printing**: Defines a macro to print MAC addresses in a readable format.
- **DNS Response Packets**: Defines sample DNS response packets.
- **Color Codes**: Defines ANSI escape codes for colored text output.

### Constants

- **Redirect Placeholder**: Defines a placeholder for a redirect URL.
- **HTTP 302 Redirect Packet**: Defines a sample HTTP 302 redirect packet.

### Usage

These structures and defines are commonly used in network programming to parse and construct network packets. For example, you might use these structures to analyze incoming packets, modify their contents, or construct new packets to send over a network.