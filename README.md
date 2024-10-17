# Domain-Scout

Automated IP, port, and HTTP status scanning from domains, complete with reporting capabilities and a user-friendly GUI.

### Project Overview

**Objective**: To develop a Python-based tool that runs locally, allowing users to input a domain name. The tool performs the following tasks:

1. Resolves the domain to its IP address.
2. Scans common ports on the resolved IP address.
3. Retrieves and displays the HTTP status code of the domain.

### Modules and Structure

#### 1. **User Interface (UI) Module**
   - **Objective**: Provide a simple interface for user interaction.
   - **Implementation**:
     - **CLI**: Use Python's `argparse` or `input()` for command-line interactions.
     - **GUI**: (Optional) Implement a graphical interface using `tkinter` or `PyQt5` for enhanced usability.
   - **Core Functions**:
     - `get_user_input()`: Collects domain input from the user.
     - `display_results()`: Displays the scan results.

#### 2. **Domain Resolution Module**
   - **Objective**: Convert the domain name to its corresponding IP address.
   - **Implementation**: Utilizes Python’s built-in `socket` library.
   - **Core Function**:
     - `resolve_domain_to_ip(domain_name)`: Returns the IP address associated with the domain.

#### 3. **Port Scanning Module**
   - **Objective**: Scan common ports on the resolved IP address to check if they are open.
   - **Implementation**: Uses the `scapy` library to send TCP SYN packets.
   - **Core Function**:
     - `scan_ports(ip_address, ports)`: Returns the status (open/closed) of each scanned port.

#### 4. **HTTP Status Code Module**
   - **Objective**: Retrieve the HTTP status code from the domain.
   - **Implementation**: Uses the `requests` library to send an HTTP GET request.
   - **Core Function**:
     - `get_http_status_code(url)`: Returns the HTTP status code for the provided URL.

#### 5. **Results Aggregation Module**
   - **Objective**: Aggregate and format the results from the above modules for display.
   - **Implementation**: Combines results into a structured format, such as a dictionary or JSON.
   - **Core Function**:
     - `aggregate_results(ip_address, port_status, http_status)`: Returns a formatted summary of all results.

#### 6. **Logging and Error Handling Module**
   - **Objective**: Log actions and handle errors gracefully.
   - **Implementation**: Uses Python’s `logging` library for logging and `try-except` blocks for error handling.
   - **Core Functions**:
     - `log_action(action, status)`: Logs actions performed by the program.
     - `handle_error(error)`: Manages exceptions and provides user feedback.

### Optional Modules

#### 7. **Configuration Module**
   - **Objective**: Allow customization of settings like ports to scan or timeout durations.
   - **Implementation**: Loads settings from a configuration file (`config.json`) or environment variables.
   - **Core Function**:
     - `load_config()`: Loads and returns configuration settings.

#### 8. **Reporting Module**
   - **Objective**: Generate and save a report of the scan results.
   - **Implementation**: Generates text or PDF reports using libraries like `fpdf` or saving to `.txt`.
   - **Core Function**:
     - `generate_report(results)`: Saves the results in a formatted report.

# Domain Scanner Program

## How to Use the Program

### Step 1: Open the Program
1. Navigate to the program's folder directory using the terminal or file explorer.
2. You can launch the program in two ways:
   - **Recommended**: Run the program using the command line by entering:
     ```bash
     python main.py
     ```
   - **Alternative**: Open the program via the graphical interface by running:
     ```bash
     python UI.py
     ```

### Step 2: Input Domains to Scan
- If you want to scan **a single domain**:
  - Simply enter the domain name in the provided box in the UI.
- If you want to scan **multiple domains at once**:
  - Create a list of domains in a Notepad file in the following format:
    ```txt
    example.com
    google.com
    etc.
    etc.
    ```
  - Save the file and load it into the program when prompted.

### Step 3: Start Scanning
1. Once the domains are entered or the file is loaded, choose the **"Text to scan"** option.
2. The program will begin scanning the domains, resolving IP addresses, checking open ports, and retrieving HTTP status codes.

### Step 4: Select Output Format
- After the scan completes, choose the output format:
  - **PDF** (Recommended)
  - **Text**

### Step 5: Access the Output
- The output report will be saved in the `output` folder located inside the program's directory.
- Review the report for detailed results on domain resolution, port status, and HTTP status codes.
