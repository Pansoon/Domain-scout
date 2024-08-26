from UI import get_user_input, display_results
from IP_address import resolve_domain_to_ip
from PORT_scan import scan_ports
from HTTP_status import get_http_status_code
from aggregation import aggregate_results
from logging_module import log_action, handle_error
from config import load_config  # Optional
from report import generate_report  # Optional
import dns.resolver
import socket
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def resolve_domain_to_ip(domain_name):
    """
    Resolves a domain name to its corresponding IP address using both socket and dnspython.
    """
    try:
        # Attempt to resolve using socket
        ip_address = socket.gethostbyname(domain_name)
        if ip_address:
            print(f"{Fore.BLACK}IP address of {domain_name} (using socket): {ip_address}")
            return ip_address
    except socket.gaierror:
        print(f"{Fore.RED}Socket resolution failed for {domain_name}. Trying dnspython...")

    try:
        # Attempt to resolve using dnspython
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['1.1.1.1']  # Cloudflare DNS
        answer = resolver.resolve(domain_name, 'A')
        ip_address = answer[0].to_text()
        print(f"{Fore.GREEN}IP address of {domain_name} (using dnspython): {ip_address}")
        return ip_address
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}")
        return None

def main():
    try:
        # Load configuration (optional)
        config = load_config() if 'load_config' in globals() else None
        
        # Step 1: Get domain name from user
        domain = get_user_input()
        log_action("User Input", f"Domain: {domain}")
        print(f"{Fore.BLACK}Domain entered: {domain}")
        
        # Step 2: Resolve domain to IP
        ip_address = resolve_domain_to_ip(domain)
        if not ip_address:
            log_action("Domain Resolution", "Failed to resolve IP address")
            print(f"{Fore.RED}Failed to resolve IP address. Exiting.")
            return

        log_action("Domain Resolution", f"IP Address: {ip_address}")
        
        # Step 3: Scan common ports
        ports = config['ports'] if config else [80, 443, 22]  # Example ports
        port_status = scan_ports(ip_address, ports)
        log_action("Port Scanning", f"Ports Scanned: {ports}")
        print(f"{Fore.BLACK}Ports scanned: {ports}")
        
        # Step 4: Get HTTP status code
        http_status = get_http_status_code(domain)
        log_action("HTTP Status Code", f"Status Code: {http_status}")
        print(f"{Fore.GREEN}HTTP Status Code for {domain}: {http_status}")
        
        # Step 5: Aggregate results
        results = aggregate_results(ip_address, port_status, http_status)
        
        # Step 6: Display results
        display_results(results)
        
        # Optional: Generate report
        if 'generate_report' in globals():
            generate_report(results)
            log_action("Report Generation", "Report saved successfully")
            print(f"{Fore.GREEN}Report generated and saved successfully.")
        
    except Exception as e:
        handle_error(e)
        log_action("Error", str(e))
        print(f"{Fore.RED}An error occurred: {e}")

if __name__ == "__main__":
    main()
