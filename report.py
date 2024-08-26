import json
import os
from datetime import datetime
from fpdf import FPDF

def generate_report(results, report_type='text', report_file=None):
    """
    Generates and saves a report of the scan results.
    
    :param results: The results dictionary containing the scan data.
    :param report_type: The format of the report ('text' or 'pdf'). Default is 'text'.
    :param report_file: The name of the report file. If not provided, it will be auto-generated.
    :return: The path to the generated report file.
    """
    if report_file is None:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        report_file = f"scan_report_{timestamp}.{report_type}"

    if report_type == 'text':
        return generate_text_report(results, report_file)
    elif report_type == 'pdf':
        return generate_pdf_report(results, report_file)
    else:
        raise ValueError(f"Unsupported report type: {report_type}")

def generate_text_report(results, report_file):
    """
    Generates a text report and saves it to a file.
    
    :param results: The results dictionary containing the scan data.
    :param report_file: The name of the report file.
    :return: The path to the generated report file.
    """
    with open(report_file, 'w') as file:
        file.write("Scan Report\n")
        file.write("="*40 + "\n")
        file.write(f"Generated on: {datetime.now()}\n\n")
        
        for key, value in results.items():
            file.write(f"{key}:\n")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    file.write(f"  {sub_key}: {sub_value}\n")
            else:
                file.write(f"  {value}\n")
            file.write("\n")
    
    print(f"Text report saved as '{report_file}'.")
    return report_file

def generate_pdf_report(results, report_file):
    """
    Generates a PDF report and saves it to a file.
    
    :param results: The results dictionary containing the scan data.
    :param report_file: The name of the report file.
    :return: The path to the generated report file.
    """
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", size=16)
    pdf.cell(200, 10, txt="Scan Report", ln=True, align="C")
    pdf.ln(10)
    
    # Date
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.now()}", ln=True, align="C")
    pdf.ln(20)
    
    # Report content
    pdf.set_font("Arial", size=12)
    
    for key, value in results.items():
        pdf.cell(200, 10, txt=f"{key}:", ln=True)
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                pdf.cell(200, 10, txt=f"  {sub_key}: {sub_value}", ln=True)
        else:
            pdf.cell(200, 10, txt=f"  {value}", ln=True)
        pdf.ln(10)
    
    pdf.output(report_file)
    print(f"PDF report saved as '{report_file}'.")
    return report_file

# Example usage within the module (optional)
if __name__ == "__main__":
    # Example results
    results = {
        "IP Address": "192.168.1.1",
        "Port Status": {"80": "open", "443": "closed"},
        "HTTP Status": "200 OK"
    }
    
    # Generate text report
    generate_report(results, report_type='text')
    
    # Generate PDF report
    generate_report(results, report_type='pdf')
