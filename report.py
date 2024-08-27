import json
import os
from datetime import datetime
from fpdf import FPDF

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
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    if report_file is None:
        report_file = f"scan_report_{timestamp}"

    # Append the correct extension based on the report type
    if report_type == 'text':
        report_file += '.txt'
    elif report_type == 'pdf':
        report_file += '.pdf'
    else:
        raise ValueError(f"Unsupported report type: {report_type}")

    # Prepend the output directory to the report file name
    report_file = os.path.join(output_dir, report_file)
    
    if report_type == 'text':
        return generate_text_report(results_list, report_file)
    elif report_type == 'pdf':
        return generate_pdf_report(results_list, report_file)

def generate_text_report(results_list, report_file):
    """
    Generates a text report and saves it to a file for multiple domains.

    :param results_list: A list of dictionaries, each containing the scan data for a domain.
    :param report_file: The name of the report file.
    :return: The path to the generated report file.
    """
    with open(report_file, 'w') as file:
        file.write("Scan Report\n")
        file.write("=" * 40 + "\n")
        file.write(f"Generated on: {datetime.now()}\n\n")
        
        for results in results_list:  # Iterating over each domain's results
            domain_name = results.get("Domain Name", "Unknown_Domain")
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
    
    print(f"Text report saved as '{report_file}'.")
    return report_file

from fpdf import FPDF
from datetime import datetime

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
    
    pdf.output(report_file)
    print(f"PDF report saved as '{report_file}'.")
    return report_file

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
        }
    ]
    
    # Generate text report
    generate_report(results_list, report_type='text')
    
    # Generate PDF report
    generate_report(results_list, report_type='pdf')
