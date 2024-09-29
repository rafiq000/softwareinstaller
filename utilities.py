from PyQt5 import QtWidgets

def show_error_message(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()

def show_info_message(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()

def show_warning_message(title, message):
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.exec_()
