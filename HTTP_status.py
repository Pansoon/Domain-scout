import requests
import re  # Import the re module for regular expression matching
from requests.exceptions import RequestException

# Dictionary of common HTTP status codes and their descriptions
HTTP_STATUS_DESCRIPTIONS = {
    200: "OK",
    301: "Moved Permanently",
    302: "Found",
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    500: "Internal Server Error",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",
    # Add more status codes and descriptions as needed
}

def get_http_status_code(url):
    """
    Retrieves the HTTP status code and description from a given URL.

    Parameters:
    url (str): The URL of the domain to retrieve the HTTP status code from.

    Returns:
    tuple: A tuple containing the HTTP status code and its description, or (None, None) if the request fails.
    """
    # Ensure the URL starts with http:// or https://
    if not re.match(r'^https?://', url):
        url = 'http://' + url
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # First try a HEAD request
        response = requests.head(url, headers=headers, timeout=5, allow_redirects=True)
        
        # If HEAD request fails or returns no content, try a GET request
        if response.status_code == 405 or not response.ok:
            response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
        
        status_code = response.status_code
        description = HTTP_STATUS_DESCRIPTIONS.get(status_code, "Unknown Status")
        
        # Print and return the HTTP status code and its description
        print(f"HTTP Status Code for {url}: {status_code} ({description})")
        return status_code, description
    
    except RequestException as e:
        # Handle exceptions (e.g., connection errors, timeouts)
        print(f"An error occurred while requesting {url}: {e}")
        return None, None

# Example usage
if __name__ == "__main__":
    domain_name = "example.com"
    url = f"http://{domain_name}"
    status_code, description = get_http_status_code(url)
