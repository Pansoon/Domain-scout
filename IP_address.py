import socket
import dns.resolver
import re
from urllib.parse import urlparse

def resolve_domain_to_ip(domain_name):
    """
    Resolves a domain name to its corresponding IP address using both socket and dnspython.

    Parameters:
    domain_name (str): The domain name or URL to resolve.

    Returns:
    str: The resolved IP address, or None if the domain could not be resolved.
    """
    # Use urlparse to extract the netloc (domain) from the URL
    parsed_url = urlparse(domain_name)
    if parsed_url.netloc:
        domain_name = parsed_url.netloc
    else:
        domain_name = parsed_url.path

    # Further sanitize to remove any trailing slashes or unwanted characters
    domain_name = domain_name.strip('/')

    # First attempt to resolve using socket
    try:
        ip_address = socket.gethostbyname(domain_name)
        if ip_address:
            print(f"IP address of {domain_name} (using socket): {ip_address}")
            return ip_address
    except socket.gaierror:
        print(f"Socket resolution failed for {domain_name}. Trying dnspython...")

    # If socket resolution fails, attempt to resolve using dnspython
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = ['1.1.1.1']  # Cloudflare DNS, can be changed to Google DNS '8.8.8.8'
        answer = resolver.resolve(domain_name, 'A')
        ip_address = answer[0].to_text()
        print(f"IP address of {domain_name} (using dnspython): {ip_address}")
        return ip_address
    except dns.resolver.NXDOMAIN:
        print(f"Domain does not exist: {domain_name}")
    except dns.resolver.Timeout:
        print(f"Timeout while resolving domain: {domain_name}")
    except dns.resolver.NoNameservers:
        print(f"No nameservers available for domain: {domain_name}")
    except Exception as e:
        print(f"An error occurred while resolving with dnspython: {e}")
    
    return None

# Example usage
if __name__ == "__main__":
    domain_name = "https://example.com/path?query=1"  # Replace with the domain you want to resolve
    resolve_domain_to_ip(domain_name)
