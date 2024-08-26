import requests

def get_http_status_code(url):
    """
    Retrieves the HTTP status code from a given URL.

    Parameters:
    url (str): The URL of the domain to retrieve the HTTP status code from.

    Returns:
    int: The HTTP status code returned by the server, or None if the request fails.
    """
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, timeout=5)
        
        # Print and return the HTTP status code
        print(f"HTTP Status Code for {url}: {response.status_code}")
        return response.status_code
    except requests.exceptions.RequestException as e:
        # Handle exceptions (e.g., connection errors, timeouts)
        print(f"An error occurred while requesting {url}: {e}")
        return None

def aggregate_results(ip_address, port_status, http_status_code):
    """
    Aggregates the results from domain resolution, port scanning, and HTTP status check.

    Parameters:
    ip_address (str): The resolved IP address of the domain.
    port_status (dict): A dictionary with ports and their open/closed status.
    http_status_code (int): The HTTP status code of the domain.

    Returns:
    dict: A dictionary with all the aggregated results.
    """
    return {
        "IP Address": ip_address,
        "Port Status": port_status,
        "HTTP Status Code": http_status_code
    }

# Example usage in a main flow
if __name__ == "__main__":
    # Example domain name
    domain_name = "example.com"
    
    # Resolve domain to IP (dummy example)
    ip_address = "93.184.216.34"  # You would normally call resolve_domain_to_ip(domain_name)
    
    # Scan ports (dummy example)
    port_status = {"80": "open", "443": "closed"}  # You would normally call scan_ports(ip_address, [80, 443])
    
    # Get HTTP status code
    url = f"http://{domain_name}"
    http_status_code = get_http_status_code(url)
    
    # Aggregate results
    results = aggregate_results(ip_address, port_status, http_status_code)
    
    # Display results (simple print for this example)
    for key, value in results.items():
        print(f"{key}: {value}")
