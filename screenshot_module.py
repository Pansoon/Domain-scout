from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json

# User-Agent strings for different devices
USER_AGENTS = {
    'android': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Mobile Safari/537.36',
    'apple': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
}

def capture_domain_screenshot(domain_url, output_dir='screenshots', screenshot_file=None, device='android', headless=True):
    """
    Captures a screenshot of the given domain, automatically adjusting headers, referer, and acting like a real browser.
    
    :param domain_url: URL of the domain to capture.
    :param output_dir: Directory to save the screenshots (default: 'screenshots').
    :param screenshot_file: The name of the screenshot file. If None, defaults to the domain name as file name.
    :param device: The device type to simulate ('android' or 'apple').
    :param headless: Whether to run the browser in headless mode (default: True).
    :return: The path to the saved screenshot.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # If no screenshot file name is provided, default to domain name
    if screenshot_file is None:
        screenshot_file = domain_url.replace("https://", "").replace("http://", "").replace("/", "_") + ".png"

    screenshot_path = os.path.join(output_dir, screenshot_file)

    # Set up Chrome options to ignore SSL certificate errors and set user-agent
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")  # Run browser in headless mode if enabled
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.set_capability("acceptInsecureCerts", True)  # Allow insecure SSL certificates

    # Set the user-agent based on the selected device
    user_agent = USER_AGENTS.get(device.lower(), USER_AGENTS['android'])  # Default to Android if not specified
    chrome_options.add_argument(f"user-agent={user_agent}")

    driver = None  # Initialize the driver to None

    try:
        # Install ChromeDriver
        chrome_install = ChromeDriverManager().install()

        # Use platform-independent path handling for ChromeDriver
        service = ChromeService(executable_path=chrome_install)

        # Initialize Chrome WebDriver with the service and options
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Use CDP to monitor and capture network traffic for dynamic headers
        driver.execute_cdp_cmd('Network.enable', {})

        def capture_request_headers():
            """Capture dynamic headers including referer, user-agent, etc."""
            logs = driver.execute_cdp_cmd('Network.getResponseBodyForInterception', {})
            return logs

        driver.execute_cdp_cmd('Network.setExtraHTTPHeaders', {"headers": {
            "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Ch-Ua-Mobile": '?0'
        }})

        # Load the domain URL
        driver.get(domain_url)

        # Wait for the page to load completely
        time.sleep(4)

        # Check if the URL was redirected and wait for the final page to load
        final_url = driver.current_url
        if final_url != domain_url:
            print(f"Redirected from {domain_url} to {final_url}")
            time.sleep(5)  # Wait for the redirected page to fully load

        # Capture the dynamic headers and referer
        headers = capture_request_headers()
        print("Captured Headers:", json.dumps(headers, indent=4))

        # Capture the screenshot and save it
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot successfully saved to {screenshot_path}")

    except Exception as e:
        print(f"Failed to capture screenshot for {domain_url}: {str(e)}")
    
    finally:
        # Ensure the browser is closed only if the driver was successfully initialized
        if driver:
            driver.quit()

    return screenshot_path

# Example usage: Capture screenshots for multiple domains with different devices
if __name__ == "__main__":
    # List of domains to capture screenshots from
    domains = ["https://www.fla-sh.cc"]

    for domain in domains:
        # Capture screenshot as Samsung Galaxy S23 (Android)
        capture_domain_screenshot(domain, device='android', headless=True)  # Fast Scan (Headless)
        time.sleep(1)  # Add a short delay between screenshots
        
        # Capture screenshot as iPhone (Apple)
        capture_domain_screenshot(domain, device='apple', headless=False)  # Detailed Scan (Full Browser)
        time.sleep(1)  # Add a short delay between screenshots
