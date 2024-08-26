import json
import os

def load_config(config_file='config.json'):
    """
    Loads configuration settings from a JSON file.
    
    :param config_file: Path to the configuration file. Default is 'config.json'.
    :return: A dictionary containing the configuration settings.
    """
    if not os.path.exists(config_file):
        print(f"Configuration file '{config_file}' not found. Using default settings.")
        return default_config()
    
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            print(f"Configuration loaded from '{config_file}'.")
            return config
    except Exception as e:
        print(f"Error loading configuration file: {e}. Using default settings.")
        return default_config()

def default_config():
    """
    Provides a set of default configuration settings.
    
    :return: A dictionary containing the default configuration settings.
    """
    return {
        "ports": [80, 443, 22, 8080],  # Default ports to scan
        "timeout": 5,                  # Default timeout for network operations in seconds
        "retry_attempts": 3,           # Default number of retry attempts for scanning
        "output_format": "json",       # Default output format (json or text)
        "log_level": "INFO",           # Default logging level (INFO, DEBUG, ERROR)
    }

def save_config(config, config_file='config.json'):
    """
    Saves the current configuration settings to a JSON file.
    
    :param config: A dictionary containing the configuration settings.
    :param config_file: Path to the configuration file. Default is 'config.json'.
    """
    try:
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
            print(f"Configuration saved to '{config_file}'.")
    except Exception as e:
        print(f"Error saving configuration file: {e}")

# Example usage within the module (optional)
if __name__ == "__main__":
    # Load the configuration
    config = load_config()

    # Modify a configuration setting (example)
    config['timeout'] = 10

    # Save the updated configuration
    save_config(config)
