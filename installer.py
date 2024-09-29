import os
import subprocess
from utilities import show_error_message, show_info_message
from logger_config import logger

def install_software(filepath):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(filepath)
            show_info_message("Installation", f"Started installation of {os.path.basename(filepath)}.")
            logger.info(f"Started installation of {filepath}")
        else:
            # For macOS or Linux, adjust accordingly
            subprocess.call(['chmod', '+x', filepath])
            subprocess.call([filepath])
            show_info_message("Installation", f"Started installation of {os.path.basename(filepath)}.")
            logger.info(f"Started installation of {filepath}")
    except Exception as e:
        logger.error(f"Failed to install {filepath}: {e}")
        show_error_message("Installation Error", f"Failed to install: {e}")

def silent_install_software(filepath):
    try:
        if os.name == 'nt':  # Windows
            # Determine installer type based on file extension
            if filepath.endswith('.msi'):
                command = f'msiexec /i "{filepath}" /quiet /norestart'
            elif filepath.endswith('.exe'):
                # This is a placeholder. Actual silent flags depend on the installer.
                command = f'"{filepath}" /S'
            else:
                show_error_message("Unsupported Installer", "Silent installation not supported for this file type.")
                return

            subprocess.run(command, shell=True, check=True)
            show_info_message("Silent Installation", f"Started silent installation of {os.path.basename(filepath)}.")
            logger.info(f"Started silent installation of {filepath} with command: {command}")
        else:
            # For macOS or Linux, adjust accordingly
            show_error_message("Unsupported OS", "Silent installation not supported on this operating system.")
    except subprocess.CalledProcessError as e:
        logger.error(f"Silent installation failed for {filepath}: {e}")
        show_error_message("Installation Error", f"Failed to silently install: {e}")
    except Exception as e:
        logger.error(f"Error during silent installation for {filepath}: {e}")
        show_error_message("Installation Error", f"Failed to silently install: {e}")
