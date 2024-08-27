import os
from datetime import datetime
from fpdf import FPDF
from collections import Counter, defaultdict

def generate_report(results_list, report_type='text', report_file=None):
    """
    Generates and saves a report of the scan results for multiple domains.

    :param results_list: A list of dictionaries, each containing the scan data for a domain.
    :param report_type: The format of the report ('text' or 'pdf'). Default is 'text'.
    :param report_file: The name of the report file. If not provided, it will be auto-generated.
    :return: The path to the generated report file.
    """
    # Ensure the output directory exists
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    if report_file is None:
        report_file = f"scan_report_{timestamp}"

    # Report type dispatch dictionary
    report_dispatch = {
        'text': ('.txt', generate_text_report),
        'pdf': ('.pdf', generate_pdf_report),
    }

    # Check if the report type is supported
    if report_type not in report_dispatch:
        raise ValueError(f"Unsupported report type: {report_type}")

    # Get the appropriate file extension and generator function
    extension, generator = report_dispatch[report_type]
    report_file = os.path.join(output_dir, report_file + extension)

    # Generate the report with a summary
    return generator(results_list, report_file)

def generate_text_report(results_list, report_file):
    """
    Generates a text report and saves it to a file for multiple domains.

    :param results_list: A list of dictionaries, each containing the scan data for a domain.
    :param report_file: The name of the report file.
    :return: The path to the generated report file.
    """
    summary = summarize_results(results_list)

    with open(report_file, 'w') as file:
        file.write("Scan Report\n")
        file.write("=" * 40 + "\n")
        file.write(f"Generated on: {datetime.now()}\n\n")
        
        for results in results_list:  # Iterating over each domain's results
            domain_name = results.get("Domain Name", "Unknown Domain")
            file.write(f"Domain: {domain_name}\n")
            file.write("-" * 40 + "\n")
            
            for key, value in results.items():
                if key != "Domain Name":
                    file.write(f"{key}:\n")
                    if isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            file.write(f"  {sub_key}: {sub_value}\n")
                    else:
                        file.write(f"  {value}\n")
                file.write("\n")
            
            file.write("=" * 40 + "\n\n")
        
        # Add the summary to the end of the report
        file.write("Summary\n")
        file.write("=" * 40 + "\n")
        for line in summary:
            file.write(line + "\n")
    
    print(f"Text report saved as '{report_file}'.")
    return report_file

def generate_pdf_report(results_list, report_file):
    """
    Generates a PDF report and saves it to a file for multiple domains.

    :param results_list: A list of dictionaries, each containing the scan data for a domain.
    :param report_file: The name of the report file.
    :return: The path to the generated report file.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', size=18)
    pdf.cell(200, 10, txt="Domain Scan Report", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    pdf.set_font("Arial", 'I', size=12)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.now()}", ln=True, align="C")
    pdf.ln(20)
    
    for results in results_list:
        domain_name = results.get("Domain Name", "Unknown Domain")
        
        # Domain Name Title
        pdf.set_font("Arial", 'B', size=14)
        pdf.cell(200, 10, txt=f"Domain: {domain_name}", ln=True, align="L")
        pdf.ln(5)
        
        # IP Address
        pdf.set_font("Arial", size=12)
        ip_address = results.get("IP Address", "N/A")
        pdf.cell(200, 10, txt=f"IP Address: {ip_address}", ln=True, align="L")
        pdf.ln(5)
        
        # Port Status
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt="Port Status:", ln=True, align="L")
        pdf.set_font("Arial", size=11)
        
        for port, status in results.get("Port Status", {}).items():
            if status.lower() == 'open':
                pdf.set_text_color(0, 128, 0)  # Green color for "open"
            elif status.lower() == 'closed/filtered':
                pdf.set_text_color(255, 0, 0)  # Red color for "closed/filtered"
            else:
                pdf.set_text_color(0, 0, 0)  # Default color for other statuses

            pdf.cell(200, 10, txt=f"  Port {port}: {status}", ln=True, align="L")
        
        pdf.set_text_color(0, 0, 0)  # Reset to default color
        pdf.ln(5)
        
        # HTTP Status
        http_status = results.get("HTTP Status", "N/A")
        pdf.set_font("Arial", 'B', size=12)
        pdf.cell(200, 10, txt=f"HTTP Status: {http_status}", ln=True, align="L")
        pdf.ln(10)
        
        # Separator between domains
        pdf.cell(200, 0, '', 'T', ln=True, align="C")  # Draw a horizontal line
        pdf.ln(10)

    # Add the summary to the end of the report
    summary = summarize_results(results_list)
    pdf.add_page()
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Summary", ln=True, align="L")
    pdf.ln(10)
    pdf.set_font("Arial", size=12)
    for line in summary:
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    
    pdf.output(report_file)
    print(f"PDF report saved as '{report_file}'.")
    return report_file

def summarize_results(results_list):
    """
    Summarizes the scan results, categorizing by HTTP status, listing domains, and separating unique and repeated IPs.

    :param results_list: A list of dictionaries, each containing the scan data for a domain.
    :return: A list of summary lines.
    """
    http_statuses = defaultdict(list)
    ip_addresses = defaultdict(list)

    for result in results_list:
        http_status = result.get("HTTP Status", "N/A")
        domain_name = result.get("Domain Name", "Unknown Domain")
        ip_address = result.get("IP Address", "N/A")
        
        http_statuses[http_status].append(domain_name)
        ip_addresses[ip_address].append(domain_name)

    summary = [
        f"Total Domains Scanned: {len(results_list)}",
        "=" * 40,
    ]
    
    for status, domains in http_statuses.items():
        summary.append(f"HTTP Status '{status}': {len(domains)} site(s)")
        for domain in domains:
            summary.append(f"  - {domain}")

    summary.append("=" * 40)
    unique_ips = [ip for ip, domains in ip_addresses.items() if len(domains) == 1]
    repeated_ips = {ip: domains for ip, domains in ip_addresses.items() if len(domains) > 1}

    summary.append(f"Unique IPs ({len(unique_ips)}):")
    for ip in unique_ips:
        summary.append(f"  - {ip} ({ip_addresses[ip][0]})")

    summary.append("=" * 40)
    summary.append(f"Repeated IPs ({len(repeated_ips)}):")
    for ip, domains in repeated_ips.items():
        summary.append(f"  - {ip} ({', '.join(domains)})")

    return summary

# Example usage within the module (optional)
if __name__ == "__main__":
    # Example results
    results_list = [
        {
            "Domain Name": "example.com",
            "IP Address": "93.184.216.34",
            "Port Status": {"80": "open", "443": "closed"},
            "HTTP Status": "200 OK"
        },
        {
            "Domain Name": "example.org",
            "IP Address": "93.184.216.35",
            "Port Status": {"80": "closed", "443": "open"},
            "HTTP Status": "301 Moved Permanently"
        },
        {
            "Domain Name": "example.net",
            "IP Address": "93.184.216.34",  # Same IP as example.com
            "Port Status": {"80": "open", "443": "open"},
            "HTTP Status": "404 Not Found"
        }
    ]
    
    # Generate text report
    generate_report(results_list, report_type='text')
    
    # Generate PDF report
    generate_report(results_list, report_type='pdf')
