The provided code is a C program for a tool named "Besside-ng," which appears to be a variant of a wireless network security testing tool. The tool seems to focus on detecting and testing vulnerabilities in Wi-Fi networks, particularly around authentication and association attacks. Below is a breakdown of the key components and functionalities of the code:

### Key Components and Functionalities

1. **Configuration Initialization (`init_conf`)**:
   - Sets up default configurations for the tool, such as channel hopping frequency, attack wait times, and logging details.

2. **Timer Callbacks (`timer_cb2str`)**:
   - Converts timer callback functions to human-readable strings for debugging and logging purposes.

3. **State Management (`print_state`)**:
   - Prints the current state of the tool, including network information, channel hopping details, and timer status.

4. **Usage Function (`usage`)**:
   - Displays the usage instructions for the tool, including available options and parameters.

5. **Main Function (`main`)**:
   - Parses command-line arguments to configure the tool.
   - Sets up signal handlers for graceful termination and state printing.
   - Initializes the network and channel configurations.
   - Calls the main function to start the tool (`pwn()`).

### Detailed Breakdown

#### Configuration Initialization

The `init_conf` function initializes various configuration settings such as:
- `cf_channels`: Initializes the channel list.
- `cf_autochan`: Enables automatic channel hopping.
- `cf_hopfreq`: Sets the frequency for channel hopping.
- `cf_deauthfreq`: Sets the frequency for deauthentication attacks.
- `cf_attackwait`: Sets the wait time between attacks.
- `cf_floodwait`: Sets the wait time between flood attacks.
- `cf_to`: Sets a timeout value.
- `cf_floodfreq`: Sets the frequency for flood attacks.
- `cf_crack_int`: Sets the cracking interval.
- `cf_wpa`, `cf_wep`, `cf_log`: Paths to capture files and log file.
- `cf_do_wep`, `cf_do_wpa`: Flags to enable WEP and WPA attacks.

#### Timer Callbacks

The `timer_cb2str` function converts a timer callback function to a human-readable string. This is used for debugging and logging purposes.

#### State Management

The `print_state` function prints the current state of the tool, including:
- Current state.
- Network information.
- Channel hopping details.
- Timer status.

#### Usage Function

The `usage` function displays the usage instructions for the tool, including available options and parameters.

#### Main Function

The `main` function:
- Parses command-line arguments to configure the tool.
- Sets up signal handlers for graceful termination and state printing.
- Initializes the network and channel configurations.
- Calls the main function to start the tool (`pwn()`).

### Example Usage

To run the tool with specific options, you might use a command like:
```sh
./besside-ng -b 00:11:22:33:44:55 -c 6 -v interface_name
```
This command sets the target BSSID to `00:11:22:33:44:55`, locks to channel `6`, and enables verbose mode on the interface `interface_name`.

### Dependencies

The code includes support for various PCRE libraries (`pcre2` and `pcre`) for regular expression handling. If these libraries are not available, the tool will not support regular expression options.

### Signal Handling

The tool sets up signal handlers for:
- `SIGINT`: Graceful termination.
- `SIGKILL`: Immediate termination.
- `SIGUSR1`: Print the current state.
- `SIGCHLD`: Handle child process termination.

### Conclusion

The provided code is a comprehensive tool for wireless network security testing, focusing on authentication and association attacks. It includes detailed configuration, state management, and usage instructions, making it a versatile and powerful tool for network security professionals.