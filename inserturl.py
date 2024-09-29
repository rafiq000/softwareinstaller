from PyQt5 import QtWidgets
import os
from config import get_main_directory, set_software_version
from utilities import show_error_message, show_info_message
from logger_config import logger

URL_FILE_PATH = os.path.join(get_main_directory(), 'software_urls.txt')
VERSIONS_FILE = os.path.join(get_main_directory(), 'software_versions.json')

class InsertURLDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(InsertURLDialog, self).__init__(parent)
        self.setWindowTitle("Insert Software URL")
        self.setFixedSize(400, 300)
        layout = QtWidgets.QVBoxLayout()

        # Software Name
        self.name_label = QtWidgets.QLabel("Software Name:")
        self.name_input = QtWidgets.QLineEdit()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        # Software URL
        self.url_label = QtWidgets.QLabel("Software URL:")
        self.url_input = QtWidgets.QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Software Version
        self.version_label = QtWidgets.QLabel("Software Version:")
        self.version_input = QtWidgets.QLineEdit()
        layout.addWidget(self.version_label)
        layout.addWidget(self.version_input)

        # Submit Button
        self.submit_button = QtWidgets.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit(self):
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        version = self.version_input.text().strip()
        if name and url and version:
            if not self.validate_url(url):
                show_error_message("Invalid URL", "Please enter a valid URL.")
                return
            try:
                with open(URL_FILE_PATH, 'a') as f:
                    f.write(f"{name}|{url}\n")
                set_software_version(name, version)
                show_info_message("Success", "URL and version added successfully.")
                logger.info(f"Added URL and version: {name} - {url} - {version}")
                self.accept()
            except Exception as e:
                logger.error(f"Failed to save URL and version: {e}")
                show_error_message("Error", f"Failed to save URL and version: {e}")
        else:
            show_error_message("Input Error", "All fields must be filled.")

    def validate_url(self, url):
        # Simple URL validation
        return url.startswith('http://') or url.startswith('https://')
