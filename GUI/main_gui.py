import json
import os
import shutil
import sys
import logging

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QListWidget,
                             QMessageBox, QTextEdit, QLabel, QSplashScreen, QProgressBar)
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer

from srcDokListen.main import main as srcDokListen_main

# Constants
WINDOW_X, WINDOW_Y = 100, 100
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 400
OUTPUT_FILE = os.path.join(os.path.expanduser('~'), 'ergebnisse.json')
LOG_FILE = os.path.join(os.path.expanduser('~'), 'analyzer.log')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)


def get_icon_path(filename):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, filename)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        icon_path = get_icon_path('GUI/ai_excel_analysis_icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        icon_path = get_icon_path('ai_excel_analysis_icon-5.jpg')
        self.setPixmap(QPixmap(icon_path))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)


class JsonDisplayWindow(QWidget):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data
        self.initUI()

    def initUI(self):
        self.setWindowTitle('JSON Display')
        self.setGeometry(400, 400, 400, 300)
        layout = QVBoxLayout()
        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        self.textEdit.setText(self.json_data)
        layout.addWidget(self.textEdit)
        self.setLayout(layout)
        self.applyStyle()

    def applyStyle(self):
        self.setStyleSheet("""
            QTextEdit {
                background-color: #2b2b2b;
                color: #ddd;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)


class AnalyzerGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.json_window = None
        self.analyzedFilePath = ""
        self.temp_files = []
        icon_path = get_icon_path('GUI/ai_excel_analysis_icon.ico')
        self.setWindowIcon(QIcon(icon_path))
        self.initUI()

    def closeEvent(self, event):
        try:
            self.cleanup_output_file()
            self.cleanup_temp_files()
        except Exception as e:
            logging.error(f"An error occurred while deleting the file: {e}")
        event.accept()

    def cleanup_output_file(self):
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
            logging.info(f"File {OUTPUT_FILE} was successfully deleted.")
        else:
            logging.info(f"The file {OUTPUT_FILE} does not exist and could not be deleted.")

    def cleanup_temp_files(self):
        for temp_file in self.temp_files:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                    logging.info(f"Deleted temporary file: {temp_file}")
                except OSError as e:
                    logging.error(f"Error deleting file {temp_file}: {e}")

    def initUI(self):
        self.setWindowTitle('DokBereinigungs Tool')
        self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
        mainLayout = QVBoxLayout()
        layout = QVBoxLayout()

        self.uploadBtn = self.create_button('Upload Excel File', self.uploadFile, layout)
        self.fileList = QListWidget()
        layout.addWidget(self.fileList)

        self.removeFileBtn = self.create_button('Remove Selected File', self.removeFile, layout, enabled=False)
        self.analyzeOrbisBtn = self.create_button('Orbis Absätze Analysieren', self.analyzeOrbis, layout, enabled=False)
        self.analyzeDokBtn = self.create_button('DokListen analysieren [BETA]', self.analyzeDok, layout, enabled=False)
        self.downloadBtn = self.create_button('Download Analyzed File', self.downloadFile, layout, enabled=False)

        self.progressBar = QProgressBar()
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        self.fileList.itemSelectionChanged.connect(self.onSelectionChanged)
        mainLayout.addLayout(layout)
        bottomLayout = QHBoxLayout()
        bottomLayout.addStretch(1)
        createdByLabel = QLabel('Julian Bick')
        bottomLayout.addWidget(createdByLabel)
        mainLayout.addLayout(bottomLayout)
        self.setLayout(mainLayout)
        self.applyStyle()

    def create_button(self, text, handler, layout, enabled=True):
        button = QPushButton(text)
        button.clicked.connect(handler)
        button.setEnabled(enabled)
        layout.addWidget(button)
        return button

    def applyStyle(self):
        self.setStyleSheet("""
            QPushButton {
                background-color: #5c6bc0;
                color: white;
                border-radius: 15px;
                padding: 10px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7986cb;
            }
            QPushButton:disabled {
                background-color: #3c4a82;
                color: #ccc;
            }
            QListWidget, QTextEdit {
                border-radius: 5px;
                font-size: 14px;
            }
            QLabel {
                font-size: 12px;
                color: #666;
            }
        """)
        self.setFont(QFont('Arial', 10))

    def updateButtonStates(self):
        has_files = bool(self.fileList.count())
        self.analyzeOrbisBtn.setEnabled(has_files)
        self.analyzeDokBtn.setEnabled(has_files)
        self.removeFileBtn.setEnabled(bool(self.fileList.selectedItems()))

    def onSelectionChanged(self):
        self.updateButtonStates()

    def uploadFile(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Excel files (*.xlsx *.xls)")
        if fname:
            self.fileList.addItem(fname)
            self.updateButtonStates()

    def removeFile(self):
        for item in self.fileList.selectedItems():
            self.fileList.takeItem(self.fileList.row(item))
        self.updateButtonStates()
        self.progress_callback(0)

    def analyzeDok(self):
        try:
            file_path = self.fileList.item(0).text()
            srcDokListen_main(file_path)
            self.display_json_result()
        except FileNotFoundError:
            self.show_error_message("The JSON file could not be found.")
        except json.JSONDecodeError:
            self.show_error_message("Failed to decode JSON.")
        except Exception as e:
            self.show_error_message(f"An unexpected error occurred: {e}")

    def show_error_message(self, message):
        QMessageBox.critical(self, "Error", message)

    def display_json_result(self):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                formatted_json = json.dumps(json_data, indent=4, ensure_ascii=False)
            self.json_window = JsonDisplayWindow(formatted_json)
            self.json_window.show()
        except Exception as e:
            self.show_error_message(f"Failed to display JSON result: {e}")

    def progress_callback(self, value):
        self.progressBar.setValue(value)

    def analyzeOrbis(self):
        from src.main import main as src_main
        try:
            file_path = self.fileList.item(0).text()
            temp_file_path = src_main(file_path)
            logging.info(f"Temporary file path: {temp_file_path}")
            self.analyzedFilePath = temp_file_path
            self.temp_files.append(temp_file_path)
            self.progress_callback(100)
            QMessageBox.information(self, "Analysis Complete", "Orbis analysis is done.")
            self.downloadBtn.setEnabled(True)
        except Exception as e:
            self.show_error_message(f"An error occurred during analysis: {e}")

    def downloadFile(self):
        if self.analyzedFilePath:
            destination, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Excel files (*.xlsx *.xls)")
            if destination:
                try:
                    shutil.copyfile(self.analyzedFilePath, destination)
                    QMessageBox.information(self, "Download Complete", f"File has been saved to {destination}")
                except Exception as e:
                    self.show_error_message(f"Failed to save file: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()
    app.processEvents()
    ex = AnalyzerGUI()
    QTimer.singleShot(3000, splash.close)
    QTimer.singleShot(3000, ex.show)
    sys.exit(app.exec_())
