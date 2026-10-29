# MODULE: buddy-ng

## 1. PURPOSE
`buddy-ng` is a network utility that handles network packets and provides a mechanism for communication between different components, including handling UDP and TCP connections, managing packet IDs, and dropping privileges.

## 2. CORE COMPONENTS
- `static unsigned char ids[8192];`: Array to track duplicate packet IDs.
- `static unsigned short last_id;`: Tracks the last seen packet ID.
- `static int wrap;`: Indicates if the packet ID has wrapped around.
- `static int is_dup(unsigned short id)`: Checks if a packet ID is a duplicate.
- `static int handle(int s, unsigned char * data, int len, struct sockaddr_in * s_in)`: Handles incoming network packets.
- `static void handle_dude(int dude, int udp)`: Handles UDP communication and manages connections.
- `static void drop_privs(void)`: Drops privileges to a lower user ID.
- `static void usage(void)`: Displays usage information.
- `int main(int argc, char * argv[])`: Main function to initialize and run the module.

## 3. OUTGOING DEPENDENCIES (Calls/Uses)
- `network.h`: Calls `verifyssid()` to verify network SSID.
- `easside.h`: Used for handling EAP authentication.
- `aircrack-ng/version.h`: Used to get version information.

## 4. INCOMING DEPENDENCIES (Used By)
- `main.cpp`: Calls `init()` to initialize the module.
- `network.cpp`: Calls functions like `handle()` to process network packets.