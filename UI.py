import re
import tkinter as tk
from tkinter import messagebox, filedialog  # Import filedialog for file selection
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from aggregation import aggregate_results
from report import generate_report
from colorama import init, Fore

# Initialize colorama for terminal output (if needed)
init(autoreset=True)

def sanitize_domain_name(domain):
    """
    Sanitizes the domain name by removing or replacing invalid characters for file names.
    """
    return re.sub(r'[\\/:"*?<>|]', '_', domain)

def load_domains_from_file():
    """
    Opens a file dialog to load domains from a .txt file.
    """
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as file:
                domains = [line.strip() for line in file if line.strip()]
            return domains
        except Exception as e:
            display_error(f"Error loading file: {e}")
            return []
    else:
        display_error("No file selected")
        return []

def run_scan():
    domain_input = entry_domain.get()
    domains = [domain_input] if domain_input else []

    if not domains:
        domains = load_domains_from_file()

    if not domains:
        display_error("No domains provided.")
        return

    sanitized_domains = [sanitize_domain_name(domain) for domain in domains]

    try:
        for domain, sanitized_domain in zip(domains, sanitized_domains):
            # Step 1: Resolve domain to IP
            ip_address = resolve_domain_to_ip(domain)
            if not ip_address:
                display_error(f"Failed to resolve IP for {domain}.")
                continue
            display_message(f"Resolved IP for {domain}: {ip_address}", Fore.BLACK)
            
            # Step 2: Scan ports
            ports = [80, 443, 22]  # You can customize this or make it user-selectable
            port_status = scan_ports(ip_address, ports)
            display_message(f"Port scan results for {domain}: {port_status}", Fore.BLACK)
            
            # Step 3: Get HTTP status code
            http_status = get_http_status_code(domain)  # Ensure this is a string, not a list
            display_message(f"HTTP status code for {domain}: {http_status}", Fore.BLACK)
            
            # Step 4: Aggregate results and include domain name
            results = {
                "Domain Name": sanitized_domain,
                "IP Address": ip_address,
                "Port Status": port_status,
                "HTTP Status": http_status
            }
            
            # Step 5: Display results
            display_results(results)
            
            # Step 6: Generate report
            report_type = report_type_var.get()
            generate_report([results], report_type=report_type)  # Pass results as a list
            display_success(f"Report generated as {report_type} format for {domain}.")
        
    except Exception as e:
        display_error(str(e))

def display_results(results):
    """
    Displays the aggregated results in the text area of the GUI.
    """
    text_results.delete(1.0, tk.END)  # Clear the text box before displaying new results
    result_text = ""
    for key, value in results.items():
        result_text += f"{key}: {value}\n"
    text_results.insert(tk.END, result_text)

def display_message(message, color=Fore.BLACK):
    """
    Displays a message in the output box of the GUI.
    """
    if color == Fore.RED:
        text_results.insert(tk.END, f"[ERROR] {message}\n", "error")
    elif color == Fore.GREEN:
        text_results.insert(tk.END, f"[SUCCESS] {message}\n", "success")
    else:
        text_results.insert(tk.END, f"{message}\n")
    
    text_results.see(tk.END)  # Scroll to the end of the text box to show the latest message

def display_error(message):
    """
    Displays an error message in red in both the output box and a message box.
    """
    display_message(f"Error: {message}", Fore.RED)
    messagebox.showerror("Error", message)

def display_success(message):
    """
    Displays a success message in green in both the output box and a message box.
    """
    display_message(message, Fore.GREEN)
    messagebox.showinfo("Success", message)

# Initialize tkinter window
root = tk.Tk()
root.title("Domain Scanner Tool")

# Configure grid layout
root.columnconfigure(1, weight=1)

# Domain Entry
tk.Label(root, text="Enter Domain:").grid(row=0, column=0, padx=10, pady=10, sticky='e')
entry_domain = tk.Entry(root, width=50)
entry_domain.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Load from File Button
tk.Button(root, text="Load from File", command=load_domains_from_file).grid(row=0, column=2, padx=10, pady=10, sticky='w')

# Report Type Option
tk.Label(root, text="Report Type:").grid(row=1, column=0, padx=10, pady=10, sticky='e')
report_type_frame = tk.Frame(root)
report_type_frame.grid(row=1, column=1, padx=10, pady=10, sticky='w')
report_type_var = tk.StringVar(value='text')
tk.Radiobutton(report_type_frame, text="Text", variable=report_type_var, value='text').grid(row=0, column=0)
tk.Radiobutton(report_type_frame, text="PDF", variable=report_type_var, value='pdf').grid(row=0, column=1)

# Run Scan Button
tk.Button(root, text="Run Scan", command=run_scan).grid(row=2, column=0, columnspan=3, pady=20)

# Results Display
text_results = tk.Text(root, height=15, width=70)
text_results.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
text_results.tag_config("error", foreground="red")
text_results.tag_config("success", foreground="green")

# Start the GUI event loop
root.mainloop()
