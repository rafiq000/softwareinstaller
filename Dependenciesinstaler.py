import os
import sys
import subprocess
import platform

def create_virtual_environment(venv_path):
    """Creates a virtual environment at the specified path."""
    try:
        import venv
        venv.create(venv_path, with_pip=True)
        print(f"Virtual environment created at {venv_path}")
    except Exception as e:
        print(f"Failed to create virtual environment: {e}")
        sys.exit(1)

def install_dependencies(venv_path, dependencies):
    """Installs the specified dependencies using pip."""
    try:
        # Determine the path to the pip executable in the virtual environment
        if platform.system() == "Windows":
            pip_executable = os.path.join(venv_path, 'Scripts', 'pip.exe')
        else:
            pip_executable = os.path.join(venv_path, 'bin', 'pip')

        # Upgrade pip to the latest version
        subprocess.check_call([pip_executable, 'install', '--upgrade', 'pip'])

        # Install each dependency
        for dependency in dependencies:
            print(f"Installing {dependency}...")
            subprocess.check_call([pip_executable, 'install', dependency])
        print("All dependencies installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")
        sys.exit(1)

def main():
    # Define the virtual environment directory name
    venv_dir = 'venv'

    # Define the list of dependencies
    dependencies = [
        'PyQt5',
        'requests'
    ]

    # Check if virtual environment already exists
    if not os.path.isdir(venv_dir):
        print("Creating virtual environment...")
        create_virtual_environment(venv_dir)
    else:
        print("Virtual environment already exists.")

    # Install dependencies
    install_dependencies(venv_dir, dependencies)

if __name__ == '__main__':
    main()
