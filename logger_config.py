import logging
import os
import json
from utilities import show_error_message

def load_config():
    CONFIG_FILE = 'config.json'
    if not os.path.exists(CONFIG_FILE):
        # Create default config if not exists
        default_config = {
            "main_directory": "E:\\project"
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(default_config, f, indent=4)
        except Exception as e:
            show_error_message("Configuration Error", f"Failed to create {CONFIG_FILE}: {e}")
            return default_config
        return default_config
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return config
    except json.JSONDecodeError as e:
        show_error_message("Configuration Error", f"Failed to read {CONFIG_FILE}. Please check the file format.")
        return {
            "main_directory": "E:\\project"
        }

config = load_config()

MAIN_DIRECTORY = config.get("main_directory", "E:\\project")

# Ensure the main directory exists
if not os.path.exists(MAIN_DIRECTORY):
    try:
        os.makedirs(MAIN_DIRECTORY)
    except Exception as e:
        show_error_message("Directory Error", f"Failed to create main directory {MAIN_DIRECTORY}: {e}")

log_file = os.path.join(MAIN_DIRECTORY, 'app.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
