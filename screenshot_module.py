from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os

# User-Agent strings for different devices
USER_AGENTS = {
    'android': 'Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Mobile Safari/537.36',
    'apple': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1'
}

def capture_domain_screenshot(domain_url, output_dir='screenshots', screenshot_file=None, device='android', headless=False):
    """
    Function to capture a screenshot with user-agent simulation and headless mode control.
    """
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # If no screenshot file name is provided, default to domain name
    if screenshot_file is None:
        screenshot_file = domain_url.replace("https://", "").replace("http://", "").replace("/", "_") + ".png"
    screenshot_path = os.path.join(output_dir, screenshot_file)

    # Set up Chrome options to ignore SSL certificate errors and set user-agent
    chrome_options = Options()
    chrome_options.headless = headless  # Control headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f'user-agent={USER_AGENTS[device]}')
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-extensions")  # Disable extensions
    chrome_options.add_argument("--start-maximized")  # Maximize browser window

    # Initialize the Chrome WebDriver
    driver = None
    try:
        print(f"Opening browser for {domain_url} with {device} device simulation...")
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

        # Load the domain URL
        driver.get(domain_url)

        # Wait for the page to load or redirection to complete
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Capture the screenshot and save it
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot successfully saved to {screenshot_path}")

        # Keep the browser open for 10 more seconds after the screenshot is taken
        print("Waiting 10 seconds before closing the browser...")
        time.sleep(10)

    except Exception as e:
        print(f"Failed to capture screenshot for {domain_url}: {str(e)}")

    finally:
        # Ensure the browser is closed after 10 seconds
        if driver:
            driver.quit()
            print("Browser closed.")

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
