import csv
import os
from datetime import datetime

# Define directory for output files
OUTPUT_DIR = 'scan_output'

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_domain_info(domain_info):
    """
    Saves domain information to a CSV file.
    
    :param domain_info: A list of dictionaries containing domain information.
    """
    domain_info_file = os.path.join(OUTPUT_DIR, 'domain_info.csv')

    # Check if file exists to determine if we need to write the header
    write_header = not os.path.exists(domain_info_file)
    
    with open(domain_info_file, 'a', newline='') as csvfile:
        fieldnames = ['Domain Name', 'Date Introduced', 'Last Active Date', 'Domain Type', 'Site Status']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        for domain in domain_info:
            # Map the dictionary keys to the CSV field names
            row = {
                'Domain Name': domain.get('domain_name'),
                'Date Introduced': domain.get('date_introduced'),
                'Last Active Date': domain.get('last_active'),
                'Domain Type': domain.get('domain_type'),
                'Site Status': domain.get('site_status')
            }
            writer.writerow(row)

def save_scan_results(scan_results):
    """
    Saves or appends the scan results to a single CSV file.
    
    :param scan_results: A list of dictionaries containing scan results.
    """
    # Use a single file for all scan results
    scan_results_file = os.path.join(OUTPUT_DIR, 'scan_results.csv')

    # Check if the file already exists to determine if we need to write the header
    write_header = not os.path.exists(scan_results_file)
    
    # Open the file in append mode
    with open(scan_results_file, 'a', newline='') as csvfile:
        fieldnames = ['Domain Name', 'Scan Date', 'Port Status', 'HTTP Status Code', 'HTTP Status Description', 'Additional Info', 'Type of Phishing']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header only if the file is new
        if write_header:
            writer.writeheader()

        # Write the new scan results
        for scan in scan_results:
            # Map the dictionary keys to the CSV field names
            row = {
                'Domain Name': scan.get('domain_name'),
                'Scan Date': scan.get('scan_date'),
                'Port Status': scan.get('port_status'),
                'HTTP Status Code': scan.get('http_status_code'),
                'HTTP Status Description': scan.get('http_status_desc'),
                'Additional Info': scan.get('additional_info'),
                'Type of Phishing': scan.get('type_of_phishing', 'N/A')  # Default to 'N/A' if not provided
            }
            writer.writerow(row)

# Example usage
if __name__ == "__main__":
    # Sample domain info
    domain_info = [
        {"domain_name": "example.com", "date_introduced": "2024-09-10", "last_active": "2024-09-13", "domain_type": ".com", "site_status": "Active"},
        {"domain_name": "example.xyz", "date_introduced": "2024-09-11", "last_active": "2024-09-12", "domain_type": ".xyz", "site_status": "Closed"},
    ]

    # Save domain info
    save_domain_info(domain_info)

    # Sample scan results
    scan_results = [
    {"domain_name": "example.com", "scan_date": "2024-09-13", "port_status": "Port 80 Open", "http_status_code": 404, "http_status_desc": "Not Found", "additional_info": "N/A", "type_of_phishing": "Spear Phishing"},
    {"domain_name": "example.xyz", "scan_date": "2024-09-13", "port_status": "Port 80 Closed", "http_status_code": None, "http_status_desc": "N/A", "additional_info": "Timeout", "type_of_phishing": "Clone Phishing"}
    ]

    # Save scan results for today
    save_scan_results(scan_results)
