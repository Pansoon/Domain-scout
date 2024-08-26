# IP-scan
 automated IP, port, http status from domain and report. Including GUI
### Project Overview
**Objective**: Develop a Python program that runs on a laptop, allowing users to input a domain name. The program will then:
1. Resolve the domain to its IP address.
2. Scan common ports on the resolved IP address.
3. Retrieve and display the HTTP status code of the domain.

### Modules and Structure

#### 1. **User Interface (UI) Module**
   - **Objective**: Provide a simple interface for user interaction.
   - **Techniques**:
     - **Command-Line Interface (CLI)**: Use Python's `argparse` or `input()` for simplicity.
     - **Graphical User Interface (GUI)** (optional): Use `tkinter` for a basic GUI.
   - **Functions**:
     - `get_user_input()`: Collect domain input from the user.
     - `display_results()`: Display the scan results.

#### 2. **Domain Resolution Module**
   - **Objective**: Convert the domain name to an IP address.
   - **Techniques**:
     - Use Python’s built-in `socket` library.
   - **Functions**:
     - `resolve_domain_to_ip(domain_name)`: Return the IP address for the domain.

#### 3. **Port Scanning Module**
   - **Objective**: Scan common ports on the resolved IP address to check if they are open.
   - **Techniques**:
     - Use the `scapy` library for sending TCP SYN packets.
   - **Functions**:
     - `scan_ports(ip_address, ports)`: Return the status (open/closed) of each port.

#### 4. **HTTP Status Code Module**
   - **Objective**: Retrieve the HTTP status code from the domain.
   - **Techniques**:
     - Use the `requests` library to send an HTTP GET request.
   - **Functions**:
     - `get_http_status_code(url)`: Return the HTTP status code for the URL.

#### 5. **Results Aggregation Module**
   - **Objective**: Aggregate and format the results from the above modules for display.
   - **Techniques**:
     - Combine results into a dictionary or JSON structure.
   - **Functions**:
     - `aggregate_results(ip_address, port_status, http_status)`: Return a formatted summary of all results.

#### 6. **Logging and Error Handling Module**
   - **Objective**: Log actions and handle errors gracefully.
   - **Techniques**:
     - Use Python’s `logging` library for logging.
     - Implement try-except blocks for error handling.
   - **Functions**:
     - `log_action(action, status)`: Log actions performed by the program.
     - `handle_error(error)`: Manage exceptions and provide user feedback.

### Optional Modules

#### 7. **Configuration Module**
   - **Objective**: Allow customization of settings, like ports to scan or timeout durations.
   - **Techniques**:
     - Use a configuration file (`config.json` or `.ini`) or environment variables.
   - **Functions**:
     - `load_config()`: Load and return configuration settings.

#### 8. **Reporting Module**
   - **Objective**: Generate and save a report of the scan results.
   - **Techniques**:
     - Generate a text or PDF report using libraries like `reportlab` or simply saving to `.txt`.
   - **Functions**:
     - `generate_report(results)`: Save the results in a formatted report.

### Implementation Plan

1. **Initial Setup**:
   - Set up a Python project with a virtual environment.
   - Install necessary libraries (`socket`, `scapy`, `requests`, `logging`).

2. **Develop Core Modules**:
   - Start with the Domain Resolution Module to resolve domains to IPs.
   - Implement the Port Scanning Module to check common ports.
   - Develop the HTTP Status Code Module to retrieve and display HTTP status.

3. **Integrate and Test**:
   - Combine the modules in the Results Aggregation Module.
   - Test with various domains to ensure correct functionality.

4. **Build User Interface**:
   - Implement a simple CLI for user interaction.
   - (Optional) Develop a GUI if a more user-friendly interface is desired.

5. **Add Logging and Error Handling**:
   - Implement the Logging and Error Handling Module to manage and record the program’s operations.

6. **Enhance with Optional Features**:
   - Add the Configuration Module for customizable settings.
   - Implement the Reporting Module to generate reports of scan results.

7. **Final Testing and Deployment**:
   - Perform comprehensive testing with edge cases.
   - Package the program for distribution or use on different machines.

### Tools and Libraries
- **Programming Language**: Python
- **Libraries**: `socket`, `scapy`, `requests`, `logging`, `tkinter` (optional for GUI), `reportlab` (optional for reporting)