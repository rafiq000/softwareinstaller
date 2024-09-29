import os
import json
from utilities import show_error_message

CONFIG_FILE = 'config.json'
VERSIONS_FILE = 'software_versions.json'

def load_config():
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

def save_config(config):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        show_error_message("Configuration Error", f"Failed to write to {CONFIG_FILE}: {e}")

def get_main_directory():
    config = load_config()
    main_dir = config.get("main_directory", "E:\\project")
    main_dir = os.path.expanduser(main_dir)  # Handle user paths like ~
    if not os.path.isabs(main_dir):
        main_dir = os.path.abspath(main_dir)
    return main_dir

def set_main_directory(new_path):
    config = load_config()
    config["main_directory"] = new_path
    save_config(config)

def load_versions():
    if not os.path.exists(VERSIONS_FILE):
        # Create empty versions file
        try:
            with open(VERSIONS_FILE, 'w') as f:
                json.dump({}, f, indent=4)
        except Exception as e:
            show_error_message("Version Error", f"Failed to create {VERSIONS_FILE}: {e}")
            return {}
    try:
        with open(VERSIONS_FILE, 'r') as f:
            versions = json.load(f)
            return versions
    except json.JSONDecodeError as e:
        show_error_message("Version Error", f"Failed to read {VERSIONS_FILE}. Please check the file format.")
        return {}

def save_versions(versions):
    try:
        with open(VERSIONS_FILE, 'w') as f:
            json.dump(versions, f, indent=4)
    except Exception as e:
        show_error_message("Version Error", f"Failed to write to {VERSIONS_FILE}: {e}")

def get_software_version(name):
    versions = load_versions()
    return versions.get(name, "Unknown")

def set_software_version(name, version):
    versions = load_versions()
    versions[name] = version
    save_versions(versions)
