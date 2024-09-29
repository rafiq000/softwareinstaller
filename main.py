import sys
import os
from PyQt5 import QtWidgets, QtCore
from config import get_main_directory, set_main_directory
from inserturl import InsertURLDialog
from downloadsoftware import DownloadSoftwareDialog
from installer import install_software, silent_install_software
from utilities import show_error_message, show_info_message
from logger_config import logger  # Import logger after config.py is loaded

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Software Manager")
        self.setGeometry(100, 100, 800, 600)

        # Central Widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        layout = QtWidgets.QVBoxLayout()

        # Menu Bar for Settings
        self.menu_bar = self.menuBar()
        self.settings_menu = self.menu_bar.addMenu("Settings")

        set_main_dir_action = QtWidgets.QAction("Set Main Directory", self)
        set_main_dir_action.triggered.connect(self.set_main_directory)
        self.settings_menu.addAction(set_main_dir_action)

        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()

        self.insert_url_button = QtWidgets.QPushButton("Insert URL")
        self.insert_url_button.clicked.connect(self.open_insert_url)
        self.button_layout.addWidget(self.insert_url_button)

        self.download_button = QtWidgets.QPushButton("Download Software")
        self.download_button.clicked.connect(self.open_download_software)
        self.button_layout.addWidget(self.download_button)

        self.install_button = QtWidgets.QPushButton("Install")
        self.install_button.clicked.connect(self.install_software)
        self.button_layout.addWidget(self.install_button)

        self.silent_install_button = QtWidgets.QPushButton("Silent Install")
        self.silent_install_button.clicked.connect(self.silent_install_software)
        self.button_layout.addWidget(self.silent_install_button)

        layout.addLayout(self.button_layout)

        # File List
        self.file_list = QtWidgets.QListWidget()
        layout.addWidget(self.file_list)

        # Refresh Button
        self.refresh_button = QtWidgets.QPushButton("Refresh File List")
        self.refresh_button.clicked.connect(self.update_file_list)
        layout.addWidget(self.refresh_button)

        central_widget.setLayout(layout)

        self.update_file_list()

    def open_insert_url(self):
        dialog = InsertURLDialog(self)
        if dialog.exec_():
            self.update_file_list()

    def open_download_software(self):
        dialog = DownloadSoftwareDialog(self)
        dialog.exec_()

    def update_file_list(self):
        self.file_list.clear()
        download_dir = os.path.join(get_main_directory(), 'downloads')
        if os.path.exists(download_dir):
            try:
                files = os.listdir(download_dir)
                for file in files:
                    self.file_list.addItem(file)
            except Exception as e:
                logger.error(f"Error listing files in {download_dir}: {e}")
                show_error_message("File List Error", f"Failed to list files: {e}")
        else:
            logger.warning(f"Download directory does not exist: {download_dir}")
            show_info_message("Download Directory Missing", "Download directory does not exist. Creating it now.")
            try:
                os.makedirs(download_dir)
                logger.info(f"Created download directory at {download_dir}")
            except Exception as e:
                logger.error(f"Failed to create download directory: {e}")
                show_error_message("Directory Creation Error", f"Failed to create download directory: {e}")

    def install_software(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            show_error_message("No Selection", "Please select a software to install.")
            return
        filepath = os.path.join(get_main_directory(), 'downloads', selected_item.text())
        if os.path.exists(filepath):
            install_software(filepath)
        else:
            show_error_message("File Not Found", "Selected file does not exist.")

    def silent_install_software(self):
        selected_item = self.file_list.currentItem()
        if not selected_item:
            show_error_message("No Selection", "Please select a software to install.")
            return
        filepath = os.path.join(get_main_directory(), 'downloads', selected_item.text())
        if os.path.exists(filepath):
            silent_install_software(filepath)
        else:
            show_error_message("File Not Found", "Selected file does not exist.")

    def set_main_directory(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Main Directory", "")
        if directory:
            confirmation = QtWidgets.QMessageBox.question(
                self,
                "Confirm Directory Change",
                f"Changing the main directory to:\n{directory}\n\nExisting data may not be accessible.",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            if confirmation == QtWidgets.QMessageBox.Yes:
                try:
                    set_main_directory(directory)
                    logger.info(f"Main directory changed to {directory}")
                    show_info_message("Directory Changed", f"Main directory set to {directory}. Restart the application to apply changes.")
                except Exception as e:
                    logger.error(f"Failed to set main directory: {e}")
                    show_error_message("Directory Change Error", f"Failed to set main directory: {e}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
