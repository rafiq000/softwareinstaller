import os
import sys
import subprocess
import platform

def get_python_executable(venv_path):
    """Returns the path to the Python executable within the virtual environment."""
    if platform.system() == "Windows":
        return os.path.join(venv_path, 'Scripts', 'python.exe')
    else:
        return os.path.join(venv_path, 'bin', 'python')

def main():
    # Define the virtual environment directory name
    venv_dir = 'venv'

    # Define the main application script
    main_script = 'main.py'

    # Check if virtual environment exists
    if not os.path.isdir(venv_dir):
        print("Virtual environment not found. Please run Dependenciesinstaler.py first.")
        sys.exit(1)

    # Get the path to the Python executable in the virtual environment
    python_executable = get_python_executable(venv_dir)

    # Check if the Python executable exists
    if not os.path.isfile(python_executable):
        print(f"Python executable not found in {venv_dir}.")
        sys.exit(1)

    # Check if the main application script exists
    if not os.path.isfile(main_script):
        print(f"Main application script '{main_script}' not found.")
        sys.exit(1)

    # Run the main application using the virtual environment's Python
    try:
        subprocess.check_call([python_executable, main_script])
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
