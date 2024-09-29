from PyQt5 import QtWidgets, QtCore
import os
from config import get_main_directory, get_software_version, set_software_version
from downloadthread import DownloadThread
from utilities import show_error_message, show_info_message
from logger_config import logger

URL_FILE_PATH = os.path.join(get_main_directory(), 'software_urls.txt')
DOWNLOAD_DIRECTORY = os.path.join(get_main_directory(), 'downloads')
VERSIONS_FILE = os.path.join(get_main_directory(), 'software_versions.json')

class DownloadSoftwareDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DownloadSoftwareDialog, self).__init__(parent)
        self.setWindowTitle("Download Software")
        self.setFixedSize(800, 700)
        self.layout = QtWidgets.QVBoxLayout()

        # Table to show downloads
        self.table_widget = QtWidgets.QTableWidget()
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["Software Name", "URL", "Current Version", "Latest Version", "Progress", "Status"])
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.layout.addWidget(self.table_widget)

        # Download Button
        self.download_button = QtWidgets.QPushButton("Download Selected")
        self.download_button.clicked.connect(self.download_selected)
        self.layout.addWidget(self.download_button)

        self.setLayout(self.layout)

        self.load_urls()

    def load_urls(self):
        if os.path.exists(URL_FILE_PATH):
            try:
                with open(URL_FILE_PATH, 'r') as f:
                    lines = f.readlines()
                    self.table_widget.setRowCount(len(lines))
                    for row, line in enumerate(lines):
                        try:
                            name, url = line.strip().split('|')
                            current_version = get_software_version(name)
                            latest_version = self.fetch_latest_version(name, url, current_version)
                            
                            self.table_widget.setItem(row, 0, QtWidgets.QTableWidgetItem(name))
                            self.table_widget.setItem(row, 1, QtWidgets.QTableWidgetItem(url))
                            self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(current_version))
                            self.table_widget.setItem(row, 3, QtWidgets.QTableWidgetItem(latest_version))
                            
                            # Progress bar
                            progress_bar = QtWidgets.QProgressBar()
                            progress_bar.setValue(0)
                            self.table_widget.setCellWidget(row, 4, progress_bar)
                            
                            # Status
                            status_item = QtWidgets.QTableWidgetItem("Pending")
                            self.table_widget.setItem(row, 5, status_item)
                        except ValueError:
                            logger.warning(f"Malformed line in URL file: {line.strip()}")
            except Exception as e:
                logger.error(f"Error reading {URL_FILE_PATH}: {e}")
                show_error_message("File Read Error", f"Failed to read URLs from {URL_FILE_PATH}: {e}")
        else:
            show_info_message("No URLs Found", "No URLs found. Please add URLs first.")

    def fetch_latest_version(self, name, url, current_version):
        # Placeholder for fetching the latest version
        # In a real scenario, implement logic to determine the latest version
        # For example, parse the URL, fetch from an API, etc.
        # Here, we'll assume the latest version is the same as current_version
        return current_version

    def download_selected(self):
        selected_rows = set()
        for item in self.table_widget.selectedItems():
            selected_rows.add(item.row())

        if not selected_rows:
            show_error_message("No Selection", "Please select at least one software to download.")
            return

        for row in selected_rows:
            name_item = self.table_widget.item(row, 0)
            url_item = self.table_widget.item(row, 1)
            latest_version_item = self.table_widget.item(row, 3)
            status_item = self.table_widget.item(row, 5)

            if name_item and url_item and latest_version_item and status_item:
                name = name_item.text()
                url = url_item.text()
                latest_version = latest_version_item.text()
                current_version = self.table_widget.item(row, 2).text()

                if latest_version == current_version:
                    status_item.setText("Up-to-date")
                    logger.info(f"{name} is already up-to-date.")
                    continue  # Skip download

                filename = os.path.basename(url)
                filepath = os.path.join(DOWNLOAD_DIRECTORY, filename)

                if os.path.exists(filepath):
                    status_item.setText("Already Downloaded")
                    show_info_message("File Exists", f"{filename} already exists. Skipping download.")
                    continue

                # Update status to Downloading
                status_item.setText("Downloading")

                # Start download in a separate thread
                thread = DownloadThread(url, filepath)
                thread.progress.connect(lambda val, r=row: self.update_progress(r, val))
                thread.finished_download.connect(lambda path, r=row, n=name: self.download_finished(path, r, n))
                thread.error_occurred.connect(lambda msg, r=row: self.download_error(msg, r))
                thread.start()
                logger.info(f"Started download for {name} from {url}")

    def update_progress(self, row, value):
        progress_bar = self.table_widget.cellWidget(row, 4)
        if progress_bar:
            progress_bar.setValue(value)

    def download_finished(self, filepath, row, name):
        progress_bar = self.table_widget.cellWidget(row, 4)
        if progress_bar:
            progress_bar.setValue(100)
        status_item = self.table_widget.item(row, 5)
        if status_item:
            status_item.setText("Completed")
        show_info_message("Download Complete", f"Downloaded {name} to {filepath}.")
        # Update the stored version
        latest_version = self.table_widget.item(row, 3).text()
        set_software_version(name, latest_version)
        self.table_widget.setItem(row, 2, QtWidgets.QTableWidgetItem(latest_version))
        logger.info(f"Download completed for {name} at {filepath}")

    def download_error(self, error_message, row):
        progress_bar = self.table_widget.cellWidget(row, 4)
        if progress_bar:
            progress_bar.setValue(0)
        status_item = self.table_widget.item(row, 5)
        if status_item:
            status_item.setText("Error")
        show_error_message("Download Error", f"Failed to download: {error_message}")
        logger.error(f"Download error at row {row}: {error_message}")
