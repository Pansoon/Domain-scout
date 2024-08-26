from UI import get_user_input, display_results, display_message, display_error, display_success
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from aggregation import aggregate_results
from logging_module import log_action, handle_error
from config import load_config  # Optional
from report import generate_report  # Optional
import dns.resolver
import socket

def resolve_domain_to_ip(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        if ip_address:
            display_message(f"IP address of {domain_name} (using socket): {ip_address}")
            return ip_address
    except socket.gaierror:
        display_error(f"Socket resolution failed for {domain_name}. Trying dnspython...")

    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['1.1.1.1']
        answer = resolver.resolve(domain_name, 'A')
        ip_address = answer[0].to_text()
        display_success(f"IP address of {domain_name} (using dnspython): {ip_address}")
        return ip_address
    except Exception as e:
        display_error(f"An error occurred: {e}")
        return None

def main_program(domain):
    try:
        config = load_config() if 'load_config' in globals() else None
        
        ip_address = resolve_domain_to_ip(domain)
        if not ip_address:
            log_action("Domain Resolution", "Failed to resolve IP address")
            display_error("Failed to resolve IP address. Exiting.")
            return

        log_action("Domain Resolution", f"IP Address: {ip_address}")
        
        ports = config['ports'] if config else [80, 443, 22]
        port_status = scan_ports(ip_address, ports)
        log_action("Port Scanning", f"Ports Scanned: {ports}")
        
        http_status = get_http_status_code(domain)
        log_action("HTTP Status Code", f"Status Code: {http_status}")
        
        results = aggregate_results(ip_address, port_status, http_status)
        
        display_results(results)
        
        if 'generate_report' in globals():
            generate_report(results)
            log_action("Report Generation", "Report saved successfully")
            display_success("Report generated and saved successfully.")
        
    except Exception as e:
        handle_error(e)
        log_action("Error", str(e))
        display_error(f"An error occurred: {e}")

if __name__ == "__main__":
    get_user_input(main_program)  # Pass the main_program function to get_user_input
