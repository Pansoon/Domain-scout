import requests
import socket
import dns.resolver

def resolve_domain_to_ip(domain_name):
    """
    Resolves a domain name to its corresponding IP address using both socket and dnspython.
    """
    try:
        # Attempt to resolve using socket
        ip_address = socket.gethostbyname(domain_name)
        if ip_address:
            print(f"IP address of {domain_name} (using socket): {ip_address}")
            return ip_address
    except socket.gaierror:
        print(f"Socket resolution failed for {domain_name}. Trying dnspython...")

    try:
        # Attempt to resolve using dnspython
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['1.1.1.1']  # Cloudflare DNS
        answer = resolver.resolve(domain_name, 'A')
        ip_address = answer[0].to_text()
        print(f"IP address of {domain_name} (using dnspython): {ip_address}")
        return ip_address
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_http_status_code(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while requesting {url}: {e}")
        return None

def aggregate_results(ip_address, port_status, http_status_code):
    """
    Aggregates the results from domain resolution, port scanning, and HTTP status check.
    """
    return {
        "IP Address": ip_address,
        "Port Status": port_status,
        "HTTP Status Code": http_status_code
    }

# Main execution
if __name__ == "__main__":
    domain_name = "example.com"  # Replace with your domain
    ip_address = resolve_domain_to_ip(domain_name)
    
    if ip_address:
        # Continue only if IP address was successfully resolved
        port_status = {"80": "open", "443": "closed"}  # Example port scan result
        http_status_code = get_http_status_code(f"http://{domain_name}")
        results = aggregate_results(ip_address, port_status, http_status_code)
        
        # Display the results
        for key, value in results.items():
            print(f"{key}: {value}")
    else:
        print("Failed to resolve IP address, cannot continue.")
