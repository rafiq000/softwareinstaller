from PyQt5 import QtCore
import requests
import os
from logger_config import logger
from utilities import show_error_message

class DownloadThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(int)
    finished_download = QtCore.pyqtSignal(str, int, str)  # filepath, row, name
    error_occurred = QtCore.pyqtSignal(str, int)  # error_message, row

    def __init__(self, url, filepath, row, name):
        super(DownloadThread, self).__init__()
        self.url = url
        self.filepath = filepath
        self.row = row
        self.name = name

    def run(self):
        try:
            response = requests.get(self.url, stream=True, timeout=10)
            response.raise_for_status()
            total_length = response.headers.get('content-length')

            with open(self.filepath, 'wb') as f:
                if total_length is None:
                    f.write(response.content)
                    self.progress.emit(100)
                else:
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        if data:
                            f.write(data)
                            dl += len(data)
                            percent = int(100 * dl / total_length)
                            self.progress.emit(percent)
            self.finished_download.emit(self.filepath, self.row, self.name)
            logger.info(f"Downloaded {self.url} to {self.filepath}")
        except Exception as e:
            logger.error(f"Failed to download {self.url}: {e}")
            self.error_occurred.emit(str(e), self.row)
