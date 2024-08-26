import logging
import os
from datetime import datetime

# Create a logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configure the logging
logging.basicConfig(
    filename=f"logs/app_log_{datetime.now().strftime('%Y-%m-%d')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def log_action(action, status):
    """
    Logs an action taken by the program.
    
    :param action: Description of the action (e.g., "Domain Resolution").
    :param status: Outcome or details of the action (e.g., "IP Address: 192.168.1.1").
    """
    logging.info(f"Action: {action}, Status: {status}")

def handle_error(error):
    """
    Handles and logs an error encountered during program execution.
    
    :param error: Exception object or error message.
    """
    logging.error(f"Error: {str(error)}")
    print(f"An error occurred: {str(error)}. Please check the log file for more details.")

# Example usage within the module (optional)
if __name__ == "__main__":
    try:
        # Example action logging
        log_action("Example Action", "This is a test log entry.")
        
        # Example error handling
        raise ValueError("This is a test error.")
    except Exception as e:
        handle_error(e)
