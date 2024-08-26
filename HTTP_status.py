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

# Example usage
if __name__ == "__main__":
    domain_name = "example.com"
    url = f"http://{domain_name}"
    status_code = get_http_status_code(url)
